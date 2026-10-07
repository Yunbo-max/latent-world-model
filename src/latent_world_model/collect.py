"""Collect retained small metadata and hashes; never infer missing results."""
import argparse
import csv
from pathlib import Path
import shutil
from .io import read_json, sha256_file, write_json


def collect(runs, output):
    runs, output = Path(runs).resolve(), Path(output).resolve()
    if output.exists():
        raise ValueError("Choose a new return packet path")
    output.mkdir(parents=True)
    inventory, metrics, statuses = [], [], []
    candidates = sorted(runs.rglob("*"))
    for path in candidates:
        if not path.is_file() or path.is_relative_to(output):
            continue
        if path.suffix not in {".json", ".jsonl", ".log", ".txt", ".yaml"}:
            continue
        relative = path.relative_to(runs)
        # Native per-example logs remain on host by default; their hashes retain
        # identity without silently publishing benchmark text to another service.
        withheld = "predictions" in path.name or "samples" in path.name
        item = {"path": str(relative), "sha256": sha256_file(path), "bytes": path.stat().st_size,
                "copied": not withheld and path.stat().st_size <= 10_000_000}
        inventory.append(item)
        if item["copied"]:
            destination = output / "records" / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, destination)
        if path.name == "results.json":
            result = read_json(path)
            for task, values in result.get("results", {}).items():
                for key, value in values.items():
                    if isinstance(value, (int, float)):
                        metrics.append({"run": str(relative.parent), "task": task, "metric": key, "value": value})
        if path.name == "status.json":
            statuses.append({"run": str(relative.parent), **read_json(path)})
    with (output / "native_metrics.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["run", "task", "metric", "value"])
        writer.writeheader()
        writer.writerows(metrics)
    write_json(output / "manifest.json", {"source_runs": str(runs), "files": inventory,
        "training_statuses": statuses, "scientific_result_verified": False,
        "note": "No missing/failed comparison is converted into a zero or omitted verdict. Native sample logs remain at listed host paths."})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", default="runs")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    collect(args.runs, args.output)


if __name__ == "__main__":
    main()
