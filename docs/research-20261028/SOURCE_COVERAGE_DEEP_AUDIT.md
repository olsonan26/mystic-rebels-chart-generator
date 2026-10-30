# Source coverage and question-answering audit - 28 October 2026

This review inspected the existing `codex/phsr-numerology-integration-20261028` checkout at `392e808f03837359e990ce38a569aa1bc837788b`, current canonical JSON, indexed PDF text and selected original photographs. It preserves the existing calculation engine, location changes, source records and approval states. It does not claim an exhaustive rereading of 1,029 photographs or a complete visual review of the 692-page compilation.

## What is actually missing

The main bottleneck is the bridge from stored source knowledge to complete contextual answers. The sources are substantially more extensive than a small glossary: 131 thematic concepts, 267 selected original assertions, 609 image-bound annotations, 50 named findings and 30 worked examples are already retained. Much of this is not assembled into the chart generator's personal-question workflow. The newer Common Ground research app provides partial ordered assessments, but explicitly leaves degree and directed-aspect stages unresolved.

There are also genuine source gaps and contradictions. These must remain visible instead of being filled with conventional astrology. A useful bounded question interface can still explain calculated facts and reviewed source concepts while showing precisely which further conclusion lacks its required rule or chart layer. Whole-corpus completion is not a prerequisite to every source explanation; it is also not established by a successful source-integrity validator.

## Fresh coverage counts

Counts below were recomputed directly from current JSON, rather than copied from historical checkpoint documents.

| Stage | Current evidence | Remaining or limitation |
|---|---|---|
| Original acquisition | All 1,029 retained Drive file IDs acquired and hashed; every recorded local path exists | Snapshot completeness is not proof of every printed page, author version or provider revision |
| OCR | 1,028 candidate OCR outputs | One failed image: `IMG_5036.JPG`, ID `1k2vapbXeUl3-rEkgCLMkHHUDAplWztE8`; OCR is not approved transcription |
| Targeted visual review | 725 distinct file records have targeted original visual review | 304 files remain `NOT_REVIEWED`; the 725 were not exhaustively transcribed or semantically signed off |
| Header identity | 722 visual headers, three partially cropped/unknown | 304 headers still unknown in the manifest |
| OCR line checks | 10,245 of 34,026 OCR locators have targeted checks | 23,781 locators remain unchecked; checked lines are not a semantic coverage percentage |
| Scan/PDF mapping | Candidate overlap, omissions, diagram losses and conflicts retained | Complete scan-to-PDF reconciliation is false; printed-page denominator remains unknown |
| Concepts | 131: 91 passage reviewed, 20 fragment, 15 incomplete, three conflict, two prior-review only | Every canonical concept still records `runtime_interpretation=ABSENT` and `answer_use=NOT_APPROVED` for the main audited report engine |
| Atomic assertions | 267 selected original-source assertions | All remain `NOT_EXECUTABLE_NOT_RUNTIME_APPROVED`; these are a selected set, not an exhaustive atomic denominator |
| Report requirements | 207: 128 source found but implementation missing, 75 source incomplete, four contradictory | All 18 complete personal-report sections remain unready |
| Reusable vocabulary | 60 eligible vocabulary annotations and one explicit conflicting-alternatives output | These allow attributed/source-bounded use, not arbitrary personal conclusions |
| Calculation capabilities | 44 entries: 16 runtime implemented, four research helpers, 24 absent product workflows | Source and numerical status must be assessed independently |

Authorities: `data/knowledge/source_manifest.json`, `source_line_reconciliation.json`, `interpretive_inventory.json`, `original_assertions.json`, `material_requirements.json`, `capabilities.json`, `report_component_use.json`, `report_knowledge_manifest.json`. The review logs have 44 initial and 683 continuation records; those record counts are not the distinct-file review denominator.

Historical source documents retain older counts such as 148, 212, 312 or 462 reviewed images. Their retained history is useful, but those counts are superseded by the authorities above. The older claim that Flora, Ixion, Nessus and Sedna meanings are absent is also superseded: all four are now retained in `source_review_continuation.json` under `source_only_concepts`, with corresponding inventory/assertion material. Their complete contextual implementation remains separate.

## New finding: the reverse semi-sextile example has an unregistered house mismatch

Original printed **503**, `IMG_4964.jpg`, Drive ID `1G66MclE-HywwkLQYhFsZUYy79hwfu3M1`, was visually reinspected in this review. Image SHA256 is `e86a29c85221bc69c80d342481c383d1db2e99426bede175e909e3975466da7e`.

The page's scenario B changes the order to natal Sun toward transit Moon. The Sun is explicitly in H5 and the transit Moon in H6. However, item 3 still calls Planet A's territory H4. The diagram, first participant and item 2 establish H5; the H4 parenthesis conflicts with that context. OCR locators 21-24 preserve the mismatch; locator 27 gives the Moon's H6.

This inconsistency is not named in the current 50 findings, and the retained `directional-semisextile-sides-original` assertion does not include it in its exclusions. It is a newly identified source issue, not an author erratum. Do not silently replace H4 with H5 in a source quotation, and do not use the inconsistent row as an exact training or regression fixture. A later canonical audit update should retain both statements and require explicit editorial/source resolution.

The compiled PDF's indexed page 429 gives the end of the previous example followed by original 504's continuation, omitting the important scenario-B opening/diagram visible on original 503. The original review record currently gives only a candidate overlap to PDF428. A keyword overlap is therefore insufficient evidence that the complete reverse example survived the compilation.

## Source-supported answer mechanics that the workflow still needs

### Resolve the receiving context before giving practical guidance

Originals **327-328** were visually rechecked:

| Printed page | Drive ID | SHA256 |
|---|---|---|
|327|`1DJYlST1HmHQm66PHxI-YYxithXKzUr_c`|`21a6f8aebcdf9412ed386a9c91b7eaeb109e0472234f5dbf8e3dc4f758070947`|
|328|`115KNB-fn2Fscix48_It1-vJ1fWA0qlrA`|`8e63022ce04cb644e62cc0e80840efce05ffcbe3506f8afcc9a376d52590dcea`|

The existing assertion `resolution-planet2-context` already retains the dependency: resolve the second participant's placement, ruler and other aspects before choosing how the first participant might adjust. Original 328 OCR locators 3-5 are a precise entry point. Source terms such as problem/solution are interpretive roles, not blame assigned to a person.

Consequently, a question response cannot be completed by looking up two planet keywords and a symmetric aspect label. It needs both participant assessments, actual direction, the receiver's context and its dependencies. `apps/common-ground/phsr.py` currently returns `directed_aspects=[]`, `condition_complete=False` and `complete_phsr=False`; nearest 15-degree geometry is explicitly diagnostic. This is a real missing implementation layer despite the assertion being present in the knowledge package.

### Keep transit reach, reading perspective and pass-through context separate

Originals **524**, **527-529** were visually rechecked. Their existing assertions and conflicts should travel together into retrieval:

| Printed page | Drive ID | Relevant retained evidence |
|---|---|---|
|524|`1aFoxChho5j7dj-GMGUkidODLqPGXALHB`|Defines N natal, T transit, P progressed and R relocated; discusses concurrent luminary phases and explicitly imagines an AI app handling them |
|527|`12lXSBzEIhp7NxkfFOjqtc3sZhTwLHd_R`|Transit Pluto at Aquarius 1:24; use transit reach and ignore natal OOIs for this transit example |
|528|`1cdlqjMOMt8CH_d50FRrKEgi9FMmU1zwl`|Transit-only reach; excludes a natal Mars/Pallas chain and distant MC/IC contacts; printed notation/participant-order inconsistencies remain |
|529|`16X_vBAGPCFUDewnpWY2k9w54ffO9x_NA`|Distinguishes secondary thematic house/occupant presence from primary ruler activation |

The source's numeric example separates offsets of 37 arcminutes to Jupiter and 26 arcminutes to Uranus from the excluded MC/IC offset of 2:01. Its Pluto reach ends at 2:54, based on the example's 1:30 reach. These establish that example's arithmetic and exclusions, not a complete universal OOI policy. The Moon at Aquarius25:57 is in the same house but has no direct conjunction to Pluto1:24. Its thematic relevance is a different relationship type.

Existing assertions `notation524-528-transit-conflict`, `pluto528-transit-only-exclusions` and `pass529-secondary-ruler-layer`, plus findings `notation524-528-transit` and `pluto528-transit-order-labels`, preserve these limits. Do not add natal and transit orbs, infer a reciprocal physical emission from a reverse reading perspective, extend a contact through a natal intermediary, or turn thematic presence into a direct aspect. The word secondary does not provide a numeric dilution factor.

A complete question workflow therefore needs distinct records for: current sky condition, direct transit-to-natal contact, natal receiving response, pass-through/ruler context, and concurrent unconnected context. `with-while` explicitly preserves simultaneous influences without inventing a causal or fused relationship. A filtered list of selected exact contacts is useful astronomy, but does not cover all five lanes.

### Preserve chart-layer scope

Original **505**, ID `1zb5BJnnHFPrkxCJGVWIQuQrRQia3olp4`, SHA256 `29d13d13189e96df7a171855a7ed6c5971a16b39e2bda3cb848b2e745ba56fd9`, was visually rechecked. It calls for the inner, static and outer chart layers with transits to them. The same page identifies the natal chart as the starting point for standard questions. It does not supply the missing progression epoch or angular algorithm.

A first natal-plus-current-sky question feature can be useful when that limited scope is explicit. It must not describe itself as the complete Dynamic Chart Approach. Do not substitute Solar Arc or an arbitrary secondary-progression convention for unresolved source methods. Printed492 remains unlocated in the retained snapshot; absence is not established.

## Priority gaps for PHDDASR and current situations

The seven-stage order is supported in compiled PDF283: Planet, House, Degree, Decan, Aspects, Sign, Ruler, returning to a planet. Sign is identified early as computational/context input while the interpretation flow preserves that order. The source uses several acronym spellings; a display name should preserve the explicit expanded stages rather than infer a new method from spelling alone.

| Priority | Gap | Concrete completion evidence |
|---|---|---|
|1|Ordered context assembly|Selected topic/question maps to explicit chart facts; all seven stages have values or precise missing-rule statuses; sign-ruler recursion and cycles retained|
|1|Receiver and Delegate condition|Both sides' placements, rulers, occupants, direct/delegated retrograde context and relevant connections included before resolution text|
|1|Directed aspect/OOI decisions|Complete per-body reach policy, cross-ecosystem rules, phase/equality conventions and source conflicts resolved or explicitly scoped|
|1|Question contract|Question, person/chart version, event/current interval, time zone, known history and requested topic recorded distinctly; user context never becomes chart-derived evidence|
|1|Actual current-sky workflow|Fresh timestamp, independent transit chart, personal overlay, both contexts, current house/ruler path, direct versus thematic versus concurrent records|
|2|Exact event timing|Orb entry, exact roots, repeat passes, station/tangency handling and exit represented separately; sampled dates never called exact peaks|
|2|Source citation path|Answer claims link to the actual source subset, including exclusions and counterevidence; source counts do not rank importance|
|2|Degree/Spark and FCA|Preserve conflicting sign/house procedures and threshold counterexamples; no canonical selection by silent majority vote|
|3|Complete dynamic layers and returns|Progression epoch/angles/year units, relocation policy, return phase/re-entry equality and natal coupling rules specified|
|3|Remaining review queue|304 unreviewed images and 23,781 unchecked OCR locators, prioritized by missing dependency and diagrams/numeric/negation content|

Relevant canonical requirements: `M01-01-01` (ordered assembly), `M01-05-01` (dialogue/known facts), `M05-01-01` through `M05-06-01` (OOI/relationships), `M12-01-01` through `M12-05-02` (current sky), `M13-*` (timing), `M14-*` (dynamic layers), `M15-*` (returns). Consult the actual requirement row for its required chart facts and dependencies, rather than this short index alone.

## Report section reconciliation

| Section | Source found / implementation missing | Incomplete | Contradictory |
|---|---:|---:|---:|
|Foundation|38|0|2|
|Planet condition|5|0|0|
|House condition|5|0|0|
|Retrograde profile|4|0|0|
|Relationships graph|3|8|1|
|Life purpose|11|0|0|
|Parts|6|1|0|
|Lunar context|6|2|0|
|Declination|3|1|0|
|Pattern resolution|6|0|0|
|Asteroid detail|26|30|1|
|Current sky|5|2|0|
|Timing|0|6|0|
|Dynamic layers|0|5|0|
|Return phases|0|5|0|
|Synastry|6|5|0|
|Locational|1|5|0|
|Special contexts|3|5|0|
|Total|128|75|4|

These are the canonical main-engine requirements, not a claim that the separate Common Ground research app implements nothing. Conversely, Common Ground's partial assessment does not close all these rows merely by existing.

## Reproduction and limits of this review

This review used read-only JSON aggregation, local-path existence checks, SQLite queries against `reference/knowledge-index.sqlite`, source/code inspection and eight selected original-image reinspections: printed327,328,503,505,524,527,528,529. No full corpus download, OCR rerun, source approval change or chart/runtime edit was performed. Existing canonical review counts were not incremented for these reinspections.

The canonical validators/export check are being executed by the coordinating audit, not duplicated here. The findings above distinguish observed source text, retained prior review metadata, actual current code and implementation proposals. Original photographs/PDF/OCR/index content remains private/local; this report contains bounded analytical summaries and source identifiers rather than a replacement transcription of the book.
