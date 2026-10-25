"""Source-defined retrograde loops from apparent geocentric longitude events.

No calendar windows, rounded degrees, or stationary speed bands classify phases.
The source leaves exact equality undefined, so the numerical root uncertainty is
reported as BOUNDARY rather than assigned an interpretive phase.
"""
from functools import lru_cache
from datetime import datetime, timezone, timedelta
import swisseph as swe
from . import astronomy as astro
from .errors import ChartError

# At least one complete loop on either side, including Mars's 780-day synodic
# period. Unsupported/file-edge searches fail explicitly instead of extrapolating.
WINDOW_DAYS = {'Mercury': 180, 'Venus': 750, 'Mars': 1000,
               'Jupiter': 500, 'Saturn': 500, 'Uranus': 500,
               'Neptune': 500, 'Pluto': 500}
STEP_DAYS = 2.0
ROOT_TOLERANCE_SECONDS = 0.1
BOUNDARY_SECONDS = 0.2

def delta(a, b):
    return (a-b+180) % 360-180

def sample(jd, body):
    data, returned = swe.calc_ut(jd, body, astro.FLAGS)
    astro.assert_backend(returned)
    return data[0], data[3]

def root(fn, a, b):
    fa, fb = fn(a), fn(b)
    if fa == 0: return a
    if fb == 0: return b
    if fa*fb > 0: raise ChartError('GRADITY_EVENT_UNBRACKETED', 'An event could not be bracketed.')
    while (b-a)*86400 > ROOT_TOLERANCE_SECONDS:
        mid = (a+b)/2
        fm = fn(mid)
        if fm == 0: return mid
        if fa*fm <= 0: b = mid
        else: a, fa = mid, fm
    return (a+b)/2

def utc_string(jd):
    # Invert UT1 with the same Swiss time model used by the chart.
    y, m, d, h, minute, second = swe.jdut1_to_utc(jd, swe.GREG_CAL)
    value = datetime(y, m, d, h, minute, tzinfo=timezone.utc)+timedelta(seconds=second)
    return value.isoformat(timespec='milliseconds').replace('+00:00', 'Z')

def event(kind, jd, body, target=None):
    lon, speed = sample(jd, body)
    return {'kind': kind, 'utc': utc_string(jd), 'jd_ut1': jd,
            'longitude_deg': lon, 'speed_longitude_deg_per_day': speed,
            'target_longitude_deg': target,
            'root_bracket_tolerance_seconds': ROOT_TOLERANCE_SECONDS}

def shadow(body, station, target, direction, limit):
    """First target crossing on the adjacent DIRECT-motion arc only."""
    previous = station
    previous_value = delta(sample(previous, body)[0], target)
    current = previous+direction*STEP_DAYS
    while abs(current-station) <= limit:
        lon, speed = sample(current, body)
        value = delta(lon, target)
        # A 180-degree branch cut is not a longitude crossing.
        if previous_value*value <= 0 and abs(previous_value-value) < 180:
            a,b = sorted((previous,current))
            crossing = root(lambda t: delta(sample(t,body)[0],target), a,b)
            if sample(crossing,body)[1] <= 0:
                break
            return crossing
        if speed <= 0: break
        previous, previous_value = current, value
        current += direction*STEP_DAYS
    raise ChartError('GRADITY_SHADOW_UNAVAILABLE', 'A complete direct-motion shadow crossing was not found within the verified search.')

@lru_cache(maxsize=256)
def cycles_for_month(name, year, month):
    body = getattr(swe, name.upper())
    anchor = astro.times(datetime(year, month, 15, 12, tzinfo=timezone.utc))['jd_ut1']
    window = WINDOW_DAYS[name]
    start, end = anchor-window, anchor+window
    low = swe.julday(1800,1,1,0)
    high = swe.julday(2400,1,1,0)
    if start < low or end >= high:
        raise ChartError('GRADITY_SEARCH_OUTSIDE_RANGE', 'Station and shadow verification needs a complete surrounding interval within 1800–2399.')
    stations = []
    previous = start
    old = sample(previous,body)[1]
    current = start+STEP_DAYS
    while current <= end:
        speed = sample(current,body)[1]
        if (old > 0 and speed <= 0) or (old < 0 and speed >= 0):
            jd = root(lambda t: sample(t,body)[1], previous,current)
            stations.append(('station_retrograde' if old > 0 else 'station_direct',jd))
        previous,old = current,speed
        current += STEP_DAYS
    result=[]
    for (first,a),(second,b) in zip(stations,stations[1:]):
        if first != 'station_retrograde' or second != 'station_direct': continue
        lon_a,lon_b = sample(a,body)[0],sample(b,body)[0]
        # An incomplete middle loop must never disappear and turn a gap into
        # supposedly verified Prograde. Reject the entire catalog on failure.
        pre = shadow(body,a,lon_b,-1,window)
        post = shadow(body,b,lon_a,1,window)
        if not pre < a < b < post: continue
        result.append([event('pregrade_entry',pre,body,lon_b),event(first,a,body),
                       event(second,b,body),event('postgrade_exit',post,body,lon_a)])
    if not result:
        raise ChartError('GRADITY_CYCLE_UNAVAILABLE', 'No complete station/shadow cycle could be verified in the surrounding interval.')
    return result

def classify(jd, cycles):
    # Check ALL boundaries before any interval: adjacent outer-planet shadows
    # can overlap, so a prior loop must not hide a later loop's exact event.
    for events in cycles:
        stamps=[e['jd_ut1'] for e in events]
        if any(abs(jd-t)*86400 <= BOUNDARY_SECONDS for t in stamps):
            return None,'BOUNDARY',events
    matches=[]
    for events in cycles:
        stamps=[e['jd_ut1'] for e in events]
        a,b,c,d=stamps
        if a < jd < d:
            matches.append(('Pregrade' if jd < b else 'Retrograde' if jd < c else 'Postgrade',events))
    if len(matches)>1:
        # The book specifies no precedence for simultaneous Postgrade of one
        # cycle and Pregrade of the next. Preserve all witnesses; do not pick.
        return None,'UNAVAILABLE',[event for _,events in matches for event in events]
    if matches:
        return matches[0][0],'VERIFIED',matches[0][1]
    before=[e for e in cycles if e[-1]['jd_ut1'] < jd]
    after=[e for e in cycles if e[0]['jd_ut1'] > jd]
    if before and after:
        # Both neighboring loops are known; this is outside their shadows.
        return 'Prograde','VERIFIED',[before[-1][-1],after[0][0]]
    return None,'UNAVAILABLE',[]

def calculate_gradity(name, jd, utc):
    base={'phase':None,'status':'UNAVAILABLE',
          'verification_scope':'documented_method_and_sampled_astronomy',
          'algorithm':'apparent-geocentric-station-shadow-v1',
          'root_bracket_tolerance_seconds':ROOT_TOLERANCE_SECONDS,
          'boundary_uncertainty_seconds':BOUNDARY_SECONDS,
          'events':[],
          'source':{'pdf_pages':[203,476,477],'reflow_pages':[207,480,481],
                    'original_printed_pages':[143,569,570]}}
    if name in ('Sun','Moon'):
        return {**base,'status':'NOT_APPLICABLE','reason':'No geocentric retrograde loop; motion is reported separately.'}
    if name not in WINDOW_DAYS:
        return {**base,'reason':'Station/shadow verification currently covers Mercury through Pluto only.'}
    try:
        # Called while the chart holds the Swiss global-state lock. Integrity
        # is checked even on a cache hit; stale cached events cannot hide damage.
        astro.verify_assets(['sepl_18.se1','semo_18.se1'])
        cycles=cycles_for_month(name,utc.year,utc.month)
        phase,status,events=classify(jd,cycles)
        reason = ('Source phase from solved stations and shadow crossings.' if status=='VERIFIED'
                  else 'Source equality convention is unspecified; within numerical event uncertainty.' if status=='BOUNDARY'
                  else 'Adjacent retrograde shadows overlap; source precedence between competing phases is unspecified.' if len(events)>4
                  else 'A complete loop before and after this instant is unavailable.')
        return {**base,'phase':phase,'status':status,'reason':reason,'events':events}
    except (ChartError,swe.Error) as exc:
        return {**base,'reason':str(exc),'error_code':getattr(exc,'code','GRADITY_EPHEMERIS_UNAVAILABLE')}
