"""Restore the delivered ZIP/base64 checkpoint without inventing new runner state."""
import argparse,base64,hashlib,io,json,zipfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--archive',required=True);p.add_argument('--manifest',required=True);p.add_argument('--destination',required=True);a=p.parse_args()
manifest=json.loads(Path(a.manifest).read_text());raw=base64.b64decode(Path(a.archive).read_bytes(),validate=True)
if hashlib.sha256(raw).hexdigest()!=manifest['archive_sha256']:raise SystemExit('Archive hash mismatch')
destination=Path(a.destination).resolve();destination.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(io.BytesIO(raw)) as z:
 for info in z.infolist():
  target=(destination/info.filename).resolve()
  if not target.is_relative_to(destination) or (info.external_attr>>16)&0o170000==0o120000:raise SystemExit('Unsafe archive member')
  if info.is_dir():target.mkdir(parents=True,exist_ok=True);continue
  data=z.read(info.filename)
  if target.exists() and target.read_bytes()!=data:raise SystemExit('Conflicting existing artifact: '+info.filename)
  target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
print(json.dumps({'restored':str(destination),'original_execution_root':manifest['execution_root'],'next_action':'Reconcile existing runner state/attempts and source identity before dispatch;do not reinitialize or reset budgets'}))
