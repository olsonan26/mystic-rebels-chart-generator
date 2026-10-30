# Current transits and aspects: evidence and missing workflow

Audit date: 28 October 2026, America/Denver. Repository: `olsonan26/mystic-rebels-chart-generator`, local branch `codex/phsr-numerology-integration-20261028`, HEAD `392e808f03837359e990ce38a569aa1bc837788b`.

This audit changes no application code, source authority, approval flag, deployment, or saved chart. Existing location/API work remains intact. Findings describe the inspected local checkout; the separate Base44 app and its deployed transit behavior were not inspected here.

## Outcome

The astronomy needed to show the sky at a chosen current time already works. The chart generator does **not** yet provide a current-transits view, natal/transit overlay, production transit event search, or typed current-situation question workflow. The Common Ground research app supplies ordered natal assessments and annual numerology, explicitly excluding transits and forecasts.

The useful next implementation can expose current positions, natal overlay, timestamped angular diagnostics and selected source-backed component explanations. Complete PURE directed-aspect interpretation requires additional rules. This is a specific implementation gap; it does not justify discarding the working astronomy or keeping every useful display unavailable.

## Verified capabilities and boundaries

| Capability | Fresh result | Evidence |
|---|---|---|
| Positions on the user's current civil date | A fixed audit snapshot at `2026-10-28 19:33:00 America/Denver` resolves to `2026-10-29T01:33:00+00:00`; 72 of 74 catalogue outputs are available, including the ten planets and Chiron | Direct `service.calculate(BirthInput(...))` invocation with all catalogue IDs; `mystic_rebels/service.py:38`; `mystic_rebels/astronomy.py:44` |
| Missing objects | Only `SophiaMean` and `SophiaTrue` unavailable in this snapshot, both with explicit `RULE_NOT_VERIFIED` | `mystic_rebels/catalog.py`; current all-object invocation |
| Scope of that count | Includes derived angles, Parts and lunar points as catalogue outputs; it is not 72 independently validated physical bodies | `mystic_rebels/catalog.py`; `mystic_rebels/service.py:68` |
| Ephemeris provenance | Swiss file backend, `pyswisseph 2.10.3.2`, native Swiss version `2.10.03`; file hashes checked and silent Moshier fallback rejected | `mystic_rebels/astronomy.py:14-35`; current invocation |
| Civil-time safety | Denver `2026-03-08 02:30` is rejected as nonexistent; `2026-11-01 01:30` demands a fold; explicit folds resolve to `07:30Z` and `08:30Z` | Direct `resolve_local` calls; `mystic_rebels/chronology.py:12` |
| Motion and Gradity | Actual speed and Rx flags available; four-phase Gradity supported for Mercury through Pluto | `mystic_rebels/gradity.py:15-20,138-166`; current invocation |
| Chiron | Longitude and speed available; full station/shadow Gradity is explicitly unavailable | `mystic_rebels/gradity.py:149-150`; current invocation |
| Current sky product interface | Absent. API routes are health/config/catalog/methodology/charts/locations/timezone; no transit/event/overlay/question route | Inspected route table; `mystic_rebels/api.py` |
| Transit chart type | `chart_type='transit'` fails schema validation; allowed types are `natal` and `dual` | Direct model invocation; `mystic_rebels/models.py:18` |
| Natal/transit UI | Birth entry and a single chart's two presentation modes; no second epoch or two-chart overlay state | `web/src/App.tsx:31-57,111,342,710,936` |
| Directed aspects | Deliberately blocked; no false conventional aspect lines produced as book-verified relationships | `mystic_rebels/service.py:23`; `astronomy_qa/test_core.py:183`; `web/src/wheelLayout.test.tsx:126` |
| Ordered assessment geometry | Common Ground records every pair's nearest 15-degree diagnostic angle and residual, with `directed_aspects=[]` | `apps/common-ground/phsr.py:42-53,71-74` |
| Current-situation research endpoint | Existing `/api/research` takes a year and one of four topics and calculates the natal chart; it returns `No activation dates, transits or forecasts are inferred by this endpoint.` | `apps/common-ground/app.py:242-273` |

The timestamp above is a reproducible audit epoch chosen from the user's date context, not a claim to have fetched a continuously updating live sky. The astronomical computation was not independently cross-validated for every current body in this audit.

## What the original scans require beyond a transit list

Fresh visual review of original photographs `reference/source_photos/IMG_4958.jpg`, `IMG_4959.jpg` and `IMG_4960.jpg` confirms printed pages 497-499. These are original-source witnesses, not new empirical validation of the author's claims.

1. **Actual contact matters.** Printed 497 distinguishes a planet crossing a natal sector from a qualified contact to an occupant or angle in another sector. Opposite signs alone must not create an aspect to an entire natal house.
2. **Assess the current sky first.** Printed 498-499 requires the transit body's own current relationships before reading its interaction with the person. A flat list of transit-to-natal equalities omits this layer.
3. **Carry current ruler context.** Printed 499 illustrates a current Moon/Uranus relationship with Pluto in the sign Uranus rules. A transit body arrives with its current relationships and rulership context. That packet must remain separate from the natal body's own condition and natal ruler graph.
4. **Preserve directed reading order and chart layers.** Printed 499 explicitly distinguishes natal/transit notation and a hand-off. The notation is not permission to invent physical reverse emission from a natal object into the current sky.

Compiled PDF pages 426-429 were text-inspected as complementary witnesses. Page 426's extracted text includes the opening of the Cosmic Dance discussion followed by a discontinuity into a page-500/return-chart fragment; it does not expose the full printed-499 discussion seen in the original photograph. PDF 428-429 contains the directional transit Moon/natal Sun worked material, but the extracted scenario/diagram sequence is discontinuous. This establishes an extraction/alignment concern, not proof that the visible compiled PDF page itself lacks every omitted element. Original scans and a visual PDF comparison must govern reconciliation.

The canonical `data/knowledge/material_requirements.json` already records seven atomic `current-sky` requirements:

| Requirement | Existing disposition |
|---|---|
| `M12-01-01` Sky-to-sky condition before overlay | Source found but implementation missing |
| `M12-02-01` Personal sky overlay | Source found but implementation missing |
| `M12-03-01` Transit sender and natal receiver | Source incomplete |
| `M12-03-02` Natal response without physical reverse emission | Source incomplete |
| `M12-04-01` Pass-through without direct contact | Source found but implementation missing |
| `M12-05-01` Connected WITH context | Source found but implementation missing |
| `M12-05-02` Concurrent WHILE context | Source found but implementation missing |

All seven retain `personal_answer_approved=false`. The first, second, fifth, sixth and seventh rows are especially useful targets: the source is present, while the product workflow is missing. The distinction prevents treating every gap as a missing book passage.

Related unresolved findings in `data/knowledge/source_blocker_findings.json` include `minor-aspect-ooi`, `handoff-equality-and-phase`, `territory90-versus180`, `point-internal-alignment-scope`, `microaspect-scope-and-boundary`, `notation524-528-transit`, `pluto528-transit-order-labels`, and `synastry543-asymmetric-reach`. These contain competing definitions, endpoint/scope issues, and asymmetric contact examples. A universal symmetric orb or a single reversed-angle rule would erase those constraints.

## Event timing: existing research is useful but not production complete

The retained after-feedback ledger, `research/astrology-numerology-20261027/nadia-phsr-after-feedback-20261027/expanded-transit-geometry.json`, reports 142 equalities, equal daily/six-hour fingerprints, and maximum angular residual about `1.0024e-10` degrees. It selects five movers, six natal targets and twelve oriented multiples of 30 degrees over 17 July 2003 through 17 July 2014. No influence orb is assigned. Houses are fixed natal Whole Sign sectors.

The generating script remains outside the product module, at `C:/Users/olson/OneDrive/Documents/Reverse Skill/reports/mystic-costar-analysis-20261027/nadia-phsr-after-feedback-20261027/calculate_research.py:24-28,53-87`. Its start/end dates, target chain and mover set are hard-coded. The product has no API using this scanner. The copied blind-trial script under repository `research/` also retains a `ROOT/'work'/'Mystic-Rebels'` import assumption appropriate to its original reports location; the archived results must not be mistaken for a portable product service.

### Fresh fault probes

The existing `roots()` function was imported without running its artifact-writing `__main__` section. Its position and interval functions were replaced in memory for two analytic checks:

| Probe | Known result | Daily bracket result | Quarter-day bracket result |
|---|---|---|---|
| `longitude=100+(t-0.5)^2`, target 100, interval [0,1) | Touch at t=0.5 | No roots | One root near 0.5 |
| `longitude=100+(t-0.4)*(t-0.6)`, target 100 | Crossings at t=0.4 and 0.6 | No roots | Both roots |

A real Mercury example corroborates the tangency class: the existing station solver finds `2026-10-24T07:12:42.572Z`, longitude about `230.97898801039716` degrees, with numerical speed near zero. Using that station longitude as the target and a one-day bracket centered on the station, the equality scanner returns no roots. A stationary touch lacks the endpoint sign change required by this algorithm.

This does **not** invalidate the stored 142 identified crossings, nor prove the historical selection actually omitted a specific natal-target event. It proves that matching coarse/fine grids is insufficient to certify arbitrary event completeness. Furthermore, the current fingerprint compares body, target, oriented offset and **local date**, not root epochs or residual differences. Two grids can agree by date while their numerical event times differ.

Before exposing general event searches, split motion into monotonic arcs at solved stations, unwrap angles, detect endpoint/equality/touch events, retain all repeated direct/Rx passes, and distinguish entry, exact contact, closest approach, station and exit. Fast movers need an adaptive bound or an appropriate official crossing routine; shrinking one fixed grid is not a general completeness proof. Exact angular residual, bracket tolerance and independent ephemeris agreement are different measures.

The separate Gradity solver already does several things well: station roots use speed, wrap discontinuities are rejected, shadow crossings require the adjacent direct-motion arc, incomplete loops fail closed, exact transitions remain `BOUNDARY`, and overlapping shadows preserve uncertainty. Its numerical bracket is 0.1 seconds, with a 0.2-second boundary band. These values do not imply matching independent physical accuracy or equally precise source birth data.

## Concrete feature sequence

### 1. Current sky and personal overlay

Add a distinct current-epoch request and response. Preserve the natal input and natal Ascendant. Let the user choose Now or a date/time/timezone, with explicit fold handling; record the resolved UTC. Current location is separately optional for event angles/relocation, never a replacement for birth location. A geocentric body position does not require guessing the person's current city.

Show two synchronized modes: current sky to current sky, and current sky over fixed natal sectors. Display longitude, Tone, Pulse, physical motion, available Gradity, and unavailable-object reasons. Keep natal and transit rulers, occupants and conditions in separate typed packets. A moving event Ascendant, relocated chart and fixed natal house are three distinct objects.

### 2. Contacts and time windows

Provide a bounded geometric diagnostic table first: mover, target, chart layers, exact or nearest angle, residual, applying/separating from actual relative motion, event UTC/local time, repeated-pass ID, source eligibility and rule gaps. For sky-to-sky calculations both bodies move; a transit-to-natal target is fixed. Do not label every nearest 15-degree multiple as an accepted aspect, omit source-relevant 72/144-degree candidates through an arbitrary selection, or infer Energy Flow from shortest separation.

Add an interval search only after the station/tangency/repeat/endpoint cases pass. A user-selected diagnostic tolerance can filter visibility if it is clearly a display choice; it must not become an invented book OOI. Influence entry/exit needs an applicable emitter/angle rule and endpoint convention. Show `not established` where the rule is absent instead of inventing peak or duration.

### 3. Question answering through PHDDASR

The typed question needs the selected person, exact current epoch or interval and user-provided situational context. Retrieve relevant source concepts and the full prerequisite graph, then assess current-sky sender, qualified natal receiver, each receiver's PHDDASR chain, applicable actual contacts, and each layer's rulers/occupants. Explain which parts can answer the question and which remain unresolved.

Begin with one reviewed topic and an explicit, auditable selection of relevant chart factors. Preserve the question and reported context separately from calculated facts; do not use the question itself as proof that a chart discovered the situation. Missing birth time should remove house/angle conclusions while retaining supported position-based explanations. Source explanation questions can be answered from reviewed source passages even when full personal synthesis is unready.

Return a readable connected explanation, practical reflection and an expandable evidence view. Include the timestamp and actual limitations. A bare glossary, a generic zodiac answer, or a preselected Chiron narrative for every question would not satisfy this workflow.

## Validation performed

Current all-catalogue calculation, route enumeration, transit-type rejection, and Denver DST gap/fold probes were executed directly against the checked-out code. No HTTP browser or deployment test was performed.

Focused existing checks:

```powershell
.\.runtime\python.exe -B -m pytest -q -p no:cacheprovider astronomy_qa/test_gradity.py astronomy_qa/test_horizons_gradity.py astronomy_qa/test_core.py -k 'station_transitions or overlapping_real or exact_event_utc or fallback_rejected or cached_events or incomplete_loop or actual_station or coordinates_match_production or independent_fits or venus_cycle_across or historical_iana or dst or backend_fallback or no_false_aspects or velocity_and_retrograde'
```

Result: **55 passed, 53 deselected**, one existing Starlette/httpx deprecation warning. This covers real loop ordering/phases, independent cached Horizons/ERFA event and coordinate samples, signed speed, UTC roundtrip, wrap handling, asset/backend rejection and DST. It is not a complete transit workflow test because that workflow is absent.

Execution used the existing `.runtime/python.exe`, Python 3.11.9, FastAPI 0.162.0, pyswisseph 2.10.3.2, tzdata 2026.5, pyerfa 2.0.1.5 and pytest 9.1.1. The repository declares Python 3.12 in `pyproject.toml`; the existing `.venv/Scripts/python.exe` lacked FastAPI. These results therefore verify the installed research runtime, not a newly reproduced declared-runtime installation.

## External primary documentation checked

The [official Swiss Ephemeris programming interface](https://www.astro.com/swisseph/swephprg.htm) was checked during this audit for UT/TT input distinctions, speed flags, ephemeris return behavior and dedicated Sun/Moon crossing functions. The source correctly distinguishes UT input to `swe_calc_ut` from TT input to `swe_calc`, asks for speed and rejects backend substitution. The official library's crossing capabilities support geometric event searches; they do not supply this book's interpretation rules or validate personal predictions.

## Remaining verification

No actual person's current-situation answer was generated. No live current-sky UI, natal overlay, full directed OOI network, event search API, question submission/render/save/reopen path, or separate Base44 behavior was validated. Original pages 497-499 received fresh targeted visual review; the rest of the transit chapter did not receive a new complete visual reconciliation in this audit.
