"""Verify frozen reference byte hashes in both checkout and committed Git blobs."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
count=0
for report in (ROOT/'evidence/astronomy-followup').glob('*-independent-events.json'):
    for record in json.loads(report.read_text(encoding='utf-8'))['raw_inputs'].values():
        name=record['raw_response']
        actual=(ROOT/name).read_bytes()
        revision=':'+name if '--staged' in sys.argv else 'HEAD:'+name
        committed=subprocess.check_output(['git','show',revision],cwd=ROOT)
        assert hashlib.sha256(actual).hexdigest()==record['sha256'],name
        assert hashlib.sha256(committed).hexdigest()==record['sha256'],name+' committed bytes'
        count+=1
print(f'All {count} checkout and committed reference blobs retain their recorded SHA256.')
