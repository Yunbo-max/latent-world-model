"""Prepare the complete comparison command manifest for the existing Local harness.

This authoring utility does not launch child workloads or replace resource
admission, native qualification, checkpoint reconciliation or the SSH harness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_plan(root, data_root, run_root, budget, python, arms, seeds):
    jobs = []
    for arm in arms:
        for seed in seeds:
            identity = f"{arm}-{budget}-seed{seed}"
            directory = run_root / identity
            directory.mkdir(parents=True, exist_ok=True)
            previous = None
            for stage, suffix, data, extra in (
                ("pretrain", budget, data_root / f"fineweb-{budget}" / "train", []),
                ("sft", "babi", data_root / "babi" / "sft" / "train",
                 ["--init-checkpoint", str(directory / "pretrain" / "last.pt")]),
            ):
                config = json.loads((root / "configs" / f"{arm}_{suffix}.json").read_text())
                config["training"]["seed"] = seed
                path = directory / f"{stage}.json"
                encoded = json.dumps(config, indent=2) + "\n"
                if path.exists() and path.read_text() != encoded:
                    raise ValueError(f"Refusing to overwrite a different effective config: {path}")
                path.write_text(encoded)
                output = directory / stage
                validation = data.parent / "valid"
                command = [python, "-m", "lwm.train", "--config", str(path),
                           "--data", str(data), "--validation", str(validation),
                           "--output", str(output), *extra]
                job_id = f"{identity}/{stage}"
                jobs.append({"id": job_id, "kind": "train", "requires": [previous] if previous else [],
                             "argv": command, "status_file": str(output / "status.json"),
                             "output": str(output), "config": str(path), "config_sha256": digest(path)})
                previous = job_id
            for task, checkpoint_stage in (("lambada", "pretrain"), ("babi", "sft")):
                command = [python, "-m", "lwm.evaluate", "--checkpoint",
                           str(directory / checkpoint_stage / "last.pt"), "--tokenizer",
                           str(data_root / "tokenizer"), "--task", task, "--data", str(data_root / task),
                           "--output", str(directory / f"eval-{task}"), "--device", "cuda"]
                jobs.append({"id": f"{identity}/eval-{task}", "kind": "evaluate",
                             "requires": [f"{identity}/{checkpoint_stage}"], "argv": command,
                             "output": str(directory / f"eval-{task}")})
    return {"format": "lwm-local-command-manifest-v1", "status": "generated_unexecuted",
            "cwd": str(root), "budget": budget, "arms": arms, "seeds": seeds,
            "acceptance": "software, native parity and cumulative GPU budget required before execute",
            "jobs": jobs}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", default="data")
    parser.add_argument("--output-root", default="runs/matrix")
    parser.add_argument("--budget", choices=("100m", "1b"), default="100m")
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    data_root, run_root = Path(args.data_root).resolve(), Path(args.output_root).resolve()
    matrix = json.loads((root / "configs" / "experiments.json").read_text())
    plan = build_plan(root, data_root, run_root, args.budget, args.python, matrix["arms"], matrix["seeds"])
    run_root.mkdir(parents=True, exist_ok=True)
    plan_path = run_root / f"commands-{args.budget}.json"
    plan_path.write_text(json.dumps(plan, indent=2) + "\n")
    print(f"Command manifest: {plan_path} ({len(plan['jobs'])} dependent jobs)")
    print("No jobs launched. Local admits each recorded argv through its existing execution harness.")


if __name__ == "__main__":
    main()
