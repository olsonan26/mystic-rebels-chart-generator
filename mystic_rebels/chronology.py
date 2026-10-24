from datetime import datetime,time,timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError, reset_tzpath
import tzdata
from .errors import ChartError

# Force the pinned IANA database rather than silently using OS data.
reset_tzpath([str(Path(tzdata.__file__).parent/'zoneinfo')])

def resolve_local(date:str,clock:str,zone_name:str,fold:int|None=None):
    try:
        naive=datetime.fromisoformat(f'{date}T{clock}')
        if naive.tzinfo is not None: raise ValueError('Enter local clock time without an offset')
    except ValueError as exc:raise ChartError('INVALID_LOCAL_TIME',str(exc))
    try:zone=ZoneInfo(zone_name)
    except ZoneInfoNotFoundError:raise ChartError('INVALID_TIMEZONE','Choose a valid IANA time zone.',zone=zone_name)
    candidates={}
    for choice in (0,1):
        aware=naive.replace(tzinfo=zone,fold=choice)
        utc=aware.astimezone(timezone.utc)
        if utc.astimezone(zone).replace(tzinfo=None)==naive:candidates[choice]=utc
    if not candidates:raise ChartError('NONEXISTENT_DST_TIME','This local time did not occur because the clock moved forward. Correct the birth time.')
    if len(set(candidates.values()))>1 and fold is None:
        raise ChartError('AMBIGUOUS_DST_FOLD','This local time occurred twice. Choose the first or second occurrence.',choices=[{'fold':k,'utc':v.isoformat()} for k,v in candidates.items()])
    chosen=candidates.get(fold if fold is not None else 0)
    if chosen is None:raise ChartError('INVALID_LOCAL_TIME','The selected occurrence is not valid.')
    return chosen
