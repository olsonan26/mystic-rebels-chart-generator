"""Provision vendor-published data, recording exact origin and SHA256. No fallback."""
from __future__ import annotations
import argparse, hashlib, json, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EPHE = ROOT / 'data' / 'ephe'
ASTEROIDS = dict(json.loads((ROOT/'data'/'minor-bodies.json').read_text()))

def fetch(url: str) -> bytes:
    req=urllib.request.Request(url,headers={'User-Agent':'Mystic-Rebels-Ephemeris-Provisioner/0.1'})
    with urllib.request.urlopen(req,timeout=90) as response:
        data=response.read()
        if response.status != 200: raise RuntimeError(f'HTTP {response.status}: {url}')
    return data

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--asteroid',type=int,action='append',default=[])
    args=parser.parse_args()
    manifest_path=ROOT/'data'/'ephemeris-manifest.json'
    old=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    commit=old.get('vendor_commit') or json.loads(fetch('https://api.github.com/repos/aloistr/swisseph/commits/master'))['sha']
    rows={row['path']:row for row in old.get('assets',[])}
    sources=[(name,f'https://raw.githubusercontent.com/aloistr/swisseph/{commit}/ephe/{name}') for name in ('sepl_18.se1','semo_18.se1','seas_18.se1')]
    for number in sorted(set(ASTEROIDS)|set(args.asteroid)):
        if not 1<=number<=999999: raise ValueError('Asteroid number outside supported range')
        stem=f'se{number:05d}' if number<100000 else f's{number:06d}'
        name=f'ast{number//1000}/{stem}s.se1'
        sources.append((name,f'https://ephe.scryr.io/ephe/{name}'))
    failures=[]
    for name,url in sources:
        target=EPHE/name
        previous=rows.get(name)
        if previous and target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()==previous['sha256']:
            print(f'VERIFIED {name}',flush=True); continue
        try:
            data=fetch(url)
            # Vendor files have a textual Swiss Ephemeris header followed by binary data.
            if len(data)<1000 or b'SWISSEPH' not in data[:150].upper() or b'<html' in data[:400].lower():
                raise RuntimeError('Not a Swiss Ephemeris binary asset')
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(data)
            rows[name]={'path':name,'source_url':url,'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'byte_size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
            print(f'INSTALLED {name} {len(data)} bytes',flush=True)
        except Exception as exc:
            failures.append({'path':name,'code':'EPHEMERIS_ASSET_UNAVAILABLE','reason':str(exc),'source_url':url})
            print(f'UNAVAILABLE {name}: {exc}',flush=True)
    manifest={'schema_version':1,'vendor_commit':commit,'official_download_documentation':'https://www.astro.com/swisseph/swedownload_e.htm','core_supported_years':[1800,2399],'additional_asteroid_years':[1800,2099],'assets':list(rows.values()),'failures':failures}
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    if any(name not in rows for name in ('sepl_18.se1','semo_18.se1','seas_18.se1')): raise SystemExit(1)

if __name__=='__main__': main()
