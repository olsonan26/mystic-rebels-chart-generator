"""Project-local official CPython 3.11 runtime for the pinned Windows binding."""
import hashlib,json,urllib.request,zipfile,io
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[1]
url='https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip'
target=root/'.runtime'
target.mkdir(exist_ok=True)
data=urllib.request.urlopen(url,timeout=90).read()
with zipfile.ZipFile(io.BytesIO(data)) as z:
    for info in z.infolist():
        resolved=(target/info.filename).resolve()
        if not resolved.is_relative_to(target.resolve()):raise RuntimeError('Unsafe archive path')
    z.extractall(target)
(target/'Lib'/'site-packages').mkdir(parents=True,exist_ok=True)
(target/'python311._pth').write_text('python311.zip\n.\nLib/site-packages\n..\nimport site\n')
(root/'data'/'runtime-manifest.json').write_text(json.dumps({'source_url':url,'sha256':hashlib.sha256(data).hexdigest(),'byte_size':len(data),'retrieved_at_utc':datetime.now(timezone.utc).isoformat()},indent=2))
print('Official CPython 3.11.9 x64 installed into .runtime')
