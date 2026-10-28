# Internal method and evidence â€” Nadia Sanchez outcome-blind trial

This is an exploratory historical comparison within user-selected age windows. The user has not supplied the events that occurred. Selection of these ages is not random; this is not a prospective prediction test or a statistically independent sample.

## Inputs and exact date boundaries

- Full birth name: Nadia Sanchez. The user confirmed no other name should be used before July 2014.
- Birth date/time supplied:17 July 1992,20:01 local, America/Los_Angeles.
- Birth epoch resolved by the existing pinned IANA rules:18 July 1992,03:01 UTC.
- User-supplied coordinates:33.8044,-118.0673.
- Name and birth time are user-supplied; no birth certificate was inspected.
- Age windows use local civil dates, start-inclusive/end-exclusive:17 July 2003â€“17 July 2005 and 17 July 2008â€“17 July 2014. These cover ages 11,12,16,17,18,19,20,21.
- Annual numerology changes on1 January in this selected engine. It is not reassigned to the birthday. Month cells at the first/last July boundary are only partly inside the selected ages.

## Numerology method: exact current STAFFprofiler engine

The calculation calls the existing compiled product adapter without changing it. Relevant source is olsonan26/STAFFprofiler main4172789db1034072f50c78178187e839fa710fb5.

- [Adapter](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/engine-adapter.ts)
- [Annual calculations](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/vendor/lfs/core/lettrology-engine/annualEngine.ts)
- [Letter-duration cycles](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/vendor/lfs/core/lettrology-engine/timelineEngine.ts)
- [Monthly calculations](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/vendor/lfs/core/lettrology-engine/monthlyEngine.ts)
- [Exact alert detector](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/pattern-indicators.js)
- [Year meanings](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/report-descriptions.js)

CY is the reduced calendar-year digit sum. PY is unreduced birth day+birth month+CYroot, preserving every reduction stage. ESS uses active letters' alphabet ordinals A1â€“Z 26; letter durations use repeating1â€“9 values. For a July birthday the annual engine indexes the previous calendar age. Annual COM adds ESSraw+PYraw. Exact 11,13,16 stages trigger; a root alone does not reconstruct them. Annual and monthly alerts remain separate.

This is a versioned method choice, not a resolution of differences with LOOKS-LIKE-COSTAR or other previously requested PY formulas. Reducing the day/month before summation changes compound trails despite equal final roots. A future unified product must settle its authoritative method before treating these alerts as canonical.

The adult/workplace interpretation bank was inspected, but its literal claims about employers, income or marriage cannot be assumed to apply to an 11-year-old. Youth-context wording in the first-pass report is an explicit new interpretive adaptation, not an approved source rule. Health, accident and outcome predictions were not imported.

Outputs: numerology.json includes every annual compound and every intersecting month, with native rule reasons. annual-meanings.json retains the selected category/raw-number source text for internal inspection. The public-facing first-pass note paraphrases rather than presenting that prose as observed biography.

## Astrology calculation and restricted scan

Existing source checkout: Mystic Rebels audited branch3d83db75c30b26d9b068576d84ec49554822fd8c. Original service and ephemeris files were read only. No secret/environment files or hosted APIs were used.

- [Numerical engine](https://github.com/olsonan26/mystic-rebels-chart-generator/blob/3d83db75c30b26d9b068576d84ec49554822fd8c/mystic_rebels/astronomy.py)
- [Placement layers](https://github.com/olsonan26/mystic-rebels-chart-generator/blob/3d83db75c30b26d9b068576d84ec49554822fd8c/mystic_rebels/placements.py)
- [Planet/field vocabularies](https://github.com/olsonan26/mystic-rebels-chart-generator/blob/3d83db75c30b26d9b068576d84ec49554822fd8c/docs/PROFILE_REPORT_KNOWLEDGE_PATH.md#L249-L273)
- [Reviewed sign vocabulary](https://github.com/olsonan26/mystic-rebels-chart-generator/blob/3d83db75c30b26d9b068576d84ec49554822fd8c/data/knowledge/source_meaning_profiles.json)
- [Blocked full directional aspect procedure](https://github.com/olsonan26/mystic-rebels-chart-generator/blob/3d83db75c30b26d9b068576d84ec49554822fd8c/docs/METHODOLOGY_SOURCE_REVIEW.md#L86-L94)
- [Swiss Ephemeris programming documentation](https://www.astro.com/swisseph/swephprg.htm)

The installed Swiss file backend calculates tropical geocentric apparent ecliptic longitudes with speed and verifies the installed core-asset checksums. Natal houses use Whole Sign. Planet function, house Field, astronomical Tone and decan Pulse remain separate. Natal MC is inH 11 and is not relabeledH10.

Before receiving outcomes, the restricted scan covered transiting Saturn,Uranus,Neptune,Pluto to natal Sun,Moon,Mercury,Venus,Mars,Ascendant,Midheaven. It retained all exact0,60,90,120,180 degree separations, with both angular orientations where applicable. No arbitrary orb, danger rank, universal aspect-strength weight, progression, Spark or complete Delegate graph was used.

Daily and six-hour sampling independently bracketed the same 59 exact roots, with bisection refining each equality. The maximum numerical angular residual was about2.9e-10 degrees. That residual is solver precision, not an independent statement of physical ephemeris accuracy, birth-time accuracy or event-timing accuracy. Dates are shown inPacific civil time and should be understood as approximate given the supplied birth details, especially for natal angles.

These are raw geometric contacts. The canonical full PURE directional OOI/aspect/interpretation engine remains blocked; this research did not enable or claim to complete it. Terms such as conjunction/square identify angular geometry here. Proposed life themes come from component vocabularies and are analytical hypotheses, not proof that the physical contact causes a human experience. Trines/sextiles were retained and mentioned to avoid selecting only adverse-sounding material; they are not validated protective effects.

Jupiter, fast-moving transit bodies, other natal objects, minor angles, influence-window entry/exit, relocations and progressions are outside this restricted scan. Fewer exact contacts at a given age cannot establish that the period was safe, quiet or free of important events.

## Timing comparison and counterexamples

There are 98 intersecting calendar-month cells:56 red,12 yellow,30 green. Fifty-nine exact contacts fall into 31 red,12 yellow,16 greenmonth cells. Approximately53% of contacts fall in red months, compared with57% of examined month cells being red. This crude comparison does not show an obvious enrichment of contacts in red months.

These counts do not form a valid significance test: contacts repeat during retrograde passes, months are not independent, some boundary months are partial, contact opportunities are clustered, and ages were chosen by the user. No p-value, accuracy percentage or causal inference is claimed.

Counterexamples deliberately retained in the first-pass reading:
-20 July 2003 Uranusâ€“Moon conjunction:green month.
-11 June 2005 Saturnâ€“Sun conjunction and 21 June Neptuneâ€“Mercury opposition:green month.
-14 February 2009 Neptuneâ€“Mars square:yellow month.
-2 April 2012 Neptuneâ€“Moon conjunction and 21 April Saturnâ€“Sun square:yellow month.
-10 August 2012 Neptuneâ€“Moon conjunction,26 August Saturnâ€“Sun square,18 November Saturnâ€“Venus square:green months.
-15 June 2013 Saturnâ€“Venus square:green month.
-21 June 2014 Saturnâ€“Mercury square:yellow month.

A hit is insufficient to validate the system. The interpretation may provide useful questions, but the computed timing comparison has not established reliable cross-system confirmation.

## Preservation and follow-up

No application code, source engine, deployment, authentication or database was changed. New files are isolated research artifacts in this folder.

NADIA_FIRST_PASS.md is the first interpretation to compare with feedback. first-pass-manifest.json records its SHA256 and those of the original calculation snapshots before event feedback. After feedback, record matches, misses, partial matches and omissions separately. Do not silently revise the first pass, move dates or substitute arithmetic to fit what happened.

