# Concrete next implementation scope

27 October 2026. **Plan only; application code and deployments were not changed.** Build on the existing local prototype at `C:/Users/olson/OneDrive/Documents/Reverse Skill/work/mystic-natal-bridge-prototype`. Preserve both original source applications and the separate Base 44 project.

The next increment should deliver an inspectable, ordered natal assessment with ruler/Delegate structure and an ESS/PY/COM year view. It should show the completed supported content and the exact unresolved stages in the same assessment. Full directional forecasts remain a separate release gate.

## Existing integration points

- `app.py:192` currently builds the chart/name comparison; its `PLANETS` list omits Chiron. Add a separate research-assessment request path that requests Chiron plus the necessary ruler/occupant objects. The current `/api/compare` flow remains available.
- `compare.py:314` composes three natal topics through exploratory digit/theme bridges. Keep that result separately versioned; do not relabel its current bridge text as PHSR+.
- `sources.py` and `data/source-pack.json` provide a frozen ingredient pack. Generate a **new** versioned PHSR rule/evidence pack from exact local source records; preserve the old pack and its provenance.
- `numerology.py` implements the selected LOOKS-LIKE-COSTAR natal formulas. Annual STAFFprofiler calculations need a distinct adapter/method ID, rather than a change to this natal calculator.
- `static/index.html`, `static/app.js` and `static/styles.css` are the existing local interface and export surfaces. Add topic/year selection there after the evidence packet is inspectable.
- Reuse Mystic `mystic_rebels.service.calculate`, `placements.py`, `astronomy.py` and supported Gradity. Retain `RULES.spark/aspects/progressions` in their current blocked states. Do not patch those source gates to make a report appear complete.

## Exact data contract

Use separate records for calculation, documented meaning, composed hypothesis, reported history and validation. A hash or a reviewed passage is not an accuracy score.

| Record | Required fields |
|---|---|
| `CaseInput` | `case_id`, birth-name text, dated name-history segments, input-provider basis, civil date/time, IANA zone, fold, UTC, time accuracy/uncertainty, coordinates with provenance, prior export reference and distinct coordinate basis |
| `MethodIdentity` | Named method/version, source repository + commit, file SHA256 s, selected rule variants, date-boundary convention, calculation backend/flags/assets, calculation vs interpretation approval separately |
| `SourceWitness` | Stable ID; original image provider ID/path/hash or compiled source ID/PDF page/text hash; printed page; excerpt/line locators; acquisition/OCR/visual/semantic statuses; competing witness IDs |
| `Rule` | ID/version, domain/stage, inputs, output type, scope/ecosystem, required conditions, witness IDs, exceptions, conflicts, missing-rule IDs, calculation support and personal-answer approval separately |
| `ChartPoint` | ID, chart/epoch ID, raw longitude, latitude/declination/speed, display DMS, physical motion, Gradity phase/status, house, Field, Tone, Pulse, sign ruler, decan association, Spark null/conflict, astronomical provenance |
| `OrderedAssessment` | Root node ID, fixed seven-stage order, per-stage facts, applied rules, completion state, supported meaning, withheld claims, unresolved dependencies, continuation node/cycle reference |
| `DelegatePayload` | Delegate ID; actual ruled sign; natal house; occupants and each occupant's assessment reference; receiving points separately typed; completeness flags for occupancy and condition |
| `Relationship` | Typed `sign_ruler`, `decan_refinement`, `house_delegate`, `occupant_carriage`, `geometry_candidate`, or `directed_aspect`; source/target IDs and chart contexts; rule/witness IDs; validity state |
| `GeometryCandidate` | Both exact longitudes/epochs, oriented difference, candidate angle, residual, applying/separating diagnostic if calculated, emitter bound witness if known; **no implicit approved edge** |
| `DirectedAspect` | Emitting/receiving body, ecosystem, Vantage and Energy Flow order, angle-band rule, OOI/cap combination, hand-off/Fringe/Turnover state, endpoint rule, receiver assessment; only construct when every required rule resolves |
| `RulerCycle` | Component ID, members/edges, first path occurrence, repeated-node references, no invented strength/weight and no arbitrary final-dispositor label |
| `TimingDiagnostic` | Method family, natal/transit distinction, selection created after/before feedback, fixed target chart, interval bounds/timezone, all event roots/repeats, convention uncertainty, candidate vs approved-event state |
| `AnnualNumbers` | Name basis + effective interval + policy ID, calendar year and prior-age index, active letters with ordinal and duration values, CY/ESS/PY/COM raw/trail/root/formula, category/raw meaning lookup and source hash |
| `MonthlyNumbers` | Parent annual ID, start/end-exclusive, PM/PME/MCOM raw/trail/root and carries, annual bands and monthly indicator reasons separately; no harm probability |
| `CrossSystemProposal` | Exact roles on both sides, narrow shared concept or tension, each side's independent evidence, hypothesis ID, no-link outcome, shared-input dependency and counterevidence |
| `ReportedEvent` | Origin, reported text/summary, date precision/window, age derived from date, received-after-freeze status, external verification state; no inference back into a chart calculation |
| `ReportClaim` | Text, kind (`calculation`, `documented_rule`, `composed_hypothesis`, `reported_history`), required evidence IDs, topic/age suitability, missing dependencies and publication eligibility |

For example, the Chiron **degree stage** must carry `degree_in_sign=11.040693934109129`, house-parity candidate Virgo, sign-parity candidate Pisces, `canonical_spark=null`, `status=conflict`, `missing_rule_ids=[D1]`. Its `sign_ruler` edge goes to Sun; its `decan_refinement` association is Sagittarius/Jupiter. These must never overwrite one another.

A degree stage's conflict does not delete its exact position or its supported decan calculation. A calculation can be complete while the corresponding interpretation remains incomplete.

## Ordered reasoning algorithm

1. Normalize inputs and preserve supplied values/provenance. Resolve the epoch and calculate actual positions with existing availability and uncertainty handling. Precompute astronomical sign only for coordinate/decan/ruler arithmetic.
2. Build the outer-sign house map and occupant lists. Type physical bodies and receiving mathematical points. Preserve unavailable objects instead of substituting a different one.
3. For each root, emit **Planet**, including its own physical motion and supported phase. Emit **House**, then its Delegate condition as a separately sourced carriage condition; no Rx contagion.
4. Emit **Degree**, exact coordinate and FCA diagnostics; leave canonical Spark unavailable on conflict. Emit **Decan**, retaining the actual Pulse sign and association type.
5. At **Aspects**, attach all eligible diagnostic geometry and rule-specific partial results. Emit a directed edge only when all required rules resolve. A partial aspect stage stays visibly partial and cannot support a complete Energy Flow claim.
6. Emit reviewed **Sign** expression; then **Ruler** with the target's actual placement and a reference to its own seven-stage assessment. Carry its ruled-sign occupants as structured condition dependencies.
7. Use a path-local visited set for explanatory traversal and store strongly connected components for repeated graph structure. Nadia's main cycle is `{Saturn,Uranus}`. A separate `CycleRef` points to its existing assessment; it does not add another copy of the theme or imply enhanced strength. A resource limit may stop a large unresolved branch, but must say why and retain the unresolved references.
8. Compose only claims whose prerequisites are present. Clearly label conditional research composition after a skipped stage. Do not describe it as a completed full PHSR+ reading. Keep the natural reading free of source/creator names; an explanation view exposes the ordered evidence and gaps.
9. Apply topic selection after assessing the necessary context, rather than selecting a few attractive placements first. A topic filter must not remove required ruler/receiver context.

## Proposed files and increments

These names describe future additions, not files created by this research phase.

| Increment | Proposed changes in the separate prototype | Reviewable result / completion criterion |
|---|---|---|
|R1: rule/evidence pack|`data/phsr-rules-v1.json`, `rule_catalog.py`, `build_phsr_pack.py`|Exact witnesses, selected order, competing variants and D1-D8 gaps; no generic fallback; original source repositories unchanged |
|R2: assessments and graph|`assessment_models.py`, `phsr.py`, `ruler_graph.py`; narrow new `app.py` research endpoint|All six Nadia nodes in correct order, direct vs delegated Rx separated, actual occupants included, Saturn/Uranus cycle terminates with references; conditional stage statuses visible |
|R3: annual view|`annual_adapter.mjs`, `annual_adapter.py`, `data/annual-method-manifest.json`|Read-only import or hash-pinned vendored copy of STAFFprofiler `assets/chart-engine.js`, plus its exact indicator/meaning functions and recorded source commit. Reproduce frozen 10 years/98 months before exposing new inputs |
|R4: topic reading/export|`report_builder.py`; focused edits to existing static files|Topic/year selector, substantive reflection, optional explanation view, structured JSON and existing print/export behavior. Trace every sentence to its packet. No fabricated biography |
|R5: timing research mode|`timing_diagnostics.py`, research-only UI/export|Continuous selection, all roots/repeats, timezone and method labels, baseline/counterexamples; exact equality view is usable without claiming an approved forecast |
|R6: gated full-method work|Only after D1-D6 decisions and source fixtures|Canonical Spark, directed aspect flow/complete Delegate condition and full timing integration implemented and verified under newly selected source rules |

R1-R4 can be built now within a clearly labeled research workflow. R5 can expose reproducible diagnostics now; a full forecast cannot be enabled by calling diagnostics a forecast. R6 remains specifically conditional, not a reason to postpone every useful feature.

## Numerology and name boundaries

Version the natal method as LOOKS-LIKE-COSTAR core at `023140de4ac9ebad8a804b4c984337135e77b19a`, and the annual trial method as STAFFprofiler at `4172789db1034072f50c78178187e839fa710fb5`. The former uses natal Pythagorean sums; the latter's annual ESS uses active-letter alphabet ordinals and 1-9 letter durations. Do not reuse a root reducer or label as proof that the formulas agree.

The initial annual screen should expose **ESS, PY and COM** with distinct roles. Show raw/trail detail in the explanation view; emphasize constructive category-specific prose in the reading. Monthly detail is optional; daily calculations and PMEI expansion are outside this increment. A red compound marker and a COM approach paragraph are separate outputs.

Represent birth and current names as dated input segments, while leaving the unresolved name-cycle adoption/reset rule unselected. An annual request crossing an unsupported name transition should return the missing policy explicitly or offer a labeled birth-name scenario. It must not silently replace the name. Nadia's frozen period remains Nadia Sanchez; no marital history is encoded from the name alone.

Catalogue text is selected by category and authentic raw/trail candidates. Do not use root 4 as a replacement for COM49/13/4 or merge main and Mini categories. A child-context rewrite needs a reviewed adaptation ID linked to the original passage; preserve both in the internal evidence. Source guidance about responsibility must not imply that children should manage adult abuse or family survival.

## Topic and report behavior

Offer a compact initial selection: **trust and boundaries**, **voice and emotional needs**, **autonomy and worth**, **yearly direction**. Topic names are proposed product choices, not source taxonomies. A general report can combine selected topics without repeating the same cycle as several confirmations.

Each topic should contain a connected reflection, a practical question or constructive focus, and its actual evidential limit. The explanation view can show Planet/House/Degree/Decan/Aspects/Sign/Ruler and graph references. Keep source names out of the personal narrative. Do not automatically label a chart “abuse,” “danger” or a life-event category. User-supplied history can be included only as explicitly reported context; it must remain separate from what the chart independently supports.

Use an explicit research/feedback switch in exported records. The blind calculation/writer packet excludes later event feedback; a retrospective packet includes it in a separate provenance section. Preserve prior output bytes and report versions so a refreshed interpretation cannot rewrite a first pass.

## Meaningful verification

| Verification | Failure it must catch |
|---|---|
|Nadia placement/source fixture|Sun reassigned to H8; Chiron marked natal Rx; second Leo decan mistaken for first/Sun; export vs user coordinates silently merged |
|Ordered trace assertions across main and supplemental routes|Sign meaning emitted before House; missing stage silently omitted; ruler named but not assessed |
|Motion/Delegate counterexamples|Direct Moon made Rx because Neptune is Rx; an Rx occupant retrograding every house occupant; receiving points becoming exact zero-radius emitters |
|Conflict fixtures|Selecting one Nadia Spark candidate by biography; dropping lexicon order variation or composite Saturn counterexample |
|Graph behavior|Infinite Saturn/Uranus recursion; repeated-node amplification; decan Jupiter substituted for Leo's Sun; missing Mercury/Venus occupant conditions hidden |
|Actual annual/monthly snapshot reproduction|Component-reduced PY; root+root COM; ordinal/duration confusion; birthday reset; annual COM repainting months;113 falsely matching 11/13 by substring |
|Date boundary and uncertainty cases|July 1 journal given age 19; July 17 windows overlapping; DST/UTC date confusion; unknown time producing houses; approximate inputs reported as exact |
|Timing exposure ledger|Only selected favorable passes retained; ages 13-15 hidden; degree date confused with transit ingress; July 1 forced into a widened Chiron conjunction window |
|Claim-to-evidence audit|A source meaning becoming known biography; a new thematic bridge becoming an established equivalence; adult workplace wording inserted into child reading |
|End-to-end local review|Calculate -> ordered packet -> select topic/year -> render reading/explanation -> JSON export -> print. Review at desktop and narrow width; no validation claim from backend tests alone |

Keep the frozen trial fixture external and read-only; write test outputs in the new prototype test area. Run focused new tests and existing prototype regression checks, without invoking STAFFprofiler's rebuild hooks. Before review, confirm Git scope in the actual repository and preserve unrelated location/API and marketing work.

The definition of the next completed increment is **a working local research flow through R4, with traceable ordered assessments and reproducible annual numbers**, plus optional R5 geometry. A customer-ready full methodology report or deployment requires a later, separately authorized scope and the unresolved rule decisions; it is not claimed by this plan.
