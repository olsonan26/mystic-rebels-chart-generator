"""Bounded subprocess adapter; data travels on stdin, never shell interpolation."""
import json
import os
from pathlib import Path
import shutil
import subprocess

def annual_numbers(name, birth_date, year):
    here=Path(__file__).resolve().parent
    manifest=json.loads((here/'data/annual-method-manifest.json').read_text(encoding='utf-8'))
    import hashlib
    for relative,digest in manifest['sha256'].items():
        if hashlib.sha256((here/relative).read_bytes()).hexdigest()!=digest:
            raise ValueError('Annual calculation source integrity check failed.')
    node=os.environ.get('COMMON_GROUND_NODE') or shutil.which('node')
    if not node:
        candidate=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
        if candidate.is_file():node=str(candidate)
    if not node:raise ValueError('Node.js is required for the annual calculation adapter.')
    kwargs={'creationflags':subprocess.CREATE_NO_WINDOW} if os.name=='nt' else {}
    try:
        result=subprocess.run([node,str(here/'annual_adapter.mjs')],
            input=json.dumps({'name':name,'birth_date':birth_date,'year':year}),
            capture_output=True,text=True,encoding='utf-8',timeout=20,**kwargs)
    except (OSError,subprocess.TimeoutExpired):
        raise ValueError('The annual calculation could not complete.') from None
    if result.returncode:
        raise ValueError('Choose a year from the birth year through 254 years after birth and verify the name.')
    return json.loads(result.stdout)
