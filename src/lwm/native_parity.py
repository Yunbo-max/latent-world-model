"""Compare all bAbI author Teacher exports with the prepared native records.

Source status: generated_unexecuted. Run on Local after the full author exporter
has actually produced all 60 files. This comparison uses the pinned author's
str_to_msg; it neither installs/qualifies the exporter nor launches a model.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import importlib
from itertools import zip_longest
import math
from pathlib import Path
import platform
import sys
import time
import traceback

from .scoring import (
    BABI_COUNTS, TASK_IDS, _verify_import, load_dataset, sha256_file,
    verify_native_source, write_json,
)


def iter_export(path, parse_message):
    """Read the author's canonical escaped, tab-separated export format."""
    needs_separator = False
    with Path(path).open(encoding="utf-8") as stream:
        for number, raw in enumerate(stream, 1):
            line = raw.rstrip("\r\n")
            where = f"{path}:{number}"
            if line == "":
                if not needs_separator:
                    raise ValueError(f"{where}: unexpected blank episode separator")
                needs_separator = False
                continue
            if needs_separator:
                raise ValueError(f"{where}: missing author episode separator")
            fields = {}
            for entry in line.split("\t"):
                key, delimiter, value = entry.partition(":")
                if not delimiter or not key or key in fields:
                    raise ValueError(f"{where}: malformed or duplicate export field")
                fields[key] = value
            if not {"text", "labels"}.issubset(fields):
                raise ValueError(f"{where}: missing teacher text or labels")
            # Upstream str_to_msg uses bool(value), so even 'False' is true.
            # The actual exporter omits False and serializes True literally.
            if "episode_done" in fields and fields["episode_done"] != "True":
                raise ValueError(f"{where}: noncanonical episode_done")
            message = parse_message(line)
            if message is None:
                raise ValueError(f"{where}: native parser returned no message")
            needs_separator = message["episode_done"]
            yield number, message
    if needs_separator:
        raise ValueError(f"{path}: missing final author episode separator")


def compare_babi_records(rows, messages, label):
    """Exact ordinal comparison; this unit alone cannot qualify native coverage."""
    missing = object()
    examples = episodes = turn = 0
    for row, item in zip_longest(rows, messages, fillvalue=missing):
        if row is missing or item is missing:
            raise ValueError(f"{label}: missing or extra teacher/prepared row after {examples}")
        line, message = item
        where = f"{label}:{line} prepared_id={row.get('id')}"
        expected = {"text": row.get("native_text"), "labels": row.get("native_labels"),
                    "episode_done": row.get("episode_done")}
        for field, value in expected.items():
            if message.get(field) != value:
                raise ValueError(f"{where}: {field} mismatch")
        if type(message.get("episode_done")) is not bool:
            raise ValueError(f"{where}: episode_done must be boolean")
        for field, value in (("episode_index", episodes), ("episode_turn", turn)):
            if type(row.get(field)) is not int or row[field] != value:
                raise ValueError(f"{where}: {field} mismatch")
        rewards = (message.get("reward", 0), row.get("native_reward"))
        if any(type(value) not in (int, float) or not math.isfinite(value) for value in rewards):
            raise ValueError(f"{where}: invalid reward")
        if rewards[0] != rewards[1]:
            raise ValueError(f"{where}: reward mismatch")
        examples += 1
        if message["episode_done"]:
            episodes += 1
            turn = 0
        else:
            turn += 1
    if not examples or turn:
        raise ValueError(f"{label}: empty export or incomplete final episode")
    return {"examples": examples, "episodes": episodes}


def verify_snapshot(files, exports, expected_files):
    """Recheck every consumed byte source and the exact final export inventory."""
    actual = {p.name for p in exports.iterdir() if p.suffix == ".txt" and p.is_file()}
    if actual != expected_files:
        raise ValueError("Teacher export inventory changed before final publication")
    for path, digest in files.items():
        if sha256_file(path) != digest:
            raise ValueError(f"{path}: input changed before final publication")


def run(data: Path, exports: Path, source: Path, output: Path) -> dict:
    """Require all native splits/tasks and publish success only after all pass."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    completed = []
    old_path = list(sys.path)
    try:
        data, exports, source = Path(data).resolve(), Path(exports).resolve(), Path(source).resolve()
        expected_files = {f"task-{task}-{split}.txt" for split in BABI_COUNTS for task in TASK_IDS}
        actual_files = {p.name for p in exports.iterdir() if p.suffix == ".txt" and p.is_file()}
        if actual_files != expected_files:
            raise ValueError(f"Require exactly 60 teacher exports; missing={sorted(expected_files-actual_files)}, extra={sorted(actual_files-expected_files)}")
        identity = verify_native_source(source, "babi")
        additional = ("parlai/utils/misc.py", "parlai/core/teachers.py",
                      "parlai/scripts/convert_data_to_parlai_format.py")
        identity["files"].update({name: sha256_file(source / name) for name in additional})
        sys.path.insert(0, str(source))
        misc = importlib.import_module("parlai.utils.misc")
        _verify_import(misc.str_to_msg, source)
        manifest_path = data / "preparation.json"
        manifest_sha = sha256_file(manifest_path)
        datasets = {}
        for split in BABI_COUNTS:
            dataset = load_dataset(data, "babi", split)
            grouped = defaultdict(list)
            for row in dataset.rows:
                grouped[row["task_id"]].append(row)
            for task in TASK_IDS:
                path = exports / f"task-{task}-{split}.txt"
                digest = sha256_file(path)
                counts = compare_babi_records(grouped[task], iter_export(path, misc.str_to_msg), str(path))
                declared = dataset.manifest["splits"][split]["tasks"][str(task)]
                if any(counts[key] != declared[key] for key in ("examples", "episodes")):
                    raise ValueError(f"{path}: native per-task denominator mismatch")
                if sha256_file(path) != digest:
                    raise ValueError(f"{path}: export changed during comparison")
                completed.append({"task_id": task, "split": split, "path": str(path),
                                  "sha256": digest, **counts})
            if sha256_file(dataset.path) != dataset.sha256:
                raise ValueError(f"{dataset.path}: prepared data changed during comparison")
            datasets[split] = {"path": str(dataset.path), "sha256": dataset.sha256,
                               "examples": len(dataset.rows)}
        # Detect modification after an individual file was checked as well.
        snapshot = {manifest_path: manifest_sha}
        snapshot.update({Path(item["path"]): item["sha256"] for item in datasets.values()})
        snapshot.update({Path(item["path"]): item["sha256"] for item in completed})
        verify_snapshot(snapshot, exports, expected_files)
        final_source = verify_native_source(source, "babi")
        final_source["files"].update({name: sha256_file(source / name) for name in additional})
        if final_source != identity:
            raise ValueError("Native source changed during comparison")
        result = {"format": "lwm-babi-teacher-parity-v1", "native_data_parity": "passed",
                  "scope": "all 60 exported task/split text, labels, rewards and episode boundaries in native order",
                  "model_adapter_parity": "pending_local", "native_scoring": "not_run_by_this_command",
                  "exporter_environment": "requires separate actual installation/import/export receipts",
                  "source": identity, "preparation_sha256": manifest_sha, "datasets": datasets,
                  "completed_tasks": completed, "examples": sum(v["examples"] for v in completed),
                  "episodes": sum(v["episodes"] for v in completed),
                  "python": platform.python_version(), "argv": sys.argv,
                  "checker_sha256": sha256_file(__file__), "wall_seconds": time.perf_counter()-started}
        write_json(output / "babi-teacher-parity.json", result)
        return result
    except Exception as error:
        write_json(output / "failure.json", {"status": "failed", "error_type": type(error).__name__,
                   "message": str(error), "completed_tasks": completed,
                   "traceback": traceback.format_exc(), "wall_seconds": time.perf_counter()-started})
        raise
    finally:
        sys.path[:] = old_path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--exports", type=Path, required=True)
    parser.add_argument("--native-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = run(args.data, args.exports, args.native_source, args.output)
    print(f"Compared {result['examples']} native questions in {len(result['completed_tasks'])} task/splits")


if __name__ == "__main__":
    main()
