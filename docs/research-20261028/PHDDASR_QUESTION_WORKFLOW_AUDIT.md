# PHDDASR and a usable question workflow: source and runtime audit

Audit date: 28 October 2026, America/Denver. Repository: `olsonan26/mystic-rebels-chart-generator`; inspected local branch `codex/phsr-numerology-integration-20261028`, HEAD `392e808f03837359e990ce38a569aa1bc837788b`.

This audit changes documentation only. Existing uncommitted location data, `mystic_rebels/api.py`, provisioning code and location tests are preserved. It does not approve a personal interpretation, alter a source disposition, or deploy either the chart generator or Base44 app.

## Finding

The requested seven-stage method is partly implemented already in the separate Common Ground local prototype. A person can calculate a chart, select one of four research topics and a calendar year, inspect ordered stages and ruler connections, read conditional prose, and export it. The main Mystic Rebels chart generator has no free-text question workflow. The prototype has no question-text input either, and its current-year setting supplies annual numerology rather than current transits.

The next useful increment is a source-traceable consultation workspace: select the person's chart, type the actual question, select a present or historical time interval, inspect the relevant natal and transit context, and receive an answer restricted to the evidence actually available. This can deliver useful partial answers before all advanced methods are resolved. It must preserve unresolved stages and cannot claim complete PHDDASR while degree-entry/Spark, directed relationships and full Delegate condition remain incomplete.

## The exact order is in an original scan

Three original images were visually inspected in this audit, and their current file bytes were SHA256 checked against the manifest:

| Original | File ID and local original | SHA256 | Fresh observation |
|---|---|---|---|
| Printed 215, PHSR+ | `1fndfULJv6qsDmXdGgJRaJ5DzPQatd-hd`; `reference/originals/1fndfULJv6qsDmXdGgJRaJ5DzPQatd-hd.jpg` | `c3fd1d22189f6e677b28bba74f4d6f42dffb6df10e00b8532a1cb101328c4891` | Starts the basic Planet, House, Sign, Ruler sequence and explains interpretation from the chart's center outward. |
| Printed 216 | `1fx8ChXffMAH7B5DpcS7b-ZaJH4fIaO11`; `reference/originals/1fx8ChXffMAH7B5DpcS7b-ZaJH4fIaO11.jpg` | `e1ef441c421655aa0ca4b886e9f2cd0ef280d58327b6498bdb5333eccfa4d990` | Names **PHD2ASR**, with Degree and Decan represented by the squared D: Planet -> House -> Degree -> Decan -> Aspects -> Sign -> Ruler, then back to a planet. Sign must be identified earlier to calculate its intermediate layers; interpretive flow stays as written. It explicitly separates planetary condition from essential dignity/strength. |
| Lexicon u | `14rP_kN5fywpxaeKDmErtPY02ZUins5vl`; `reference/originals/14rP_kN5fywpxaeKDmErtPY02ZUins5vl.jpg` | `2c5446665a34729820b9b7310446125404372e7392c1af4992ccc72f4e0cb4dc` | Names **PHD2SAR** and places Sign before Aspect. This is a real competing source sequence. The same page also describes pass-through influence through a sign/house ruler without a direct aspect. |

The compiled witness `pure-reflow-9d5fb55c`, PDF 283, supports the chapter sequence. PDF 284 continues the condition/context qualifications. Those complete relevant cached pages were read from the read-only `reference/knowledge-index.sqlite` `pages` table; original imagery was used to verify the important ordering independently of OCR.

Therefore PHDDASR is a faithful plain-text spelling of the chapter sequence and the user's selected flow. It is not a newly invented expansion. Keep a versioned `selected_sequence=chapter_216` decision and preserve the lexicon variation, represented canonically by `original_assertions.json#lexicon-u-phd2sar-order`, rather than rewriting the competing source.

There is a review-register gap: `source_manifest.json` still labels the printed-215 and printed-216 scan records `visual_review_status=NOT_REVIEWED`, `semantic_review_status=PENDING`. The preserved case-study `SOURCE_RULE_MATRIX.md` says both were visually inspected in that earlier work; this audit has now inspected them too. These evidence trails need a deliberate source-review reconciliation. This document does not silently upgrade their canonical statuses.

## What runs now

| Capability | Verified implementation evidence | Practical status |
|---|---|---|
| Main chart calculation | `mystic_rebels/api.py:52`, `mystic_rebels/models.py:18`, `web/src/App.tsx:111` | Actual natal/dual chart flow. `chart_type` accepts natal/dual, without a transit chart request type. Main API has health/config/catalog/methodology/chart/location/timezone routes, no question/research route. |
| Separate local assessment | `apps/common-ground/app.py:242`, `:248`, `:254` | `/api/research` calculates a natal chart and assessment, then annual numerology. It binds locally through the app's launcher/server. Its presence in this repository is not proof that the deployed chart generator uses it. |
| Seven ordered stages | `apps/common-ground/phsr.py:8`, `:23`, `:53` | Planet, House, Degree, Decan, Aspects, Sign, Ruler exist for available main planets and Chiron. Each stage records its status. |
| Actual planet versus house condition | `phsr.py:37`, `:40`, `:55`, `:59` | Sun/father and Moon/mother conventions are retained. Occupant physical motion and the house Delegate's retrograde condition are separate. No Rx contagion is applied. |
| Degree | `phsr.py:62` | Exact within-sign degree plus both competing Spark candidates. Canonical Spark remains null and meaning absent. |
| Decan and sign | `phsr.py:66`, `:74` | Uses actual Pulse/Tone and reviewed sign profiles. Decan-associated planet is distinct from sign ruler. |
| Aspect stage | `phsr.py:44`, `:71` | Computes absolute separations and the nearest 15-degree diagnostic angle. Every relationship is marked geometry-only; `directed_aspects=[]`. No approved Energy Flow is produced. |
| Ruler routes and cycles | `phsr.py:13`, `:77`, `:80` | Follows modern sign rulers, stops at repeated nodes, retains cycle and missing-node information, lists occupants of ruled signs. `condition_complete=False` remains explicit. |
| Reading | `apps/common-ground/report_builder.py:1`, `:51` | Four manually selected topics: trust/boundaries, voice/emotional needs, autonomy/worth, yearly direction. Chooses Chiron, Moon, Saturn or Sun as topic root and traverses that root's route. |
| Interface | `apps/common-ground/static/index.html:40`, `static/research.js:13` | Topic dropdown, integer calendar year and Explore button. No textarea or question string is collected or sent. |
| Timing | `apps/common-ground/app.py:273` | Explicitly states that the endpoint infers no activation dates, transits or forecasts. A current calendar year is not an as-of sky calculation. |
| Export | `apps/common-ground/README.md`; `static/research.js:38` | The selected research packet is available to the existing reading export. This audit inspected code and did not independently exercise browser printing or downloads. |

The preserved Nadia chart fixture reproduces the route Chiron -> Sun -> Moon -> Neptune -> Saturn -> Uranus -> Saturn repeat. The repeated Saturn/Uranus component is not counted as extra strength or confirmation.

## Additional omissions found in this pass

### 1. The runtime source pack is a selected subset with an unresolved dependency

`build_phsr_pack.py:15` selects 32 inventory records and 13 meaning profiles. Their two recorded SHA256 inputs match the current canonical local bytes. All 32 selected records retain `answer_use=NOT_APPROVED`; the overall packet and result also retain `personal_report_approved=False`. Those restrictions are real and must remain attached.

However, the selected record dependency closure is incomplete: `phsr` depends on `planet-lexicon`, which is absent. This matters because planetary keywords carry important exclusions, including the source's warning against assuming a planet alone supplies a real-life outcome.

The pack does not include the canonical `original_assertions.json`, `source_blocker_findings.json`, `material_requirements.json` or `source_line_reconciliation.json`. A record may mention finding IDs without delivering the findings themselves. The recovered lexicon order variation is absent from the runtime packet. `objective-context` and `agency` are also absent. These are precisely relevant to free questions, because they distinguish chart observations, personal context, ordinary-language articulation and choices.

Before a flexible writer uses this pack, retrieve a topic's complete dependencies, associated original assertions, competing witnesses, limitations, relevant findings and required chart facts. The existing `report_knowledge_manifest.json`/topic exports and `knowledge_audit` machinery are a better starting authority than a second hand-selected glossary.

`phsr.py:10` loads the JSON without checking its recorded input hashes at runtime. The current hashes do match; freshness verification is a missing enforcement capability, not a finding that the current pack is stale.

### 2. Occupant presence is not full occupant assessment

`phsr.py:29` assesses only the modern-ruler planet set plus Chiron. The endpoint requests additional asteroids, nodes and points; their presence can be listed in a Delegate payload, but most have no full assessment reference. Even the assessed occupants lack completed directed relationships. The code accurately keeps `condition_complete=False`.

A general question cannot assume that listing Mercury, Venus, Chiron and Vertex in a ruled sign is the same as carrying their complete conditions. Keep physical emitters, receiving mathematical points and unsupported bodies separately typed. Preserve unavailable objects, and show the exact consequence for a requested answer.

### 3. Prose uses broad node references, not a complete claim proof

`report_builder.py:13` and `:23` contain authored Field/function adaptations, then append reviewed decan/sign meanings. `:79` attaches every stage index to each composed node paragraph even though degree-entry meaning and aspects remain unused/unresolved. This is traceability to an assessment, not proof that all seven stages support every sentence.

Use sentence/claim IDs linked to the actual contributing stages and source adaptation IDs. Keep calculation, documented source statement, composed hypothesis and user-reported context as separate claim types. Store the actual skipped dependencies alongside any qualified answer. This permits concise readable prose without losing the explanation trail.

### 4. Annual numerology is currently mandatory even for an astrology topic

`app.py:264` always calls `annual_numbers`; a ValueError returns `ANNUAL_UNAVAILABLE` before returning the otherwise valid natal assessment. A future astrology question endpoint should not require the annual adapter or a governing name policy unless that answer requests those layers. Optional numerology can use its separate pinned method and date/name policies.

### 5. Free questions require a relevance planner, not only a new input box

The four roots in `report_builder.py:1` are proposed product choices. They do not establish a source-authorized taxonomy for every question. A question about work, relocation or an unnamed relationship cannot simply be routed to whichever phrase matches a keyword. Build the chart context first, retain relevant ruler/receiver/occupant dependencies, record why a focus was selected, and allow the operator to inspect or choose the focus. The user-reported situation must not change planetary calculations or retroactively validate the method.

### 6. Broader source concepts are already stored but absent from the narrow composer

Canonical `interpretive_inventory.json#objective-context` describes an objective chart assessment followed by subjective relevance and dialogue; `#agency` describes choices and avoiding dependency. `original_assertions.json#lexicon-q-r-context-first` states that topic Lenses use the whole chart and that Mix-n-Match is conditional on full planetary conditions. Its witnesses include original lexicon q/r/s, file IDs `1gn14uuYHIUg9LHdwrbCmPjx6mjqFwDHF`, `1tLi2tR-oWF852zfo3FwLv7w8yWgzkhxn`, `1U3X82jY8Oc95Y9cv0-3z8OtW_nPz-Pd2`.

These existing source records support investigating a conversational workflow; they do not approve unconstrained keyword assembly. PDF 135-136 and 139-140 were read in this audit as secondary witnesses for objective observation, conversation, personal relevance and articulation. Other source claims about accuracy remain source claims, not independent outcome validation.

## Concrete question workflow

The recommended first release is an operator consultation view inside the preserved chart workflow, using these explicit contracts:

1. **Choose chart and question.** Reuse the actual chart ID/fingerprint, supplied birth data and uncertainty. Collect the question verbatim, optional reported context, desired focus and date/time window. Default the as-of instant once using the user's timezone; persist the exact UTC instant in the answer. Current-location input is needed only for methods that actually use it.
2. **Plan the evidence.** Create a `QuestionPlan` with interpreted intent, topic candidates, chosen roots, chart layers, required facts and reasons for selection. A focus helps relevance; it must not discard necessary ruler/receiver/occupant context. Ask a focused follow-up only when ambiguity changes the answer materially.
3. **Retrieve the full source context.** Use the canonical knowledge authority, complete dependency closure, linked original assertions, conflicts, applicability and exclusions. Carry the selected chapter order plus the lexicon variant. Match rule versions to calculations and retain answer-use statuses.
4. **Assess natal PHDDASR.** Reuse existing supported stages and modern ruler graph. Add missing type/completeness metadata for all relevant occupants. Keep degree and aspects incomplete when their required rules do not resolve. A partial answer may use supported components but must say which missing stage limits the conclusion.
5. **Calculate dated sky context.** Use a separate as-of chart and a fixed natal chart. Calculate current positions and relative geometry, including motion and repeat passes over a requested interval. Retain natal versus transit ecosystem and source/target direction. Geometric equality, orbital eligibility and interpreted influence are separate records. A current-year numerology value cannot substitute for a transit.
6. **Answer the actual question.** Supply a direct, bounded response; explain the relevant natal context and, when computed, the current timing context; distinguish reported circumstances from the chart's suggested themes. Offer a constructive option or useful question. Do not assert hidden biography, another person's thoughts or a guaranteed outcome.
7. **Show the explanation.** An expandable view exposes the seven stages, actual chart coordinates/epochs, selected roots, ruler cycles, transit repeats, claim/source IDs, skipped dependencies and uncertainty. Ordinary prose need not reproduce internal implementation details.
8. **Preserve the consultation.** If saving is part of the selected workflow, retain question/context versions, input fingerprint, exact as-of instant, source/rule versions, calculations and answer revisions. A refresh creates a new dated answer and must not rewrite earlier output or convert feedback into a blind first pass.

Proposed request fields: `chart_id_or_input`, `question`, `reported_context`, `focus`, `as_of_local`, `timezone`, optional `window_start`, `window_end`, `current_location` and `include_numerology`. Proposed result sections: `answer`, `natal_assessment`, `timing_evidence`, `claim_ledger`, `missing_dependencies`, `sources` and `provenance`. These are design proposals; no such endpoint was created by this audit.

## Priorities and acceptance evidence

| Priority | Deliverable | Meaningful acceptance criterion |
|---|---|---|
| 1 | Complete source packet and a source decision register | Every selected concept's dependencies and linked contradictions resolve; lexicon/chapter order variation survives serialization; stale source hashes fail a check. |
| 2 | Question and evidence planner with bounded natal response | Different real questions select documented relevant context; unsupported questions return a precise limitation rather than the same four canned readings; unknown time withholds house-dependent claims. |
| 3 | Present sky and transit-to-natal diagnostics | Frozen exact UTC instant, correct natal target, clear timezones, motion/repeat passes, no weekly-sample-as-exact claim and no hidden generic orb assumptions. |
| 4 | Directed aspects and complete Delegate condition, incrementally | Body-specific OOI, angle-cap combination, endpoints, receiver exceptions, ecosystems, Vantage, hand-off/Turnover/Fringe and cycle conditions have explicit source decisions and fixtures. Partial supported geometry remains available while unresolved semantics stay partial. |
| 5 | Full-method claim composition | Each personal claim passes its actual source/calculation/context prerequisites. An invalid writer draft cannot invent a citation or turn a missing stage into a complete result. Feedback stays separate from blind evidence. |

The unresolved D1-D8 register in `research/astrology-numerology-20261027/nadia-phsr-after-feedback-20261027/SOURCE_RULE_MATRIX.md` remains useful, with current implementation progress distinguished from the older plan: structural assessments, cycle handling and annual values now exist; canonical Spark, complete directed conditions and full forecasting still do not. Not every question requires progressions, relocation, activation-calendar or name-transition decisions; enforce only the prerequisites of the claims actually being made.

## Verification performed

- Fresh source/code inspection on the stated HEAD; verified the absence of free-question routes in the main API and current prototype request/UI.
- Visually inspected three originals named above; exact original SHA256 values match their records. Read complete relevant cached PDF pages 135, 136, 139, 140, 283 and 284. This is targeted review, not an exhaustive book re-read.
- Measured the runtime pack: 32 records, 13 profiles, 32 `NOT_APPROVED` records, one omitted transitive dependency (`planet-lexicon`); both recorded input byte hashes match.
- Exercised `phsr.assess` on the preserved recalculated Nadia chart fixture. Seven-stage order, ruler path, repeated Saturn, null canonical Spark, empty directed aspects, and all four topic composers passed direct assertions. This does not freshly validate ephemeris calculations or personal accuracy.
- Ran `tests_comparison.py`: **13 tests passed**, 0.037 seconds. These verify the existing natal comparison's method/uncertainty/citation boundaries, not the proposed free-question flow.
- Attempted `python -m unittest discover -s apps/common-ground -p test_research.py -v`. It stalled before results after the TestClient import warning and was interrupted. It is **not recorded as a pass or a demonstrated product defect**. The environment has a known restricted-socket/TestClient limitation; this audit did not change the app or tests to work around it.
- No browser end-to-end run, deployment verification or Base44 live-code inspection was performed by this sub-audit.

All repository-relative paths above resolve beneath `C:\Users\olson\OneDrive\Documents\Reverse Skill\work\Mystic-Rebels`.
