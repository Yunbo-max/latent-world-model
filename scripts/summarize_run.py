"""Summarize actual Local logs, never substitute an estimated training result."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run")
    parser.add_argument("--project-tokens", type=int, default=100000000)
    args = parser.parse_args()
    rows = [json.loads(line) for line in (Path(args.run) / "events.jsonl").read_text().splitlines()]
    starts = [index for index, item in enumerate(rows) if item["event"] == "start"]
    if not starts:
        raise ValueError("No actual start receipt")
    window = rows[starts[-1]:]
    updates = [item for item in window if item["event"] == "update"]
    if len(updates) < 4:
        raise ValueError("Need at least four actual updates to exclude the first two warmup updates")
    first, last = updates[1], updates[-1]
    elapsed = last["elapsed_seconds"] - first["elapsed_seconds"]
    seen = last["seen_targets"] - first["seen_targets"]
    optimized = last["optimized_targets"] - first["optimized_targets"]
    if elapsed <= 0 or seen <= 0:
        raise ValueError("Invalid measured duration or token count")
    rate = seen / elapsed
    result = {"run": args.run, "start": window[0], "measured_updates": len(updates) - 2,
              "seen_targets_per_second": rate, "optimized_targets_per_second": optimized / elapsed,
              "measured_seconds": elapsed, "peak_allocated_bytes": max(item["peak_memory_bytes"] for item in updates),
              "projected_training_body_hours": args.project_tokens / rate / 3600,
              "projection_scope": "Estimate from this measured profile; excludes future validation/checkpoint/evaluation, retries and other arms",
              "status": json.loads((Path(args.run) / "status.json").read_text())}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
