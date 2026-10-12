"""Apply a manifest-bound checkpoint delta to an exact base restoration only."""
import argparse
import base64
import hashlib
import io
import json
import zipfile
from pathlib import Path

ap=argparse.ArgumentParser();ap.add_argument('--archive',required=True);ap.add_argument('--manifest',required=True);ap.add_argument('--destination',required=True);a=ap.parse_args()
m=json.loads(Path(a.manifest).read_text());raw=base64.b64decode(Path(a.archive).read_bytes(),validate=True)
if hashlib.sha256(raw).hexdigest()!=m['archive_sha256']:raise SystemExit('Delta archive hash mismatch')
root=Path(a.destination).resolve();root.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(io.BytesIO(raw)) as z:
    names=set(z.namelist())
    if names!=set(m['members']):raise SystemExit('Member inventory mismatch')
    staged=[]
    for name in sorted(names):
        target=(root/name).resolve()
        if not target.is_relative_to(root) or target.is_symlink():raise SystemExit('Unsafe destination')
        data=z.read(name);meta=m['members'][name]
        if hashlib.sha256(data).hexdigest()!=meta['sha256']:raise SystemExit('Member digest mismatch: '+name)
        if target.exists():
            old=hashlib.sha256(target.read_bytes()).hexdigest()
            if old not in [meta['previous_sha256'],meta['sha256']]:raise SystemExit('Conflicting live or non-base file: '+name)
        elif meta['previous_sha256'] is not None:raise SystemExit('Restore the base first: '+name)
        staged.append((target,data))
    for target,data in staged:
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(data)
print(json.dumps({'delta_members':len(staged),'destination':str(root),'next_action':'Reconcile original runner identity and cumulative budget;do not init a new runner or overwrite live state.'}))
