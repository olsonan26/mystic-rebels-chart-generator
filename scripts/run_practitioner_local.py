"""Run the existing app plus the explicitly configured local review workflow."""
import json
import os
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

if __name__=='__main__':
    config=ROOT/'tmp/practitioner-private/config.json'
    if not config.is_file():
        raise SystemExit('Run scripts/setup_practitioner.py first.')
    for key,value in json.loads(config.read_text(encoding='utf-8')).items():
        if key not in {'NADIA_REVIEW_STORE','NADIA_REVIEW_PASSWORD_HASH','NADIA_REVIEWER_NAME'}:
            raise SystemExit('Unexpected private configuration key.')
        os.environ[key]=value
    import uvicorn
    uvicorn.run('api.index:app',host='127.0.0.1',port=8011,access_log=False)
