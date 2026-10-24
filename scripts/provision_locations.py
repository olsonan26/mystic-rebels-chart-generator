"""Create compact, attributed offline place search from pinned GeoNames data."""
import gzip,json,hashlib
from pathlib import Path
from importlib.metadata import version
import geonamescache
root=Path(__file__).resolve().parents[1]
cache=geonamescache.GeonamesCache();countries=cache.get_countries()
rows=[]
for c in cache.get_cities().values():
    rows.append({key:c[key] for key in ('geonameid','name','latitude','longitude','timezone','population','countrycode')})
    rows[-1]['country']=countries.get(c['countrycode'],{}).get('name',c['countrycode'])
payload=json.dumps(rows,ensure_ascii=False,separators=(',',':')).encode()
compressed=gzip.compress(payload,mtime=0)
target=root/'data'/'locations.json.gz';target.write_bytes(compressed)
(root/'data'/'locations-manifest.json').write_text(json.dumps({'provider':'GeoNames','license':'CC BY 4.0','attribution_url':'https://www.geonames.org/','geonamescache_version':version('geonamescache'),'location_kind':'city centroid, not a certified individual birth location','count':len(rows),'sha256':hashlib.sha256(compressed).hexdigest(),'byte_size':len(compressed)},indent=2)+'\n')
print(f'{len(rows)} cities, {len(compressed)} bytes')
