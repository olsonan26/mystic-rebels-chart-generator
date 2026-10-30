# Exact caution-pattern inventory in LOOKS-LIKE-COSTAR

Read-only source audit at commit `023140de4ac9ebad8a804b4c984337135e77b19a`. No application code was edited, executed, built or deployed. This document records existing symbolic rules and their code paths. It does not validate predictions of injury, illness, relationship outcomes, or financial events.

## Scope and counts

The explicit `warningPatterns` table contains **22 rows**:

- **3 annual conditions**, stored under `level: 'month'`.
- **10 monthly rows**, covering **9 distinct PME/PM conditions**; PME8/PM3 has two different titles.
- **9 daily rows**.

Sources: [complete rule bank, data.ts:1362-1390](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/data.ts#L1362-L1390); [monthly evaluator, descriptions.ts:104-131](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/descriptions.ts#L104-L131); [daily evaluator, descriptions.ts:85-102](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/descriptions.ts#L85-L102).

This inventory does not turn every use of “caution,” “risk” or “careful” in long prose banks into another numeric rule. Daily Essence and Monthly Combiner meaning entries have caution prose fields, and annual prose includes conditional cautions, but those are separate from this explicit combination table.

## Annual conditions: complete table

Here ESS means **Yearly Essence**, and PY means **Personal Year**. These conditions are directional: ESS4/PY9 differs from ESS9/PY4.

| Exact condition | Existing rule title | Existing suggested emphasis, summarized | Annual COM, derived for context only | Source line |
|---|---|---|---|---|
| ESS=4 AND PY=9 | Added Burden (Yearly) | Pace obligations, delegate and complete outstanding work. | 4+9=13→4 | data.ts:1377 |
| ESS=9 AND PY=4 | Unexpected Event (Yearly) | Allow flexibility and contingency planning. | 9+4=13→4 | data.ts:1378 |
| PY=9, with no ESS requirement | Emotional Closure Year | Complete promises and consider endings, environment and relationships. | Varies with ESS | data.ts:1389 |

Important: **the evaluator never receives or tests annual COM**. The first two rules share COM13/4 but have different meanings because their ESS/PY ordering differs. COM4 on its own is therefore not a code-defined caution trigger. Source: [monthly evaluator](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/descriptions.ts#L104-L131). Annual COM itself is calculated from PY+Yearly Essence at [numerology.ts:169-174](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/numerology.ts#L169-L174).

Because PY9 alone also matches the third rule, ESS4/PY9 produces **two annual entries** in the result: Added Burden and Emotional Closure. These can coexist with monthly-specific entries.

## Monthly conditions: complete table

PM means **Personal Month**. PME means **Personal Month Essence**, calculated from Yearly Essence+PM. MCOM is the monthly combiner, PME+PM. All values tested here are the supplied reduced `.value` fields; the current service calculates 1–9 final values.

| Exact condition | Existing rule title | Suggested emphasis, summarized without predicting events | Derived MCOM, not a separate trigger | Source line |
|---|---|---|---|---|
| PME=4 AND PM=9 | Monthly Added Burden | Set priorities and leave room for obligations. | 13→4 | data.ts:1379 |
| PME=9 AND PM=4 | Monthly Unexpected Event | Keep plans adaptable and use checklists. | 13→4 | data.ts:1380 |
| PME=2 AND PM=6 | Relationship Sensitivity | Communicate gently and avoid escalations. | 8 | data.ts:1381 |
| PME=6 AND PM=2 | Couples Teamwork Required | Divide responsibilities and clarify needs. | 8 | data.ts:1382 |
| PME=5 AND PM=8 | Money Shock/Volatility | Review commitments and avoid impulsive financial actions. | 13→4 | data.ts:1383 |
| PME=8 AND PM=5 | Money Pressure | Pay attention to resources, commitments and spending. | 13→4 | data.ts:1384 |
| PME=3 AND PM=4 | Create → Structure | Convert ideas into plans and test assumptions. | 7 | data.ts:1385 |
| PME=2 AND PM=7 | Detail Discipline | Check facts and be patient with process. | 9 | data.ts:1386 |
| PME=8 AND PM=3; bank also declares isDouble=true | Money Theme (Creative Month) | Keep creative projects and resource commitments clear. | 11→2 | data.ts:1387 |
| PME=8 AND PM=3; bank also declares isDouble=true | Surprise Factor | Preserve flexibility in projects and commitments. | 11→2 | data.ts:1388 |

The `isDouble` qualifier is **declared but never evaluated**. The code casts it as a possible condition at descriptions.ts:116, then only checks ESS, PY, PM and PME at lines119-122. Thus both PME8/PM3 rows currently fire whenever those two numbers match; no separate “double” requirement is enforced. The source does not define what “double” was intended to mean. It must not be invented.

These are annual/monthly **pair conditions**, not a universal danger ranking by COM digit. MCOM4 is shared by four monthly rows above, while several other ways to make4 are not listed as triggers. Sources: [rule rows](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/data.ts#L1379-L1388); [checks](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/descriptions.ts#L115-L126).

Current service formulas:

- PY = reduce(birth day + birth month + target calendar year).
- PM = reduce(PY + calendar month).
- Yearly ESS = name-cycle result.
- PME = reduce(Yearly ESS + PM).
- Annual COM = reduce(PY + Yearly ESS).
- Monthly COM/MCOM = reduce(PME + PM).

Source: [numerology.ts:52-84](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/numerology.ts#L52-L84), [numerology.ts:169-180](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/numerology.ts#L169-L180).

## Daily conditions: complete table

The daily evaluator defines **compoundRoot as the FIRST number in the reduction chain**, not every intermediate compound. For example, a chain29/11/2 has compoundRoot29 and final value2.

For `type: 'compound'`, a row matches only compoundRoot. For `type: 'value'`, a row matches **either final value OR compoundRoot**. Despite the name “value,” rows16,11,25 and29 can therefore match an initial compound. No row tests an arbitrary intermediate number.

| Exact bank condition | Existing rule title | Actual matching behavior | Source line |
|---|---|---|---|
| compoundRoot=11 | Health & Stress Checkpoint | Initial compound11 only. | data.ts:1364 |
| compoundRoot=13 | Accident/Disruption Window | Initial compound13 only. | data.ts:1365 |
| compoundRoot=16 | Lesson & Health Focus | Initial compound16 only. | data.ts:1366 |
| final value=7 OR compoundRoot=7 | Ground & Plan Day | Includes13? No; includes16/7 and25/7 because their final value is7. | data.ts:1369 |
| final value=16 OR compoundRoot=16 | Humility & Awareness Day | Current service final value is1–9, so it acts on initial16. | data.ts:1370 |
| final value=9 OR compoundRoot=9 | Release & Compassion Day | Includes any current final9 chain. | data.ts:1371 |
| final value=11 OR compoundRoot=11 | Insight & Sensitivity Day | Current service final value is1–9, so it acts on initial11. | data.ts:1372 |
| final value=25 OR compoundRoot=25 | Strategize & Center Day | Current service final value is1–9, so it acts on initial25. | data.ts:1373 |
| final value=29 OR compoundRoot=29 | Inspired Protection Day | Declared, but not reachable from the current main service's normal date formula (see below). | data.ts:1374 |

Examples showing overlap and raw-versus-reduced semantics:

- 11/2 → Health & Stress Checkpoint **and** Insight & Sensitivity Day.
- 13/4 → Accident/Disruption Window.
- 16/7 → Lesson & Health Focus **and** Ground & Plan Day **and** Humility & Awareness Day.
- 25/7 → Ground & Plan Day **and** Strategize & Center Day.
- 29/11/2, if supplied directly to the evaluator → Inspired Protection Day; the intermediate11 does **not** add the11 rules.

The current main service uses reduced calendar-day digit (1–9), PM(1–9), and PME(1–9), so its raw daily-essence sum cannot exceed27. Consequently the29 row is not reachable through the normal `getTimelineSliceForDate` path for valid dates. This is a source-derived bound, not a runtime test. The Advanced Timeline daily dialog uses the full calendar day and can create29, but it does not call the warning evaluator.

Sources: [main daily formula](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/numerology.ts#L86-L105), [Daily Essence final-value construction](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/numerology.ts#L145-L161), [Advanced Timeline daily formula](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/components/charts/AdvancedTimelineChart.tsx#L1086-L1104).

## Which UI paths consume the rules?

This is static call-path verification, not a live browser or deployed behavior claim.

| Path | What the source actually does |
|---|---|
| Year & Month screen | Calls getMonthInfo(selected month), which calculates PY/PM/ESS/PME and calls getMonthLevelWarnings. Displays the result as “Monthly patterns to watch.” This includes annual-labelled conditions because all13 rows share level='month'. |
| Home screen | Calls getTimelineSliceForDate(today), then renders its day-level warnings as “Critical Patterns.” |
| Day detail modal | Receives the selected day's timeline slice and displays its day-level warnings. It displays annual/monthly meanings separately but does not automatically add the13 annual/monthly warning rows. |
| Advanced Timeline chart and its internal daily dialog | Calculates number rows and compound tooltips; no call to either warning evaluator and no explicit caution-combination table found in this file. Its daily dialog uses a different raw-day treatment, so identical final digits cannot establish identical compound warnings. |
| CalendarView.tsx | Has a warning indicator based on slice.warnings. No imports/usages of this component were found in the fetched app source, so it must not be presented as an active route. |
| Year & Month calendar hover descriptions | Uses Daily Essence meaning summary/positive/caution text; that prose is separate from structured warningPatterns and the month warning list. |

Sources: [getMonthInfo](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/services/numerology.ts#L189-L217); [YearAndMonthScreen calls](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/components/YearAndMonthScreen.tsx#L217-L225), [warning display](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/components/YearAndMonthScreen.tsx#L334-L345); [HomeScreen](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/components/HomeScreen.tsx#L54-L60), [Home warning display](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/components/HomeScreen.tsx#L107); [DetailsModal](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/components/DetailsModal.tsx#L85-L126); [App routing](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/App.tsx#L249-L267), [App modal](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/App.tsx#L345-L352); [calendar hover prose](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/components/YearAndMonthScreen.tsx#L238-L245); [Advanced Timeline daily dialog](https://github.com/olsonan26/LOOKS-LIKE-COSTAR/blob/023140de4ac9ebad8a804b4c984337135e77b19a/components/charts/AdvancedTimelineChart.tsx#L1086-L1141).

## Implication for the proposed combination with Mystic Rebels

There is a real, inspectable repository rule bank to preserve. The annual4/9 and9/4 distinctions and the monthly directional pair distinctions can be compared with a separately sourced astrological context. But the source itself does not show that these numeric combinations predict danger, illness, accidents, relationship conflict or money loss, nor that a matching astrological theme raises a measured probability.

A faithful first comparison can say: “This numeric pair carries this source's caution theme; here is the independently sourced chart context; consider this practical reflective question.” It should not convert two symbolic warnings into a factual forecast. Annual/monthly orientation remains possible while daily numerology is excluded, as the user prefers.

No new warning rules, severity scores, astrological correspondences, or product behavior were added.

