# Mystic Rebels: U.S. war-onset backtest — October 31, 2026

## Executive result

**No demonstrated war-timing signal in the prespecified historical control comparison.**

Five *distinct formally declared U.S. wars* were compared to non-onset dates from each event's own calendar year. The frozen feature was the count of **outgoing transit-to-natal 0° conjunction contacts** using the PURE ASTROLOGY source-confirmed Orbs of Influence for the Sun (10°), Moon (3°), Mars (4°), and Pluto (1.5°). The *transit* is the emitting ecosystem; the natal body is the receiving ecosystem. We **never** add both planets' radii. Saturn ~7.5° is provisional and **not counted**.

| Prespecified comparison | Five U.S. war dates | Same-year non-onset dates | One-sided Monte Carlo `p` |
|---|---:|---:|---:|
| Outgoing source-confirmed transit conjunction contacts | 7 total; mean **1.40**/date | expected 5.25 total; mean **1.05**/date | **0.260** |
| Transit Mars conjunction contacts | 2 total | expected 0.98 total | **0.256** |
| Transit Pluto conjunction contacts | 1 total | expected 0.97 total | **0.967** |
| Uranus within 1° of U.S. founding Uranus | **0/5 dates** | 0 in these five comparison years | not informative |
| Any Uranus/Neptune/Pluto same-body 1° return | **0/5** | 0 in these five comparison years | not informative |

The randomization is a **same-calendar-year, stratified non-onset-date benchmark**: 100,000 draws, one sampled non-onset day for each of the five war years; exclude the ±30 days surrounding each first formal U.S. declaration. It is not a test against genuinely verified peaceful years; many control dates occur **during wars**. It is deliberately a conservative *onset-day versus other-day* comparison, not a general war/not-war classifier.

A p-value of 0.260 offers **no meaningful evidence of onset-day enrichment** for the directional-conjunction count. These were exploratory analyses assembled after past wars were already known; the p-values are descriptive, not confirmatory scientific significance or proof of predictive accuracy. The 5 cases are few, and the features/parameters were not fixed before the earlier retrospective discoveries.

## Dates and event definitions

**Primary cohort (first U.S. signed formal declaration for each of five distinct wars):** June 18, 1812; May 13, 1846; April 25, 1898; April 6, 1917; December 8, 1941. The legal dates are recorded by Congress and the U.S. Navy (sources below). The 11 individual declarations are **not** 11 distinct wars.

**Secondary, description-only cohort:** Fort Sumter Apr. 12, 1861; WWII European outbreak Sept. 1, 1939; D-Day June 6, 1944; Korea Jun. 27, 1950; Gulf of Tonkin Resolution Aug. 7, 1964; Desert Storm Jan. 17, 1991; Afghanistan Oct. 7, 2001; Iraq Mar. 20, 2003; Russian invasion of Ukraine Feb. 24, 2022. The secondary dates are **heterogeneous** and must not be silently pooled with direct U.S. declarations.

## Uranus return — the prior headline observation

The U.S. founding *astronomical* reference Uranus = Gemini ~8.90° on July 4, 1776, 12:00 **UTC**. Uranus on Fort Sumter's date was ~0.45° from that reference; on D-Day ~0.44°. Their apparent closeness to their respective exact returns is real astronomy but is **post-selected** in historically complex periods. Even within 1° of that natal longitude, Uranus stayed there approximately **177 calendar dates in 1860–1861** and **131 calendar dates in 1943–1944**. Such extended intervals make it easy to find a major event after knowing where to look.

For the next cycle (again, **astronomical reference, not a war forecast**) Uranus lies within 1° of the same reference for approximately **163 calendar dates in 2027–2028**, partitioned as:

- July 4 – September 3, 2027 (62 days)
- September 27 – November 30, 2027 (65 days)
- April 23 – May 28, 2028 (36 days)

No reasonable war risk estimate or date prediction follows from these orbital windows.

## Source-fidelity boundaries

- **No houses or True Placement interpretation.** A nation's exact July 4, 1776 chart time is not established by an exact historical clock record. The repository's certified SWIEPH astronomy is 1800–2399, so the 1776 positions were sampled with **MOSEPH** Swiss-family approximation, which is intentionally labelled exploratory. The sample instant is 12:00 **UTC**, which must not be confused with 12:00 **Philadelphia local time**.
- **No outgoing OOI asserted for Uranus or Neptune.** Their return calculations are raw ecliptic-longitude proximity indicators, not source-verified aspects. Saturn's OOI approximation is flagged provisional and excluded from the score.
- **Only conjunctions.** Other aspect geometries, Aspect Arc, Fringe, Vantage, Exactitude ordering, progressed charts, Spark, and natal house/ruler relationships have NOT been implemented by this research module. The production chart generator's `aspects` capability remains BLOCKED; this module must not be advertised as a replacement.
- **No future outcome labels.** No World War III prediction is provided. The presence of known wars at past orbital return dates is not causal evidence, and military conflict can occur without return patterns.

## Run

Requires Python with `pyswisseph` and no network:

```sh
python -m unittest -v astronomy_qa.test_source_conjunctions
python -m research.usa_war_2026.war_case_controls
```

Output file `research/usa_war_2026/historical_test_results.json` is written by the second command. The study uses deterministic random seed 20261031. A mathematical reference epoch is used; this does **not** call a deployed private chart API.

## Next research gates

1. Secure a fully attested PURE ASTROLOGY table for all directional OOIs and every supported angle. Verify actual author-specific Aspect Arcs and Fringe behavior with independently documented examples before changing production `RULES` statuses.
2. Acquire a historically documented founding time or predeclare a set of plausible times, rather than optimizing birth time to wars. Improve 1776 astronomy using independently validated historical ephemeris assets, not silently Moshier or adjusted zodiac.
3. Pre-register one *single* outcome definition (e.g., U.S. new armed conflict onsets with independently documented day, and a defensible daily no-onset control universe), then evaluate blind chronological holdouts with a false-alarm count, precision, recall, base rates, and confidence intervals.
4. Include counterexample studies: Uranus-return windows without U.S. escalation; wars and crises with no relevant return. Do not select conspicuous events because they are near attractive astrological dates.

## Sources

PURE ASTROLOGY — Nadia Canonical Source v1, pp. 236–246 and 161–165 (private source provided by owner). Repository `mystic_rebels/service.py` and `docs/PRECISION.md` (configuration and blocked capabilities).

- U.S. Senate: https://www.senate.gov/about/powers-procedures/declarations-of-war.htm
- U.S. Navy war dates: https://www.history.navy.mil/content/history/nhhc/research/library/online-reading-room/title-list-alphabetically/d/declarations-war-authorizations-use-military-force.html
- National Archives, July 4 adoption: https://www.archives.gov/founding-docs/timeline
- National Archives, Fort Sumter: https://www.archives.gov/milestone-documents/telegram-announcing-the-surrender-of-fort-sumter
- National WWII Museum, June 6: https://www.nationalww2museum.org/media/press-releases/d-day-fact-sheet-0