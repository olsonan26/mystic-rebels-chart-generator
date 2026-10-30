# Nadia: timing and preserved ESS/PY/COM comparison

**After-feedback research, 27 October 2026.** The original trial remains unchanged. New geometry and hypotheses here were developed with the disclosed history already known.

## What “Chiron showed up” can mean

| Possible meaning | What is supported | Nadia result |
|---|---|---|
| Natal presence | A natal placement is fixed at birth | Chiron has always been in natal H8/Leo in this chart; it did not enter that natal house at 11 |
| Age-degree activation | Original 247 onward distinguishes it from a transit. Original 255 gives 30-year recurrence;257 explicitly supplies fractional-age and cycle context | Natal 11°02′26″ supplies a candidate at age 11.040694; not an onset observation |
| Transiting Chiron enters a sign / fixed natal house | Actual longitude crossings can be calculated | It is in Capricorn/H1 at the start of the age 11 window. Its later Aquarius/H2 and Pisces/H3 entries are listed below; there is no age 11 ingress into natal H8 |
| Transiting Chiron contacts a natal point | Exact angular equalities can be calculated independently of meanings | Sixteen major equalities to the six natal chain nodes in the continuous 11-21 period |
| Another transit contacts natal Chiron | Another distinct event family | Fourteen major equalities from Saturn/Uranus/Neptune/Pluto to natal Chiron |
| A retrograde station or passage | Transit speed changes sign at a dated station |22 Chiron stations within these 11 years; recurrence alone supplies weak specificity. Natal Chiron remains direct |
| Full PURE activation/forecast | Source asks for whole context, directed flow, progressions/transits/relocations | Not completed by any one of the above. Progression rules, full aspect conditions and coupling are still unresolved |

The degree route is a plausible reconstruction of the age 11 reference. The original reading transcript is unavailable, so which timing procedure Logan actually used remains unconfirmed. A retrograde Chiron transit is not assumed as the explanation.

## Degree timing: a supported concept with unresolved dates

The handoff's conservative statement about fractional ages can now be refined: original printed 257 explicitly gives 0°30′ at six months. This is primary support for a fractional-age concept, beyond the compiled book and integer-only software helper. It still does not choose a calendar implementation or quantify delayed manifestation. Its astronomical rationale is retained as the author's proposed rationale, not an independently verified physical mechanism.

| Natal node | Degree | First-cycle age label | Approximate fractional-age candidate | Limit |
|---|---|---:|---|---|
| Chiron direct |11°02′26″|11|About 1-2 August 2003 under two explicit calendar conventions|No recorded onset date to compare; direct placements can also manifest later in original 251 |
| Sun direct |25°44′25″|25|Outside the requested interval|The Sun can participate as ruler without its own age-degree activation |
| Moon direct |2°06′47″|2|Outside the requested interval|No new Moon activation at 11 is inferred |
| Uranus Rx |15°37′24″|15|About 1-2 March 2008 before any unquantified delay|Age 15 was not in the frozen trial; no preserved month state assigned |
| Saturn Rx |16°36′09″|16|About 22 February 2009 before any unquantified delay|February 2009 is yellow; no annual 11/13/16 marker in 2009 |
| Neptune Rx |17°20′30″|17|About 19 November 2009 before any unquantified delay|November 2009 is yellow; no annual 11/13/16 marker in 2009 |

Calendar alternatives in `degree-and-condition-diagnostics.json` are: (a) fractional interpolation between successive local birth anniversaries and (b) elapsed mean tropical years of 365.24219 days from the birth epoch. These are **explicit research assumptions**, not two equally approved source algorithms. Their difference is a real reason not to print an exact activation clock time. No retrograde delay is invented, and no candidate is moved to a known event.

Mercury's 17°19′38″, Jupiter's 12°33′44″ and Pluto's 20°11′37″ are also retained as supplementary degree diagnostics, with no event-fit selection. An activation is not dormancy turning into inevitable harm. The first 30-year Aries/H4 context and its Mars/Venus ruler route are worked in `NADIA_WORKED_CASE.md`; that context applies across all these ages.

## New transit calculation and its limits

Before running this new scan, `timing-selection.json` recorded its **after-feedback** selection: all five movers Chiron/Saturn/Uranus/Neptune/Pluto to all six natal nodes Chiron/Sun/Moon/Neptune/Saturn/Uranus; all oriented multiples of 30°, retaining unsigned 0/30/60/90/120/150/180. The continuous window is 17 July 2003 through 17 July 2014, end exclusive, in Pacific civil time. Ages 13-15 are retained as coverage comparisons; they are not known event-free controls.

Daily and six-hour bracketing find the same 142 equalities:82 in the five-angle major subset and 60 in the additional 30°/150° subset. Bisection residuals and asset SHA256 values are retained in `expanded-transit-geometry.json`. Grid agreement verifies this computation against another sampling interval, not independent astronomical accuracy or completeness at arbitrary tangencies. Birth-record uncertainty also remains.

Houses in event rows are **fixed natal sectors**. They are not a moving event Ascendant, a relocated house claim or evidence of residence. Oriented longitude offsets do not supply the author's Energy Flow direction. No influence window is assigned. The complete unfiltered ledger is `expanded-contacts.csv`; targets and angles differ from the old scan, so 142 is not an improved replacement for the old 59.

Swiss API settings and returned-backend checks follow the existing local engine and the [official programming interface](https://www.astro.com/swisseph/swephprg.htm). This is calculation provenance; the documentation does not validate personal interpretation.

### All major contacts involving Chiron in the new selection

Dates are Pacific civil dates; R/D describes the **transiting mover**, not the natal target. Color is the preserved monthly indicator; an em dash means the original age-window output does not cover that date.

| Date | Age | Mover -> natal target | Geometry | Motion | Preserved month |
|---|---:|---|---:|---|---|
|2003-09-02|11|Neptune -> Chiron|180°|R|red|
|2003-11-29|11|Chiron -> Uranus|0°|D|green|
|2003-12-09|11|Neptune -> Chiron|180°|D|red|
|2003-12-19|11|Chiron -> Neptune|0°|D|red|
|2004-04-07|11|Chiron -> Sun|180°|D|red|
|2004-05-26|11|Chiron -> Sun|180°|R|red|
|2005-01-02|12|Chiron -> Sun|180°|D|red|
|2005-11-04|13|Saturn -> Chiron|0°|D|—|
|2005-12-09|13|Saturn -> Chiron|0°|R|—|
|2006-07-07|13|Saturn -> Chiron|0°|D|—|
|2007-02-11|14|Chiron -> Chiron|180°|D|—|
|2007-09-16|15|Chiron -> Chiron|180°|R|—|
|2007-11-20|15|Chiron -> Chiron|180°|D|—|
|2008-02-15|15|Chiron -> Saturn|0°|D|—|
|2008-09-22|16|Chiron -> Saturn|0°|R|red|
|2008-11-26|16|Chiron -> Saturn|0°|D|green|
|2010-10-27|18|Saturn -> Chiron|60°|D|yellow|
|2011-03-11|18|Chiron -> Moon|0°|D|red|
|2011-05-16|18|Saturn -> Chiron|60°|R|red|
|2011-07-09|18|Saturn -> Chiron|60°|D|red|
|2011-09-14|19|Chiron -> Moon|0°|R|green|
|2012-01-05|19|Chiron -> Moon|0°|D|green|
|2013-01-25|20|Saturn -> Chiron|90°|D|green|
|2013-03-14|20|Saturn -> Chiron|90°|R|red|
|2013-05-16|20|Uranus -> Chiron|120°|D|green|
|2013-09-20|21|Uranus -> Chiron|120°|R|green|
|2013-10-10|21|Saturn -> Chiron|90°|D|green|
|2014-03-07|21|Uranus -> Chiron|120°|D|green|
|2014-04-09|21|Chiron -> Uranus|60°|D|green|
|2014-05-20|21|Chiron -> Neptune|60°|D|green|

The arrows name calculation mover/target roles. They do not assert approved directional emissions. No adverse or protective weight is attached to an angle. New contacts at ages 13-15 show why the first restricted ages could not establish a continuous timing story.

### Actual Chiron sign / natal-sector crossings

21 February 2005: Aquarius/H2;31 July 2005: retrograde back to Capricorn/H1;5 December 2005: Aquarius/H2 again;19 April 2010: Pisces/H3;20 July 2010: retrograde back to Aquarius/H2;8 February 2011: Pisces/H3 again. The late 19 April and late 5 December dates are Pacific-local conversions. They must not be silently replaced with another zone's calendar date. All 22 stations, without selecting just a favorable one, are in `chiron-stations-and-ingresses.json`.

### The dated journal is an important non-exactness check

The first Chiron-Moon equality is 11 March 2011, about 112 days before 1 July. The next is 14 September, about 75 days after it. She was 18 on 1 July. A reference position 12 elapsed hours after Pacific midnight puts Chiron aroundPisces 5°14′, retrograde, **3.11995° from natal Moon**. The journal's actual clock time is unknown. No selected equality occurs on that date.

That departure exceeds Chiron's documented 1° outgoing radius. It cannot be called an active Chiron-to-Moon conjunction at the journal date under that simple recovered bound. Adding Moon's radius, silently widening an orb, invoking unspecified Fringe or converting the 8-day proximity of Saturn-Chiron on 9 July into a preselected window would rescue the match after the fact. No such rescue is used here. A broad age 18 thematic comparison can be discussed; an exact journal-event prediction has not been established.

## Preserved annual results and constructive COM role

All 10 annual states and 98 months were reproduced from the **unchanged STAFFprofiler compiled asset and indicator functions**, including raw formulas, active-letter ordinals, authentic trails, annual alerts and monthly colors. `numerology-reexecution-verification.json` contains zero discrepancies. No npm build/test/start hooks ran.

| Year | ESS | PY | COM | Source-specific COM approach, paraphrased |
|---|---|---|---|---|
|2003|17/8|29/11/2|46/10/1|Consider future directions and available ideas/opportunities|
|2004|17/8|30/3|47/11/2|Plan precisely, monitor details, discuss concerns and revise when circumstances require|
|2005*|17/8|31/4|48/12/3|Speak, review information and participate creatively without overextending|
|2008|17/8|25/7|42/6|Recognize responsibility and whether support/help is needed|
|2009|17/8|26/8|43/7|Question, inspect and understand commitments before acting|
|2010|17/8|27/9|44/8|Organize practical/material demands and effort|
|2011|14/5|28/10/1|42/6|Responsibility with an explicit opening to check whether the person needs help|
|2012|6|29/11/2|35/8|Organize practical/material demands; source text matches 44 here|
|2013|19/10/1|30/3|49/13/4|Understand circumstances, prepare and plan before proceeding|
|2014*|19/10/1|31/4|50/5|Manage time/activity and allow offered help when circumstances change|

*Only the portions before 17 July belong to the frozen 2005/2014 windows. January 1 is the annual state boundary; birthdays do not reset these values. No married/current-name substitution was introduced.

ESS's source category describes present attitude/frame of mind, supporting its use as an experiential lens; PY describes annual cycle/trend; COM describes approach. Their symbolic vocabularies are not interchangeable. The adult bank's work, income and marriage claims were not transplanted literally onto a child. A youth-context COM adaptation is new editorial work, not a recovered original child-reading rule.

**Worked 2011 arithmetic:** activeI(9)+E(5)=ESS14/5; CY2+0+1+1=4; PY17+7+4=28/10/1; COM14+28=42/6. None has an annual 11/13/16 stage. July: PM1+7=8; PME5+8=13/4; MCOM4+8=12/3. July is red from monthly PME13, not annual COM42. The proposed comparison is change/new direction alongside responsibility and a need for support. It does not make Nadia responsible for fixing adult behavior.

**Worked 2013 arithmetic:** activeN(14)+E(5)=ESS19/10/1; PY17+7+6=30/3; COM19+30=49/13/4. The 13 is an actual COM stage. It is not produced by concatenating roots, and it does not automatically turn every 2013 month red. July 2013, for example, is yellow in the preserved monthly output.

## Matches, misses and ambiguity

| Reported history / question | What the frozen first pass actually offered | After-feedback assessment |
|---|---|---|
|Paternal abuse approximately 11-21|Broad relational/emotional questions; no specific abuse identification; no Chiron|Chiron-H8-Leo-Sun father route is reconstructable, but the abuse was disclosed before this reconstruction. The age 11 label is a candidate correspondence without a dated onset comparison|
|Maternal physical abuse, especially younger|Emotional-familiarity questions, not a specific prediction of violence|Moon/mother convention and H3 communication route organize an inquiry; they do not distinguish violence from other family contexts|
|1 July 2011 journal, age 18|A weaker exact-contact claim,2010→2011 closure/new-start transition|Responsibility/help themes in COM42 and JulyPME13 can be compared with the account. Chiron-Moon equalities were newly found around the period, not on the journal date. Original limitation remains|
|Public-speaking interest and faith/journaling|No specific public-speaking or faith/journal discovery|Actual Moon-H3/Pisces and Mercury/Jupiter routes offer thematic comparisons after feedback; no biographical discovery credited|
|Police report around 21|Private commitments, direction and conversations at 21|Exact report date is missing; neither November/December 2013 red months nor another contact can be called a date hit|
|Long-running difficulty|RepeatedESS17/8 and many monthly markers|A long background cannot distinguish onset, continuation and disclosure. Do not count every repeated year/contact as another confirmation|

The original trial has **31 red /12 yellow /16 green contacts out of 59**, against **56 red /12 yellow /30 green month cells out of 98**. About 53% of contacts versus 57% of cells were red: no obvious enrichment. Its explicit counterexamples, including green June 2005 and green August/November 2012, remain preserved.

The **new** Chiron-to-chain major family has 16 contacts across the continuous interval,12 within the preserved windows: **6 red,0 yellow,6 green**. The outer-four-to-natal-Chiron major family has 14 continuous,11 in the preserved windows: **5 red,1 yellow,5 green**. These do not show an obvious improvement in red-month concentration. The wider six-target major selection has 63 contacts in preserved windows,35 red/7 yellow/21 green; the separate 30°/150° extension has 37,25 red/2 yellow/10 green. These selections overlap other families and contain repeated passes, so none is an independent validation sample. The additional-angle ratio must not be promoted as a newly discovered success after inspecting it.

No calculation establishes a probability of abuse or danger. A red-month base rate near 57%, broad events spanning many years, and many selectable chart factors make retrospective thematic agreement easy to obtain. Unknown events and unreported event-free periods remain unknown, not true negatives.

## A later genuinely blind test

Freeze method IDs, names/time uncertainty, eligible nodes/angles, directional rules, window lengths, topics and scoring criteria **before** receiving histories. Use separate people with independently withheld timelines, including neutral and constructive events; Nadia remains a development case. Predetermine how onset, continuation, disclosure and unrelated events differ. Require narrow statements, allow no supported claim, and have raters compare the intended reading with plausible shuffled/date-shifted alternatives without knowing its identity. Keep a complete miss/false-alarm ledger; group repeated retrograde passes instead of counting each as independent. Hold out people, not adjacent months of the same person's history. Compare astrology alone, numerology alone and the combined method against their exposure rates. No threshold, p-value or success claim is fitted from Nadia.
