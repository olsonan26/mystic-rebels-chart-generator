# Mystic Rebels / PURE ASTROLOGY: The U.S. and World War Onset Evidence Audit
**Research date: October 31, 2026 | Source-scope: source-defined outgoing conjunctions only | NOT a World War III forecast**

## Executive answer
This investigation did **not** assume war patterns must fit or must fail. It found two **exploratory positive differences** against nearby calendar dates but neither persisted when compared to randomized dates throughout the same years. The U.S. apparent result also changed when the event dates were shifted by one day. There is no validated predictive model or probability of World War III in the results.

The dataset was not selected by searching for attractive dates: it was taken as all **95 distinct Correlates of War (COW) Inter-State War v4.0 conflicts** with an earliest participant start date, 1823–2003. For comparison with the United States, this audit used the **13 COW-coded U.S. interstate participant start dates** (not U.S. congressional declaration dates; different endpoints). The 95 war dates and 13 U.S. dates are frozen in the CSV and Python script.

## Source and provenance
- Book: **PURE ASTROLOGY — Nadia Complete Edition**, house/planet/sign/ruler interpretation, transit-versus-natal distinction and source-defined Orbs of Influence. Do not interpret PHSR without a valid founding time.
- Outgoing 0° conjunction radius applied to the *transiting emitter only*: Sun 10°, Moon 3°, Mars 4°, Pluto 1.5°. Never add an orb from another planet. This study does NOT assume Uranus/Neptune outgoing influence thresholds, Saturn (provisional), or standard astrology aspect thresholds.
- Orb values were originally recovered in the user’s Phase 8 source audit. The user’s current repository has advanced directional aspects **BLOCKED**, so this is a discrete research implementation, not a claim that the full engine runs.
- Astronomical calculations use Swiss Ephemeris **Moshier** (MOSEPH) tropical geocentric longitudes. The user’s certified SWIEPH repository only supports 1800–2399; the 1776 founding planetary positions here are a **separately labeled astronomical proxy**, never a full certified U.S. natal chart.
- U.S. Declaration was adopted July 4, 1776, but no defensible minute/second precision for the founding moment. The reference instant was set to **12:00 UTC** (NOT noon Philadelphia); its Moon and all house-dependent True Placements are excluded.
- Official COW dataset page: https://correlatesofwar.org/data-sets/COW-war/ . Date codebook: https://correlatesofwar.org/wp-content/uploads/Inter-StateWars_Codebook.pdf . Data rows: https://raw.githubusercontent.com/onurkulak/yearsPassedWithWars/master/Inter-StateWarData_v4.0.csv (archival mirror of COW v4.0).
- COW StartMonth1/StartDay1/StartYear1 refer to **the onset of sustained fighting for a particular participant**, NOT declaration dates; each WarNum is counted only once for the worldwide cohort, using the earliest participant date. When extracting American involvement, use the U.S. participant row, not the worldwide start.

## Frozen cohorts and controlled comparisons
- All 95 inter-state wars (1823–2003): test astronomical source-defined contacts in the *Universal ecosystem* (transiting emitter → other transiting body), plus secondary transit→U.S. founding longitude probes.
- 13 U.S. participation starts from COW (1846–2003): test source-defined incoming transits against U.S. founding longitudes, excluding natal Moon.
- **Month control (main):** sample dates within the *same calendar month and year*, excluding only days that were themselves coded war starts. This avoids biasing the benchmark by removing the entire duration of a conjunction around the start date.
- **Year control (robustness):** randomly sample dates from the entire same calendar year, excluding only the actual start dates. This tests whether the month comparison merely captures a season/period effect.
- For each event, independently sample one eligible matched date, repeat **100,000 Monte Carlo replicates** with fixed seed 20261031. Report a one-sided p-value for counts at least as high as the observed counts. Multiple-feature familywise values are exploratory maximum-statistic adjustments across 13 correlated measures.
- **Important statistics caveat:** shared years, correlated slow planets, month effects, reused epochs, multiple tested features, and event-date uncertainty all make these descriptive randomization contrasts, not confirmatory causal proof. The controls may still be dates during ongoing wars.

## All-event results (95 inter-state wars)
| Tested source-grounded measure | War onsets (95) | Month-matched expected | Month p(↑) | Year-matched expected | Year p(↑) |
|---|---:|---:|---:|---:|---:|
| All Universal outgoing conjunctions | 127 | 123.87 | 0.3704 | 126.73 | 0.5026 |
| Universal outgoing Mars contacts | 20 | 19.30 | 0.4687 | 21.56 | 0.6708 |
| Universal outgoing Pluto contacts | 8 | 6.37 | 0.2954 | 7.11 | 0.4161 |
| Mars→Saturn | 0 | 0.80 | 1.0000 | 2.03 | 1.0000 |
| Mars→Pluto | 4 | 2.11 | 0.1196 | 2.29 | 0.1937 |
| Pluto→Mars | 1 | 0.77 | 0.5692 | 0.91 | 0.6048 |
| U.S. any same-body outer planet return ≤1° (non-aspect diagnostic) | 1 | 0.83 | 0.8265 | 2.13 | 0.9277 |

**Investigated positive indication:** the narrow **transit Mars→transit Pluto conjunction** occurs on 4 of 95 war-onset dates, against ~2.11 month-matched expected (one-sided p≈0.120, exploratory familywise p≈0.478); the year-matched expected is ~2.29 (p≈0.194). These figures are not unusually strong after testing 13 features.
The four COW-coded global war-onset dates with this Mars→Pluto source-radius contact are:
- 1876-03-27 — First Central American (Mars–Pluto longitudinal separation 2.30°, compared with outgoing Mars radius 4°).
- 1900-07-17 — Sino-Russian (Mars–Pluto longitudinal separation 2.97°, compared with outgoing Mars radius 4°).
- 1906-05-27 — Third Central American (Mars–Pluto longitudinal separation 2.09°, compared with outgoing Mars radius 4°).
- 1947-10-26 — First Kashmir (Mars–Pluto longitudinal separation 0.88°, compared with outgoing Mars radius 4°).

These are *not* the dates of U.S. entry into the two World Wars. The strongest observed global signal is thus not a "World War I/II signature."

## U.S.-involvement results (13 COW U.S. participant start dates)
| Tested measure | U.S. starts (13) | Month-matched expected | Month p(↑) | Year-matched expected | Year p(↑) |
|---|---:|---:|---:|---:|---:|
| Total incoming source-defined conjunction contacts | 17 | 12.54 | 0.0234 | 12.58 | 0.1399 |
| Incoming Mars contacts | 2 | 2.35 | 0.8152 | 2.52 | 0.7363 |
| Incoming Pluto contacts | 2 | 2.00 | 1.0000 | 1.47 | 0.4867 |
| Transit Mars→natal Mars | 1 | 0.71 | 0.5868 | 0.25 | 0.2232 |
| Uranus near its 1776 longitude ≤1° (not a verified aspect) | 0 | 0.00 | 1.0000 | 0.00 | 1.0000 |

**Investigated positive indication:** 17 incoming source-defined conjunction contacts versus ~12.54 within-month expected (p≈0.023), but ~12.58 year-matched expected (p≈0.140). Multiple-feature corrected month p≈0.116. There is a *modest exploratory month-scale difference*, but no consistent annual benchmark result.
A small sample of 13 events is extremely sensitive to coding choices and exact dates. For full transparency:

| U.S. participant date in COW | War / episode | Source-defined transit→founding contact(s) |
|---|---|---|
| 1846-04-25 | Mexican-American | Mars→Mars (1.29°) |
| 1898-04-22 | Spanish-American | None |
| 1900-06-17 | Boxer Rebellion | Sun→Venus (6.79°); Sun→Mars (4.71°) |
| 1917-04-17 | WWI COW participation | Pluto→Venus (0.07°) |
| 1941-12-07 | WWII COW participation | Moon→Mercury (0.65°) |
| 1950-06-27 | Korean | Sun→Sun (7.66°); Sun→Venus (2.68°); Sun→Jupiter (0.58°) |
| 1965-02-07 | Vietnam Phase 2 | None |
| 1968-01-13 | Laotian Phase 2 | Sun→Pluto (5.19°); Pluto→Neptune (0.36°) |
| 1970-05-01 | Communist Coalition | Mars→Uranus (0.21°) |
| 1991-01-16 | Gulf War | Sun→Pluto (1.71°) |
| 1999-03-24 | Kosovo | Moon→Venus (1.73°); Moon→Jupiter (1.52°) |
| 2001-10-07 | Afghanistan | Sun→Saturn (0.51°); Moon→Uranus (2.27°) |
| 2003-03-19 | Iraq | Moon→Saturn (1.46°) |

## Bias check: an attractive result we **rejected for a specific reason**
An initial month control excluded every day within ±7 days of a known war onset. Under that setup, the 4 Mars→Pluto events compared with only ~1.21 expected and a one-sided p≈0.0056 (familywise p≈0.0245).
**That exclusion is invalid for this hypothesis**: it systematically removes nearby days that often share the same multi-day Mars→Pluto transit condition, artificially lowering the comparison rate. Removing that exclusion and sampling every eligible day in the same month changes the result to 4 vs ~2.11, p≈0.120. The broader year control gives p≈0.194. This was an audit correction, not a decision to suppress evidence.
Likewise, the original U.S. sample under the ±7-day filter suggested 17 vs ~12.17, p≈0.0118. The properly specified month benchmark gives 17 vs 12.54, p≈0.0234; this does not survive adjustment for 13 investigated measures or the year baseline.

## Chronological split (same exact feature without refitting)
- Global Mars→Pluto, first 47 COW wars (1823–1929): 3 events vs 1.31 expected, p≈0.104.
- Global Mars→Pluto, next 48 COW wars (1931–2003): 1 event vs 0.80 expected, p≈0.639.
- U.S. total incoming conjunctions, first 6 COW starts (1846–1950): 8 vs 6.96, p≈0.349.
- U.S. total incoming conjunctions, later 7 starts (1965–2003): 9 vs 5.58, p≈0.014.
These splits are **retrospective sensitivity checks**, not a true untouched holdout. They show unequal concentration across the historical period.

## Date sensitivity and founding-time sensitivity
- Shifting all 13 U.S. participation dates **one day earlier** reduces incoming contacts from 17 to 14; shifting them **one day later** reduces 17 to 13. A one-day uncertainty matters for fast lunar transits.
- In the universal 95-war Mars→Pluto feature, shifting all dates one day earlier produces 5 matches; the actual dates produce 4; one day later gives 4. A very broad multi-day conjunction can survive a day shift.
- With founding *reference* longitudes recalculated at 00:00, 06:00, 12:00, 16:00, 20:00 and 23:00 UTC July 4, 1776, the sum of 13-event incoming contacts was respectively **18, 18, 17, 17, 17, 17**. This is not a birth-time rectification; **houses/True Placements are entirely missing**, which is a far larger limitation than one contact.

## 2027–2028: measurable configurations, NOT a World War III prediction
- For U.S. reference Uranus Gemini ~8.90°, the planet stays within *raw astronomical* 1° longitude for **163 calendar days** across July–November 2027 and April–May 2028. No verified Uranus outgoing orb is used, and raw proximity is not an author-defined aspect.
- **January 6–16, 2028** (UTC reference dates) is the next identified **Universal Mars→Pluto ≤4° outgoing conjunction** within the requested 2026–2028 window. This is a source-defined angular *contact*, but the 95-war comparison did not demonstrate reliable war-onset discrimination.
- There are **61 days** in calendar years 2027–2028 with three or more incoming source-radius contacts to the fixed founding longitude reference. Without a verified event classifier this produces many possible dates, not a unique prediction.
- No model here supports any probability, specific geopolitical opponent, war declaration, or World War III date.

## Proper next scientific and source-fidelity gates
1. Verify author-specific Aspect Arc, forced/mutual reach, Fringe, ruler direction, and all outgoing orbs from original photographed pages; do not substitute traditional zodiac/aspect rules.
2. Choose a source-justified national ecosystem origin, establish how the system reads collective/national entities, and avoid inventing a July 4 birth clock. Run sensitivity over plausible epochs, not arbitrary selection of a chart that fits wars.
3. Include verified peace periods, not just other days *within* war years; use the same units of observation. Match date uncertainty and account for overlapping wars.
4. Freeze **one** operational feature and event definition before looking at an independent held-out era (e.g., UCDP 2004–2025 with consistent coding, separately sourced). Record every false alarm and missed conflict.
5. Report effect sizes, base rates, multiple-testing adjustments, false-positive rates, and predictive scores in the public research ledger. No changes to the production chart interpretation without regression tests.

## Reproduction
Install `pyswisseph` and `numpy`, then run `python run_research.py`. The script reads `cow_interstate_onsets_1816_2007.csv` and writes `research_results_unbiased_controls.json`. The earlier exclusion-biased output is retained solely to illustrate the correction. The dataset is a COW v4.0 subset (public archival mirror), not an original dataset of historical events invented for this hypothesis.

## Bottom line
**Evidence that fits:** some source-defined contacts appear more often near U.S. participation starts within the same months; 4 global wars begin under a Mars→Pluto conjunction.
**Evidence that does not fit:** the pattern is not robust to matching controls across entire years; the earlier seemingly significant Mars→Pluto result relied on an invalid exclusion rule; the correlations do not consistently occur at the major World War onsets; no national house/True Placement layer has been validated.
**Therefore:** important hypothesis-generating observations; *not* evidence that war is forecastable by the system, and not evidence that the system is necessarily incapable of useful predictions. We do not know until source-complete, locked, forward-tested rules are available.