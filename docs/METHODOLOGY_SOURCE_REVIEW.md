# Alchemystic Astrology source review

Reviewed for Mystic Rebels on 2026-10-24. Source fidelity, astronomical calculation accuracy, and evidence for an interpretation are separate assessments. No source statement in this review establishes scientific validation of an interpretation.

## Source identity and page numbers

The supplied `reference/source_pdf/PURE_ASTROLOGY_Nadia_Complete.pdf` contains 692 PDF pages, 1,375,464 bytes, SHA256 `9d5fb55cf6d4f2134ed780c2694503d2dde42bdad68add60ff35acef0237161d`. Its metadata title is `PURE ASTROLOGY - Nadia Complete Edition`; ReportLab created the reflowed file. Text extraction produced 1,014,743 characters with boundaries preserved for all 692 pages. The PDF is a reference, not a direction to change Mystic Rebels branding.

There are **three distinct numbering systems**:

1. PDF page: one-based page in this 692-page file.
2. Reflow footer: the number printed at the bottom of the generated page, normally PDF page + 4.
3. Original printed page: an embedded page number from the source book, often present in a heading, `Page n`, or `-----n` divider. Multiple originals can occur on one PDF page.

For example the four Gradities appear on **PDF 203 / reflow footer 207 / original printed 143**, not original printed 207. The original book's printed 207 instead appears in the table of contents as Bidirectional Rulership. Citations below specify all available identifiers; ranges do not imply every original page in that range survived compilation.

### Coverage and visual inspection

The **complete 692-page PDF received a page-bounded semantic review** across the three review workers: PDF 1-230 (feature reviewer), PDF 231-460 and 581-692 (methodology reviewer), and PDF 461-580 (astronomy reviewer). Each reviewer read full page-bounded text rather than keyword matches alone and reread truncated output. The methodology reviewer additionally read every Gradity/Sophia/perigee/apogee match throughout the file. The machine-readable evidence records these confirmed worker ranges separately from full-file extraction. This completes review of the supplied file, not recovery of the original book pages it omits.

The source is not a facsimile. Only six embedded images exist, and many apparent diagrams have become bare headings or OCR-like strings. Rendered inspection checked PDF 203, 292-297, 343, 421-422, 431, 434, 458, 475-477, 499-500, 502, and 508. In particular:

- PDF 499-503 (reflow 503-507) show isolated headings for Orbital Focus, Lunar Apogee, Empty Earth, Lunar Perigee, and Lunar Path. They do not contain a recoverable lunar-orbit diagram.
- PDF 475 (reflow 479) contains Prograde Begins / Earth Orbit labels, without a recoverable orbit diagram.
- PDF 421 ends a sentence in the introductory discussion; PDF 422 starts midway through original 493. Original Progressions 491-492 is absent from the compiled body.
- PDF 507 proceeds from Lilith Arc into PDF 508's Sophia text at original 620, beginning mid-sentence. Original 617-619, including the Sophia chapter opening, is absent.
- PDF 294 jumps from the opening OOI discussion to a 239 divider. PDF 296 jumps from the Mars 5 / Saturn 8 question to original 244. The original 238 Sun / 240 Saturn passages and 242 Fringe diagram cited by the older research are not reproduced here.

These are source-package gaps confirmed by rendered pages, not text-extraction failures. Prior research claims to have seen original photos, but those photos are not installed in this repository's `reference` folder. A secondary research description is not the missing primary image.

## Findings and comparison to implementation

### Gradity: source-defined phases, formerly missing event calculations

**Source:** PDF 203 / reflow 207 / original 143 explicitly lists Prograde, Pregrade, Retrograde, Postgrade. PDF 476 / reflow 480 discusses exact directional stations as Inertial Points; the original page identifier for that fragment is not visible. PDF 477 / reflow 481 / original 569-570 repeats the operative degree rules.

**Method:** Let R be a station from positive to negative geocentric ecliptic-longitude speed, and D the following negative-to-positive station. Pregrade begins at the prior forward crossing of the longitude reached at D. Retrograde occupies the R-to-D traversal. Postgrade ends at the later forward crossing of the longitude at R. Forward motion outside the shadow intervals is Prograde when the adjacent event search establishes that exclusion. Signed speed alone cannot distinguish the three forward phases. Longitude must be unwrapped when a loop crosses 0 Aries.

**Former implementation:** `web/src/gradeity.ts` recognized Retrograde from motion but returned no phase for all forward-moving bodies. Its future cycle classifier accepted event timestamps but did not calculate them. `mystic_rebels/service.py` supplied speed, without a loop-event search. The actual unavailable label was Gradity's **Unverified** table/inspector fallback.

**Supported improvement:** Solve actual station and boundary events using the existing ephemeris; verify those events against an independent reference using the same time scale, frame, correction convention and body center. Expose the events and phase provenance. Search failure or insufficient event range remains unavailable, not a guessed Prograde.

**Exactness limits:** The source does not assign equality at boundary instants and does not give a near-zero stationary speed threshold. Retain an explicit boundary/unresolved phase at the mathematical events. Its day-before/day-of/day-after discussion describes interpretive significance; it does not define a three-day astronomical stationary state. Sun and Moon do not form the planetary retrograde loops described here (PDF 271-272 / reflow 275-276 / original 194-195); distinguish not-applicable from unverified.

### Spark: contradictory rules and a newly located example

**Source:** PDF 292 / reflow 296 has an odd/even **sign** discussion before the original 235 divider. PDF 293 / reflow 297 / original 235-236 then directs odd/even **house** arithmetic. PDF 433 / reflow 437 / original 509-510; PDF 434 / reflow 438 / original 510; and PDF 435 / reflow 439 / original 511-512 supply conflicting worked cases.

With zero-based zodiac indexes, integer degree `g = floor(longitude % 30)`, one-based house `H`, and one-based astronomical sign `Z`:

`candidate_H = (g + (6 if H is even else 0)) % 12`

`candidate_Z = (g + (6 if Z is even else 0)) % 12`

| Source case | PDF / reflow / original | House candidate | Sign candidate | Source label |
| --- | --- | --- | --- | --- |
| Progressed MC Gemini 14°50, H10 | 433 / 437 / 509 | Sagittarius | Gemini | Gemini |
| Progressed Mercury Leo 2°28, H12 | 433 / 437 / 509 | Sagittarius | Gemini | Gemini |
| Austin MC Aries 10°57, H10 | 434 / 438 / 510 | Leo | Aquarius | Aquarius |
| Austin Mars Libra 5°56, H4 | 434 / 438 / 510 | Pisces | Virgo | Pisces |
| Los Angeles MC Pisces 18°39, H9 | 435 / 439 / 511 | Libra | Aries | Aries |
| Composite Ascendant Virgo 20°, H1 | 458 / 462 / 546 | Sagittarius | Gemini | Gemini |
| Composite Saturn Libra 28°, H2 | 458 / 462 / 546 | Aquarius | Leo | Pisces |
| Composite Jupiter Sagittarius 6°, H4 | 458 / 462 / 546 | Aries | Libra | Libra |

The composite Saturn line was visually checked on PDF 458: it really says 28°, Pisces degree, and Gemini decan. **Neither proposed parity formula reproduces it.** Do not silently change the degree, sign, or source label. H and Z agreeing in an odd-ordinal rising template cannot decide the rule; those templates mathematically give identical parity.

**Implementation:** Production `placements.derive` keeps `spark: null`, and `RULES.spark` remains blocked. `phase10Research.sparkParityResearchCandidates` correctly preserves both integer-degree candidate indexes and canonical null. Candidate arithmetic can be regression-tested; a canonical interpretation cannot yet be verified.

### Fusion Cusp Areas: diagnostic widths, not a replacement placement

**Source:** PDF 431 / reflow 435 / original 507-508 specifies 5% of sign/decan/degree widths: 1°30, 30 arcminutes, and 3 arcminutes. PDF 434 / reflow 438 / original 510 calls Austin Mars 5°56 a Pisces Spark with Aries FCA.

**Comparison:** Austin MC 10°57 is exactly 3 arcminutes before the next degree and fits the stated degree width. Mars 5°56 is 4 arcminutes from 6°, so it fails that same width. Its printed FCA claim contradicts the numeric rule. The existing `approachingFusionCusps` diagnostic matches the numeric widths and correctly leaves Mars outside. It deliberately provides no after-boundary strength. The PDF's decan wording refers to first/last spill but supplies no complete exception/weighting algorithm.

**Post-boundary examples also exist:** PDF 612 / reflow 616 / original 732 calls Interamnia 0°12 Virgo in H2 an FCA affecting H1 and H2; PDF 683 / reflow 687 / original 956 calls 0 Aries within FCA. Therefore an approaching-only detector must explicitly say it is partial. These examples support the existence of blending after a sign boundary but do not supply an unambiguous weighted strength, sign/house reassignment, retrograde rule or all-scale exception procedure.

**Required tests:** all three threshold exactitudes, just inside/outside, 359.999/0 wrap, exact cusp, invalid numbers, and the unchanged 5°56 counterexample. Diagnostic inclusion does not change the primary astronomical sign, Whole Sign house, Tone, Pulse, or Spark.

### Directional aspects and OOI: partial examples, incomplete universal engine

**Direct primary support:** PDF 295 / reflow 299 / original 239 explicitly gives Moon radius 3° each way and the 15°23 example spanning 12°23-18°23. PDF 297 / reflow 301 / original 245-246 rejects summed radii across ecosystems, distinguishes Saturn-to-Moon from Moon-to-Saturn, and gives Chiron's 1° OOI. PDF 457 / reflow 461 / original 543 reiterates a one-way Venus-to-Pluto Synastry example. Preserve source/target direction and chart context separately from a symmetric angular separation.

**Newly confirmed contradiction:** PDF 343 / reflow 347 / original 378 says Pluto reaches 1.5°, then advances 24°42 only to 25°42 (1°), and treats Moon 25°57 as unreached. A literal 1.5° reaches 26°12, which includes that Moon. These two claims cannot both define the same radius.

**Research comparison:** The existing Phase 9 research describes original photos for Sun 10°, Mars 4°, Saturn approximately 7.5°, and the 8°02-9°56 Mars/Saturn Fringe interval. The supplied PDF omits those primary passages/diagram. The original Moon3 and Chiron1 survive; the universal outgoing catalog for Mercury, Venus, Jupiter, Uranus, Neptune and the asteroids does not. Saturn's approximate qualifier must survive if the photo-supported diagnostic is used. Pluto requires a conflict flag.

**Implementation:** `RULES.aspects` correctly blocks the complete aspect network. `outgoing_emission:false` for mathematical points must not become a zero-radius emitter at exactitude. A selected example or interval diagnostic cannot support a full directional wheel or Energy Flow narrative. The major-angle definitions, aspect-specific bands, 180 hand-offs, Turnover/Fringe priorities and receiving-point exceptions are not a complete executable specification in this PDF.

### Sophia: preserve unavailable while the governing source is missing

**Source:** PDF 504 / reflow 508 / original 612-to-614 fragment describes lunar apogee/perigee and rejects interpolated lunar points. PDF 508 / reflow 512 / original 620 gives Mean Priapus at 29° Gemini and says an osculating Lilith retrograde implies an osculating Sophia retrograde. PDF 509 / reflow 513 / original 621-622 gives osculating Priapus at 13° Cancer. PDF 512 / reflow 516 / original 623 describes the arc between Mean and True Sophia, without a numeric arc-selection formula. Original 617-619 is missing, visually confirmed.

**Implementation:** `SophiaMean` and `SophiaTrue` remain disabled in `catalog.py` because their methods are not yet verified. Their requested API records report unavailable with RULE_NOT_VERIFIED. This is a missing primary definition/independent comparison problem, not missing numeric ephemeris assets alone.

**Astronomical distinction:** The osculating Kepler ellipse has opposite perigee/apogee directions; a natural/interpolated lunar perigee is a different construction. Establishing one physical construction accurately does not establish which the missing Sophia chapter names. Do not substitute a generic White Moon/Selena cycle or an interpolated-perigee constant. The PDF's untimed, rounded author examples cannot be used as high-precision numerical fixtures.

### Progressions, activations, return phases and interpretation

**Progressions:** PDF 254-255 / reflow 258-259 / original 182-184 discusses Ascendant flips; PDF 422 / reflow 426 / original 493 starts after the missing Progressions chapter; PDF 430-435 / reflow 434-439 / original 506-512 layers Progressed/Natal/Relocated charts. None specifies day-for-year mapping, time scale, angular advancement, target epoch, or relocation coupling. Preserve `RULES.progressions` as blocked. Do not infer conventional secondary progressions or solar arcs.

**Age-degree activation:** PDF 299-303 / reflow 303-307 / original 247-254 then 262 describes undated or approximate life events and retrograde delay, not a timestamp algorithm. Original printed 255's 2/32/62/92 example is present only in the older photograph-based research, not this PDF body. The existing integer-degree age-label helper is consequently a secondary-source diagnostic; fractional-day prediction remains unresolved.

**Phased returns:** PDF 441-442 / reflow 445-446 / original 518-to-520 fragments states Solar Conjunction through next Semisextile, then to Sextile, and gives repeated Saturn phase examples. PDF 443-447 / reflow 447-451 / original 521-524 discusses context and concurrent luminary phases. It supplies useful event definitions but no fully ordered retrograde phase/re-entry selection, equality convention, geographic anchoring and priority algorithm. Event root finding can be tested independently; full phase interpretation stays blocked.

**Interpretation order:** PDF 283 / reflow 287 / original 215-216 gives Planet → House → Degree → Decan → Aspects → Sign → Ruler, with a note that the sign is technically assessed before interpreting degree/decan/aspects. PDF 383 / reflow 387 / original 448-449 gives the FREE-theory forward/reverse house sequence. PDF 450-451 / reflow 454-455 / original 532-534 distinguishes connected `with` from concurrent independent `while`. These are source-faithful structural statements, not permission to generate a complete reading from an incomplete aspect graph.

### Existing verified placement rules crosschecked

- Modern rulers: PDF 257-258 / reflow 261-262 / original 185-187 agrees with the implementation's twelve modern rulers.
- Triplicity decans: PDF 289-291 / reflow 293-295 / original 227-230 agrees with `(sign_index + 4 * floor(degree_within_sign / 10)) % 12`, and explicitly sets the 10° and 20° transitions.
- Whole Sign houses: PDF 245-247 / reflow 249-251 / original 176-178 and PDF 404 / reflow 408 / original 462 explicitly float Ascendant within its sign and distinguish MC from H10. No house geometry replacement is supported or needed.
- Fixed source OOB threshold: PDF 305 / reflow 309 / original 267, not original 269, states absolute declination exceeding 23.44°. This source convention is distinct from epoch-dependent astronomical obliquity. Do not use it as a physical obliquity accuracy claim.

### Later chapters do not fill the missing definitions

The astronomy review of PDF 461-580 found three further cautions: PDF 479 / reflow 483 / original 571-572 says nodes are always retrograde, which must not be imposed on a true/osculating node's physical speed; PDF 529 / reflow 533 / original 653 suggests 30 arcminutes or perhaps 1 degree for point-to-point contacts despite no outgoing OOI, leaving a separate ambiguous exactness rule; PDF 568 / reflow 572 / original 687-688 contains a Chiron diagram value 14°22 retrograde and prose value 19° for the same Michael Jackson example. The latter is not a usable numerical fixture without correction. None authorizes changing the engine to reproduce an inconsistent example.

The complete PDF 581-650 passage covers asteroid interpretations and relocation/Paran/Local Space examples. It contains no universal asteroid outgoing-radius catalog and no progression epoch algorithm. PDF 627-628 / reflow 631-632 / original 766-767 identifies Varuna 16°35 Gemini H11 as Pregrade with Leo degree, which is another rounded/untimed interpretive example, not an independent event fixture. PDF 650 / reflow 654 / original 840 explicitly treats a proposed geographic zodiac anchoring as conjecture requiring custom calculations and controlled testing.

PDF 651-669 / reflow 655-673 discusses sidereal epochs and historical interpretations. The model's proposed physical explanations and dates are source claims; no independent physical verification is supplied by the book. It does not supersede the project's tropical engine or justify adding a different zodiac. PDF 682-684 / reflow 686-688 / original 955-958 expressly leaves multiple timing techniques unresolved and excludes Solar Arc Directions. PDF 686-688 / reflow 690-692 / original 960-969 describes Birth Time Rectification using appearance and biography without a fully specified numerical search objective. These readings add context and exclusions, not implementable missing formulas.

## Focused questions for Logan

1. Does Spark parity use astronomical sign or Whole Sign house? Please resolve progressed MC Gemini14°50/H10 → Gemini versus Austin Mars Libra5°56/H4 → Pisces, and the composite Saturn Libra28°/H2 → Pisces case that matches neither formula (PDF 433, 434, 458 / original 509, 510, 546).
2. Does Austin Mars 5°56 qualify for degree FCA despite being 4 arcminutes before 6°, when the stated width is 3 arcminutes (PDF 431, 434 / original 508, 510)? Is this a typo or an explicit exception? What are the after-boundary and retrograde rules?
3. Please supply original Sophia printed617-619 and confirm the mean and true construction. Is true Sophia the opposite of the same osculating Lilith ellipse, with matching speed, or another lunar-perigee procedure? The current PDF rejects interpolation but omits the defining section.
4. Please supply original Progressions491-492 and specify epoch mapping, year/day definition and angles. How do relocation and time advance interact, including the Ascendant-flip examples?
5. Please resolve Pluto1.5° versus 24°42→25°42 at original378 (PDF343), then supply the outgoing OOI catalog and directional per-aspect/Fringe rules. What is exact-threshold inclusion, and which rules differ within one chart versus Synastry/transits?
6. At an exact Pregrade-entry, station, or Postgrade-exit instant, is Gradity intentionally unassigned, or does the new phase own equality? The application can preserve a boundary record until this is answered.

These questions block only the dependent interpretations. They do not block the independently tested Gradity event calculation, source diagnostics, existing chart display or astronomical engine.
