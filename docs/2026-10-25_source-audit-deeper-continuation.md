# Source audit: 150 additional images after the 100-image checkpoint

This checkpoint supersedes the earlier 312-image checkpoint. The source audit remains incomplete. The 462 targeted images have selected passages or diagrams inspected; they have not received exhaustive semantic approval. No answering layer, chart formula, UI, access control or deployment was changed.

| Stage | Previous checkpoint | Current checkpoint | Added here |
|---|---:|---:|---:|
| Retained IDs acquired and hashed | 1,029 | 1,029 | 0 |
| Successful OCR outputs | 1,028 | 1,028 | 0 |
| Targeted image reviews | 312 | 462 | 150 |
| Selected atomic assertions | 128 | 170 | 42 |
| Hash-bound line annotations | 181 | 331 | 150 |
| Image-checked OCR locators | 3,500 | 4,977 | 1,477 |
| Named findings retained | 19 | 26 | 7 |
| Files without targeted review | 717 | 567 | -150 |
| Unchecked OCR locators | 30,526 | 29,049 | -1,477 |

All 34,026 OCR locators remain in the ledger. Lexical comparison categories remain 16,394 automatic match candidates, 3,312 partial candidates and 14,320 without qualifying matches; these are not semantic correctness or omission counts. The severely blurred IMG_5036 remains the one failed OCR item. No completed acquisition or OCR was repeated.

Thematic inventory remains 131 records; requirements remain 207 across 18 sections: 116 source found but implementation missing, 87 source incomplete and four contradictory. All 18 sections remain unready. A named finding is not the same unit as a requirement disposition. Additional source context does not automatically complete a requirement or enable an interpretation.

## Durable evidence

Three exact-ID batches, each containing 50 previously unreviewed images, are saved in:

- `evidence/source-pipeline/axis-audit-import.json`: templates, articulation, Quinconic Flow, STQ, return phases and first synastry context; 15 assertions.
- `evidence/source-pipeline/relationship-audit-import.json`: asymmetric synastry, composites, election/horary, Earth activations, retrograde stages and eclipse conditions; 15 assertions.
- `evidence/source-pipeline/lunar-depth-audit-import.json`: node models, remaining eclipse context, MC/IC, AC/DC, Vertex/Invertex, Axial Flow and nonagesimals; 12 assertions.

Each inspection includes file ID, image SHA256, OCR-output SHA256, visually read printed header, selected OCR line ranges, applicability and limitations. The canonical declarations remain `source_review_batch_notes.tsv`, `source_assertion_additions.tsv`, `source_line_annotations.json` and `source_blocker_findings.json`. Generated manifests, assertions, requirements and line queues are rebuilt from those declarations. Raw photographs, OCR text and local indexes remain in ignored `reference/`.

The public import files provide exact source identity; filenames are labels, not printed page numbers. Headers were inspected on the images. Diagram checks are bounded: topology, selected glyphs or worked coordinates are identified in the observations; a targeted record does not approve every coordinate on that page.

## Discoveries and retained limits

1. **Templates and Articulation:** printed 462-467 explicitly describe Rising Sign templates as foundations before planets, rulers, aspects, progression and relocation, rather than twelve fixed personality types. Printed 464 distinguishes H4 feeling language and H12 absence/unknown language. Assertions `templates462-foundation-scope` and `articulation464-word-choice` preserve those restrictions.
2. **Quinconic Flow:** printed 472 gives the image-grounded sequence `1 → 6 → 11 → 4 → 9 → 2 → 7 → 12 → 5 → 10 → 3 → 8 → 1`. OCR mangles its arrows and digits. This is an ideal house framework, not proof that actual bodies aspect each other or a fixed event timetable. See `quinconic472-house-sequence`.
3. **Sextile Threading and STQ:** printed 478-481 separate odd/even house rings. Printed 483, 485 and 486 give STQ chains 1-4-8-1, 2-5-9-2 and 10-1-5-10. The author explicitly rejects isolating those patterns from the rest of the chart; printed 484 proposes Planet B of the Square as an interpretive entry point. Actual aspect geometry and OOI remain required.
4. **Frozen return charts versus current transits:** printed 518 defines conjunction-to-semi-sextile and subsequent sextile phase boundaries; 519 retains retrograde Venus in the frozen phase chart despite its changed current motion. Printed 520 separates current transits from resonance-chart context. Thirty days remains approximate, with exact event/re-entry/location/equality rules unresolved.
5. **Printed notation conflict:** 524 defines N=natal, T=transit, P=progressed and R=relocated. Printed 528 says Transit=P while its own examples use T. Finding `notation524-528-transit` preserves both. Contact labels also vary in natal-first/transit-first order despite prose claiming Transit Vantage.
6. **Transit-only Pluto exclusion:** printed 527-528 uses transit Pluto 1:24 Aquarius with Jupiter 0:47 Scorpio (37 arcminutes off square) and Uranus 1:50 Sagittarius (26 arcminutes off sextile). MC/IC 3:25 is 2:01 away, beyond the stated 1:30 reach to 2:54. The source explicitly rejects extending natal Mars activation through Pallas 3:57 using natal OOI. See `pluto528-transit-only-exclusions`; label direction remains preserved separately.
7. **One-way synastry is explicit:** printed 543 says Venus may square another person's Pluto at a 4° offset without Pluto squaring back, comparing transit Moon's 3° OOI with a Jupiter 8° away. This is cross-ecosystem context; exact-contact equality and role-reversal examples 334-338 remain scoped to within-ecosystem examples. Receiving a response does not prove reciprocal emitted contact.
8. **Separate chart identities:** printed 535 lists eight synastry charts and 536 adds current transits. Printed 548-550 separates composites from Davison time/place midpoints and actual event inception charts. Printed 556 distinguishes a question/decision chart from actual book inception. These passages do not provide complete pairing, midpoint, progression or inception algorithms.
9. **Personal Earth Activation definition recovered:** printed 563-564 supplies moment/location Ascendant context and exactness, beyond the compiled PDF fragment. Reference frame, aspect set, tolerances and polar handling remain incomplete; no point OOI or guaranteed event result is enabled.
10. **Four motion stages:** printed 569 defines Pregrade, Retrograde and Postgrade using the future end and original start degrees; 575 distinguishes three non-retrograde stages. Printed 576 alternates Prograde/Postgrade paragraph subjects and says Neptune/Pluto never go Prograde. Keep the categorical statement and ambiguity without promoting a model-independent classifier.
11. **Later node qualification found:** printed 607-608 explicitly says True Lunar Nodes can occasionally move direct, distinguishing Mean Nodes. This qualifies the unqualified always-retrograde statements on 567/571/572. Printed 609 gives mean 14:35 versus true 13:28 and emphasizes order. Finding `nodes607-true-direct-qualification` retrieves both the general wording and exception. Printed 600-601 separately supplies non-opposite planetary-node context with unspecified observer/model conventions.
12. **Two eclipse-table conflicts:** printed 595 uses South Node for Southern Solar categories, while 596 names North Node in the Fringe Southern Solar row. Printed 596's True Lunar rows use the node conjunct Moon, but Forced/Fringe Lunar rows use node conjunct Sun at Full Moon, conflicting with the stated Moon-side categorization. Both branches remain stored and unapproved. The source's 3°/10°/13° taxonomy remains separate from astronomical eclipse detection; no astronomical eclipse is relabeled physically absent.
13. **Anchors and geometry:** printed 626-640 distinguishes MC/IC from zenith/nadir and whole-sign H10/H4 cusps, and horizon/ecliptic AC/DC from due geographic East/West. Printed 648 describes spatially perpendicular prime vertical and meridian; that does not imply their ecliptic intersections are always 90° apart. Printed 658-660 supplies the qualitative MC → Vertex → IC → Invertex Axial Flow, with AC/DC action and response separately described.
14. **Additional counterevidence retained:** printed 630 explicitly calls MC 3° Taurus a Capricorn degree and “my Spark,” adding context without choosing between earlier sign/house rules. Printed 652/656 says a person's planet **or point** can aspect another person's Vertex/Invertex; 657 uses Vertex-to-Sun wording. These remain linked to receiver-only anchors on 645 and qualified internal alignment on 653, without inventing an outgoing point OOI.
15. **Nonagesimal worked coordinates:** printed 662 distinguishes the highest ecliptic point from MC/zenith; 664 distinguishes its lowest opposite. Printed Nona 13:06 versus Venus 14:47 differs 1:41; Subnona 13:06 Scorpio versus Ceres Rx 13:36 differs 30 arcminutes. The Venus/Ceres opposition is 1:11 off exact. None of these separations establishes universal point OOI.

All previous Spark, FCA/Mars, Pluto coordinate, Chiron, Eunomia, minor-angle, handoff/equality, territory, lunar-width and geographic-distance evidence remains. The two distinct photographs of printed315 remain distinct. Printed492 is still unlocated, not proven absent. Author anecdotes, psychological descriptions and prediction claims remain source claims, not independently validated personal facts or outcome evidence.

## Validation

Final evidence is `evidence/source-pipeline/continuation-deeper-verification.json` and `continuation-deeper-regeneration.json`. The expanded full regression run passed 335 Python tests, zero failures/skips, with the existing Starlette/httpx deprecation warning. The run covers the final 150-image declaration snapshot. Application, UI, access, test source, Vercel and Git attributes have no changes from starting commit `aeb0525e2415b9ae8f6eeab23f9afd9fd2d74f97`.

All existing line, source-pipeline, audit-retrieval, register, semantic, source and requirement validators passed. Rebuilding all six generated knowledge files reproduced identical bytes; 692 compiled PDF pages and 300 thematic witness pages retained their hashes. All 23 concept probes retrieved all 26 named findings plus requirement M08-04-01. A supplemental audit-focused run passed 48 tests, with the same existing warning and no failures/skips. Its first expanded run correctly rejected three probes assigned to incompatible sections; those probes were corrected to existing section contracts without loosening the contracts or removing evidence. An independent coverage check then found the return-notation finding lacked a selected probe; a return-phase probe was added. The verifier now explicitly fails if any named finding is absent from the retrieved packets.

These are provenance, consistency and audit-retrieval checks. They are not exhaustive semantic signoff, astronomy approval or production answering verification. No frontend build, application restart, deployment or personal answering layer was performed.

## Exact continuation

Continue on `codex/methodology-verification-20261024`, preserving the current checkout. Check Git status/diff first. The prior later user instruction authorizes publishing completed audit work on this branch; its automatic Vercel deployment guard remains disabled for this branch. Do not reset, switch branches or alter chart/UI/access behavior.

Use `evidence/source-pipeline/remaining-queue.json` for 567 files and `line-review-queue.json` for 29,049 unchecked locators. Already targeted pages also need deeper passage and diagram reconciliation. Neither queue measures complete semantic coverage.

The remaining targeted file queue is distributed as follows; do not mistake progress through the current chapter sequence for coverage of the earlier batches:

| Source batch | IDs still without targeted review |
|---|---:|
| BATCH 1 | 56 |
| BATCH 2 | 66 |
| BATCH 3 | 73 |
| BATCH 4 | 31 |
| BATCH 5 | 79 |
| BATCH 6 | 1 |
| BATCH 7 | 39 |
| BATCH 8 | 222 |

That is another 6-12 batches of 50-100 images merely for a first targeted pass over the remaining files, followed by deeper reconciliation across reviewed and unreviewed pages. It is not an estimate of semantic completion or a time estimate.

The next recommended file in the current chapter sequence is **IMG_5261.JPG**, exact ID **1s5nQxujY3JxHuCHdzXfoVvnheB9RJ6a3**, image SHA256 **943dac4136607af2cbd0f3ed910823133530f05724307bff949e666cbd8c40ed**, OCR SHA256 **f41326543c40a32b65725c9a1e6d9c0c2355e4cd68a86429f704b0f3b6c0b39b**. Its printed header has not yet been visually inspected. Exact pending locators and pending numeric/glyph priorities are in the verification artifact. Inspect the image before naming its printed page or asserting content.

Continue a substantial batch from exact pending IDs, then deepen the numeric/glyph, negation and diagram checks across already targeted pages. Reconcile eclipse node/reference-body conflicts, point-emission scope, phase/re-entry endpoints, planetary-node frames and remaining original492 uncertainty. Save exact witnesses and competing branches; do not enable unresolved formulas. Run the continuation/manifest/inventory/assertion/requirement builders sequentially, reconcile the ledger, validate and update this checkpoint with fresh counts.
