"""Generate exact author-runner configs; source code/scoring remain upstream.

This is baseline reuse, not a new latent-world-model implementation. The upstream
runner resumes weights/epochs, not optimizer/RNG state; an interrupted epoch is
not an exact restart. Its published reasoning datasets have separate budgets.
"""
import argparse
from pathlib import Path
import subprocess
import yaml
from .assets import verify_assets
from .io import read_json, sha256_file, write_json


def make_configs(repository, assets, output, dataset, seed, sources):
    repository, assets, output = map(lambda p: Path(p).resolve(), (repository, assets, output))
    expected = read_json(sources)["coconut"]["revision"]
    actual = subprocess.check_output(["git", "-C", str(repository), "rev-parse", "HEAD"], text=True).strip()
    if expected != actual or subprocess.check_output(["git", "-C", str(repository), "diff", "HEAD"], text=True):
        raise ValueError("Coconut checkout must be the pinned, unmodified author revision")
    receipt = verify_assets(assets / "gpt2")
    model = read_json(sources)["models"]["gpt2"]
    if receipt["repo"] != model["repo"] or receipt["revision"] != model["revision"]:
        raise ValueError("GPT-2 acquisition does not match pinned source")
    if output.exists() and any(output.iterdir()):
        raise ValueError("Config output exists; use a new round directory")
    output.mkdir(parents=True, exist_ok=True)
    prefix = "prosqa" if dataset == "prosqa" else "gsm"
    required_data = [repository / "data" / f"{prefix}_{split}.json" for split in ("train", "valid", "test")]
    for path in required_data:
        rows = read_json(path)
        if not isinstance(rows, list) or not rows or any(not {"question", "steps", "answer"} <= row.keys() for row in rows):
            raise ValueError(f"Incomplete native Coconut data: {path}")
    with (repository / "args" / f"{prefix}_coconut.yaml").open() as stream:
        base = yaml.safe_load(stream)
    base.update({"project": "latent-world-model-baselines", "save_path": str(output / "checkpoints"),
        "model_id": str(assets / "gpt2"), "seed": seed, "bf16": False,
        "batch_size_training": 1, "gradient_accumulation_steps": 128, "debug": False,
        "train_path": str(required_data[0]), "val_path": str(required_data[1]),
        "save_only_improve": True})
    commands = []
    for arm in ("cot", "no_cot", "coconut"):
        config = dict(base)
        config.update({"name": f"{prefix}-{arm}-s{seed}", "coconut": arm == "coconut",
            "cot": arm == "cot", "no_cot": arm == "no_cot", "no_thoughts": False,
            "only_eval": False, "save_only_improve": arm != "coconut"})
        if arm != "coconut":
            config.update({"c_thought": 0, "max_latent_stage": 0, "epochs_per_stage": 1,
                           "resume": 0, "load_model_path": "None", "reset_optimizer": False})
        if dataset == "gsm8k" and arm == "cot":
            with (repository / "args/gsm_cot.yaml").open() as stream:
                original_cot = yaml.safe_load(stream)
            config["num_epochs"] = original_cot["num_epochs"]
        if dataset == "gsm8k" and arm == "coconut":
            # This dependency cannot be a guessed future checkpoint: do not emit a
            # launchable config until Local passes the actual selected CoT checkpoint.
            config["load_model_path"] = "REQUIRES_ACTUAL_COT_CHECKPOINT"
        path = output / f"{arm}-train.yaml"
        with path.open("w") as stream:
            yaml.safe_dump(config, stream, sort_keys=False)
        commands.append({"arm": arm, "config": str(path),
            "status": "blocked_on_actual_cot_checkpoint" if dataset == "gsm8k" and arm == "coconut" else "generated_unexecuted",
            "argv": ["python", "-m", "torch.distributed.run", "--standalone", "--nnodes=1",
                     "--nproc_per_node=1", str(repository / "run.py"), str(path)],
            "env": {"WANDB_MODE": "disabled", "TOKENIZERS_PARALLELISM": "false"}})
    write_json(output / "launch-cards.json", {"commands": commands,
        "source_revision": expected, "data": {str(p): sha256_file(p) for p in required_data},
        "training_precision": "float32, author bf16=false",
        "global_examples_per_update": 128,
        "caveats": ["Microbatch reduction changes token/example weighting relative to author 4x32 runs; this is a resource-adapted baseline, not exact numerical reproduction.",
                    "Author preprocessing uses num_proc=32; native task admission must reserve those CPU workers.",
                    "Every arm retains official full datasets and answer extraction; no 0.1B token equivalence is implied.",
                    "Do not blindly restart the author training runner: resume is weights/epoch only.",
                    "This file is a command card, not a frozen admitted Research Autopilot harness plan."]})


def bind_checkpoint(config_path, checkpoint, output, evaluation=False, repository=None):
    config_path, checkpoint, output = Path(config_path), Path(checkpoint).resolve(), Path(output)
    if not checkpoint.is_file():
        raise ValueError("An actual produced checkpoint is required")
    if output.exists():
        raise ValueError("Do not overwrite a bound config")
    with config_path.open() as stream:
        config = yaml.safe_load(stream)
    config["load_model_path"] = str(checkpoint)
    if evaluation:
        if not repository:
            raise ValueError("--repository is required to retain the author's eval stage")
        prefix = "gsm" if "gsm" in config["name"] else "prosqa"
        if config["coconut"]:
            try:
                completed_epoch = int(checkpoint.name.removeprefix("checkpoint_"))
            except ValueError as error:
                raise ValueError("Retain the author's checkpoint_N filename for stage qualification") from error
            if (completed_epoch - 1) // config["epochs_per_stage"] <= config["max_latent_stage"]:
                raise ValueError("Held-out Coconut evaluation requires a checkpoint from the fully latent final stage")
            with (Path(repository) / "args" / f"{prefix}_coconut_eval.yaml").open() as stream:
                eval_config = yaml.safe_load(stream)
            config["resume"] = eval_config["resume"]
        else:
            config["resume"] = 0
        config.update({"only_eval": True, "val_path": str(Path(repository).resolve() / "data" / f"{prefix}_test.json"),
                       "name": config["name"] + "-heldout-eval"})
    elif not config["coconut"]:
        raise ValueError("A CoT initialization is only bound to the Coconut training arm")
    with output.open("w") as stream:
        yaml.safe_dump(config, stream, sort_keys=False)
    write_json(output.with_suffix(".binding.json"), {"checkpoint": str(checkpoint),
               "checkpoint_sha256": sha256_file(checkpoint), "source_config_sha256": sha256_file(config_path),
               "result_config_sha256": sha256_file(output), "evaluation": evaluation})


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="action", required=True)
    make = sub.add_parser("configs")
    make.add_argument("--repository", default="vendor/coconut")
    make.add_argument("--assets", default="assets")
    make.add_argument("--output", required=True)
    make.add_argument("--dataset", choices=["prosqa", "gsm8k"], required=True)
    make.add_argument("--seed", type=int, default=17)
    make.add_argument("--sources", default="configs/sources.json")
    bind = sub.add_parser("bind")
    bind.add_argument("--config", required=True)
    bind.add_argument("--checkpoint", required=True)
    bind.add_argument("--output", required=True)
    bind.add_argument("--evaluation", action="store_true")
    bind.add_argument("--repository", default="vendor/coconut")
    args = parser.parse_args()
    if args.action == "configs":
        make_configs(args.repository, args.assets, args.output, args.dataset, args.seed, args.sources)
    else:
        bind_checkpoint(args.config, args.checkpoint, args.output, args.evaluation, args.repository)


if __name__ == "__main__":
    main()
