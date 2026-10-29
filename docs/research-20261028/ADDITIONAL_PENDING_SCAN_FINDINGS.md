# Four additional pending scans: consultation context and an unindexed term

28 October 2026, America/Denver. This supplements the initial deep audit while the private source-recovery upload is running. The four original images below received complete-page visual inspection and SHA256 verification against the current source manifest. Their canonical manifest statuses remain `NOT_REVIEWED`; this separate record does not silently update the canonical counters or grant runtime approval. The initial three reviews inspected 14 distinct originals; these four bring the session's distinct targeted original-image count to 18. This remains targeted review, not a full book reread.

## Witness identity

| Printed page | Original filename | File ID | SHA256 |
|---|---|---|---|
|209, Layering|`IMG_4630.jpg`|`1EFQFt-Q6VOBbB6D9zI6IvaIDgeFYEz7Z`|`ad4862928b146e83450a0bb1c92a3362855369329c93737ab891f5967d97a843`|
|290|`IMG_4720.jpg`|`1mQT4-IIMXH1XWd4F8QDJrO_qC3ssNMMS`|`4c5556eb0e67296a4912e217aeac3bf3b80945e482dbf53959d3548828143ec7`|
|299, Fusion Cusp Areas|`IMG_4731.jpg`|`1vbfmauH6HhR8Ii44p65buRbH-4Cmy3_M`|`56a394e1e35190b0db378e789f9f7d581189032af8382d4b079fd69399ac85e9`|
|ae, Alchemystic Lexicon|`IMG_5683.JPG`|`1jxm2vIrsKoWvlCBM8hVXPTbbWnJdrDOu`|`4a02de7a6340aafeb71aa936af88e897cd337726979a022bc25e14a901ce9cd6`|

Paths resolve to `reference/originals/<file_id>.jpg`. The originals and candidate OCR are included in the private recovery snapshot even though these new observations are saved separately in Git.

## Newly located semantic gap: Velocity Focus

Lexicon ae explicitly names **Velocity Focus** and describes a point of maximum acceleration in a planet's motion, with an accompanying claim about heightened influence. Searches of all five canonical semantic authorities below found zero occurrences of `velocity focus`, `velocity-focus`, `acceleration` or `peak potency`:

- `data/knowledge/interpretive_inventory.json`
- `data/knowledge/original_assertions.json`
- `data/knowledge/source_blocker_findings.json`
- `data/knowledge/capabilities.json`
- `data/knowledge/material_requirements.json`

This establishes an omitted named source concept within those five registers, not absence from every raw OCR line or private archive. The scan was acquired, and its OCR was available; acquisition/searchability did not make its meaning part of the selected concept/assertion/requirement register.

Do not replace this with maximum speed, a retrograde station, exact angular contact or a generic transit peak. Acceleration is distinct from signed longitude speed. The entry does not specify the measured coordinate/frame, derivative/time scale, search window, whether magnitude or signed acceleration is maximized, or how the proposed strength relates to contact/OOI eligibility. Its influence claim is an author assertion, not empirical validation or an executable forecasting rule.

Next source work: locate the full explanatory passage and numerical examples, retain any maximum-speed versus maximum-acceleration variation, define what is actually calculated, and add a source-bound concept with explicit dependencies and limitations. The current `mystic_rebels/gradity.py` station/shadow calculations and `apps/common-ground/phsr.py` geometry do not implement this named technique. A future current-situation view should not label an arbitrary sampled date as its Velocity Focus.

## A question needs more than a single topic house

Printed 290 explicitly expands a relationship inquiry beyond H7: include its actual ruler, the actual Libra sector, Venus, and the actual Taurus sector because Venus carries both sign contexts. These must be located in the person's chart; Taurus and Libra sectors are not fixed H2/H7 positions for every Ascendant. The page also calls for directed Energy Flow and contextual interpretation rather than assuming that a relationship indicator opposing Venus explains itself.

Implementation consequence: a question planner may choose a starting topic, but it must then carry applicable ruler/sign-house dependencies and relevant occupants. It cannot substitute a rigid mapping such as relationship -> H7 -> one paragraph. This reinforces the existing need for complete Delegate payloads and receiver condition; it does not authorize a new universal Venus outcome rule or create a physical aspect merely from shared rulership.

`apps/common-ground/phsr.py` already lists both ruled signs and their occupants for Venus/Mercury. That structural progress should be reused. Its `condition_complete=False` remains accurate because most occupants do not have complete assessments or directed relationships. A listed occupant is not a completed contextual evaluation.

## A repeated ruler is a graph reference, not a hierarchy

Printed 209 distinguishes the author's Delegate method from a simple Planet -> Sign -> Ruler chain. It requires collecting and assessing the contents of a ruled sign/house to understand the ruler's condition. It also explicitly rejects promoting an eventual self-ruled planet to a final ruler that dominates earlier topics.

The existing prototype's cycle termination and lack of strength multiplication are appropriate structural safeguards. A general answer still needs to assess the content carried by each Delegate. Do not close a repeated route by inventing a controlling planet, a final personality label or confirmation from repeated nodes. The remaining page text continues onto the next page; this review does not reconstruct that continuation from memory.

## Cusp context is bilateral, while the existing helper is approaching-only

Printed 299 describes both late-sign blending toward the next sign and residual prior-sign influence just after entry. It gives approximate sign limits of 28.5 degrees and 1.5 degrees. This reinforces already retained canonical evidence: `source_blocker_findings.json` includes bidirectional scope, and `original_assertions.json#fca-after-boundary-interamnia-original` preserves a post-boundary example.

`web/src/phase10Research.ts#approachingFusionCusps` deliberately reports only approaching proximity and leaves `after_boundary_strength=null`. That is an honest partial diagnostic, not the whole source technique. The PHDDASR sign/decan assessment currently lacks a contextual FCA layer. Source review should distinguish presence/distance on each side from a numeric blend strength, ownership/equality conventions, retrograde handling and the unresolved degree-scale threshold example. None of those missing details is supplied by simply drawing a gradient.

Keep actual longitudes and astronomical sign/house classification unchanged. A contextual overlay is distinct from moving a plotted object or replacing its primary sign/ruler. This page alone does not establish numerical weights, every scale, endpoint ownership or a complete implementation.

## Relation to the saved audit

These observations extend [the deep audit](DEEP_AUDIT_AND_NEXT_STEPS.md) and its question/current-sky implementation priorities. They strengthen the distinction between missing source material, an unindexed source term, and stored but unimplemented contextual rules. The canonical 304-file pending queue and 725 targeted-review count remain unchanged pending deliberate reconciliation of review registers.
