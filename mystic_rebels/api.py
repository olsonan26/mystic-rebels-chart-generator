from __future__ import annotations
import functools,os,unicodedata,gzip,json
from pathlib import Path
from fastapi import FastAPI,Query,Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from .models import BirthInput
from .service import calculate,object_catalog
from .errors import ChartError
from . import astronomy
from .chart_chat import router as chart_chat_router

app=FastAPI(title='Mystic Rebels Chart API',version='0.1.0')
app.include_router(chart_chat_router)

@app.exception_handler(ChartError)
async def chart_error(request:Request,exc:ChartError):return JSONResponse(status_code=422,content={'error':exc.record()})

@app.middleware('http')
async def headers(request,call_next):
    max_size=131072 if request.url.path.startswith('/api/chart-chat') else 32768
    if request.method=='POST' and int(request.headers.get('content-length','0') or 0)>max_size:
        return JSONResponse(status_code=413,content={'error':{'code':'PAYLOAD_TOO_LARGE','message':'Chart input is too large.'}})
    response=await call_next(request)
    response.headers['Cache-Control']='no-store' if request.url.path.startswith('/api/chart') else 'no-cache'
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Referrer-Policy']='strict-origin-when-cross-origin'
    return response

@app.get('/api/health')
def health():
    try:
        with astronomy.LOCK:
            astronomy.initialize();astronomy.verify_assets(['sepl_18.se1','semo_18.se1','seas_18.se1'])
        return {'status':'ready','product':'Mystic Rebels','swiss_version':astronomy.swe.version,'assets':len(astronomy.manifest()['assets'])}
    except ChartError as exc:return JSONResponse(status_code=503,content={'status':'unavailable','error':exc.record()})

@app.get('/api/config')
def config():return {'supabase_url':os.environ.get('SUPABASE_URL',''),'supabase_publishable_key':os.environ.get('SUPABASE_PUBLISHABLE_KEY','')}

@app.get('/api/catalog')
def catalog():return object_catalog()

@app.get('/api/methodology')
def methodology():
    # Metadata only. Copyright source text and the private research search index
    # are not served by this endpoint or added to the function bundle.
    from knowledge_audit.registry import load_registry,validate_registry,coverage
    registry=load_registry();validate_registry(registry,check_files=False)
    return {'product':registry['product'],'schema_version':registry['schema_version'],
            'audit_status':registry['audit_status'],'coverage':coverage(registry),
            'intelligence_layers':registry['intelligence_layers'],
            'rules':registry['rules']}

@app.post('/api/charts')
def chart(data:BirthInput):return calculate(data)

def normalize(text):return ''.join(c for c in unicodedata.normalize('NFKD',text) if not unicodedata.combining(c)).casefold()

@functools.lru_cache(maxsize=1)
def cities():
    rows=[]
    with gzip.open(astronomy.ROOT/'data'/'locations.json.gz','rt',encoding='utf-8') as f:
        data=json.load(f)
    for c in data:
        rows.append({**c,'search_key':normalize(c['name']+' '+c['country'])})
    return rows

@app.get('/api/locations')
def locations(q:str=Query(min_length=2,max_length=100)):
    search=normalize(q)
    results=[c for c in cities() if search in c['search_key']]
    results.sort(key=lambda c:(not c['search_key'].startswith(search),-c['population']))
    return [{'id':c['geonameid'],'name':f"{c['name']}, {c['country']}",'latitude':c['latitude'],'longitude':c['longitude'],'timezone':c['timezone'],'provenance':f"GeoNames city centroid, geonamescache 3.0.2, ID {c['geonameid']}"} for c in results[:12]]

@app.get('/api/timezone')
def timezone(latitude:float=Query(ge=-90,le=90),longitude:float=Query(ge=-180,le=180)):
    import tzfpy
    return {'timezone':tzfpy.get_tz(longitude,latitude),'method':'tzfpy coordinate polygon lookup; historical civil offset resolved separately by IANA'}

dist=Path(__file__).resolve().parents[1]/'dist'
if dist.exists():app.mount('/',StaticFiles(directory=str(dist),html=True),name='web')
