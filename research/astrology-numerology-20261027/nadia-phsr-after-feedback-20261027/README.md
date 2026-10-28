# Nadia PHSR+ case study and next implementation scope

Prepared 27 October 2026, America/Denver. **After-feedback analysis. Research artifacts only.**

The full handoff was read. Existing work and the frozen first-pass trial were preserved. The supported analysis is completed in four linked documents plus a reader-facing draft:

1. [Source/rule matrix](SOURCE_RULE_MATRIX.md): exact witnesses, calculation requirements, implementation status, retained conflicts and eight specific decisions.
2. [Manually worked case](NADIA_WORKED_CASE.md): Chiron -> Sun -> Moon -> Neptune -> Saturn -> Uranus -> Saturn, in the requested seven-stage order. Includes the actual Delegate occupants, the separate Jupiter/Mercury decan route and the Aries/H4 -> Mars -> Venus activation-context route.
3. [Timing and ESS/PY/COM comparison](TIMING_AND_NUMEROLOGY.md): age-degree versus transits, all new Chiron major contacts, original misses/nonmatches, the age 18 journal comparison, and a future blind-test design.
4. [Concrete implementation plan](IMPLEMENTATION_PLAN.md): existing integration points, exact records and graph behavior, proposed files/increments, meaningful verification and source decisions still needed.
5. [Reader-facing draft](NADIA_READER_DRAFT.md): substantive conditional prose without source-name clutter or invented events.

## Main findings

- **The father-related route is reconstructable without moving the Sun.** Direct Chiron is H8/Leo, second decan Sagittarius; its actual sign ruler Sun is H7/Cancer, then Moon H3/Pisces. The chain continues through Neptune H1, Saturn H2 and Uranus H1. The later disclosed abuse remains reported history, not a fact discovered from this reconstruction.
- **A primary page adds fractional-age support.** Original printed 257 explicitly maps 0°30′ to six months. Original 255 gives 30-year recurrence. Chiron 11°02′26″ therefore supports a candidate at age 11.040694, approximately 1-2 August 2003 under two stated calendar conventions. It does not establish an abuse onset or a verified manifestation date. The different Spark candidates remain unresolved.
- **Chiron adds real calculation detail at age 18, after feedback.** The new scan finds Chiron-Moon equalities 11 March 2011,14 September 2011 and 5 January 2012. The 1 July 2011 journal date has no exact contact in the new selection; reference Chiron is about 3.12° from Moon, beyond its documented 1° outgoing radius. The old sparse age 18 result is not rewritten.
- **The numerology reproduces exactly.** All 10 frozen annual states and 98 month states, including indicators, match the unmodified compiled STAFFprofiler engine. COM's documented role is constructive approach; ESS/PY/COM retain their separate formulas, categories and trails.
- **The comparison does not establish predictive improvement.** Within preserved trial windows, the new major Chiron-to-chain contacts split 6 red /6 green. The original 31/59 red contacts versus 56/98 red month cells still shows no obvious enrichment. Police-report timing around 21 remains too imprecise for an exact-date score.

## Evidence and preservation

`frozen-trial-verification.json` verifies all seven original manifest entries. `preservation-before.json` and `preservation-verification.json` compare every Git-listed tracked/untracked source file in Mystic and STAFFprofiler, the separate prototype, and every frozen-trial file. Source identities were checked in their actual checkouts: Mystic branch `codex/methodology-verification-20261024` at `3d83db75c30b26d9b068576d84ec49554822fd8c`; STAFFprofiler at `4172789db1034072f50c78178187e839fa710fb5`.

LOOKS-LIKE-COSTAR is a downloaded source-text snapshot, not an independent Git checkout. Its recorded source commit is `023140de4ac9ebad8a804b4c984337135e77b19a`. All 102 local files have one additional trailing LF compared with their recorded Git blobs; removing that LF in memory reproduces all 102 blob hashes. Frozen bytes were not repaired. The parent workspace Git revision was not substituted for the snapshot identity.

Original scans and compiled text remain distinct. Five original pages were visually inspected here:215,216,255,257,686. Seventy-seven selected cached passages have matching text hashes; original image hashes were checked separately. Complete interpretation approval is not inferred from acquisition, OCR, image review or arithmetic.

`RESEARCH_MANIFEST.json` records the new output hashes. `calculate_research.py` and `verify_numerology.mjs` reproduce the separate research calculations without writing to applications or the frozen trial. `collect_evidence.py --verify-only` performs the preservation comparison. `expanded-contacts.csv` retains the full 142-contact selection, including additional 30°/150° geometry and ages omitted from the old trial.

All substantive new claims are explicitly after-feedback. No application code, original knowledge register, deployment, database, memory file or frozen first-pass document was changed.
