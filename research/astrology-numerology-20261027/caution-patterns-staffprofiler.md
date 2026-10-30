# STAFFprofiler caution-pattern audit

Read-only inspection, 27 October 2026. Repository `olsonan26/STAFFprofiler`, branch `main`, HEAD `4172789db1034072f50c78178187e839fa710fb5`. Tracked worktree was clean. Existing untracked marketing work, captures and fixtures were preserved. No product code, engine, test or UI was modified. No build or test suite was run. Read-only calls imported the already compiled calculation module to check concrete outputs.

## Coverage and provenance

Inspected the complete annual, monthly and compound-trail core files; their product adapter; compiled calculation module; runtime indicator, pressure and marker modules; deployment file manifest; report category maps and resolver; period-report routing; relevant tests as source; retained LFS reference UI; and saved alert/editorial verification documents. Searched relevant code and catalogues for danger, warning, caution, careful,49/94 and11/13/16. This is not a new audit of every original Vaughan document or a claim of validated predictive outcomes.

`vendor/lfs/source-manifest.json` pins eight calculation sources to `olsonan26/LFS-SOFTWARE@463d8919faae0210a47eb16395285652c247b993`. All eight local source SHA256 values were independently checked and matched their manifest. The retained `vendor/lfs/reference-ui` is reference material, not a second production warning engine. The catalogue source comment identifies the user-authorized Peter Vaughan Staff Profiler editor collected9October2026; the editorial audit preserves original-versus-corrected text hashes and paragraph structure. Those facts establish recorded provenance, not independent prediction accuracy. [Source manifest](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/vendor/lfs/source-manifest.json), [vendor README](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/vendor/lfs/README.md), [catalogue source](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/report-descriptions.js#L1-L3), [editorial audit scope](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/docs/report-narrative-review.md#L1-L11).

## Exact calculation rules

| Field | Actual implemented calculation | Source lines |
|---|---|---|
| CY | Digit sum of visible calendar year, then full reduction trail | annualEngine82–87 |
| PY | Birth day + birth month + CY.root; preserve raw and trail | annualEngine90–98 |
| ESS / displayed PYE | Sum full alphabet ordinals A1…Z26 of active name-cycle letters | annualEngine101–110 |
| Annual COM | ESS.raw + PY.raw; not a concatenated pair and not simply root+root | annualEngine114–121 |
| PM | PY.root + reduced CM; Jan–Sep1…9, Oct–Dec1…3 | monthlyEngine16–30,82–90 |
| PME | ESS.root + PM active; use PM.raw if its authentic trail includes a canonical power, otherwise PM.root | monthlyEngine98–107 |
| MCOM | PME active + PM active; retain PME.raw only if exactly11,22or33, otherwise PME.root; PM follows its canonical power carry | monthlyEngine118–129 |

Pinned source: [annualEngine](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/vendor/lfs/core/lettrology-engine/annualEngine.ts#L81-L121), [monthlyEngine](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/vendor/lfs/core/lettrology-engine/monthlyEngine.ts#L77-L129).

Annual storage is by calendar year. For non-January births the engine uses prior-age letter selection for that calendar state; the birthday leaf display does not move the state boundary. Monthly calculation records span first-of-month to first-of-next-month; ends are exclusive. The adapter supplies the actual next annual state for December crossover. [Annual age selection](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/vendor/lfs/core/lettrology-engine/annualEngine.ts#L162-L182), [adapter](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/engine-adapter.ts#L40-L49), [dated calculation records](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/pattern-indicators.js#L11-L24).

## Exact active warning and display rules

The active red-marker set is **11,13,16**, occurring as complete numeric stages of the actual reduction trail. A root2 is not evidence for11, root4 is not evidence for13, and root7 is not evidence for16. A substring is not a stage:113→5 has no11/13 marker.22and33 can be retained operands in one formula but are not red markers. [Core reducer](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/vendor/lfs/core/lettrology-engine/compoundTrail.ts#L19-L70), [runtime detector](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/pattern-indicators.js#L1-L9).

| UI element / signal | Actual trigger |
|---|---|
| Monthly red fill and source strips | PM, PME or MCOM has a complete11/13/16 stage |
| PYE top annual band | Annual ESS trail has11/13/16 |
| PY bottom annual red band | Annual PY trail has11/13/16 |
| PY bottom orange band | PY.root=9, unless its red band has priority |
| Annual COM own row | Its authentic compound can mark its own row; it does not repaint monthly fill or create a PYE/PY band |
| Yellow mirrored digits | Positive equal roots in any of the four ordered field pairs below, provided no monthly red signal wins |
| Green monthly fill | No monthly red and no yellow mirror |
| Birthday leaf shape | Calendar month at/after birth month; not a new arithmetic trigger |

The four mirrors are **PYE↔PY; PYE↔PM; PME↔PY; PME↔PM**. COM and MCOM do not create mirror pairs here. A yellow rule is not a claimed dangerous event. [Runtime annual bands](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/pattern-indicators.js#L27-L38), [monthly/mirror logic](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/pattern-indicators.js#L40-L56), [retained row correction](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/docs/timeline-alert-verification.md#L5-L15).

## Why4+9,49,94 and13must stay distinct

These examples were directly evaluated against the checked-in compiled reducer and monthly functions:

| Input or operation | Actual trail | Red compound marker |
|---|---|---|
| Standalone4 |4 | None |
| Standalone9 |9 | None |
| Raw49 |49/13/4 |13 |
| Raw94 |94/13/4 |13 |
| Raw113 |113/5 | None |
| Annual ESS.raw4 + PY.raw9 |13/4 |13 in COM |
| Annual ESS.raw13(root4) + PY.raw9 |22/4 | No COM marker; ESS itself still has13 |
| PME with ESS.root4 and PM9 |13/4 |13 in PME |
| PME with ESS.root9 and PM4 |13/4 |13 in PME; field roles reversed |

**The pair label ESS4/PY9 is not the raw number49.** Annual COM uses raw operands, so equal root pairs do not guarantee equal COM trails. A genuine raw49 catalogue entry is selected only when49is an actual candidate value. Arithmetic addition is commutative for the examples above; interpretive roles are not interchangeable. Two unrelated chart values must not be concatenated or added merely to manufacture a power number. Existing source tests explicitly exercise both input orders through actual canonical sum functions. [Operand/marker records](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/pattern-indicators.js#L12-L24), [pair source tests](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/tests/timeline-alerts.test.mjs#L25-L34).

## The caution wording is real stored catalogue content

There is substantive authored caution text, not just generic colored cells. But the meanings depend on **category plus selected number**, and different catalogues can retain different detail:

- Main Essence11 discusses losses through rushing and overlooked detail; Essence13discusses care and avoiding risk; Essence16discusses recurring unresolved issues and reframes the period as improvement. Main Essence49and94alias the13text. [Main catalogue](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/report-descriptions.js).
- Main Personal Year13has explicit caution/risk evaluation and unexpected-event language; Personal Year16has evaluation/caution language. These are source interpretations, not established accident probabilities. Main Personal Year49is a distinct entry rather than merely the13alias.
- Compact Mini PY11contains vigilance about new and unexpected matters; Mini PY49stresses risk evaluation and caution; Mini PY94stresses not taking excitement for granted. Those49and94texts are distinct. [Compact PY11](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/compact-report-descriptions.js#L884), [PY49](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/compact-report-descriptions.js#L922), [PY94](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/compact-report-descriptions.js#L967).
- Compact Mini ESS49and94are distinct; the same is true for Mini COM49and94. This means a shared13marker does not justify erasing raw-compound narrative distinctions. [ESS49](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/compact-report-descriptions.js#L698), [ESS94](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/compact-report-descriptions.js#L743), [COM49](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/compact-report-descriptions.js#L810), [COM94](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/compact-report-descriptions.js#L855).
- Compact monthly PM11and13contain clear care/vigilance or unexpected-change themes. PM49and94also have caution text, but ordinary PM arithmetic is bounded2…18, so their existence in the reference catalogue does not make them naturally reachable runtime PM values. [PM11](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/compact-report-descriptions.js#L1117), [PM13](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/compact-report-descriptions.js#L1119), [PM49](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/compact-report-descriptions.js#L1155), [PM94](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/compact-report-descriptions.js#L1196).

The resolver selects the **raw number first**, then actual trail stages, then the root. It does not replace all matching compounds with one root interpretation. Annual full reports use Essence/Personal Year/Combiner; period cards use compact Mini categories; monthly cards use PME/PM/MCOM categories. The two routes must be named when comparing text. [Resolver](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/person-report.js#L36-L55), [period routes](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/report-periods.js#L6-L26).

Not every13entry contains the same alarming wording. For example compact Mini ESS13and MCOM13can discuss working well and applying practical effort, while the broader Personal Year13text is more cautionary. Therefore red13must not be translated into one invented universal “danger” interpretation.

## Runtime versus retained drafts

The shipping file list and runtime imports use `pattern-indicators.js`, `chart-markers.js` and `pressure-index.js`. They do **not** ship the separate `pattern-pressure.js`/`pressure-view.js` draft. The active index gives red people33.33%,66.67%or100% according to the number of active PM/PME/MCOM channels; yellow is25and green0. Annual PYE/PY/orange bands remain separate context. The unintegrated draft instead assigns highest severity across annual and monthly signals, including orange65. These are different models, and draft tests do not establish shipped behavior. [Build file list](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/build.mjs#L7-L13), [runtime pressure model](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/pressure-index.js#L1-L44), [documented discrepancy](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/docs/report-narrative-review.md#L13-L19).

The core also calculates annual root-mirror intensification,9→1reset, birthday lapse(currentPY.raw+next-ageESS.raw), and month crossover(current activePM+next activePME). Copied LFS reference UI can show these. STAFFprofiler's main monthly indicator and pressure records do not consume them as extra red monthly channels. [Annual diagnostics](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/vendor/lfs/core/lettrology-engine/annualEngine.ts#L183-L223), [month crossover](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/vendor/lfs/core/lettrology-engine/monthlyEngine.ts#L172-L208), [reference UI options](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/vendor/lfs/reference-ui/src/components/StudentTimeline.tsx#L193-L209).

Daily mode is a presentation of the parent month's calculation at each date. `charts.js:45–51` selects day dates, then looks up their year/month and calls the same monthly indicator; no independent daily arithmetic is called. The unintegrated draft explicitly refuses daily datasets, but that refusal is not the active Daily screen's behavior. [Actual date-to-parent-month path](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/charts.js#L45-L51).

## Concrete checked runtime example

The existing fictional sample Oliver Lewis, birth12December1981, produces2026PYE21/3, PY25/7, COM46/10/1. Read-only direct execution of the checked-in compiled module returned:

|2026month|PM|PME|MCOM|Monthly result|
|---|---|---|---|---|
|January|8|11/2|19/10/1|Red; PME only;33.33%|
|April|11/2|14/5|16/7|Red; PM+MCOM;66.67%|
|May|12/3|6|9|Yellow mirror;25%; no red compound|
|June|13/4|16/7|20/2|Red; PM+PME;66.67%|
|July|14/5|8|13/4|Red; MCOM only;33.33%|

This verifies existing module behavior for a fixture and selected periods. It does not verify the deployed UI or a real person's circumstances. The retained source tests and alert verification contain the twelve-month expected table. [Existing fixture and fixed table](https://github.com/olsonan26/STAFFprofiler/blob/4172789db1034072f50c78178187e839fa710fb5/tests/timeline-alerts.test.mjs#L7-L23).

## Integration implications

Preserve field roles, raw operands, complete trails and category-specific source prose. Keep four separate ideas visible: a raw compound, an ordered pair of chart fields, a computed sum, and an interpretive catalogue entry. Across systems, audit formula differences before mapping any warning: the copied LFS engine's annual COM is raw+raw and its ESS is active-letter ordinals; another app's reduced-digit essence or combiner is not automatically the same quantity. Author-catalogue caution content can be retained as attributed symbolic guidance, while an empirical association with actual events would require a separate study.
