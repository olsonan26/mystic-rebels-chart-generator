# Independent station and shadow verification

The Gradity implementation now has independent astronomical event references for
Mercury's March–May 2024 loop and Venus's January–May 2025 loop. Venus's loop crosses
0° Aries: its retrograde station is at 10.835728° and direct station at 354.624899°.
The independent reference solver does not consume any Swiss longitude or speed.

## Matched conventions and measured differences

Eight raw NASA JPL Horizons responses under `evidence/astronomy-followup/` retain
584 samples at ten-minute spacing, with query URLs and SHA256 hashes in the two
`*-independent-events.json` reports. Each query uses Earth geocenter `500@399`,
Mercury `199` or Venus `299`, observer quantity 45 (apparent ICRF RA/DEC), and
`AIRLESS`. The corrections include light time, solar light deflection, and stellar
aberration. The returned post-1962 UT labels are UTC. ERFA independently converts
UTC → TAI → TT, applies its IAU 2006 ICRS-to-mean-ecliptic/equinox-of-date matrix,
and adds IAU 2000A/2006 nutation in longitude for the true equinox. Production keeps
its existing Swiss file engine, apparent geocentric coordinates and flags 258.

NASA quantity 31 is also retained as a diagnostic. Its native IAU76/80 convention
is **not** silently treated as the production coordinate model. The matched q45
rotation retains the small Swiss long-term-precession versus IAU2006 and provider
apparent-correction differences, which are measured below.

| Sampled cycle | Max matched longitude residual | Max event-time residual |
| --- | ---: | ---: |
| Mercury, 2024 | 0.001096818 arcsecond | 0.457753 second |
| Venus, 2025 | 0.001502739 arcsecond | 2.582079 seconds |

The independent event fit uses a fifth-degree polynomial over each twelve-hour
JPL window. Stations are derivative roots; shadow entries/exits repeat the
opposite station's longitude on the adjacent direct arc. Fourth-degree refits
measure stability separately (largest sampled station change: 0.004507 second).
Longitude fit residuals are below 0.000004 arcsecond. The accepted regression
tolerances are 0.02 arcsecond in matched longitude and ten seconds in event time.
These tolerate the residual coordinate/correction models and finite-difference
versus native analytic-speed station definitions; they are **sampled agreement
gates**, not universal uncertainty guarantees. The production numerical root
bracket of 0.1 second is a separate solver quantity. Its small boundary band is a
numerical equality guard, not a claim of subsecond physical accuracy.

## Offline regressions

`astronomy_qa/test_horizons_gradity.py` checks all eight event times and longitudes,
rebuilds both independent cycles from the raw JPL inputs, checks all 584 matched
coordinate samples, verifies immutable raw hashes, and verifies ordered phases
across Venus's 360°/0° wrap. No network is used by the tests. The original 165-body
reference comparisons and other numerical fixtures remain intact.

Reproduce the reference analysis with
`python scripts/astronomy_followup_horizons.py`; existing cached responses are
reused. Run `python -m pytest astronomy_qa/test_horizons_gradity.py -q` for the
independent event checks. The reference script's Swiss production comparison runs
only **after** the independent JPL event fit and cannot affect its reference roots.

Authoritative sources: [NASA Horizons observer quantities and time/frame conventions](https://ssd.jpl.nasa.gov/horizons/manual.html),
[NASA Horizons API parameters](https://ssd-api.jpl.nasa.gov/doc/horizons.html),
[ERFA IAU2006 ecliptic rotation](https://github.com/liberfa/erfa/blob/master/src/ecm06.c),
[ERFA IAU2000A/2006 nutation](https://github.com/liberfa/erfa/blob/master/src/nut06a.c),
and [Swiss calculation flags and speed conventions](https://www.astro.com/swisseph/swephprg.htm).

## Sophia remains a separate source question

Swiss supports physically distinct mean, osculating and natural/interpolated lunar
apsides. Its [general documentation, section 2.2](https://www.astro.com/swisseph/swisseph.htm)
explains that natural/interpolated perigee is generally not opposite natural
apogee; osculating apsides are instantaneous two-body constructions. Mean apsides
do not have a direct JPL mean-apsis output for an independent position comparison.

The supplied book rejects interpolated points at PDF page 504, reflow page 508,
original printed page 614. It names Mean Priapus/Sophia at 29° Gemini (PDF page 508,
reflow 512, printed 620) and Osculating Priapus at 13° Cancer (PDF page 509, reflow
513, printed 621–622), and links osculating Sophia's retrograde state to osculating
Lilith's at PDF page 508 / printed 620. However, the chapter's opening original
printed pages 617–619 are absent from the supplied PDF. Those witnesses support
two named variants but do not establish the missing exact position formula.
No interpolated perigee is substituted and neither Sophia entry is promoted to
Verified. A physically plausible perigee calculation alone would not verify the
author's exact intended Sophia definition.

Formula fidelity for the source-defined Gradity phase labels is distinct from
this astronomical comparison and from scientific evidence for their meanings.
