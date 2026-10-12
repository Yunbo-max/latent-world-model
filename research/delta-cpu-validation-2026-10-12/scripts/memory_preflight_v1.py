"""Read-only cgroup observation; does not reserve memory or evict other projects."""
import argparse
import json
import time
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--output', required=True)
ap.add_argument('--need-mib', type=int, default=128)
ap.add_argument('--margin-mib', type=int, default=256)
args = ap.parse_args()
cg = Path('/sys/fs/cgroup')
limit_text = (cg / 'memory.max').read_text().strip()
limit = None if limit_text == 'max' else int(limit_text)
current = int((cg / 'memory.current').read_text())
stats = {k: int(v) for k, v in (line.split() for line in (cg / 'memory.stat').read_text().splitlines())}
events = {k: int(v) for k, v in (line.split() for line in (cg / 'memory.events').read_text().splitlines())}
headroom = None if limit is None else max(0, limit - current)
required = (args.need_mib + args.margin_mib) * 1024 ** 2
inactive_clean_estimate = max(0, stats.get('inactive_file', 0) - stats.get('file_dirty', 0) - stats.get('file_writeback', 0))
eligible = limit is not None and headroom >= required
record = dict(observed_at_epoch=time.time(), memory_max_bytes=limit, memory_current_bytes=current,
              memory_stat=stats, memory_events=events, uncharged_headroom_bytes=headroom,
              estimated_incremental_working_set_bytes=args.need_mib * 1024 ** 2,
              safety_margin_bytes=args.margin_mib * 1024 ** 2,
              inactive_clean_file_cache_estimate_bytes=inactive_clean_estimate,
              decision='ready_without_assumed_reclaim' if eligible else 'waiting_for_memory',
              conservative_rule='Use raw headroom for this small workload; report reclaimable cache separately, do not treat it as guaranteed allocation.',
              waiting_rule='Retain same experiment identity, recheck on next existing wake; notify after three memory-blocked wakes or proven minimum-workset excess.',
              limitations='Shared host observation is not a reservation; cache estimate is heuristic; no other files/processes were modified.')
Path(args.output).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({k: record[k] for k in ['memory_max_bytes', 'memory_current_bytes', 'uncharged_headroom_bytes', 'decision']}))
