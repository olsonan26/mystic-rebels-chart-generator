"""Research-only evidence extraction. Never writes to applications or frozen trial."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json, hashlib, sqlite3, subprocess
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MYSTIC = ROOT / 'work/Mystic-Rebels'
TRIAL = HERE.parent / 'nadia-sanchez-blind-trial'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def save(name, data):
    (HERE/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def snapshot():
    result = {}
    for relative in ['work/Mystic-Rebels', 'work/staffprofiler-recreation/repository']:
        base=ROOT/relative
        def git(*args):
            return subprocess.check_output(['git','-C',str(base),*args],text=True,encoding='utf-8').strip()
        files=git('ls-files','--cached','--others','--exclude-standard').splitlines()
        result[relative]={'git_root':git('rev-parse','--show-toplevel'), 'head':git('rev-parse','HEAD'),
            'branch':git('branch','--show-current'), 'status':git('status','--short'),
            'file_hashes':{name:sha(base/name) for name in files if (base/name).is_file()}}
    base=ROOT/'work/mystic-natal-bridge-prototype'
    result['work/mystic-natal-bridge-prototype']={'file_hashes':{
        str(p.relative_to(base)):sha(p) for p in sorted(base.rglob('*'))
        if p.is_file() and not any(x in ['__pycache__','.git','.runtime','node_modules'] for x in p.parts)}}
    result['frozen_trial']={p.name:sha(p) for p in sorted(TRIAL.iterdir()) if p.is_file()}
    return result

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if '--verify-only' in sys.argv:
        before=read(HERE/'preservation-before.json'); after=snapshot()
        save('preservation-verification.json',{'checked_utc':datetime.now(timezone.utc).isoformat(),
            'application_checkouts_prototype_and_trial_unchanged': before==after,
            'changed_sections':[k for k in before if before[k]!=after.get(k)]})
        print('Preservation unchanged:',before==after)
        raise SystemExit(0 if before==after else 1)
    if (HERE/'preservation-before.json').exists():
        raise SystemExit('Baseline already exists; do not replace it.')
    save('preservation-before.json',snapshot())
    manifest=read(TRIAL/'first-pass-manifest.json')
    checks=[{'path':name,'expected':digest,'actual':sha(TRIAL/name),
        'match':sha(TRIAL/name)==digest} for name,digest in manifest['files'].items()]
    save('frozen-trial-verification.json',{'all_match':all(c['match'] for c in checks),'files':checks})
    db=sqlite3.connect((MYSTIC/'reference/knowledge-index.sqlite').as_uri()+'?mode=ro',uri=True)
    pages=[179,193,203,218,245,246,247,257,258,259,271,272,273,274,280,283,284,
        289,290,291,292,293,295,296,297,299,300,301,302,303,304,319,321,322,324,
        331,332,343,344,345,365,366,367,368,383,426,427,428,429,431,434,450,451,
        457,458,476,477,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578]
    excerpts=[]
    for p in pages:
        row=db.execute('select source_id,pdf_page,text,text_sha256,review_status from pages where pdf_page=?',(p,)).fetchone()
        d=dict(zip(['source_id','pdf_page','text','text_sha256','review_status'],row))
        d['text_hash_matches']=hashlib.sha256(d['text'].encode()).hexdigest()==d['text_sha256']
        excerpts.append(d)
    save('cached-passage-evidence.json',excerpts)
    assertions=read(MYSTIC/'data/knowledge/original_assertions.json')['assertions']
    concepts={'phsr','spark-entry','tone-pulse','delegate-condition','age-degree','chiron',
        'directional-context','natal-transit-order','energy-flow','retrograde','house-field'}
    selected=[a for a in assertions if a.get('concept_id') in concepts]
    save('original-assertion-evidence.json',selected)
    pipeline=read(MYSTIC/'data/knowledge/source_pipeline.json')['files']
    ids={w['file_id'] for a in selected for w in a.get('witnesses',[])}
    ids.add('1jWGIAg-BIRh7DqzsFZ3knecUkxWNZudb')
    originals=[]
    for file_id in sorted(ids):
        if file_id not in pipeline: continue
        item=pipeline[file_id]; path=MYSTIC/item['local_path']
        rec={'file_id':file_id,'name':item['name'],'local_path':str(path),
            'expected_sha256':item['content_sha256'],'actual_sha256':sha(path),
            'hash_matches':sha(path)==item['content_sha256'],'ocr_path':str(MYSTIC/item['ocr_path'])}
        ocr=read(MYSTIC/item['ocr_path']);rec['ocr_text']=ocr['text'];rec['ocr_status']=ocr.get('status')
        originals.append(rec)
    save('original-witness-evidence.json',originals)
    export_path=Path('C:/Users/olson/Downloads/Nadias chart mystic rebels.json')
    export=read(export_path)
    keys=['id','longitude_deg','speed_longitude_deg_per_day','declination_deg','retrograde',
        'out_of_bounds','sign','degree_in_sign','degree_floor','decan','tone','pulse','house','field',
        'sign_ruler','spark','display_dms']
    save('supplied-chart-evidence.json',{'source_path':str(export_path),'sha256':sha(export_path),
        'input':export['input'],'time':export['time'],'angles':export['angles'],
        'points':[{**{k:p.get(k) for k in keys},'gradity_phase':p.get('gradity',{}).get('phase'),
            'gradity_status':p.get('gradity',{}).get('status')} for p in export['points'] if p.get('available')]})
    snapshot_manifest=read(HERE.parent/'source-snapshot.json')
    costar=HERE.parent/'evidence/LOOKS-LIKE-COSTAR'
    blobs=[]
    for record in snapshot_manifest['costar']['files']:
        p=costar/record['path']; data=p.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        # Downloaded source snapshots may have an added trailing newline; preserve it and report it.
        blobs.append({'path':record['path'],'recorded_git_blob':record['gitBlobSha'],
            'actual_git_blob':actual,'exact_match':actual==record['gitBlobSha'],'sha256':sha(p)})
    save('costar-snapshot-verification.json',{'recorded_commit':snapshot_manifest['costar']['commit'],
        'note':'Source-text snapshot, not a Git checkout. Parent git revision is not its revision.',
        'files':blobs,'exact_blob_matches':sum(r['exact_match'] for r in blobs),'total_files':len(blobs)})
    print(json.dumps({'frozen_hashes':checks,'cached_pages':len(excerpts),
        'cached_hashes_match':all(x['text_hash_matches'] for x in excerpts),
        'original_witnesses':len(originals),'original_hashes_match':all(x['hash_matches'] for x in originals),
        'costar_exact_blob_matches':sum(r['exact_match'] for r in blobs),'costar_files':len(blobs)},indent=2))
