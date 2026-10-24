"""Frozen, independently retrieved JPL reference epochs; no live network in CI."""
import json,math
from datetime import datetime
from pathlib import Path
import pytest,swisseph as swe
from mystic_rebels import astronomy as astro
from mystic_rebels.catalog import BY_ID

REPORT=json.loads((Path(__file__).resolve().parents[1]/'evidence'/'independent-astronomy.json').read_text())
MAJORS={'Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto'}

@pytest.mark.parametrize('reference',REPORT['comparisons'],ids=lambda r:r['object']+'-'+r['utc'][:10])
def test_independent_jpl_icrf_reference(reference):
    astro.initialize();tt=astro.times(datetime.fromisoformat(reference['utc']))['jd_tt']
    data,flags=swe.calc(tt,BY_ID[reference['object']]['body'],reference['icrf_requested_flags'])
    astro.assert_backend(flags)
    ra=((data[0]-reference['icrf_reference_ra_deg']+180)%360-180)*3600*math.cos(math.radians(reference['icrf_reference_dec_deg']))
    dec=(data[1]-reference['icrf_reference_dec_deg'])*3600
    # Numerical agreement gates over these three measured epochs, not infinite-epoch claims.
    tolerance=.01 if reference['object'] in MAJORS else 1.0
    assert math.hypot(ra,dec)<tolerance

def test_reference_coverage_and_no_provider_failures():
    assert not REPORT['failures']
    assert len(REPORT['comparisons'])==165
    assert {p['object'] for p in REPORT['comparisons']}=={id for id,row in BY_ID.items() if row['group'] in ('Planets','Asteroids','Minor bodies')}
