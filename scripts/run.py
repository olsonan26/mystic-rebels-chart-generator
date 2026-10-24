"""Start the same ASGI app used by the hosted Python function."""
import os,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
env=root/'.env'
if env.exists():
    for line in env.read_text(encoding='utf-8-sig').splitlines():
        if line.strip() and not line.lstrip().startswith('#') and '=' in line:
            key,value=line.split('=',1)
            os.environ.setdefault(key.strip(),value.strip().strip('"'))
import uvicorn
uvicorn.run('mystic_rebels.api:app',host='127.0.0.1',port=8000)
