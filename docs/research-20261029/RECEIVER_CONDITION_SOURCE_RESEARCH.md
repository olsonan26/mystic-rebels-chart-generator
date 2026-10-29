# Receiving condition, rulers and Delegate payloads

29 October 2026, America/Denver. Targeted primary-source research for the next natal consultation increment. All eleven complete original images in the witness table were freshly visually inspected and their exact bytes matched `source_manifest.json` SHA256 values. This is source-faithfulness research, not empirical validation, an exhaustive chapter review, or approval of complete personal interpretation. The existing location changes and application behavior were not edited by this research task.

**Subsequent reconciliation:** originals208-212 have now been added to the canonical continuation review, with eight assertions across this and the conjunction research. Pending labels below describe the research baseline; current implementation and totals are in [the implementation record](DIRECTED_CONTEXT_IMPLEMENTATION.md).

## What the originals establish

**Bidirectional rulership includes what a ruler carries, not only the ruler of its current sign.** Printed 207 begins with the ordinary Moon-in-Leo-to-Sun lookup, then distinguishes the Moon's own role as Cancer's ruler. Its separate personal worked chart continues on 208: the Moon is in Aquarius/H7, but Cancer occupies H12 and contains the North Node. The author requires that Cancer/H12/occupant context before moving on to Aquarius's ruler. These are two different examples, not a contradiction between a Leo and Aquarius Moon. A structural graph can preserve both the forward ruler reference and the reverse ruled-sector contents. It cannot infer the author's reported emotional or relationship history for another person. [Originals 207-208; witness table below.]

**A Delegate requires the complete contents of the ruled sign and its actual house.** Printed 209 explicitly distinguishes the method from a simple Planet -> Sign -> Ruler chain. It requires collecting and assessing everything in that ruled area. It also rejects a final-ruler hierarchy: arriving at a self-ruled or repeated node does not make that planet dominant or multiply its influence. Printed 210 continues the procedure: assess the variables in a layer before carrying its expression through the ruler into the next layer. This supports a graph with stable condition references and cycle back-references, rather than an infinitely expanded tree or a chosen final dispositor. [Originals 209-210.]

**Actual chart sectors replace fixed natural-house shortcuts.** Printed 210 supplies a particularly useful topology fixture: Gemini Rising places Cancer in H2, so the Moon represents the Cancer/H2 context in that chart while retaining its own symbolic function. This does not turn Moon into a universal money placement or import a fixed Venus/H2 correspondence. The known modern ruler map is separately retained in `original_assertions.json#sign185-modern-rulership-map`; do not replace Uranus/Neptune/Pluto with traditional co-rulers. [Original 210; existing original185-186 assertion.]

**Question focus is a Lens across the whole chart.** Printed 211 explains that the same planet's themes are considered through the question's context. H7 alone supplies partner/relating context rather than a complete love reading, and H10 alone is not a complete career reading. The continuation on 212 explicitly requires assessment of the whole chart and distinguishes several relationship subtopics across different houses. Topic roots can guide relevance; they cannot delete ruler/occupant/receiver prerequisites or manufacture a rigid one-house answer. The author's accuracy claims remain source assertions. [Originals 211-212.]

**An ordered relationship needs the receiving side's actual condition.** Printed 327 presents the author's Planet1/Planet2 resolution convention, including conjunctions. The continuation on 328 explicitly calls for Planet2's placement, ruler and other aspects before synthesis. Its Mars-to-Ascendant versus Ascendant-to-Mars distinction shows that the ordered interpretive relation cannot be reconstructed from an unordered separation alone. This supports assembling a receiving-context packet. It does not establish universal physical emission from mathematical points or supply a complete algorithm for assigning each role. Do not turn the author's problem/solution wording into blame about a person. [Originals 327-328; existing `resolution-planet2-context` assertion.]

**Current-sky condition and natal receiving condition are distinct layers.** Printed 497 rejects creating a contact to an entire natal house from sign alignment alone. Printed 498-499 requires the current body's own sky-to-sky relationships before overlaying it on a person. Original499's Moon/Uranus example includes Pluto occupying Uranus's ruled sign: its structural lesson is that current ruler payloads accompany current relationships. Its notation and hand-off examples are not an executable universal event algorithm. Keep the current-sky graph, natal graph and actual inter-layer contact as separate objects, even when they share body IDs. [Originals 497-499.]

## Concrete implementation boundary

A **typed structural context graph** is implementable now. It should expose calculated facts and required dependencies without claiming complete condition or allowing an LLM to fill missing stages. The following is an engineering representation of the source dependencies, not an assertion that the author supplied this JSON schema.

| Record | Minimum retained fields | Required boundary |
|---|---|---|
| Graph scope | chart/layer ID, epoch, resolved house geometry, evaluated catalog IDs, unavailable IDs, omitted IDs/reasons | A calculated subset must never be described as all possible occupants. Record whether catalog inventory was actually evaluated. |
| Condition node | stable point ID and type, calculated placement, direct physical motion, stage/condition reference, incoming/outgoing qualified contact refs, missing prerequisites | Geometry-only candidate arrays do not prove presence or absence of qualified aspects. Mathematical/derived points retain their actual emission policy. |
| Forward sign ruler | actual sign, source-selected modern ruler, condition ref or explicit missing ref | Separate from a decan-associated planet and from the natural inner-wheel house theme. |
| House Delegate | actual Whole Sign sector/sign, its ruler, occupant IDs, each occupant's condition reference and availability | Derive the sign from the person's Ascendant/cusps. Never substitute H2 -> Venus or H4 -> Moon universally. Unknown birth time leaves this unresolved. |
| Reverse payload | each sign ruled by the node, actual house for each sign, all evaluated occupants including points/asteroids, condition refs and unavailable/missing entries | Mercury and Venus each retain both ruled-sign payloads. Empty evaluated occupancy does not mean no theme or no condition. |
| Cycle | finite path, repeated node, cycle members, missing-node record | Self-rulership and cycles terminate by reference without ranking a final ruler, strength multiplication or dropping collected payloads. |
| Receiving context | separately typed sender/receiver/layers, receiver's placement/ruler/Delegate/occupants/contact refs and missing prerequisites | Construct this only for a specifically identified relation/candidate. Do not invent an active relationship from an empty graph or turn reverse interpretive notation into physical emission. |
| Completeness | inventory/structure coverage separately from degree, directed aspect, Delegate synthesis and personal-answer approval | `structure_complete` can describe a verified finite inventory graph; `condition_complete`, `complete_phddasr` and full-report approval remain false while their required methods are incomplete. |

Use references to shared nodes instead of recursively copying every payload into every node. Cycles must remain visible. A graph can contain all catalog occupants and still lack complete meaning or qualified contacts; do not conflate these coverage dimensions.

Keep **occupant physical Rx**, **house Delegate physical Rx** and any source-defined carried-house interpretation in different fields. The previously retained `retrograded-house` and `double-retrograde` concepts expressly prohibit making all occupants physically retrograde, cancelling two Rx layers, or treating a house as a moving body. These concepts were inspected as canonical metadata in this pass; their compiled-PDF witnesses were not freshly visually re-reviewed here. The proposed structural addition must preserve those already recorded restrictions without claiming a newly completed body-specific Rx interpretation.

## Source decisions suitable for canonical assertions

These minimal paraphrased candidates are ready for deliberate canonical source-review reconciliation. They are **not** edits made by this research note; exact IDs are proposals. Their implementation/answer-use status must remain separate from visual/passage review.

| Proposed assertion ID | Concept | Paraphrased proposition | Limits / original witnesses |
|---|---|---|---|
| `delegate208-reverse-sector-occupants` | `delegate-condition` | The Moon's worked condition includes its ruled Cancer sector and that sector's North Node before following the Moon's own Aquarius ruler. | Worked topology, not the author's autobiography applied to others; no point-emission rule. Originals207-208. |
| `delegate209-no-final-ruler` | `delegate-condition` | A Delegate carries ruled-area contents; a terminal/self-ruled/repeated planet is not a controlling final ruler. | Requires complete condition; repetition is not strength. Original209. |
| `delegate210-layer-before-carriage` | `delegate-condition` | Each layer's energies and variables must be assessed before its expression is carried through the ruler into the next area. | Dependency/order rule; neither a completed synthesis algorithm nor a personality claim. Original210. |
| `delegate210-gemini-cancer-house-example` | `delegate-condition` | Gemini Rising locates Cancer in H2, making Moon the Delegate for that actual sector while retaining Moon's own function. | Explicit Whole Sign topology example, not universal Moon=money or Venus=H2. Original210. |
| `lens211-whole-chart-context` | `objective-context` | A question's Lens adjusts relevance across the whole chart; H7 alone is relating/partner context rather than a complete relationship reading. | No fixed one-house/one-paragraph classifier or new strength ranking. Originals211-212; depends on `delegate-condition` and `directional-context`. |

The existing `resolution-planet2-context`, `sign185-modern-rulership-map`, `ecosystem-within-between-scope`, `receiver-anchor-natal-emitter-radius`, `receiver-anchor-transit-exact` and `parts673-receiver-exactitude` assertions remain material constraints. The dedicated point/anchor examples must not be flattened into a universal receiver or emitter catalog.

## Required regression fixtures

1. **Original208 topology:** for the worked Aquarius Moon/H7, Cancer is H12 and includes North Node. Moon's reverse payload retains that H12 occupant with its point type before forward reference to Uranus. The source's narrated semi-sextile notation does not grant physical outgoing emission to North Node.
2. **Original210 topology:** synthetic Gemini Ascendant -> Cancer/H2 -> Moon Delegate. An occupant of Cancer belongs to the Moon's H2 payload even when Moon itself is elsewhere. Moon's own function and placement remain separate.
3. **Dual-rule payload:** Mercury retains both Gemini and Virgo sectors; Venus retains Taurus and Libra. Each uses the chart's actual house, including empty sectors. No fixed H2/H7 or H3/H6 assumption.
4. **All catalog coverage:** a non-core asteroid or point in a ruled sector gets a typed condition/missing reference. An unavailable catalog object stays listed as unavailable; absence cannot prove no occupant. UI-hidden objects cannot silently vanish from an asserted full-catalog payload.
5. **Self-loop and multi-node cycle:** finite node/edge counts, explicit back-reference, no repeated strength or final-ruler classification. Preserve all evaluated payload entries reachable before a repeat.
6. **Separate motion:** direct occupant with Rx Delegate stays physically direct; Rx occupant with direct Delegate does not turn siblings Rx; double Rx does not cancel.
7. **Unknown birth time:** sign ruler and sign membership can remain known, but the actual house/Delegate field is unresolved; no H12 or H2 claim is fabricated.
8. **Receiving context:** A->B and B->A resolve different receiving packets; qualification and role assignment have separate statuses. An explicitly source-qualified direct conjunction may reference both packets but cannot infer completed problem/solution or Vantage synthesis.
9. **Natal/current separation:** `natal:Uranus` and `sky:Uranus` never collide. Sky ruler payload is derived from the sky epoch, natal payload from birth epoch; a sky-to-natal relation does not modify the natal graph's positions or create reverse physical emission.
10. **Writer gate:** a structural condition reference can support a calculated graph fact. It cannot by itself support a claim that the full ruler/Delegate or aspect method is complete. Missing degree/aspect/receiver prerequisites survive export/retrieval/rendering.

## Remaining gaps and source tensions

- No page reviewed here supplies the full body-by-angle OOI/cap combination, equality ownership, Fringe/forced-contact/hand-off implementation, or a universal receiving-object exception table. The parent directed-aspect research must settle its own bounded rule contract.
- Original208's point-to-Ascendant narrative and original328's reverse Ascendant ordering must be preserved as interpretive source notation, alongside the receiver-only and non-emission restrictions in the dedicated point/Part/anchor sources. They do not justify broad outgoing emission from every plotted point.
- Original499 narrates N->T ordering and a later hand-off while also saying the current chart acts upon the natal person. Preserve notation versus physical-layer distinctions; do not silently choose one as a general event algorithm. Previously recorded original503 H5/H4 and 524/528 notation conflicts remain relevant.
- The needed context graph is more than a forward ruler chain, but the reviewed pages do not give a fully deterministic prose-combination algorithm or conflict weighting. Preserve `condition_complete=false` until all actual required stages and selected procedures are resolved and tested.
- Canonical scan statuses currently still mark208-212 pending/not reviewed despite the fresh complete-page review here;209 also has the earlier October28 targeted note. This research adds a durable evidence trail but does not silently change the source-manifest counters. The integrating agent should reconcile all five deliberately, preserve their original hashes and maintain non-exhaustive semantic-review labels.
- This targeted pass does not close all128 source-found implementation requirements, all75 source-incomplete requirements or full personal-report approval. It supplies concrete structural progress and source findings that can enter the chatbot packet without pretending full completion.

## Exact original witnesses freshly checked

Paths for207-328 below are `reference/originals/<file_id>.jpg`;497-499 use their `reference/source_photos/<filename>` paths. Original files remain private. Complete-page visual review and exact SHA256 checks were performed for every row; hashes matched the current manifest. Pending/reviewed labels below describe the register before reconciliation, not the fresh evidence just gathered.

| Printed page | Filename / file ID | SHA256 | Current canonical visual status |
|---|---|---|---|
|207|`IMG_4628.jpg`; `1NYHIqbNXnZLOo0rSsGIG-Z8ATJtE4tbF`|`0c9ac377e2965aa0c21a256472b9c38daaff03bc338fc6de8a6528c4cc6623e7`|Targeted reviewed|
|208|`IMG_4629.jpg`; `1KT6y5V39GuJ5h1XAVQ2zhnCTlX9vYmrt`|`7ce599151d458d07174d0f69575d428a0a806e53f2209880c26a29a968183ff0`|Pending|
|209|`IMG_4630.jpg`; `1EFQFt-Q6VOBbB6D9zI6IvaIDgeFYEz7Z`|`ad4862928b146e83450a0bb1c92a3362855369329c93737ab891f5967d97a843`|Pending|
|210|`IMG_4631.jpg`; `1eG5QLD-30EDYS6uU9PQNnqK_SSYCkPpQ`|`a7cdff92b01a69041b5c008c6c1d6cecdec00618a67eb072d8fbb81fffef04a1`|Pending|
|211|`IMG_4632.jpg`; `1wc_DWXMYxOvnx3-c3r9YoxAoug7qfznn`|`2cedfcc8b15656096e8e197e56272dc509c1160fc76082d87a97ac22b5b7d807`|Pending|
|212|`IMG_4633.jpg`; `12NIpjGeWBfruBDNiqQyD3VUe2COIxgnK`|`504174a1df9a2f9153b60e64d2b20dbef6e50327e760486953af48271a01ab41`|Pending|
|327|`IMG_4761.jpg`; `1DJYlST1HmHQm66PHxI-YYxithXKzUr_c`|`21a6f8aebcdf9412ed386a9c91b7eaeb109e0472234f5dbf8e3dc4f758070947`|Targeted reviewed|
|328|`IMG_4762.jpg`; `115KNB-fn2Fscix48_It1-vJ1fWA0qlrA`|`8e63022ce04cb644e62cc0e80840efce05ffcbe3506f8afcc9a376d52590dcea`|Targeted reviewed|
|497|`IMG_4958.jpg`; `1dIuNnhmpb0Hp40w5Cl8Fsy6oX99eH_yB`|`6ba3f7f64bb7340b5649d43c8765645098be322d7200466eb32d0546c2c0d19a`|Targeted reviewed|
|498|`IMG_4959.jpg`; `1UWojxsm05OUqe_jJwInJH_Dj998UEg2S`|`58ad56549f73710a3b26b661e7189f99247bb4fa6e232011fbee14593de337bf`|Targeted reviewed|
|499|`IMG_4960.jpg`; `1OPxXGSiPg1GKp_YT7NeaFGmUHM7f9YBM`|`0eff94d350b81ab4b93e7c4cf0f56a7d61d98ee3708827bd114f9d3e3db38646`|Targeted reviewed|

Canonical records inspected: `data/knowledge/interpretive_inventory.json` (`delegate-condition`, `directional-context`, `vantage-resolution`, `retrograded-house`, `double-retrograde`); `original_assertions.json` (named IDs above); `source_manifest.json`; `source_blocker_findings.json`. Runtime inspected: `mystic_rebels/chat_context.py` and `apps/common-ground/phsr.py`. The prototype already preserves selected occupant types/refs and incomplete status; the main chatbot's payload currently lists simpler ruled-sign/occupant references. The separate applications must not be described as the same verified consumer.
