"""Run one CPU command with controlled threads and observed RSS; no hidden retry."""
import argparse
import json
import os
import resource
from pathlib import Path
import signal
import subprocess
import sys
import time

ap=argparse.ArgumentParser();ap.add_argument('--resource-output',required=True);ap.add_argument('--rss-mib',type=int,default=256);ap.add_argument('argv',nargs=argparse.REMAINDER);args=ap.parse_args()
argv=args.argv[1:] if args.argv and args.argv[0]=='--' else args.argv
if not argv:raise SystemExit('Missing argv')
env=dict(os.environ)
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[key]='1'
def enforce_data_limit():
    cap=args.rss_mib*1024**2
    resource.setrlimit(resource.RLIMIT_DATA,(cap,cap))
t=time.perf_counter();child=subprocess.Popen(argv,env=env,preexec_fn=enforce_data_limit);peak=0;limit_exceeded=False;rss_samples=0
while child.poll() is None:
    try:
        status=Path(f'/proc/{child.pid}/status').read_text()
        rss=next(int(line.split()[1])*1024 for line in status.splitlines() if line.startswith('VmRSS:'))
        peak=max(peak,rss)
        rss_samples+=1
        if rss>args.rss_mib*1024**2:
            limit_exceeded=True;child.terminate()
            try:child.wait(timeout=3)
            except subprocess.TimeoutExpired:child.kill()
            break
    except (FileNotFoundError,StopIteration,ProcessLookupError):pass
    time.sleep(.02)
rc=child.wait();usage=resource.getrusage(resource.RUSAGE_CHILDREN);kernel_peak=int(usage.ru_maxrss*1024)
path=Path(args.resource_output);path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps({'argv':argv,'returncode':rc,'elapsed_seconds':time.perf_counter()-t,'peak_observed_rss_bytes':max(peak,kernel_peak),'kernel_child_maxrss_bytes':kernel_peak,'proc_rss_samples':rss_samples,'data_allocation_limit_mib':args.rss_mib,'sampled_rss_limit_exceeded':limit_exceeded,'cpu_user_seconds':usage.ru_utime,'cpu_system_seconds':usage.ru_stime,'thread_environment_requested':1,'actual_solver_threads':'not_measured','sampling_seconds':.02,'rss_scope':'Linux RUSAGE_CHILDREN peak includes inherited process pages; proc sampling may be unavailable across PID namespaces; RLIMIT_DATA caps data allocations,not total RSS'},indent=2)+'\n')
raise SystemExit(125 if limit_exceeded else rc)
