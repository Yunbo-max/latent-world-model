"""Capture base-bound changed files and a consistent existing runner database."""
import base64,datetime,hashlib,io,json,sqlite3,tempfile,zipfile
from pathlib import Path

root=Path('.');snap=root/'recovery_batches/batch02';snap.mkdir(parents=True,exist_ok=True)
base_raw=base64.b64decode((root/'RECOVERY.zip.b64').read_bytes(),validate=True)
base_manifest=json.loads((root/'RECOVERY_MANIFEST.json').read_text())
assert hashlib.sha256(base_raw).hexdigest()==base_manifest['archive_sha256']
with zipfile.ZipFile(io.BytesIO(base_raw)) as z:previous={n:z.read(n) for n in z.namelist() if not n.endswith('/')}
db=root/'.research-autopilot/simple-loop.sqlite3'
with tempfile.TemporaryDirectory() as temporary:
    backup=Path(temporary)/'snapshot.sqlite3'
    con=sqlite3.connect(str(db));out=sqlite3.connect(str(backup));con.backup(out);out.close();con.close()
    check=sqlite3.connect(str(backup));assert check.execute('pragma integrity_check').fetchone()[0]=='ok';check.close()
    db_bytes=backup.read_bytes()
changes={};members={}
for path in root.rglob('*'):
    if not path.is_file() or path.is_symlink():continue
    name=path.relative_to(root).as_posix()
    if name.startswith(('recovery_parts/','recovery_batches/')) or '__pycache__' in name or name in ['RECOVERY.zip.b64','RECOVERY_MANIFEST.json','RECOVERY_PARTS.json','PUBLISH_MANIFEST.json'] or name.endswith(('-wal','-shm','.lock')):continue
    data=db_bytes if path==db else path.read_bytes()
    if previous.get(name)==data:continue
    changes[name]=data
    members[name]={'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'previous_sha256':hashlib.sha256(previous[name]).hexdigest() if name in previous else None}
buffer=io.BytesIO()
with zipfile.ZipFile(buffer,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name,data in sorted(changes.items()):z.writestr(name,data)
raw=buffer.getvalue();encoded=base64.b64encode(raw)
(snap/'RECOVERY_DELTA.zip.b64').write_bytes(encoded)
manifest={'kind':'base-plus-incremental-runner-snapshot','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'base_source_commit':'1e3bb300270eaaf6f8ff9555757d7bce31e87988','base_archive_ref':'RECOVERY.zip.b64',
    'base_archive_sha256':base_manifest['archive_sha256'],'archive_sha256':hashlib.sha256(raw).hexdigest(),
    'base64_sha256':hashlib.sha256(encoded).hexdigest(),'archive_bytes':len(raw),'execution_root':str(root.resolve()),'members':members,
    'restore_order':'Restore base;assemble sorted delta parts without separators and verify hash;apply restore_delta_snapshot_v1.py to stopped exact-base state;reconcile original source,attempts,budget;never init.',
    'sqlite':'consistent backup;integrity_check ok','live_supervisor_note':'awaiting decision at capture;reconcile actual PID before any new supervisor'}
(snap/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
partdir=snap/'parts';partdir.mkdir(exist_ok=True);parts=[]
for i in range(0,len(encoded),8192):
    data=encoded[i:i+8192];name=f'part-{i//8192:04d}.b64';(partdir/name).write_bytes(data)
    parts.append({'path':'recovery_batches/batch02/parts/'+name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(snap/'PARTS.json').write_text(json.dumps({'parts':parts,'concatenate':'lexicographic order,no separators','base64_sha256':manifest['base64_sha256'],'archive_sha256':manifest['archive_sha256']},indent=2)+'\n')
with zipfile.ZipFile(io.BytesIO(raw)) as z:assert z.testzip() is None
print(json.dumps({'members':len(members),'archive_bytes':len(raw),'parts':len(parts),'sqlite_integrity':'ok'}))
