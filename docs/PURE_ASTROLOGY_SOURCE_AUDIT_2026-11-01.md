# PURE ASTROLOGY / Mystic Rebels: source-to-code audit (2026-11-01)

**Source of truth:** the user's canonical PURE ASTROLOGY book, checked directly at printed pp. 103, 156–157, 161–162, 188–190, 227–230, 271, 661–665 and 670–679. Compared to the actual **main** branch of `olsonan26/mystic-rebels-chart-generator` (not merely earlier assistants' paraphrases). **Scope:** current natal chart generator's numerical and semantic placement layer, not a scientific validation of astrology as a predictive discipline.

## Primary conclusion

- **No source contradiction found in the implemented Whole Sign house / True Placement / Tone / Pulse / modern sign-ruler formulas.** The previous assistant incorrectly said House 7's natural Libra ruler, Venus, was the PHSR sign-ruler for Gemini. In the actual code, Gemini correctly maps to **Mercury**.
- **Confirmed product gap fixed by this PR:** the API already returned `sign_ruler` but the user-facing inspector and placement table omitted this essential PHSR field. The branch now displays **Sign ruler** clearly.
- **Confirmed material correctness defect fixed by this PR:** although the input specified birth-time uncertainty, the old engine always published definitive house/True Placement results for the central clock even when the plausible birth interval crossed a rising-sign boundary. The engine now checks the Ascendant throughout short uncertainty intervals and **withholds houses and Ascendant-dependent Parts if the rising sign may change**; uncertainty of 60+ minutes or unspecified clock error fails closed conservatively. A regression reproduces a Gemini→Cancer rising flip across 2024-01-01 00:04–00:05 UTC near Los Alamitos. Angles and astronomical positions remain clock-reference estimates. This does not yet solve per-body Tone boundary uncertainty.
- **Confirmed major coverage gap:** mapping a planet to `sign_ruler` is *not* a full Delegates/recursive PHSR reading. Nor is a complete Energy Flow / directional aspect / Reverse-Vantage / natal-transit forecast engine present. These stages are explicitly marked **BLOCKED**, rather than claimed correct or finished.
- **The unsupported 1776 issue remains:** the production ephemeris supports **1800–2399 UTC**. The prior American founding positions in research used a distinct **MOSEPH 1776 proxy** with unknown official founding time; the chart engine cannot certify a natal U.S. 1776 whole-sign chart or interpret its full PHSR.

## Source traceability

| Rule / capability | Exact source rule and evidence | Main branch behavior | Audit verdict |
|---|---|---|---|
| Ascendant / first house | Printed p. 157: eastern-horizon ecliptic intersection lies in a sign; that entire sign becomes House 1 | `astronomy.angles` gets Ascendant from Swiss `houses_ex(..., b'W')`; `placements.house` uses integer zodiac sign indices | **PASS, calculation method** |
| 12 Whole Sign houses | Source p. 162 and historical passage: each sign occupies a complete house | `(floor(planet_lon/30)-floor(asc_lon/30))%12+1` | **PASS**, independent forward-count test |
| Natural house energy | p. 156: 1=Aries, 2=Taurus ... 12=Pisces; independent from outer sign | `field` and `true_placement` equal `SIGNS[house-1]` | **PASS** |
| Tone | p. 157 and PHSR p. 103: astronomical zodiac sign influences expression | `tone=SIGNS[floor(lon/30)]` | **PASS** |
| Pulse | p. 103, pp. 227–230: decans are 0–10°, 10–20°, 20–30° in same-element zodiac sequence; Virgo→Capricorn→Taurus | `pulse=SIGNS[(sign+4*decan)%12]` | **PASS** |
| Modern sign ruler | pp. 188–190: modern Pluto rules Scorpio, Uranus Aquarius, Neptune Pisces; p. 103 P→H→S→R→repeat | `sign_ruler=RULERS[sign]`; e.g. Gemini→Mercury, Cancer→Moon | **PASS, first hop only**; inspector/table gap **FIXED** |
| Scorpio Asc + Cancer example | Book Dual Wheel example printed p. ~103: a Cancer placement in 9H is Sagittarius True Placement and Moon the Cancer sign ruler | Synthetic Scorpio AC 220°, Cancer longitude 100° → House 9, Sagittarius Field, Cancer Tone, Moon ruler | **PASS** |
| House 7 + Gemini example | A Sagittarius rising chart places Gemini in House 7 (Libra Field), but its Tone ruler is Mercury | Synthetic AC 245°, Gemini 75° → 7H, Libra, Gemini, Libra Pulse, Mercury | **PASS** |
| Independent Whole Sign cusps | One complete sign per house | Swiss `houses_ex` Whole Sign cusp sweep; first cusp = 0° of Asc sign, not exact Asc degree | **PASS**, four horizon/date cases |
| Retrogrades | Source retrogrades are treated as directional/internal; astronomical classification `dlongitude/dt<0` | Swiss longitude speed <0 | **Astronomical classification implemented**, book's full interpretation not done |
| Out-of-Bounds | Printed p. 271: absolute declination greater than **23.44°** | `abs(eq[1])>23.44` | **PASS source threshold**; not a full declination/parallel interpretation |
| Fortune, Spirit, Love | Printed pp. 670–679: AC+Moon−Sun; AC+Sun−Moon; AC+Venus−Sun, no day/night inversion | `service.calculate` matches three formulas; normalizes longitude | **PASS source-formula review**; full interpretations missing |
| Nonagesimal / Subnonagesimal | Source pp. 661–665: Asc−90° and opposite point Asc+90°; book illustration Leo 13°06→Taurus 13°06 | `astronomy.angles`: `ac-90`, `ac+90`; existing independent geometry tests | **PASS source-formula review** |
| PHSR Delegates / recursive traversal | p. 103 says to REPEAT; book Rulership and Delegates chapters require following interconnected rulers | Only first `sign_ruler` property exposed, no recursive evaluator | **BLOCKED** |
| Degrees / Spark | Source additional D/Spark techniques | `spark=None`; RULES marks Spark BLOCKED | **BLOCKED** |
| Natal/Transit directional aspects | Source pp. 161, later Aspects and Orbs chapters: directional ordering, asymmetric reach, cross-ecosystem reverse reading | No complete aspect/transit engine; RULES already BLOCKED aspects | **BLOCKED** |
| Vantages, Energy Flow, Fringe | Source says positioning, directional aspects and cross-system flow are required | No complete source-verified evaluator | **BLOCKED** |
| Progressions / predictive forecasts | Incomplete source-specific procedures | Production marks progressions BLOCKED; new explicit `predictive_engine=BLOCKED` | **BLOCKED** |

## Tested, not assumed

An independent local regression script (`verify_placement_logic.py` provided separately with this audit) executed **10,425 assertions** across sign-house/pulse/ruler combinations, book examples, zodiac boundaries and four Whole Sign Swiss geometry samples. They all passed. This is a **logic test**, not a local test of the repository's full pinned SWIEPH runtime or every user-facing interaction. A new pytest module checks the source examples and the full 12×12 mapping grid in CI.

**Critically:** The existing repository documentation says 238 numerical checks, 165 cached NASA Horizons comparisons, frontend geometry checks and a successful hosted deployment were recorded earlier. This audit has inspected their test code and recorded claims; it has **not** re-run those remote historical jobs nor independently certified every claimed precision figure. CI run status after this PR is separate.

## Fixes proposed

1. Add `sign_ruler` to the typed frontend `Point` model; the API had it already.
2. Show **Sign ruler** in both the object inspector and full placement table. Keep the inspector usable when the extra field wraps.
3. Add `delegate_traversal`, `energy_flow`, `transit_synastry`, `predictive_engine` as explicitly **BLOCKED** in the API capabilities (do NOT silently claim that a sign-ruler map equals complete rulership analysis).
4. Fail closed on an uncertain Ascendant crossing a sign boundary, rather than assigning fictional definitive houses, and withhold Ascendant-dependent Parts.
5. Add source-anchored test module for all 12 Ascendant signs × 12 planet signs, near-boundary degrees and decans, unknown time, example charts, and unimplemented-rule claims.

## Open / important limitations

- A **correct house formula does not guarantee a correct source interpretation.** Degrees, aspect arcs, fringe, Vantages, full delegate traversal, progressive house movement and transits remain out of scope.
- The book's metaphysical claims are claims of its author; numerical conformity to the book does not scientifically prove the causal or predictive validity of astrology.
- We cannot create a source-certified 1776 U.S. founding chart with the present 1800+ ephemeris or an unverified founding-time Ascendant. Do not apply retrospective WWI/WWII coincidence results as national war forecasts.
- A single book excerpt can contain OCR page ordering problems: all quoted source statements should be checked against their print-page context before implementing controversial or advanced cases.
- **Remaining clock uncertainty problem:** planetary zodiac sign/Tone near a sign boundary may also vary during the declared birth-time window. The current new guard specifically covers the **Ascendant rising sign**, not the time interval for every moving body. Do not treat approximate Moon or planetary sign at a cusp as guaranteed; a future epoch-bracketed all-body check is required.
- The full 72-body performance, exact 1776 ephemeris compatibility, browser scenarios and Vercel production deployment have **not** been newly re-executed in this audit. Run the complete PR CI, then independently validate with the pinned Swiss files before merging.

**Status:** A source-comparison and test-backed placement-layer audit, not a blanket certification of the whole system.
