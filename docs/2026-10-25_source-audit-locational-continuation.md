# Locational source audit: 50 new images and three reinspections

This checkpoint supersedes the 512-image checkpoint for local audit progress. It adds 50 previously unreviewed file IDs from the exact saved queue, three reinspections, 16 selected assertions and 53 hash-bound annotations. No completed acquisition or OCR was repeated. Reviews cover selected headers/passages/diagrams; they are not exhaustive semantic approval.

| Stage | Previous | Current | Added here |
|---|---:|---:|---:|
| Acquired and hashed IDs | 1,029 | 1,029 | 0 |
| Successful OCR outputs | 1,028 | 1,028 | 0 |
| Targeted image reviews | 512 | 562 | 50 |
| Selected assertions | 182 | 198 | 16 |
| Hash-bound annotations | 386 | 439 | 53 |
| Checked OCR locators | 5,859 | 6,842 | 983 |
| Named findings | 29 | 33 | 4 |
| Files without targeted review | 517 | 467 | -50 |
| Unchecked OCR locators | 28,167 | 27,184 | -983 |

The denominator remains 34,026 OCR locators, not a semantic coverage denominator. Inventory remains 131 thematic records and 207 requirements across 18 sections. All 18 sections remain unready: 116 requirements have source found but implementation missing, 87 have incomplete source, and four remain contradictory. One severely blurred image remains unreadable. Printed 492 remains unlocated, not proven absent.

Durable batch receipt: `evidence/source-pipeline/locational-next-audit-import.json`. Final verification: `locational-next-verification.json` in the same directory. Canonical declarations remain the two authored TSV files, line annotations and named findings under `data/knowledge/`; the existing builders regenerate derived files. Private photographs, OCR, contact sheets and working helpers stay under ignored `reference/`.

## Concrete findings

1. **Full profile context precedes line interpretation.** Printed 790-791 requires Delegate condition, the whole relocated chart, natal assessment within DCA and the person's reason for moving. Printed 813 supplies a worked chain: Capricorn Field → Aries Tone → ruler Mars → Cancer Field/Libra Tone → Apex role. These are useful report dependencies, not isolated keyword meanings. Printed 803 expressly says different aspects, sign, motion and Chiron context change the example's interpretation.
2. **Sky and zodiac frames remain separate.** Printed 788-789/823 distinguishes Zodio ecliptic projections from Mundo angularity for Parans and Local Space. Printed 796-797 separates HR/HS/AP/SA from zodiacal AC/DC/MC/IC conjunctions. Printed 805 says Parans are read after chart assessment while signs and houses still change expression. These are source conventions requiring independent numerical fixtures; the author's map critique is not itself validation of a projection.
3. **Paran imprint event window is unresolved.** Printed 808 retains natal imprint with new location Parans layered over it. It also describes first breath and an angular moment at birth, lists Sun-HR/Moon-AP and Neptune-HR/Saturn-AP, and acknowledges Sun/Neptune natal opposition. Finding `parans808-event-window` preserves the distinction between a possible instantaneous birth-sky reading and a diurnal event window. No selection epoch or tolerance was inferred.
4. **Explicit research limits.** Printed 798 defers Sky Quadrants and Parallels; printed 817 expressly calls its Visibility Spectrum an unproven theory. It proposes 0/90/180/270 roles and 45/135 midway points while leaving Paran window/inclination questions open. Finding `parans817-unproven-spectrum` prevents these proposals being treated as supplied operational rules.
5. **Paris role ambiguity.** Printed 818 says Venus is at Horizon-Setting and Subapex at the same time near Paris. Finding `paris818-dual-sky-role` retains both roles and the missing event/location window. It does not silently choose a role or create a same-instant numeric fixture. Country-based preferences and remote-activation anecdotes remain author claims, not facts about national groups, report subjects or empirical remote efficacy.
6. **Local Space activation scope.** Printed 828 qualifies physical travel as necessary and excludes remote activation of Local Space; printed 833 describes an online first contact along a Moon line before meeting. Finding `local828-physical-online-scope` retains the exclusion and anecdote without declaring a reconciled rule. Printed 829-830 defines azimuth clockwise from true north, requires recalculation at a new origin and preserves natal imprint separately. The recalculation epoch, point-altitude convention and event tolerance remain unspecified. Printed 833-835 distinguishes output from oppositional receipt; its accident and intimate anecdotes do not become personal predictions.
7. **Distance approximation deepened.** Reinspection of printed 822 confirms the approximation sign in 111 × cos(latitude) × orb and the Moon/Baltimore example 257.742 km/160.195 miles. Printed 821 supplies C(phi)=2piRcos(phi), which OCR omitted. Printed 823 gives Jupiter 8-degree OOI/427.22-mile reach with a 140-mile offset: 140/427.22 is about 32.770%, while 2.63/8 is 32.875%. Their agreement is approximate. This does not establish universal ecliptic-angle to ground-distance conversion or a complete perpendicular line-distance/intensity law.
8. **MC/Sun scope qualification.** Reinspections preserve printed 389's square and 390's semi-square wording. Printed 825 explicitly contrasts natal MC/Sun semi-square with a relocated Los Angeles square and corrects displayed Sun-square-MC to MC-square-Sun. This adds scope context to the earlier named finding without claiming an erratum or verified longitude fixture.
9. **Distinct photographs of printed 801.** IMG_5483 and IMG_5484 visibly reproduce the same layout/wording but have different IDs and image hashes. Both are retained in `source_visual_duplicate_groups.json`, alongside the earlier printed 315 group. File-ID progress does not imply distinct printed-page progress.

Printed 799's near-Hawaii screenshot shows Venus above the eastern horizon and Pluto below the western horizon; it is not an exact zero-altitude simultaneity fixture. Printed 824-827 requires directed non-conjunction line context, including AC-square-Mars, MC-square-Sun, Mercury-semi-sextile-AC and DC-quincunx-Mercury. No generic relocation ranking, personality diagnosis, injury forecast or income guarantee was added.

All previous Spark, FCA/Mars, Pluto, Chiron, Eunomia, sign/house wording, coordinate/diagram arithmetic, territory, synastry/equality, receiver-only anchors, lunar/solar scope, notation, eclipse, True Node, phase/re-entry, Spirit sign-error and Sedna label witnesses remain intact. Earlier source reviews and annotations were preserved.

## Report-building readiness and validation

See [PROFILE_REPORT_KNOWLEDGE_PATH.md](PROFILE_REPORT_KNOWLEDGE_PATH.md) for the durable path from source identities to meanings, assertions, applicability, dependencies, report requirements and retrieval evidence. Git stores reviewed knowledge and evidence; full originals/OCR/indexes are private under `reference/` and require restoration/hash verification on a fresh checkout. This session does not establish an independent private-asset backup.

Fresh regression: **335 tests passed**, zero failures/skips, in **107.06 seconds**, with the existing Starlette/httpx deprecation warning. Local socket access was used for TestClient based on the previously verified environment limitation. XML: `evidence/source-pipeline/locational-next-tests.xml`.

All six generated knowledge files rebuilt identically. Register, semantic, source, requirement, PDF witness, line, pipeline and retrieval checks passed. PDF identity remains 692 pages with 300 thematic witness pages. The retrieval verifier now includes a Local Space probe: **25 concept packets retrieve all 33 named findings**. Evidence is in `locational-next-regeneration.json`, `locational-next-verification.json`, `line-verification.json`, `stage-verification.json` and `evidence/source-continuation/retrieval-check.json`.

These establish source provenance, reproducibility, saved-state consistency and local audit retrieval. They do not establish astronomical correctness, complete semantic reconciliation or approved personal reports. No application, chart engine, UI, access control, frontend build, restart or deployment changed. The branch's automatic-deployment guard remains in place.

| Use | Current disposition |
|---|---|
| Preserve/retrieve these report conditions, limits and competing witnesses | Implemented in the audit data |
| Use source meanings in a cited personal report | Still requires validated chart-context selection and evaluated report synthesis |
| Calculate Parans, distance influence, Local Space and imprint behavior | Requires explicit conventions and independent numerical fixtures |
| Turn unproven Visibility Spectrum or anecdotes into report rules | Blocked; source limits remain explicit |

## Exact continuation

Stay on `codex/methodology-verification-20261024`; inspect root, branch, HEAD, status and diff first. Preserve current work. Do not reset, switch branches, redeploy or alter chart/UI/access behavior. Validated audit changes may be committed and pushed to the existing branch; keep its automatic-deployment guard.

Use the regenerated remaining queues: **467 files** and **27,184 unchecked OCR locators**. By batch: BATCH 1: 56; BATCH 2: 66; BATCH 3: 73; BATCH 4: 31; BATCH 5: 79; BATCH 6: 1; BATCH 7: 0; BATCH 8: 161. These are first targeted-review counts, not semantic completion.

Next recommended file: **IMG_5520.JPG**, exact ID **1FcEvd5j9w9xBfFPUSv_AsbNlYzrlZoT4**. Image SHA256: `9f39d418b2cd71ef1e4310a7c3902b13dcda3049f26dc4641543a031009dd683`. OCR SHA256: `ace601039b2c717e05de1c9ac07734cf46c6f1cacf03a4290b942491b0727eea`. Printed header is not yet visually inspected. Begin at pending OCR locator 1 after viewing the actual image; exact pending locators are in the verification and line queue.

Continue another 50-100 image batch and deeper numeric/glyph/negation/diagram work. Earlier batches also need first targeted inspection. Resolve neither the new event-window/role/activation-scope ambiguities nor earlier conflicts by assumption. Reuse declarations, rebuild sequentially and regenerate/validate both queues. No completed acquisition or successful OCR needs repeating.
