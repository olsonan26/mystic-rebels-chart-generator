"""Record BEFORE presentation edits; verify every calculation/export field afterward."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from mystic_rebels.service import calculate
from mystic_rebels.models import BirthInput
from mystic_rebels.placements import derive,RULERS,SIGNS
from mystic_rebels.catalog import CATALOG

OUT=ROOT/'evidence'/'wheel-refinement'
BASE=OUT/'before.json'
def canonical(chart):
    return {k:v for k,v in chart.items() if k!='created_at_utc'}
def hashes(normalize_manifest=False):
    paths=sorted((ROOT/'mystic_rebels').glob('*.py'))+[ROOT/'data'/'ephemeris-manifest.json',ROOT/'data'/'minor-bodies.json']
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n') if normalize_manifest and p.name=='ephemeris-manifest.json' else p.read_bytes()).hexdigest() for p in paths}
def calculate_cases(inputs):
    return [canonical(calculate(BirthInput(**value))) for value in inputs]
def across_environments(charts):
    values=json.loads(json.dumps(charts))
    for chart in values:
        chart['configuration'].pop('python_version',None)
        chart['configuration'].pop('asset_manifest_sha256',None)
    return values
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    if '--record' in sys.argv:
        if BASE.exists():raise SystemExit('Baseline exists; refusing to overwrite it.')
        base=json.loads((ROOT/'evidence'/'cloud-input.json').read_text())
        base['objects']=[r['id'] for r in CATALOG]
        cases=[base,{**base,'name':'Sofia reference','local_date':'1992-09-02','local_time':'17:46:00','timezone':'Europe/Sofia','latitude':42+41/60,'longitude':23+19/60},{**base,'name':'Unknown time','time_accuracy':'unknown','local_time':None},{**base,'name':'Southern hemisphere','local_date':'2000-01-01','local_time':'12:00:00','timezone':'Australia/Sydney','latitude':-33.8688,'longitude':151.2093}]
        rulers=[{'sign_index':i,'decan_index':d,'pulse':derive(i*30+d*10)['pulse'],'ruler':RULERS[(i+4*d)%12]} for i in range(12) for d in range(3)]
        result={'baseline_commit':'e250662ebbf799f00f94c869a68d8bdab1d3f8ea','engine_hashes':hashes(),'inputs':cases,'charts':calculate_cases(cases),'decan_display_reference':rulers}
        BASE.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        (OUT/'git-source-baseline.json').write_text(json.dumps({'baseline_commit':result['baseline_commit'],'files':hashes(True)},indent=2)+'\n',encoding='utf-8',newline='\n')
        print('Recorded four complete chart/export snapshots and 36 decan references before edits.')
        return
    before=json.loads(BASE.read_text(encoding='utf-8'))
    source_before=json.loads((OUT/'git-source-baseline.json').read_text())
    assert source_before['baseline_commit']==before['baseline_commit']
    assert source_before['files']==hashes(True),'Calculation engine or catalog changed'
    raw_hashes=hashes()
    assert all(value==raw_hashes[path] for path,value in before['engine_hashes'].items() if path.endswith('.py')),'Engine source bytes changed'
    after=calculate_cases(before['inputs'])
    assert across_environments(before['charts'])==across_environments(after),'Calculated values or interpretation outputs changed'
    assert across_environments(json.loads(json.dumps(after)))==across_environments(before['charts']),'JSON calculation/export values changed'
    report={'engine_sources_byte_identical':True,'manifest_catalog_content_identical':True,'cases':len(after),'point_records':sum(len(c['points']) for c in after),'all_calculation_and_interpretation_fields_equal':True,'json_export_calculation_fields_equal':True,'same_environment_export_values_equal':before['charts']==after,'excluded_metadata_fields':['created_at_utc generation timestamp','configuration.python_version runtime environment','configuration.asset_manifest_sha256 raw file hash differs with Git CRLF/LF normalization; manifest content hash is checked separately'],'baseline_sha256_lf_normalized':hashlib.sha256(BASE.read_text(encoding='utf-8').encode('utf-8')).hexdigest()}
    (OUT/'numerical-regression.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
if __name__=='__main__':main()
