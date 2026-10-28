"""After-feedback research, isolated from applications and the frozen first pass.

All event rows are angular diagnostics, never approved PURE directed aspects.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,math,csv,hashlib
from datetime import datetime,timezone,timedelta
from zoneinfo import ZoneInfo
from functools import lru_cache

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
MYSTIC=ROOT/'work/Mystic-Rebels'
TRIAL=HERE.parent/'nadia-sanchez-blind-trial'
sys.path.insert(0,str(MYSTIC))
from mystic_rebels import astronomy as astro
from mystic_rebels.models import BirthInput
from mystic_rebels.service import calculate
from mystic_rebels.placements import derive,SIGNS,RULERS,dms

PAC=ZoneInfo('America/Los_Angeles')
CHAIN=['Chiron','Sun','Moon','Neptune','Saturn','Uranus']
BODIES={name:getattr(astro.swe,name.upper()) for name in ['Chiron','Saturn','Uranus','Neptune','Pluto']}
ANGLES=[0,30,60,90,120,150,180]
OFFSETS=[0,30,60,90,120,150,180,210,240,270,300,330]
START='2003-07-17';END='2014-07-17'

def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def save(name,data):(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def wrap(x):return (x+180)%360-180
def jd_local(day):return astro.times(datetime.fromisoformat(day).replace(tzinfo=PAC).astimezone(timezone.utc))['jd_ut1']
def utc(jd):
    y,m,d,h,mi,se=astro.swe.jdut1_to_utc(jd,astro.swe.GREG_CAL)
    return datetime(y,m,d,h,mi,0,tzinfo=timezone.utc)+timedelta(seconds=se)
def age(day):return day.year-1992-((day.month,day.day)<(7,17))

@lru_cache(maxsize=300000)
def pos(jd,body):
    xx,flags=astro.swe.calc_ut(jd,body,astro.FLAGS);astro.assert_backend(flags)
    return xx[0]%360,xx[3]

def refine(fn,a,b):
    fa=fn(a)
    for _ in range(50):
        m=(a+b)/2;fm=fn(m)
        if abs(fm)<1e-11 or b-a<2e-9:return m
        if fa*fm<=0:b=m
        else:a=m;fa=fm
    return (a+b)/2

def roots(body,target,step):
    a0,b0=jd_local(START),jd_local(END)
    grid=[a0+i*step for i in range(math.ceil((b0-a0)/step))]+[b0]
    values=[wrap(pos(t,body)[0]-target) for t in grid]
    out=[]
    for i in range(len(grid)-1):
        fa,fb=values[i:i+2]
        if abs(fb-fa)>180 or fa*fb>0:continue
        t=refine(lambda t:wrap(pos(t,body)[0]-target),grid[i],grid[i+1])
        if a0<=t<b0 and (not out or abs(t-out[-1])>1e-5):out.append(t)
    return out

def fingerprint(rows):return [(r['transit'],r['target'],r['oriented_offset_deg'],r['local_date']) for r in rows]

def scan(step,natal):
    rows=[]
    for name,body in BODIES.items():
        for target in CHAIN:
            point=natal[target]
            for offset in OFFSETS:
                target_lon=(point['longitude_deg']+offset)%360
                for jd in roots(body,target_lon,step):
                    lon,speed=pos(jd,body);local=utc(jd).astimezone(PAC)
                    place=derive(lon,natal['Ascendant']['longitude_deg'])
                    rows.append({'transit':name,'target':target,'angle_deg':min(offset,360-offset),
                        'oriented_offset_deg':offset,'jd_ut1':jd,'exact_utc':utc(jd).isoformat(),
                        'exact_local':local.isoformat(),'local_date':local.date().isoformat(),'age':age(local),
                        'longitude_deg':lon,'display_dms':dms(lon),'speed_deg_per_day':speed,
                        'transit_retrograde':speed<0,'transit_natal_house':place['house'],
                        'transit_pulse':place['pulse'],'transit_sign_ruler':place['sign_ruler'],
                        'residual_deg':abs(wrap(lon-target_lon)),
                        'interpretation_status':'RAW_EQUALITY_NOT_APPROVED_DIRECTED_EDGE'})
    return sorted(rows,key=lambda r:(r['jd_ut1'],r['transit'],r['target']))

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    config={'analysis_status':'AFTER_FEEDBACK_HYPOTHESIS_DEVELOPMENT',
        'feedback_known_before_selection':True,'selection':'All 5 movers to all 6 natal chain nodes; all 12 oriented multiples of 30 degrees; continuous local ages 11 through 21.',
        'movers':list(BODIES),'targets':CHAIN,'angles_unsigned':ANGLES,'offsets':OFFSETS,
        'window_start_inclusive':START,'window_end_exclusive':END,'timezone':str(PAC),
        'houses':'Fixed natal Whole Sign sectors, not an event-time Ascendant or relocated chart',
        'orbs':'None assigned; equality roots only','direction':'Oriented ecliptic difference is not source Energy Flow direction',
        'major_subset':[0,60,90,120,180],'extra_geometry_subset':[30,150],
        'controls':'All selected contacts and missing original ages 13-15 retained, no event-fit filter'}
    save('timing-selection.json',config)
    astro.initialize();assets=astro.verify_assets(['sepl_18.se1','semo_18.se1','seas_18.se1'])
    export=read(Path('C:/Users/olson/Downloads/Nadias chart mystic rebels.json'))
    req=BirthInput(**{**export['input'],'name':'Nadia Sanchez','latitude':33.8044,'longitude':-118.0673,
        'coordinate_provenance':'User-supplied coordinates; compare separately with supplied export'})
    fresh=calculate(req)
    save('recalculated-chart-user-coordinates.json',fresh)
    natal={p['id']:p for p in fresh['points'] if p.get('available')}
    original={p['id']:p for p in export['points'] if p.get('available')}
    save('natal-verification.json',{'assets':assets,'source_export_input':export['input'],
        'calculated_input':fresh['input'],'utc_agreement':fresh['time']['birth_utc']==export['time']['birth_utc'],
        'chain_comparison':[{'id':k,'longitude_difference_deg':wrap(natal[k]['longitude_deg']-original[k]['longitude_deg']),
            'house_agreement':natal[k]['house']==original[k]['house'],
            'pulse_agreement':natal[k]['pulse']==original[k]['pulse'],
            'motion_agreement':natal[k]['retrograde']==original[k]['retrograde']} for k in CHAIN],
        'ascendant_difference_deg':wrap(fresh['angles']['Ascendant']-export['angles']['Ascendant'])})
    degree_rows=[]
    for name in CHAIN+['Mars','Venus','Mercury','Jupiter','Pluto','Ascendant']:
        p=natal[name];g=p['degree_in_sign'];i=math.floor(g);h=p['house'];z=p['sign_index']+1
        birthday=datetime(1992+i,7,17,20,1,tzinfo=PAC)
        next_birthday=datetime(1993+i,7,17,20,1,tzinfo=PAC)
        birthday_fraction=birthday+(next_birthday-birthday)*(g-i)
        tropical_candidate=datetime(1992,7,17,20,1,tzinfo=PAC).astimezone(timezone.utc)+timedelta(days=365.24219*g)
        house_delegate=RULERS[(9+h-1)%12]
        degree_rows.append({'id':name,'degree_in_sign':g,'integer_age_label':i,'natal_retrograde':p['retrograde'],
            'age_label_window_start':f'{1992+i}-07-17','age_label_window_end_exclusive':f'{1993+i}-07-17',
            'source_fractional_age_candidate':g,'birthday_interpolation_candidate_local':birthday_fraction.isoformat(),
            'mean_tropical_year_candidate_local':tropical_candidate.astimezone(PAC).isoformat(),
            'calendar_convention_status':'UNSELECTED_RESEARCH_ALTERNATIVES_NOT_EVENT_TIMESTAMPS',
            'retrograde_delay_days':None,'spark_house_candidate':SIGNS[(i+(6 if h%2==0 else 0))%12],
            'spark_sign_candidate':SIGNS[(i+(6 if z%2==0 else 0))%12], 'spark_canonical':None,
            'natal_house':h,'house_delegate':house_delegate,'house_delegate_retrograde':natal[house_delegate]['retrograde']})
    save('degree-and-condition-diagnostics.json',degree_rows)
    pairs=[]
    points=[p for p in natal.values() if p['id'] in CHAIN+['Mercury','Venus','Mars','Jupiter','Pluto','Ascendant','Midheaven']]
    for p in points:
        for q in points:
            if p['id']>=q['id'] or not ({p['id'],q['id']} & set(CHAIN)):continue
            delta=abs(wrap(q['longitude_deg']-p['longitude_deg']))
            near=min(list(range(0,181,15))+[72,144],key=lambda a:abs(a-delta))
            pairs.append({'a':p['id'],'b':q['id'],'separation_deg':delta,'nearest_diagnostic_angle':near,
                'distance_from_angle_deg':abs(delta-near),'status':'GEOMETRY_ONLY_NO_DIRECTED_EDGE'})
    save('natal-pair-geometry.json',pairs)
    print('Natal verified; beginning daily and six-hour scans.',flush=True)
    daily=scan(1,natal);print('Daily roots',len(daily),flush=True)
    six=scan(.25,natal);print('Six-hour roots',len(six),flush=True)
    save('expanded-transit-geometry.json',{'configuration':config,'verification':{
        'daily_count':len(daily),'six_hour_count':len(six),'grid_agreement':fingerprint(daily)==fingerprint(six),
        'max_residual_deg':max(r['residual_deg'] for r in six),'asset_hashes':assets},'contacts':six})
    annual=read(TRIAL/'numerology.json')['records'];yearmap={r['calendar_year']:r for r in annual}
    windows=read(TRIAL/'numerology.json')['age_windows']
    for row in six:
        year=int(row['local_date'][:4]);month=int(row['local_date'][5:7]);record=yearmap.get(year)
        original_window=any(w['start']<=row['local_date']<w['end_exclusive'] for w in windows)
        match=next((m for m in record['months'] if m['month']==month),None) if record and original_window else None
        row['in_original_trial_window']=original_window
        row['preserved_month_tone']=match['indicator']['tone'] if match else None
        row['preserved_annual_values']={k:record[k]['trail'] for k in ['ess','py','com']} if match else None
        row['preserved_monthly_values']={k:match[k]['trail'] for k in ['pm','pme','mcom']} if match else None
    save('expanded-timing-numerology-comparison.json',six)
    with (HERE/'expanded-contacts.csv').open('w',encoding='utf-8',newline='') as f:
        cols=['local_date','age','transit','target','angle_deg','oriented_offset_deg','transit_retrograde',
            'transit_natal_house','in_original_trial_window','preserved_month_tone']
        w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(six)
    events=[];body=BODIES['Chiron'];a0,b0=jd_local(START),jd_local(END)
    grid=[a0+i for i in range(math.ceil(b0-a0))]+[b0]
    for i in range(len(grid)-1):
        a,b=grid[i:i+2]
        if pos(a,body)[1]*pos(b,body)[1]<=0:
            t=refine(lambda t:pos(t,body)[1],a,b);local=utc(t).astimezone(PAC)
            events.append({'kind':'station_retrograde' if pos(t-.01,body)[1]>0 else 'station_direct',
                'local_date':local.date().isoformat(),'exact_local':local.isoformat(),'age':age(local),
                'longitude_deg':pos(t,body)[0],'display_dms':dms(pos(t,body)[0])})
    for sign in range(12):
        for t in roots(body,sign*30,.25):
            local=utc(t).astimezone(PAC);after=derive(pos(t+.01,body)[0],natal['Ascendant']['longitude_deg'])
            events.append({'kind':'sign_and_fixed_natal_house_ingress','local_date':local.date().isoformat(),
                'exact_local':local.isoformat(),'age':age(local),'entering_sign':after['sign'],
                'entering_natal_house':after['house'],'retrograde_crossing':pos(t,body)[1]<0})
    save('chiron-stations-and-ingresses.json',sorted(events,key=lambda x:x['exact_local']))
    journal_jd=jd_local('2011-07-01')+.5
    journal_pos,speed=pos(journal_jd,body)
    save('journal-date-diagnostic.json',{'civil_date':'2011-07-01','age':18,
        'reference_only':'12 elapsed hours after Pacific midnight; journal clock time is unknown',
        'chiron_longitude_deg':journal_pos,'chiron_display_dms':dms(journal_pos),'transit_retrograde':speed<0,
        'distance_from_natal_moon_conjunction_deg':abs(wrap(journal_pos-natal['Moon']['longitude_deg'])),
        'same_date_exact_contacts':[r for r in six if r['local_date']=='2011-07-01'],
        'note':'No orb window or event cause inferred from proximity.'})
    summary={}
    families={
        'transit_chiron_to_chain_major':lambda r:r['transit']=='Chiron' and r['angle_deg'] in [0,60,90,120,180],
        'outer_four_to_natal_chiron_major':lambda r:r['transit']!='Chiron' and r['target']=='Chiron' and r['angle_deg'] in [0,60,90,120,180],
        'all_expanded_major':lambda r:r['angle_deg'] in [0,60,90,120,180],
        'additional_30_150':lambda r:r['angle_deg'] in [30,150]}
    for name,predicate in families.items():
        rows=[r for r in six if predicate(r)];in_trial=[r for r in rows if r['in_original_trial_window']]
        summary[name]={'continuous_count':len(rows),'count_in_original_windows':len(in_trial),
            'month_tones':{tone:sum(r['preserved_month_tone']==tone for r in in_trial) for tone in ['red','yellow','green']},
            'counts_by_age':{a:sum(r['age']==a for r in rows) for a in range(11,22)}}
    save('comparison-summary.json',summary)
    print(json.dumps(summary,indent=2))
