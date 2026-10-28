# LOOKS-LIKE-COSTAR astrology: integration findings

Inspected 2026-10-27. Source snapshot: `olsonan26/LOOKS-LIKE-COSTAR`, commit `023140de4ac9ebad8a804b4c984337135e77b19a`, downloaded by the parent through connected GitHub tools. All references below use repository paths and one-based source lines. Mystic comparisons use its audited source checkout at `work/Mystic-Rebels`; this note does not change either application or establish live behavior.

## Main finding

The best first merger can be entirely natal: retain independently calculated name/date numbers and Mystic's natal placements, then compare their specific meanings in the relevant life context. Daily numerology and predictive astrology are unnecessary for this first layer. LOOKS-LIKE-COSTAR already contains Alchemistic astrology ideas that closely resemble Mystic's structural methodology. The uploaded answer understates that overlap when it characterizes the older repository primarily as conventional astrology.

That overlap is useful architecture, not proof that a number corresponds to a celestial placement. A shared word such as responsibility can originate from very different roles: a full-name ability number, a called-name social impression, a planetary function, a sign's style, or a house's context. A credible merger preserves those roles.

## Strong structural similarities and useful applications

| Existing material | Concrete evidence | Proposed use in combined system | Status |
|---|---|---|---|
| Function, context, expression and dependency are separate | `alchemistic_astrology_knowledge_base/core_frameworks/phsr_framework.ts:6-28` separates planet, house, sign and ruler; template at 31-52 | Match a number's specific role and theme to an appropriate astrological function, then use actual house/True Placement/Tone/Pulse context to refine it | Shared structure verified; cross-system mapping proposed |
| Ordered relationships matter | `core_frameworks/free_theory_matrix.ts:6-162` contains 12 rows with 11 other-sign entries each; Aries→Gemini at 9 differs from Gemini→Aries at 34 | Keep A→B and B→A distinct when explaining how one person's needs or capacities meet another's. Numerology's ordered couple rows offer a compatible data shape, not an astrological aspect | Existing directional data; merger hypothesis |
| Rulers create a dependency graph | `phsr_framework.ts:88-110` follows sign rulers until missing data or a loop; modern rulerships at 112-125 | A theme repeated in an outer number and a placement can be followed into the actual natal ruler's context instead of ending at a generic paragraph | Reusable graph concept; PURE conditions must govern |
| Several contexts contribute to one life domain | `vocational_synthesis.ts:3-4, 9-37, 43-127` distinguishes MC, H10, H6 and H2; `components/rectificationMethodology.ts:18-19` separately identifies MC as ambition and includes ASC motivation | A career comparison can distinguish motivation, ambition, organization of work, daily working style and earning. This is richer than assigning a career to one number | Structural bridge, pending methodology reconciliation |
| Relationship analysis is more than a compatibility score | `synastry.ts:14-23` uses H2/H5/H7/H8 and house-ruler overlays | Compare numerical needs/interaction patterns with values, enjoyment, partnership and intimacy contexts independently, with citations for each side | Framework exists as prose; no validated combined score |
| Gift and difficult expression coexist | `aspect_spectrum.ts:38-79` records perception, reality and support phase; `nodes_integration.ts:40-93` has integrated polarities | Explain how the same shared theme may be constructive or difficult without assuming that lexical agreement means an easy relationship | Writing structure useful; don't infer an individual's maturity or biography |
| Numerical labels needn't equal zodiac ordinals | `name-engine/data/numbers.ts:4-38` defines first-name, called-name and full-name roles; PHSR defines a separate taxonomy | Compare the role and meaning, never infer number 7 = seventh house or number 8 = Scorpio from the ordinal alone | Recommended design rule |
| General qualities can receive finer astrological context | Mystic `data/knowledge/source_meaning_profiles.json` gives source-reviewed sign meanings, e.g. Gemini at 242, Virgo at 560, Libra at 690 and Capricorn at 1025 | One number can have several precise links: quality/refinement, justice/perspectives, management/endurance and practical building should be distinguished rather than collapsed into one planet | Many-to-many thematic map proposed |

For example, numerology's number 2 includes quality and precision as well as cooperation (see the separate numerology findings). Mystic's reviewed Virgo vocabulary concerns analysis, refinement, service and the next practical step, while Libra concerns balancing perspectives and exchange. These are two different candidate resonances for the same number. Neither establishes that 2 is Virgo or Libra. Similarly, number 6's care and management can resonate with Cancer's nurture and Capricorn's endurance in different contexts. This can reveal nuance that a one-to-one correspondence table would discard.

The concrete opportunity is a contextual explanation such as: “The name-derived material emphasizes careful standards; the natal material adds analysis/refinement in this particular field, while a separate placement emphasizes balancing perspectives.” The chart and number values must actually exist for that person; this is a composition example, not a personal finding.

## Corrections to the uploaded answer

1. **The older astrology material is already explicitly Alchemistic.** PHSR, a 132-entry directional FREE matrix, Whole Sign houses, delegated rulership, fusion cusps, multiple-house lenses, and an aspect spectrum are named throughout the code. Those structural similarities should be evaluated before importing any conventional interpretation. Source: `core_frameworks/phsr_framework.ts`, `free_theory_matrix.ts`, `fusion_cusps.ts`, `seven_lenses.ts`, `aspect_spectrum.ts`, and `calculations/whole_signs_calculator.ts`.

2. **The uploaded hierarchy is not a complete source assembly rule.** COSTAR's PHSR is Planet→House→Sign→Ruler (`phsr_framework.ts:2`). Mystic's source review records Planet→House→Degree→Decan→Aspects→Sign→Ruler, with a note that sign is technically assessed before degree/decan/aspects (`docs/METHODOLOGY_SOURCE_REVIEW.md:112`). The uploaded Planet→Field→Tone→Pulse→Degree→Rulership chain can serve as informal shorthand only. A merger must follow the audited source's actual scope and composition rules.

3. **An orb table does not provide PURE's directional influence engine.** COSTAR `astrology_data/orbs.ts:128` accepts the larger of the two planets' aspect-specific orb allowances, creating a symmetric pair check. Mystic's reviewed source distinguishes Saturn→Moon from Moon→Saturn and forbids summing influence across ecosystems (`METHODOLOGY_SOURCE_REVIEW.md:88-94`). These are materially different models.

4. **A natal comparison can precede transits.** Number meanings, name roles, PMEI and natal placements can be compared without forecast timing, progressions, daily numerology or a completed advanced aspect network. Any missing PURE calculation should remain absent from the comparison rather than being filled from COSTAR prose.

## Source conflicts that must be reconciled

| Topic | COSTAR evidence | Mystic evidence / disposition |
|---|---|---|
| Chiron | `chiron_acceptance.ts:1-29` defines an acceptance teacher; `phsr_framework.ts:65` repeats it | Reviewed meaning is “Fractured Structures,” comparing expected standards with structures that do not fit and developing an authentic alternative (`source_meaning_profiles.json:1299-1305`). It rejects an automatic permanent unhealable-wound narrative at 1376-1384. Replace older meanings rather than blending them |
| Fusion cusp width | `fusion_cusps.ts:9-29` applies a ±1.5° sign-boundary blend and dual rulers | Mystic source review distinguishes 5% widths at sign/decan/degree scales and unresolved exceptions/post-boundary rules (`METHODOLOGY_SOURCE_REVIEW.md:78-84`). Do not promote older prose to a complete engine |
| Direction | FREE matrix has directional entries; `free_theory.ts:51-56` instead reduces pair distance to the shortest unsigned path | Preserve matrix direction separately from geometric separation; neither alone is the complete source-verified PURE aspect procedure |
| Solar arcs and rectification | `rectificationMethodology.ts:149-155, 179-181` recommends Solar Arc techniques; numerical examples use approximate one-degree-per-year advancement | Mystic source review explicitly records source exclusion of Solar Arc Directions and missing numerical rectification objective (`METHODOLOGY_SOURCE_REVIEW.md:127`). Don't import the method |
| Internal rectification consistency | `rectificationMethodology.ts:172` calls Neptune the secondary ruler for Pisces→Aries; its own `phsr_framework.ts:113` makes Mars ruler of Aries. At 228-229 it correctly uses Sun as the prior Leo influence into early Virgo, conflicting with blanket “NEXT sign” language | Treat rectification text as unverified legacy material, not an authoritative calculator |
| Rulerships | `phsr_framework.ts:112-125` uses the twelve modern rulers | Mystic confirms twelve modern rulers (`METHODOLOGY_SOURCE_REVIEW.md:116`). This is a genuine agreement, not a blanket rulership conflict |
| Elements versus PMEI | `elements_modalities.ts:9-32` defines elemental qualities and count rules at 53-56 | Four elements and four PMEI planes have different definitions and inputs. Similar vocabulary permits a comparison; it does not justify automatic equality or a shared percentage |
| MC and vocation | `vocational_synthesis.ts:3-4, 46-57` labels MC public calling; rectification text at 18-19 insists MC is ambition and career includes ASC/H10/H6/H2 | Preserve separate angle/house fields and resolve exact meaning against audited source before composing advice |
| Biographical claims | `life_story_structure.ts:45-103` provides childhood wounds and age-act narratives; communication templates sometimes assert childhood atmosphere (`voice_tone_guide.ts:87-89`) | These are writing templates, not observed life history. Neither code nor a chart establishes that a person experienced those events |
| Eunomia | Not present in inspected COSTAR astrology data | Mystic has two incompatible source alternatives (`source_meaning_profiles.json:1401-1450`); keep them separate and do not infer justice/order from a numerical similarity |

## What is code versus prompts, and what is reachable

This is a **source inspection**, not a hosted runtime test.

- The source includes an `AstrologyScreen.tsx` that accepts a chart image and question, assembles a knowledge object, serializes it, and calls Gemini (`components/AstrologyScreen.tsx:290-387`). It is prompt-mediated interpretation, not an independent deterministic natal ephemeris.
- A search across all 102 snapshot files finds no import or render of `AstrologyScreen` outside its own file. The entrypoint imports and routes name-analysis, home, year, you, love and shop (`App.tsx:1-25, 234-312`). Thus the astrology screen appears unreachable from this source entrypoint. This is not a claim about another deployed version.
- The assembled knowledge includes most frameworks, sign interpretations, the FREE matrix and prose on synastry/relocation. However, it sets `timing: {}` and `interpretation_rules: aspectSpectrum` with an “Assumption” comment (`AstrologyScreen.tsx:319-341`).
- `JSON.stringify` sends data/template strings, while exported functions such as `calculateRulerChain` and `generateFREEExplanation` are omitted as functions; their existence in imported modules does not execute them on a chart. The code does not call those functions here.
- The separate Whole Sign calculator has a correct sign-index modulo construction and rejects unknown signs (`calculations/whole_signs_calculator.ts:41-58`), but it is not called by `AstrologyScreen` or `App`. It requires already known signs; it does not calculate planetary positions or an Ascendant from birth data.
- Chiron's detailed acceptance table, life-story module, planet-in-house table, orb checker, Whole Sign helper and communication guides are not imported into the assembled screen knowledge. Some related instructions still appear in the system prompt. Their presence in repository files does not mean all their details are used.
- Six of the seven lens objects are empty (`seven_lenses.ts:21-28`). A request for seven detailed lenses is not evidence of seven completed knowledge tables.
- Rectification asks Gemini to calculate candidate charts from time/location and events without an ephemeris tool, extracts a “final time” by regex, and can fall back to the first time-looking string (`AstrologyScreen.tsx:99-145`). The wizard minimum is three events (`87-88`), whereas its embedded methodology asks for 8–12 (`rectificationMethodology.ts:25`). This cannot be treated as verified birth-time reconstruction.
- The Sun-sign helper uses fixed calendar-date thresholds (`services/astrology.ts:3-34`); use Mystic's actual ephemeris for the natal merger, especially near solar ingress boundaries.

## Practical natal-only merger

1. Preserve numeric calculations and each number's role. Preserve Mystic's validated natal engine and its source status fields.
2. Build a versioned source-backed theme catalogue. Record theme, source passage, system, role, required context, unresolved exceptions, and whether each relation is source-explicit or a new hypothesis.
3. Compare within a chosen domain: expression/communication, values/relationship needs, work organization, or inquiry/learning. Keep planet function, actual field, sign expression, Tone/Pulse and delegate context distinct.
4. Present three possible outcomes: shared emphasis, complementary capacities, or different demands. Allow “no supported connection.” Show why a connection was proposed and what each source contributes.
5. Preserve one-way relational explanations when source-supported. A pair of numbers is never an angular aspect; matching data shapes do not turn numerology into astrology.
6. Before calling a relationship empirically supported, test independently calculated charts/numbers on a predeclared set of hypotheses with comparison cases. Birth-date-derived features share an input, so their agreement is not independent confirmation. Textual similarity alone establishes neither personal accuracy nor predictive power.

This supports a substantive combined natal research view before any timing expansion. It does not establish that any unsourced combined interpretation is ready for customers.

## Coverage ledger

- Fully read all 15 files under `alchemistic_astrology_knowledge_base` (system prompt plus 14 core-framework files; verified by file inventory).
- Read all four `astrology_data` modules across their exported sections: orb values/checker, natal retrogrades, 120 planet/sign entries and 120 planet/house entries. The first five personal planet/sign tables and Jupiter are fuller; outer-planet entries and Mercury–Pluto house entries are explicitly condensed in the source.
- Fully read `calculations/whole_signs_calculator.ts`, `services/astrology.ts`, `App.tsx`, `components/rectificationMethodology.ts`, both communication-guide files, and `name-engine/data/numbers.ts` for the role distinction example.
- Read AstrologyScreen's imports, rectification handler, knowledge assembly, AI call and chat UI. Wizard presentation between roughly lines 165–240 was scanned through relevant references rather than every JSX line.
- Searched all 102 files for import/call/reachability links; searched `YouScreen`, `ChartsScreen`, `BottomNav` and `types.ts` for astrology integration. Other product UI files were not fully audited by this subtask.
- Mystic material was read selectively: methodology review and reviewed meaning-profile/manifest sections. The separate Mystic audit supplies its broader coverage and status.
- No application build, hosted UI test, ephemeris run, dependency installation or scientific validation was performed for this source analysis.

Canonical source base: [LOOKS-LIKE-COSTAR at inspected commit](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/tree/023140de4ac9ebad8a804b4c984337135e77b19a). Mystic comparison base: [audited methodology branch](https://github.com/olsonan26/mystic-rebels-chart-generator/tree/3d83db75c30b26d9b068576d84ec49554822fd8c).
