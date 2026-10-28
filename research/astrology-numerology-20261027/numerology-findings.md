# LOOKS-LIKE-COSTAR natal numerology and lettrology audit

Audit date: 2026-10-27. Repository snapshot: [olsonan26/LOOKS-LIKE-COSTAR at 023140de4ac9ebad8a804b4c984337135e77b19a](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/tree/023140de4ac9ebad8a804b4c984337135e77b19a). The local evidence directory contains UTF-8 source text fetched by the parent via the connected GitHub tool; it is a review snapshot rather than a byte-for-byte archive. No original repository code was changed or executed by this audit.

Scope: all services and name-engine file inventories; full natal formulas, PMEI engine, all 26 letter cards, name cue/composition engines and number banks; natal meaning banks; relationship matrix keys and representative full ordered pairs; career bank; ancillary access, rewriting and report stubs. Daily/yearly material was inspected to identify boundaries and disagreements, not recommended for the first integration.

## 1. Main finding

The most useful integration object is **number + calculation role + source meaning + underlying letters**, rather than an isolated digit. A 6 Soul Urge describes a motive in this implementation; a 6 Called Name describes how others see someone; a PMEI Emotional count of 6 is a raw count and an in-plane harmony rule. They are different quantities with overlapping vocabularies. A professional merger should preserve this distinction.

Sources: [core numbers and formulas](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/numerology.ts#L254-L332), [called-name descriptions](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/calledNameDescriptions.ts#L1-L71), [PMEI raw counts and harmony](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/pmeiEngine.ts#L267-L350).

## 2. Exact number vocabulary already present

These are summaries of the repository's authored symbolic descriptions, not observations established about people. The source code does not establish planet/sign equivalences or empirical associations with placements.

| Number | Specific themes | Detail a simple keyword match would miss | Sources |
|---|---|---|---|
| 1 | Initiation, will, independent direction, leadership | Strategy and planning belong here too; speed and starting without finishing are its watchouts. | pmeiEngine.ts:52; data.ts:1302,1327,1339,1351 |
| 2 | Cooperation, diplomacy, sensitivity, detail, precision, justice | The career bank includes programming, avionics, quality assurance, data validation, law and fine restoration. It is not purely an emotional/relationship symbol. | pmeiEngine.ts:53; data.ts:1303,1328,1340,1352; careerGuidanceData.ts:15-23 |
| 3 | Creativity, expressive language, performance, social energy | Sensitivity to harsh tone and withdrawal when criticized are as relevant as outward charisma. | pmeiEngine.ts:54; data.ts:1304,1329,1341,1353; nameNumberDescriptions.ts:17-22 |
| 4 | Craft, practicality, durable structure, loyalty, method | Hands-on construction and exactness; inflexibility, controlling details and perfection strain are possible shadows. | pmeiEngine.ts:55; data.ts:1305,1330,1342,1354 |
| 5 | Change, movement, persuasion, adaptability, versatility | It also has practical/technical skills and communication; issue is scattering across too many activities, rather than change being bad. | pmeiEngine.ts:56; data.ts:1306,1331,1343,1355; careerGuidanceData.ts:56-64 |
| 6 | Care, responsibility, stewardship, home, beauty, organization | Direct management, supervision, money management and law are explicit; care can become control. | pmeiEngine.ts:57; data.ts:1307,1332,1344,1356; calledNameDescriptions.ts:40-46; careerGuidanceData.ts:66-74 |
| 7 | Inquiry, analysis, truth, refined standards, depth, intuition | It is mapped to Intuitive PMEI while much of its description is analytical. Do not equate PMEI labels with ordinary word use or automatically call it Air. | pmeiEngine.ts:30,58; data.ts:1308,1333,1345,1357 |
| 8 | Executive direction, enterprise, governance, resources, outcomes | Responsibility and ethics accompany material achievement; force/control and stubbornness are shadows. | pmeiEngine.ts:59; data.ts:1309,1334,1346,1358 |
| 9 | Humane service, compassion, broad synthesis, completion | Closure and boundaries distinguish it from 6 care; it is Intuitive PMEI despite empathic language. | pmeiEngine.ts:30,60; data.ts:1310,1335,1347,1359 |

Canonical compact bank: [pmeiEngine.ts:51-61](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/pmeiEngine.ts#L51-L61). Full natal banks: [data.ts:1301-1360](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/data.ts#L1301-L1360). Additional distinct first-name/public/direction contexts: [name-engine/data/numbers.ts](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/data/numbers.ts#L1-L40).

Master handling is not uniform. The core reducer preserves 11,22,33, while most natal description banks fall back to 2,4,6. The career bank has an explicit 11 inspired-messenger entry and no separate 22 or 33 entry. The couple daily bank explicitly describes 11 sensitivity/intuition, 22 large-scale building, and 33 compassionate care, then inherits root-number advice. Those daily descriptions are not automatically an authoritative natal master-number doctrine.

Sources: [core reducer](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/numerology.ts#L333-L371), [description fallbacks](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/descriptions.ts#L37-L94), [career bank](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/careerGuidanceData.ts#L25-L34), [daily master entries](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/coupledynamics.ts#L173-L205).

## 3. Role-aware bridges worth developing

| Numerology feature | Existing definition/calculation | Integration question (proposed, not established correspondence) |
|---|---|---|
| Soul Urge | Vowel-weighted full-name sum; prose explicitly describes motives. | Does a sourced astrological function describe similar needs, and does its True Placement specify where/how those needs operate? |
| Expression | All letters of full name, preserving masters. | Do chart functions/fields describe ways of acting that support or complicate the symbolic ability vocabulary? |
| Called Name | Reduced first name plus reduced last name; public-perception descriptions. | Where does public/social presentation reinforce or diverge from internal motives? |
| Birth Force | Digit sum of the full birth date, preserving masters. | Which natal chart themes echo a birth-based numerology theme? Date dependence must be controlled in any study. |
| Ultimate Goal | Reduced month+day+year plus reduced full-name sum, then reduced with masters. | How could a life-direction theme be expressed through specific chart fields? Preserve this method's actual formula and name. |
| Balance Number | Initial-letter values, reduced with masters. | What coping response does the numerology text suggest when an astrological tension theme is present? This is a reflective prompt, not evidence of actual behavior. |
| PMEI | Raw full-birth-name letter counts across four channels. | Does a chart theme reinforce or contrast a preferred symbolic operating channel? Keep both distributions separate. |
| Letter identity and order | All 26 letters have light/shadow, verbs, first/middle/last text and roles. | Could a role-level composition vocabulary distinguish how a process begins, is developed, and is completed? |

Formula sources: [numerology.ts:238-391](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/numerology.ts#L238-L391); [balance text](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/data.ts#L1313-L1323).

One especially valuable nuance is that **same numerical value does not erase letter identity**. B,K,T all have Pythagorean value 2. B is a gentle mediator; K is a creative/novel intuitive process; T is a fairness/listening/peacemaking process. Therefore a planetary theme that resembles K's creativity should not be assigned to every 2. Source: [letters B](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/data/letters.ts#L22-L36), [K](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/data/letters.ts#L143-L150), [T](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/data/letters.ts#L230-L237); [letter values](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/constants.ts#L5-L12).

## 4. PMEI has richer mechanics than four broad personality labels

- Bins are Physical={4,5}, Mental={1,8}, Emotional={2,3,6}, Intuitive={7,9}. Each letter contributes one count, not its numerical weight. Counts must sum to full birth-name letters. They must never be digit-reduced.
- The engine's named genius factor is a top-minus-runner-up raw-count margin of at least 2. It is an internal rule, not a validated psychometric measure or comparison with other people.
- Zero plane is an all-or-nothing switch in this text, not a missing capacity or karmic diagnosis.
- Non-Emotional planes whose raw count is 2,3,6 receive an emotional-susceptibility flag.
- In-plane harmony asks whether the raw total itself belongs to that plane's number set.
- Emotional raw counts of 4,8,7/9 add physical, mental, intuitive spillover narratives respectively.
- Bad-habit value is total letter count; only digits 1,5,8 have explicit shadow entries. Other digits use neutral placeholder language.

Sources: [PMEI specification and constants](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/pmeiEngine.ts#L1-L68), [spillovers](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/pmeiEngine.ts#L202-L224), [calculation](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/pmeiEngine.ts#L267-L350).

Inference: an interface can show PMEI and chart element/mode patterns side by side as separate symbolic maps. Neither shared vocabulary nor the number four proves that Physical=Earth, Mental=Air, Emotional=Water and Intuitive=Fire. No such correspondence was found in these files.

## 5. Relationship and sequence structures

The love bank contains a complete ordered 9x9 set (81 rows), preserving A-to-B perspective: 4-to-5 and 5-to-4 have different authored descriptions, as do 6-to-8 and 8-to-6. This provides an existing structural model for an eventual perspective-aware report. It does not establish a compatibility percentage, observed relationship outcome, or equivalence to a particular aspect. Some wording makes confident outcome claims; it must not be elevated to verified prediction.

Source: [loveDescriptions.ts](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/loveDescriptions.ts#L4-L86), specifically rows 36/44 and 57/73.

The letter rule bank contains 25 ordered pair rules and three trio rules. Pair inversion can alter the narrative (ST vs TS, AR vs RA). This is a useful composition shape to compare with directionality in an astrology framework, but the underlying systems have different calculations. Source: [pair_trio_rules.ts:4-35](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/data/pair_trio_rules.ts#L4-L35).

The current engine only consumes the first matching adjacent pair in library order. It does not consume trio_rules at all. Therefore the presence of the trio bank must not be described as an implemented feature. Source: [buildCues pair loop](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/src/engine.ts#L95-L104).

## 6. Calculation and provenance issues to preserve before merging

1. **Ultimate Goal is not a date-only Life Path.** getCoreNumbers explicitly labels it Ultimate Goal and adds name and date. ChartData.calculateLifePath nevertheless stores that same name+date result as lifePath and uses it for pinnacle stage timing (36 minus this result). Do not quietly import an outside formula or equate these labels. Sources: [numerology.ts:254-306](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/numerology.ts#L254-L306), [charting.ts:149-182](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/charting.ts#L149-L182).
2. **Master numbers expose meaningful method differences.** For 1980-11-11, the Ultimate Goal birthday component starts at 1980+11+11=2002, reducing to 4; Birth Force sums date digits to 22 and preserves it. This is a worked reading of the source formulas, not a bug determination or execution claim. Distinct methods need distinct identifiers.
3. **Vowel disagreement.** constants.ts and PMEI use A/E/I/O/U. The name cue library additionally treats Y as vowel. Its first-vowel motive considers only the first TWO name characters. A Soul Urge and the cue's motive are different features. Sources: [constants.ts:12](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/constants.ts#L12), [letters.ts:4](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/data/letters.ts#L4), [engine.ts:27-31,89-91](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/src/engine.ts#L27-L31).
4. **Different reduction paths.** Numerology core preserves 11,22,33; name cue reducer collapses everything to one digit. For first name KA and last name H, getCalledNameValue yields 11 (3+8); name cue calledTotal yields 2. Same displayed concept can use different values. Sources: [core called-name calculation](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/numerology.ts#L373-L391), [cue calculation](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/src/engine.ts#L11-L16), [called cue](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/src/engine.ts#L130-L146).
5. **Full direction cue omits middle names.** The source comment says for now just first+last. ChartData's displayed nameParts and yearly letter rows also keep only the first THREE parts, while the standalone yearly essence uses all name parts. Source: [engine.ts:139-145](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/src/engine.ts#L139-L145), [charting.ts:128,218](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/charting.ts#L128), [numerology.ts:66-76](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/numerology.ts#L66-L76).
6. **Positional data is richer than the active cue output.** All letter cards have first/middle/last descriptions, but helm/rudder pick from generic micro pools whenever present; all 26 cards have micro text. Middle synthesis picks one representative letter of the dominant middle role. This loses detail in the existing data. Source: [engine.ts:41-62,81-107](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/src/engine.ts#L41-L62).
7. **Generated writing is not new evidence.** hash.ts selects stable prose by FNV-1a modulo pool length; it is deterministic text selection. compose.ts adds a fixed synthesis and trims beyond nine blocks. profileGenerator.tsx is an obsolete stub saying report generation moved to Gemini prompts. textTransformer.ts uses Gemini to rewrite perspective with a fallback substitution. These mechanisms do not discover relationships or validate them. Sources: [hash.ts](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/src/hash.ts#L1-L17), [compose.ts:65-85](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/name-engine/src/compose.ts#L65-L85), [profileGenerator.tsx](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/profileGenerator.tsx).
8. **Astronomy authority must be external to this date lookup.** services/astrology.ts uses fixed calendar Sun-sign dates without time or location. It cannot establish exact Sun ingress, planetary longitude or True Placement. Source: [astrology.ts](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/astrology.ts#L1-L38).
9. **Daily formulas already disagree.** numerology.ts daily essence combines unreduced personal-day sum with reduced personal-month essence; ChartData.getDailyDataForMonth uses personal month + day + yearly essence. Their master/compound outputs may differ. Deferring this as the user permits removes unnecessary scope, but the methods must not later be merged merely by label. Sources: [numerology.ts:82-106](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/numerology.ts#L82-L106), [charting.ts:279-305](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/charting.ts#L279-L305).
10. **Knowledge coverage is not provenance approval.** These TS meaning banks do not carry per-claim book/page witnesses. Comments sometimes say user-provided packet/PDF or rewritten text, but those are not verified primary-page citations. Preserve them as repository-authored sources until reconciled with the intended primary methodology. services/descriptions.ts also contains conventional past-life karmic-debt explanations for 13/14/16/19; they must not silently migrate into PURE doctrine.

## 7. Recommended initial integration

Build a read-only, static natal comparison prototype that accepts frozen outputs from both independent calculators. For each proposed connection, retain:

- The exact numerology feature, name basis, raw value, reduction chain, letters, vowel convention and method version.
- The exact astrological object/function, True Placement/field, Tone/Pulse and governing source witness.
- A shared narrow concept such as precision, novelty, nurturing responsibility, social expression or humane closure.
- Relationship type: reinforcement, contrast, complementary skill, or no supported relation.
- Source status separately from hypothesis status; an authored match is not an observed correlation.
- Counterevidence and context, including public vs inner-motive mismatch.

No natal bridge proposed here needs daily numerology or a transit engine. Career/creative process, communication and inner-vs-public presentation are practical initial report sections.

Do not count multiple name-derived features as independent confirmations. Expression, Soul Urge, Called Name and PMEI share input letters and arithmetic. Likewise numerological birth features and astrology share birth-date information. A later real association study needs preselected hypotheses/features, held-out cases, shuffled/controlled baselines and correction for testing many potential matches. Its result cannot be inferred from thematic similarity or repository inspection.


## 8. Coverage ledger

Full read means the complete substantive source was inspected in tool output; targeted means sections/openings or call sites were inspected and no claim of complete sentence-by-sentence reading is made. Data presence is distinguished throughout from active execution. This audit did not run the app, Gemini, or calculations.

| File(s), relative to snapshot | Coverage |
|---|---|
| services/numerology.ts | Full read; natal and timeline formula paths traced. |
| services/pmeiEngine.ts | Full read; raw-count engine, copy generation, thresholds and spillovers traced. |
| services/charting.ts | Full read; duplicate natal/name and timeline paths traced. |
| services/descriptions.ts | Full read; lookup fallback and conventional karmic suffix behavior traced. |
| services/nameNumberDescriptions.ts; services/calledNameDescriptions.ts | Full read of all nine entries each. |
| services/careerGuidanceData.ts | Full read; all 1-9 and explicit 11 entries; getter traced. |
| services/data.ts | Targeted natal sections (Birth Force, Balance, Life Path/Ultimate Goal text, Expression, Soul Urge), export inventory and excerpts of cycle sections. Long natal paragraphs inspected through source excerpts; not all 297 KB read in full. |
| services/loveDescriptions.ts | All 81 ordered row keys counted and opening text scanned; complete selected 4→5,5→4,6→8,8→6 and several adjacent examples inspected. Not all full paragraphs read. |
| services/coupledynamics.ts | Targeted broad matrix sections, master-number inheritance and final composition function; some long output truncated, so not a claimed full read. Daily scope is deferred. |
| services/marriageadvice.ts | Targeted yearly, monthly and master entries; not claimed full read. |
| services/accessControl.ts; services/astrology.ts; services/textTransformer.ts; services/profileGenerator.tsx | Full read; peripheral to natal crosswalk but integration authority and report-generation boundaries inspected. |
| services/goingthroughit.ts; services/letterMeanings.ts; services/nameGenerator.ts | Empty source files (local evidence has trailing newline only). |
| name-engine/src/engine.ts; compose.ts; types.ts; hash.ts | Full read; data flow, selection and missing rule consumption traced. |
| name-engine/data/letters.ts | Full read of all 26 letter cards. |
| name-engine/data/numbers.ts; pair_trio_rules.ts; templates.ts | Full read; 25 pair rules counted; three declared trios inspected. |
| name-engine/data/letters.json; numbers.json; pair_trio_rules.json; templates.json | Full read: each is a comment-only obsolete file pointing to the TypeScript counterpart. |
| constants.ts | Full read to verify A-Z mapping, vowel set and master/debt constants. |
| App/UI/astrological framework files | Outside this sub-audit; parent/parallel astrology audit owns these paths. |

The snapshot was supplied to this sub-audit at the fixed GitHub commit listed above. Exact current branch/network identity verification is owned by the parent audit.

## 9. Data flow and redundancy rules

The natal path is:

1. Full name → weighted all-letter sum → Expression.
2. The same full name → weighted vowel-only sum → Soul Urge.
3. Full name initials → Balance.
4. First and last name only, each reduced → Called Name.
5. Full birth name → one vote per letter into PMEI bins → counts, zero/harmony/margin/cross-match flags.
6. Date → digit sum → Birth Force; separately month+day+year reduction enters Ultimate Goal.
7. Expression + that separate birthday component → Ultimate Goal.

These related outputs are useful as different lenses, but not independent evidence. An integration should be able to say “same source input, different role” before it says “several confirmations.”

Two specific anti-shortcut examples are built into the code: 4 and 8 both carry structure/organization, but letter-value 4 belongs to Physical while 8 belongs to Mental; 5 belongs to Physical although its prose includes communication/adaptation, and 7 belongs to Intuitive although its prose includes research/analysis. Therefore automatic Earth/Air/Water/Fire relabeling would change the numerology method rather than integrate it.

Sources: [PMEI map and vocabulary](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/pmeiEngine.ts#L27-L61), [core natal flow](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/numerology.ts#L254-L332).

