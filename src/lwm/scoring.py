"""Native score contracts, strict joins, official replay and paired uncertainty.

Source status: generated_unexecuted. Local formulas are auditable previews;
only an actual pinned official replay can qualify native aggregation. Even that
replay does not establish inference/tokenizer/state parity with an official LM.
This module imports no model/scientific runtime until official replay is asked
for. It never downloads benchmark assets or selects a mutable latest run.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
import hashlib
import importlib
import inspect
import io
import json
import math
from pathlib import Path
import random
import re
import subprocess
import sys
import time
from typing import Any


SOURCE_STATUS = "generated_unexecuted"
PARLAI_REVISION = "a29567f7ce76992fd1f03c51ba9e3b155a37ea51"
HARNESS_REVISION = "d6de81643928d653435c431bae19945d41d32520"
BABI_SHA256 = "f7f0bee187efca0d81c3daac1b162cda4eb7f9505dee5ad6846eabbed3dbf92e"
LAMBADA_SHA256 = "4aa8d02cd17c719165fc8a7887fddd641f43fcafa4b1c806ca8abc31fabdb226"
LAMBADA_REVISION = "900124bf3b8235c6daf21033af9948b3f07346c4"
LAMBADA_BYTES = 1819752
BABI_COUNTS = {"train": (179998, 56396), "valid": (20002, 6265),
               "test": (20000, 6267)}
TASK_IDS = tuple(range(1, 21))


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def row_fingerprint(row: dict) -> str:
    payload = json.dumps(row, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def read_jsonl(path: str | Path) -> list[dict]:
    rows = []
    with Path(path).open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                raise ValueError(f"Blank JSONL record at {path}:{number}; no rows may be dropped")
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"Malformed JSONL at {path}:{number}") from error
            if not isinstance(row, dict):
                raise ValueError(f"Expected a JSON object at {path}:{number}")
            rows.append(row)
    if not rows:
        raise ValueError(f"Empty dataset: {path}")
    return rows


def write_json(path: str | Path, value: Any) -> None:
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2,
                  allow_nan=False)
        stream.write("\n")


def _count(value: Any, label: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{label} must be a positive integer")
    return value


def _index(rows: list[dict]) -> dict[str, dict]:
    result = {}
    for row in rows:
        identity = row.get("id")
        if not isinstance(identity, str) or not identity:
            raise ValueError("Every record must have a nonempty string id")
        if identity in result:
            raise ValueError(f"Duplicate ID: {identity}")
        result[identity] = row
    if not result:
        raise ValueError("An empty denominator is invalid")
    return result


def lambada_context_target(text: str) -> tuple[str, str]:
    """Pinned lambada_openai.yaml: split literal spaces, with no strip()."""
    if not isinstance(text, str):
        raise ValueError("LAMBADA text must be a string")
    words = text.split(" ")
    return " ".join(words[:-1]), " " + words[-1]


def encode_hf_pair(tokenizer, context: str, continuation: str) -> dict:
    """Pinned TemplateLM._encode_pair causal branch, including rstrip move.

    Source: lm_eval/api/model.py at HARNESS_REVISION. No truncation, chat
    template, automatic BOS, or independent encoding of a nonempty-context
    target is introduced. Empty context follows the harness prefix-token case.
    """
    if not isinstance(context, str) or not isinstance(continuation, str):
        raise ValueError("Context and continuation must be strings")

    def encode(text):
        return list(tokenizer.encode(text, add_special_tokens=False,
                                     split_special_tokens=False, truncation=False))

    original_context, original_continuation = context, continuation
    if context == "":
        prefix = int(tokenizer.eos_token_id)
        target_ids = encode(continuation)
        if target_ids and target_ids[0] == prefix:
            context_ids, target_ids = target_ids[:1], target_ids[1:]
        else:
            context_ids = [prefix]
        prefix_token_used = True
    else:
        trailing = len(context) - len(context.rstrip())
        if trailing:
            continuation = context[-trailing:] + continuation
            context = context[:-trailing]
        whole_ids = encode(context + continuation)
        context_ids = encode(context)
        target_ids = whole_ids[len(context_ids):]
        prefix_token_used = False
    if not context_ids or not target_ids:
        raise ValueError("Native HF pair produced empty context/target token IDs")
    return {"context": original_context, "target": original_continuation,
            "tokenizer_context": context, "tokenizer_target": continuation,
            "context_token_ids": context_ids, "target_token_ids": target_ids,
            "prefix_token_used": prefix_token_used}


@dataclass(frozen=True)
class NativeDataset:
    task: str
    split: str
    path: Path
    manifest_path: Path | None
    manifest: dict
    rows: list[dict]
    sha256: str


def _validate_babi(rows: list[dict], manifest: dict, split: str) -> None:
    source = manifest.get("source", {})
    if source.get("sha256") != BABI_SHA256 or source.get("parlai_revision") != PARLAI_REVISION:
        raise ValueError("bAbI source archive or ParlAI revision is not the pinned native source")
    if manifest.get("context_policy") != "all_observed_facts_then_current_question_no_prior_questions_or_answers":
        raise ValueError("Unsupported bAbI context policy")
    if manifest.get("answer_prefix") != " ":
        raise ValueError("bAbI preparation must declare the single-space answer prefix")
    # All native split totals must be declared, even when only test is evaluated.
    for name, (examples, episodes) in BABI_COUNTS.items():
        declared = manifest.get("splits", {}).get(name, {})
        if declared.get("examples") != examples or declared.get("episodes") != episodes:
            raise ValueError(f"Incorrect native bAbI {name} denominator in manifest")
        tasks = declared.get("tasks", {})
        if set(tasks) != {str(task) for task in TASK_IDS}:
            raise ValueError(f"bAbI {name} manifest must contain exactly all 20 tasks")
        if sum(_count(t.get("examples"), "task examples") for t in tasks.values()) != examples:
            raise ValueError(f"bAbI {name} per-task example counts do not sum to total")
        if sum(_count(t.get("episodes"), "task episodes") for t in tasks.values()) != episodes:
            raise ValueError(f"bAbI {name} per-task episode counts do not sum to total")
        if name == "test" and any(t["examples"] != 1000 for t in tasks.values()):
            raise ValueError("Native bAbI test requires 1000 questions per task")

    _index(rows)
    counts = Counter()
    episodes = defaultdict(set)
    previous_episode = None
    previous_done = True
    previous_turn = None
    facts: list[str] = []
    for row in rows:
        task_id = row.get("task_id")
        if type(task_id) is not int or task_id not in TASK_IDS:
            raise ValueError("bAbI task_id must be an integer in 1..20")
        expected_id = f"babi:{BABI_SHA256}:task:{task_id}:split:{split}:question:{counts[task_id]}"
        if row.get("id") != expected_id or row.get("question_index") != counts[task_id] or row.get("split") != split:
            raise ValueError("bAbI question identity/order is not its native source ordinal")
        task_source_sha = manifest["splits"][split]["tasks"][str(task_id)].get("source_sha256")
        if not isinstance(task_source_sha, str) or len(task_source_sha) != 64 or row.get("source_sha256") != task_source_sha:
            raise ValueError("bAbI row source SHA-256 differs from its native task file")
        episode_id = row.get("episode_id")
        if not isinstance(episode_id, str) or not episode_id:
            raise ValueError("bAbI episode_id is required for state and cluster audits")
        key = (task_id, episode_id)
        if key != previous_episode:
            if not previous_done or episode_id in episodes[task_id]:
                raise ValueError("bAbI episode is interleaved or its previous end is missing")
            episode_index = len(episodes[task_id])
            if row.get("episode_index") != episode_index or episode_id != f"babi:{BABI_SHA256}:task:{task_id}:split:{split}:episode:{episode_index}":
                raise ValueError("bAbI episode identity/order is not its native source ordinal")
            episodes[task_id].add(episode_id)
            facts = []
            previous_turn = None
        new_facts = row.get("new_facts")
        question = row.get("question")
        if not isinstance(new_facts, list) or any(not isinstance(x, str) for x in new_facts):
            raise ValueError("bAbI new_facts must be an explicit list of native fact strings")
        if not isinstance(question, str) or not question:
            raise ValueError("Missing native bAbI question")
        facts.extend(new_facts)
        if row.get("context") != "\n".join(facts + [question]):
            raise ValueError("bAbI context does not equal observed facts plus the current question")
        if row.get("native_text") != "\n".join(new_facts + [question]):
            raise ValueError("bAbI native teacher text differs from the fact/question audit")
        labels = row.get("native_labels")
        if not isinstance(labels, list) or len(labels) != 1 or not isinstance(labels[0], str) or not labels[0]:
            raise ValueError("Every selected native bAbI question needs its one nonempty label")
        if row.get("answer") != labels[0]:
            raise ValueError("bAbI answer differs from native_labels")
        if task_id in (8, 19) and "," in labels[0]:
            raise ValueError("Native task 8/19 labels must retain teacher comma-to-space conversion")
        turn = row.get("episode_turn")
        if type(turn) is not int or (previous_turn is None and turn not in (0, 1)) or (previous_turn is not None and turn != previous_turn + 1):
            raise ValueError("bAbI episode turns are missing or out of order")
        if type(row.get("episode_done")) is not bool:
            raise ValueError("bAbI episode_done must be a native boolean")
        if previous_episode == key and previous_done:
            raise ValueError("A completed bAbI episode was continued")
        counts[task_id] += 1
        previous_episode, previous_done, previous_turn = key, row["episode_done"], turn
    if not previous_done:
        raise ValueError("The final bAbI episode has no end boundary")
    expected = manifest["splits"][split]
    if len(rows) != expected["examples"] or sum(map(len, episodes.values())) != expected["episodes"]:
        raise ValueError("bAbI actual questions/episodes differ from the complete native split")
    for task_id in TASK_IDS:
        declared = expected["tasks"][str(task_id)]
        if counts[task_id] != declared["examples"] or len(episodes[task_id]) != declared["episodes"]:
            raise ValueError(f"Native bAbI task {task_id} coverage is incomplete")


def load_dataset(data: str | Path, task: str, split: str = "test") -> NativeDataset:
    """Accept a preparation directory, or the exact raw LAMBADA source file."""
    location = Path(data).resolve()
    if task not in ("babi", "lambada"):
        raise ValueError("Unknown native task")
    if task == "lambada" and split != "test":
        raise ValueError("This fixed LAMBADA task has only the test split")
    manifest_path = (location if location.is_dir() else location.parent) / "preparation.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        expected_format = f"lwm-{task}-preparation-v1"
        if manifest.get("format") != expected_format:
            raise ValueError(f"Expected {expected_format}")
        info = manifest.get("splits", {}).get(split)
        if not isinstance(info, dict):
            raise ValueError(f"Missing prepared {split} manifest")
        path = (manifest_path.parent / info["file"]).resolve()
        if not path.is_relative_to(manifest_path.parent):
            raise ValueError("Prepared split path escapes its data directory")
        if location.is_file() and path != location:
            raise ValueError("Explicit --data file differs from its selected split manifest")
        data_sha = sha256_file(path)
        if data_sha != info.get("sha256"):
            raise ValueError("Prepared split SHA-256 mismatch")
        rows = read_jsonl(path)
        if len(rows) != _count(info.get("examples"), "prepared examples"):
            raise ValueError("Prepared manifest denominator differs from actual row count")
    elif task == "lambada" and location.is_file():
        path = location
        data_sha = sha256_file(path)
        if data_sha != LAMBADA_SHA256 or path.stat().st_size != LAMBADA_BYTES:
            raise ValueError("Raw LAMBADA bytes do not match the fixed native source")
        rows = read_jsonl(path)
        manifest_path = None
        manifest = {"format": "lwm-lambada-preparation-v1", "dataset": "lambada_openai",
                    "source": {"repo_id": "EleutherAI/lambada_openai",
                               "revision": LAMBADA_REVISION,
                               "path": "data/lambada_test.jsonl",
                               "sha256": LAMBADA_SHA256, "bytes": LAMBADA_BYTES},
                    "splits": {"test": {"file": path.name, "sha256": data_sha,
                                         "examples": 5153}}}
        rows = [{**row, "id": f"lambada:{LAMBADA_SHA256}:{index}",
                 "source_row": index} for index, row in enumerate(rows)]
    else:
        raise ValueError("A preparation.json manifest is required beside the selected data")

    if task == "babi":
        if split not in BABI_COUNTS:
            raise ValueError("Unknown bAbI split")
        _validate_babi(rows, manifest, split)
    else:
        source = manifest.get("source", {})
        if source.get("sha256") != LAMBADA_SHA256 or source.get("revision") != LAMBADA_REVISION or source.get("bytes") != LAMBADA_BYTES:
            raise ValueError("LAMBADA manifest does not identify the fixed native source")
        if len(rows) != 5153:
            raise ValueError("LAMBADA requires all 5153 native passages")
        original_rows = None
        if manifest_path is not None:
            native_file = manifest.get("native_file")
            if not isinstance(native_file, str):
                raise ValueError("Prepared LAMBADA must retain the pinned original JSONL")
            original_path = (manifest_path.parent / native_file).resolve()
            if not original_path.is_relative_to(manifest_path.parent):
                raise ValueError("Original LAMBADA file escapes its preparation directory")
            if sha256_file(original_path) != LAMBADA_SHA256 or original_path.stat().st_size != LAMBADA_BYTES:
                raise ValueError("Retained original LAMBADA bytes differ from the pinned native source")
            original_rows = read_jsonl(original_path)
            if len(original_rows) != 5153:
                raise ValueError("Retained original LAMBADA denominator differs")
        for index, row in enumerate(rows):
            if row.get("id") != f"lambada:{LAMBADA_SHA256}:{index}" or row.get("source_row") != index:
                raise ValueError("LAMBADA native sample identity/order differs from pinned source rows")
            context, target = lambada_context_target(row.get("text"))
            if original_rows is not None and (row["text"] != original_rows[index].get("text") or row.get("source_document") != original_rows[index]):
                raise ValueError("Prepared LAMBADA row differs from the retained native source document")
            if "context" in row and row["context"] != context:
                raise ValueError("Prepared LAMBADA context changed native whitespace or word split")
            if "target" in row and row["target"] != target:
                raise ValueError("Prepared LAMBADA target changed its native leading space")
        _index(rows)
    return NativeDataset(task, split, path, manifest_path, manifest, rows, data_sha)


def validate_predictions(native: list[dict], predictions: list[dict], task: str) -> list[dict]:
    expected, observed = _index(native), _index(predictions)
    if set(expected) != set(observed):
        missing, extra = set(expected) - set(observed), set(observed) - set(expected)
        raise ValueError(f"Prediction ID mismatch: {len(missing)} missing, {len(extra)} extra")
    ordered = []
    for row in native:
        prediction = observed[row["id"]]
        if prediction.get("task") != task or prediction.get("input_sha256") != row_fingerprint(row):
            raise ValueError(f"Prediction task/input identity mismatch: {row['id']}")
        ordered.append(prediction)
    return ordered


# Adapted from ParlAI core/metrics.py at PARLAI_REVISION (MIT).
# Preserve its exact punctuation class and operation order; do not sort tokens.
_ARTICLES = re.compile(r"\b(a|an|the)\b")
_PUNCTUATION = re.compile(r'''[!"#$%&()*+,\-./:;<=>?@\[\]\\^`{|}~_']''')


def normalize_answer(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError("normalize_answer expects a string")
    return " ".join(_ARTICLES.sub(" ", _PUNCTUATION.sub(" ", text.lower())).split())


def babi_exact_match(prediction: Any, labels: list[str]) -> int:
    if not isinstance(labels, list) or not labels or any(not isinstance(x, str) for x in labels):
        raise ValueError("Native labels must be a nonempty string list")
    if not isinstance(prediction, str) or not prediction:
        return 0
    normalized = normalize_answer(prediction)
    return int(any(normalized == normalize_answer(label) for label in labels))


def _binary(value: Any, label: str) -> int:
    if type(value) not in (int, float, bool) or value not in (0, 1):
        raise ValueError(f"{label} must be a binary score")
    return int(value)


def aggregate_babi(predictions: list[dict]) -> dict:
    groups = defaultdict(list)
    for row in predictions:
        if type(row.get("task_id")) is not int or row["task_id"] not in TASK_IDS:
            raise ValueError("Invalid bAbI task identity")
        groups[row["task_id"]].append(_binary(row.get("exact_match"), "exact_match"))
    if set(groups) != set(TASK_IDS):
        raise ValueError("Native bAbI aggregation requires all 20 tasks")
    task_metrics = {str(task): {"accuracy": sum(groups[task]) / len(groups[task]),
                                "examples": len(groups[task])} for task in TASK_IDS}
    macro = sum(item["accuracy"] for item in task_metrics.values()) / 20
    return {"tasks": task_metrics, "accuracy": macro, "macro_accuracy": macro,
            "mean_error": 1.0 - macro,
            # Use an integer comparison to preserve the strict >5% rule.
            "failed_tasks_error_gt_0_05": sum(20 * (len(groups[t]) - sum(groups[t])) > len(groups[t]) for t in TASK_IDS),
            "examples": sum(map(len, groups.values()))}


def aggregate_lambada(predictions: list[dict]) -> dict:
    if not predictions:
        raise ValueError("LAMBADA cannot aggregate an empty denominator")
    likelihoods, accuracy = [], []
    for row in predictions:
        ll, greedy = row.get("log_likelihood"), row.get("is_greedy")
        if type(ll) not in (int, float) or not math.isfinite(ll) or ll > 1e-7:
            raise ValueError("Native log likelihood must be a finite nonpositive number")
        if type(greedy) is not bool:
            raise ValueError("Native is_greedy must already be boolean")
        likelihoods.append(float(ll))
        accuracy.append(int(greedy))
    mean_ll = sum(likelihoods) / len(likelihoods)
    try:
        perplexity = math.exp(-mean_ll)
    except OverflowError:
        perplexity = None
    return {"acc": sum(accuracy) / len(accuracy), "perplexity": perplexity,
            "perplexity_status": "overflow" if perplexity is None else "finite",
            "mean_log_likelihood_per_example": mean_ll, "examples": len(predictions)}


def verify_native_source(source: str | Path, task: str) -> dict:
    root = Path(source).resolve()
    revision = PARLAI_REVISION if task == "babi" else HARNESS_REVISION
    def git(*args):
        return subprocess.run(["git", "-C", str(root), *args], check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip()
    if git("rev-parse", "HEAD") != revision:
        raise ValueError(f"Native scorer checkout must be at pinned revision {revision}")
    if git("status", "--porcelain", "--untracked-files=no"):
        raise ValueError("Native scorer tracked files are modified; use the pinned clean source")
    names = (["parlai/core/metrics.py", "parlai/core/message.py", "parlai/tasks/babi/agents.py"]
             if task == "babi" else ["lm_eval/api/task.py", "lm_eval/api/metrics.py",
                                     "lm_eval/api/model.py", "lm_eval/models/huggingface.py",
                                     "lm_eval/tasks/lambada/lambada_openai.yaml"])
    return {"path": str(root), "revision": revision,
            "files": {name: sha256_file(root / name) for name in names}}


def _verify_import(obj, root: Path) -> None:
    if not Path(inspect.getfile(obj)).resolve().is_relative_to(root):
        raise ValueError("An already imported native package came from a different checkout")


def _metric_number(value: Any) -> float:
    result = float(value.value() if hasattr(value, "value") else value)
    if not math.isfinite(result):
        raise ValueError("Native scorer returned a non-finite metric")
    return result


def replay_native(dataset: NativeDataset, predictions: list[dict], source: str | Path) -> dict:
    """Actually invoke pinned author code; never infer a PASS from source text."""
    ordered = validate_predictions(dataset.rows, predictions, dataset.task)
    identity = verify_native_source(source, dataset.task)
    root = Path(identity["path"])
    stdout, stderr = io.StringIO(), io.StringIO()
    started = time.perf_counter()
    old_path = list(sys.path)
    sys.path.insert(0, str(root))
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            if dataset.task == "babi":
                metrics_module = importlib.import_module("parlai.core.metrics")
                message_module = importlib.import_module("parlai.core.message")
                TeacherMetrics = metrics_module.TeacherMetrics
                _verify_import(TeacherMetrics, root)
                _verify_import(message_module.Message, root)
                metrics = {task: TeacherMetrics(metrics_list="accuracy") for task in TASK_IDS}
                for native, prediction in zip(dataset.rows, ordered, strict=True):
                    text = prediction.get("prediction")
                    # Invalid/empty answers are errors, never skipped by None.
                    text = text if isinstance(text, str) else ""
                    labels = native["native_labels"]
                    if prediction.get("task_id") != native["task_id"] or prediction.get("native_labels") != labels:
                        raise ValueError("Prediction task or labels differ from native bAbI data")
                    expected = babi_exact_match(text, labels)
                    if _binary(prediction.get("exact_match"), "exact_match") != expected:
                        raise ValueError("Stored bAbI score differs from its prediction")
                    score = metrics_module.ExactMatchMetric.compute(text, labels)
                    if score is None or _metric_number(score) != expected:
                        raise ValueError("Pinned native per-question exact match differs from local contract")
                    metrics[native["task_id"]].evaluate_response(message_module.Message({"text": text}), labels)
                reports = {str(task): metric.report() for task, metric in metrics.items()}
                native_report = metrics_module.aggregate_named_reports(reports, micro_average=False)
                per_task = {task: {"accuracy": _metric_number(report["accuracy"]),
                                   "examples": int(_metric_number(report["exs"]))}
                            for task, report in reports.items()}
                for task, report in per_task.items():
                    if report["examples"] != dataset.manifest["splits"][dataset.split]["tasks"][task]["examples"]:
                        raise ValueError("Native scorer reduced a bAbI task denominator")
                local = aggregate_babi(ordered)
                accuracy = _metric_number(native_report["accuracy"])
                if not math.isclose(accuracy, local["accuracy"], rel_tol=0, abs_tol=1e-12):
                    raise ValueError("Native macro aggregation differs from local preview")
                result_metrics = {**local, "accuracy": accuracy, "macro_accuracy": accuracy,
                                  "tasks": per_task,
                                  "native_report": {key: _metric_number(value) for key, value in native_report.items()}}
            else:
                task_module = importlib.import_module("lm_eval.api.task")
                utils = importlib.import_module("lm_eval.utils")
                _verify_import(task_module.ConfigurableTask, root)
                config = utils.load_yaml_config(str(root / "lm_eval/tasks/lambada/lambada_openai.yaml"))
                config["dataset_path"] = "json"
                config["dataset_name"] = None
                native_path = (dataset.manifest_path.parent / dataset.manifest["native_file"]
                               if dataset.manifest_path else dataset.path)
                config["dataset_kwargs"] = {"data_files": {"test": str(native_path)}}
                task = task_module.ConfigurableTask(config=config)
                if len(task.dataset["test"]) != 5153:
                    raise ValueError("Official task loader changed the native LAMBADA denominator")
                all_acc, all_ll = [], []
                for index, (native, prediction) in enumerate(zip(dataset.rows, ordered, strict=True)):
                    document = task.dataset["test"][index]
                    if document["text"] != native["text"]:
                        raise ValueError("Official task loader changed native row content/order")
                    context, target = lambada_context_target(native["text"])
                    if task.doc_to_text(document) != context or task.doc_to_target(document) != target:
                        raise ValueError("Official context/target transform differs from the adapter")
                    aggregate_lambada([prediction])  # Reject coercions/non-finite values first.
                    score = task.process_results(document, [(prediction["log_likelihood"], prediction["is_greedy"])])
                    if score["acc"] != int(prediction["is_greedy"]) or score["perplexity"] != prediction["log_likelihood"]:
                        raise ValueError("Native LAMBADA per-example result differs")
                    all_acc.append(score["acc"])
                    all_ll.append(score["perplexity"])
                aggregators = task.aggregation()
                native_acc = float(aggregators["acc"](all_acc))
                native_ppl = float(aggregators["perplexity"](all_ll))
                if not math.isfinite(native_acc) or not math.isfinite(native_ppl):
                    raise ValueError("Official LAMBADA aggregation overflowed or was non-finite")
                local = aggregate_lambada(ordered)
                if local["perplexity"] is None or not math.isclose(native_acc, local["acc"], rel_tol=0, abs_tol=1e-12) or not math.isclose(native_ppl, local["perplexity"], rel_tol=1e-12, abs_tol=0):
                    raise ValueError("Native LAMBADA aggregation differs from the local preview")
                result_metrics = {**local, "acc": native_acc, "perplexity": native_ppl}
    finally:
        sys.path[:] = old_path
    return {"native_aggregation_replay": "passed", "model_adapter_parity": "pending_local",
            "scope": "complete native per-example scoring and aggregation, not model forward parity",
            "task": dataset.task, "split": dataset.split, "examples": len(ordered),
            "source": identity, "data_sha256": dataset.sha256,
            "prediction_records_sha256": row_fingerprint({"rows": ordered}),
            "metrics": result_metrics, "wall_seconds": time.perf_counter() - started,
            "per_example_tolerance": 0, "aggregate_float_tolerance": 1e-12,
            "argv": sys.argv, "cwd": str(Path.cwd()),
            "stdout": stdout.getvalue(), "stderr": stderr.getvalue()}


def _quantile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    left = math.floor(position)
    right = min(left + 1, len(ordered) - 1)
    return ordered[left] + (ordered[right] - ordered[left]) * (position - left)


def paired_bootstrap(left: list[dict], right: list[dict], task: str,
                     iterations: int = 2000, seed: int = 0,
                     confidence: float = 0.95) -> dict:
    """Right-minus-left accuracy; native bAbI questions stay in episode clusters.

    This helper accepts numeric engineering cases. The CLI additionally requires
    full native evaluation manifests/denominators. Intervals condition on these
    checkpoints and examples; they do not cover training-seed variability or
    authorize simultaneous per-task significance claims.
    """
    if task not in ("babi", "lambada") or type(iterations) is not int or iterations < 2 or not 0 < confidence < 1:
        raise ValueError("Invalid paired-bootstrap configuration")
    a, b = _index(left), _index(right)
    if set(a) != set(b):
        raise ValueError("Paired analysis requires exactly identical IDs")
    groups = defaultdict(lambda: defaultdict(list))
    for identity, lrow in a.items():
        rrow = b[identity]
        fields = ("task", "input_sha256", "native_labels", "task_id", "episode_id") if task == "babi" else ("task", "input_sha256", "target", "target_token_ids")
        if any(lrow.get(name) != rrow.get(name) for name in fields):
            raise ValueError(f"Paired record identity/content differs: {identity}")
        if lrow.get("task") != task or not isinstance(lrow.get("input_sha256"), str):
            raise ValueError("Missing paired task/input provenance")
        if task == "babi":
            task_id, unit = lrow.get("task_id"), lrow.get("episode_id")
            if type(task_id) is not int or not isinstance(unit, str) or not unit:
                raise ValueError("bAbI paired analysis requires episode identities")
            delta = _binary(rrow.get("exact_match"), "right exact_match") - _binary(lrow.get("exact_match"), "left exact_match")
        else:
            if type(lrow.get("is_greedy")) is not bool or type(rrow.get("is_greedy")) is not bool:
                raise ValueError("LAMBADA greedy flags must be boolean")
            task_id, unit = 0, identity
            delta = int(rrow["is_greedy"]) - int(lrow["is_greedy"])
        groups[task_id][unit].append(delta)
    clusters = {key: [(sum(values), len(values)) for _, values in sorted(units.items())]
                for key, units in sorted(groups.items())}
    point = sum(sum(total for total, _ in units) / sum(size for _, size in units)
                for units in clusters.values()) / len(clusters)
    rng = random.Random(seed)
    draws = []
    for _ in range(iterations):
        task_deltas = []
        for units in clusters.values():
            selected = [units[rng.randrange(len(units))] for _ in range(len(units))]
            task_deltas.append(sum(total for total, _ in selected) / sum(size for _, size in selected))
        draws.append(sum(task_deltas) / len(task_deltas))
    tail = (1 - confidence) / 2
    return {"task": task, "metric": "macro_accuracy" if task == "babi" else "acc",
            "delta_right_minus_left": point,
            "confidence_interval": [_quantile(draws, tail), _quantile(draws, 1 - tail)],
            "confidence": confidence, "iterations": iterations, "seed": seed,
            "examples": len(a), "clusters": sum(map(len, clusters.values())),
            "resampling_unit": "episode_within_task" if task == "babi" else "passage",
            "limitations": ["Conditional on these checkpoints; no training-seed uncertainty",
                            "Percentile interval; no multiplicity adjustment",
                            "No per-task or causal claim follows from an aggregate interval"]}


def _run_manifest(predictions: Path) -> dict:
    manifest = json.loads((predictions.parent / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("execution_status") != "completed" or manifest.get("predictions_sha256") != sha256_file(predictions):
        raise ValueError("Prediction file lacks its matching completed immutable run manifest")
    task, split = manifest.get("task"), manifest.get("split")
    if (task not in ("babi", "lambada") or
            (task == "lambada" and split != "test") or
            (task == "babi" and split not in BABI_COUNTS)):
        raise ValueError("Run manifest has an unsupported native task/split")
    expected = 5153 if task == "lambada" else BABI_COUNTS[split][0]
    if type(manifest.get("examples")) is not int or manifest["examples"] != expected:
        raise ValueError("Run manifest lacks its complete native denominator")
    return manifest


def factorial_bootstrap(memory4: list[dict], reset4: list[dict],
                        memory1: list[dict], reset1: list[dict], task: str,
                        iterations: int = 2000, seed: int = 0,
                        confidence: float = 0.95) -> dict:
    """Paired (M4-R4)-(M1-R1), with shared native resamples for all four arms.

    The original design's interaction estimand uses the same episode/passage
    units as paired_bootstrap. It is not four independently bootstrapped means.
    """
    if task not in ("babi", "lambada") or type(iterations) is not int or iterations < 2 or not 0 < confidence < 1:
        raise ValueError("Invalid factorial-bootstrap configuration")
    indexed = [_index(rows) for rows in (memory4, reset4, memory1, reset1)]
    if any(set(rows) != set(indexed[0]) for rows in indexed[1:]):
        raise ValueError("Interaction requires exactly identical four-arm IDs")
    fields = (("task", "input_sha256", "native_labels", "task_id", "episode_id")
              if task == "babi" else ("task", "input_sha256", "target", "target_token_ids"))
    groups = defaultdict(lambda: defaultdict(list))
    for identity, reference in indexed[0].items():
        rows = [arm[identity] for arm in indexed]
        if (reference.get("task") != task or not isinstance(reference.get("input_sha256"), str)
                or any(any(row.get(field) != reference.get(field) for field in fields) for row in rows[1:])):
            raise ValueError(f"Interaction input identity differs: {identity}")
        if task == "babi":
            task_id, unit = reference.get("task_id"), reference.get("episode_id")
            if type(task_id) is not int or not isinstance(unit, str) or not unit:
                raise ValueError("Interaction requires native episode IDs")
            values = [_binary(row.get("exact_match"), "interaction exact_match") for row in rows]
        else:
            if any(type(row.get("is_greedy")) is not bool for row in rows):
                raise ValueError("Interaction greedy flags must be boolean")
            task_id, unit = 0, identity
            values = [int(row["is_greedy"]) for row in rows]
        groups[task_id][unit].append(values[0] - values[1] - values[2] + values[3])
    clusters = {key: [(sum(values), len(values)) for _, values in sorted(units.items())]
                for key, units in sorted(groups.items())}
    point = sum(sum(total for total, _ in units) / sum(size for _, size in units)
                for units in clusters.values()) / len(clusters)
    rng, draws = random.Random(seed), []
    for _ in range(iterations):
        effects = []
        for units in clusters.values():
            selected = [units[rng.randrange(len(units))] for _ in units]
            effects.append(sum(total for total, _ in selected) / sum(size for _, size in selected))
        draws.append(sum(effects) / len(effects))
    tail = (1 - confidence) / 2
    return {"task": task, "estimand": "(memory4-reset4)-(memory1-reset1)",
            "interaction": point, "confidence_interval": [_quantile(draws, tail), _quantile(draws, 1-tail)],
            "confidence": confidence, "iterations": iterations, "seed": seed,
            "examples": len(indexed[0]), "clusters": sum(map(len, clusters.values())),
            "resampling_unit": "episode_within_task" if task == "babi" else "passage",
            "limitations": ["Conditional on four checkpoints; no training-seed uncertainty",
                            "Exploratory percentile interval; no multiplicity adjustment",
                            "Interaction does not alone establish causal mechanism or novelty"]}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    replay = sub.add_parser("replay", help="Actually replay complete predictions through pinned author scoring code")
    replay.add_argument("--task", required=True, choices=("babi", "lambada"))
    replay.add_argument("--data", type=Path, required=True)
    replay.add_argument("--split", default="test", choices=("train", "valid", "test"))
    replay.add_argument("--predictions", type=Path, required=True)
    replay.add_argument("--native-source", type=Path, required=True)
    replay.add_argument("--output", type=Path, required=True)
    compare = sub.add_parser("compare", help="Paired bootstrap from two explicitly selected prediction files")
    compare.add_argument("--left", type=Path, required=True)
    compare.add_argument("--right", type=Path, required=True)
    compare.add_argument("--output", type=Path, required=True)
    compare.add_argument("--iterations", type=int, default=2000)
    compare.add_argument("--seed", type=int, default=0)
    compare.add_argument("--confidence", type=float, default=0.95)
    interaction = sub.add_parser("interaction", help="Complete native four-arm paired interaction")
    for name in ("memory4", "reset4", "memory1", "reset1"):
        interaction.add_argument("--" + name, type=Path, required=True)
    interaction.add_argument("--output", type=Path, required=True)
    interaction.add_argument("--iterations", type=int, default=2000)
    interaction.add_argument("--seed", type=int, default=0)
    interaction.add_argument("--confidence", type=float, default=0.95)
    args = parser.parse_args(argv)
    args.output.mkdir(parents=True, exist_ok=False)
    if args.command == "replay":
        dataset = load_dataset(args.data, args.task, args.split)
        result = replay_native(dataset, read_jsonl(args.predictions), args.native_source)
        result["predictions_sha256"] = sha256_file(args.predictions)
        write_json(args.output / "native-replay.json", result)
    elif args.command == "interaction":
        names = ("memory4", "reset4", "memory1", "reset1")
        paths = [getattr(args, name) for name in names]
        manifests = [_run_manifest(path) for path in paths]
        for manifest in manifests[1:]:
            if any(manifest.get(field) != manifests[0].get(field) for field in ("task", "split", "data_sha256", "examples")):
                raise ValueError("Interaction manifests cannot be paired")
        task, split = manifests[0]["task"], manifests[0]["split"]
        rows = [read_jsonl(path) for path in paths]
        expected = 5153 if task == "lambada" else BABI_COUNTS[split][0]
        if manifests[0]["examples"] != expected or any(len(arm) != expected for arm in rows):
            raise ValueError("Interaction lacks a complete native denominator")
        result = factorial_bootstrap(*rows, task, args.iterations, args.seed, args.confidence)
        result["runs"] = {name: {"path": str(path.resolve()), "sha256": sha256_file(path)}
                          for name, path in zip(names, paths, strict=True)}
        result["native_qualification"] = {name: manifest.get("qualification")
                                         for name, manifest in zip(names, manifests, strict=True)}
        write_json(args.output / "factorial-bootstrap.json", result)
    else:
        left_manifest, right_manifest = _run_manifest(args.left), _run_manifest(args.right)
        for field in ("task", "split", "data_sha256", "examples"):
            if left_manifest.get(field) != right_manifest.get(field):
                raise ValueError(f"Run manifest {field} differs; cannot pair")
        task = left_manifest["task"]
        left, right = read_jsonl(args.left), read_jsonl(args.right)
        expected = 5153 if task == "lambada" else BABI_COUNTS[left_manifest["split"]][0]
        if len(left) != expected or len(right) != expected or left_manifest["examples"] != expected:
            raise ValueError("Comparison does not cover a complete native denominator")
        result = paired_bootstrap(left, right, task, args.iterations, args.seed, args.confidence)
        result["runs"] = {"left": {"path": str(args.left.resolve()), "sha256": sha256_file(args.left)},
                          "right": {"path": str(args.right.resolve()), "sha256": sha256_file(args.right)}}
        result["native_qualification"] = {"left": left_manifest.get("qualification"),
                                           "right": right_manifest.get("qualification")}
        write_json(args.output / "paired-bootstrap.json", result)


if __name__ == "__main__":
    main()
