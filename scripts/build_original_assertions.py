"""Author-reviewed atomic source assertions, separate from executable formulas."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from knowledge_audit.sources import load_manifest

# id | concept | kind | original scans | paraphrased proposition | limitation
ROWS = '''sophia-mean-opposition|sophia|formula_specification|IMG_5086.JPG|Mean Sophia is opposite the matching Mean Lilith placement.|Only a source specification; verify coordinate frame and independent fixture before runtime release.
sophia-osculating-opposition|sophia|formula_specification|IMG_5086.JPG|Osculating Sophia is opposite the matching Osculating Lilith placement.|Do not substitute interpolated perigee, a different ellipse, or arbitrary Selene motion.
sophia-perigee-identity|sophia|construction_meaning|IMG_5084.JPG IMG_5085.JPG|The source's Sophia names lunar perigee and explicitly distinguishes arbitrary Selene constructions.|Source physical explanations and interpretive claims are not inherited scientific validation.
sophia-mean-undercurrent|sophia|descriptive_meaning|IMG_5086.JPG|Mean Sophia describes a persistent background pull toward attachment or belonging.|A theme is not known personal history or a diagnosis.
sophia-osculating-reactivity|sophia|descriptive_meaning|IMG_5086.JPG|Osculating Sophia describes a more immediate and situational response to external triggers.|Full house, ruler, arc and relationship conditions remain required.
sophia-retrograde-reworking|sophia|contextual_exception|IMG_5086.JPG|Osculating Sophia retrograde retains attachment while its expression needs reworking.|Original619 continues onto620; do not treat this one page as a complete retrograde theory.
progression-relative-time|core-trinity|approximate_formula_description|IMG_4952.jpg|A lived year corresponds approximately to a day of planetary motion, illustrated by the Sun's roughly one degree per year.|Exact year/day definition, time scale, angles and location coupling are unspecified; original492 remains unlocated.
progression-relative-bodies|core-trinity|contextual_rule|IMG_4952.jpg|Progressed bodies retain their own relative pace rather than advancing every body by a fixed solar amount.|Do not infer a conventional solar-arc algorithm.
core-trinity-simultaneous|core-trinity|contextual_rule|IMG_4952.jpg IMG_4968.jpg|Natal, progressed and relocated layers are referenced together rather than replacing one another.|A three-wheel illustration is not a verified progression or relocation workflow.
natal-static-baseline|core-trinity|contextual_rule|IMG_4952.jpg|The natal layer remains a fixed baseline as the other layers change.|Do not overwrite natal evidence when a progressed placement changes.
ooi-radius-not-diameter|directional-context|formula_specification|IMG_4658.jpg IMG_4660.jpg|An OOI number is reach in one direction; total span is twice that radius.|Geometry and interpretive approval are distinct; per-aspect bands remain separate.
ooi-sun-ten|directional-context|numeric_source_parameter|IMG_4659.jpg|The passage assigns the Sun a ten-degree OOI.|Partial catalog witness; no approval of every Sun aspect or all contexts.
ooi-moon-three|directional-context|numeric_source_parameter|IMG_4658.jpg IMG_4659.jpg IMG_4660.jpg|Moon OOI is three degrees in each direction.|Do not reuse an emitter radius as an exact activation rule for every point.
ooi-mars-four|directional-context|numeric_source_parameter|IMG_4661.jpg|The passage assigns Mars a four-degree OOI.|A partial catalog parameter is not a full aspect-network implementation.
ooi-saturn-approximate|directional-context|approximate_source_parameter|IMG_4661.jpg|The passage describes Saturn OOI as around seven and a half degrees.|Preserve the approximation; do not silently promote to an exact universal threshold.
ooi-chiron-one|forced-contact|numeric_source_parameter|IMG_4667.jpg|The example assigns Chiron a one-degree OOI.|Its separate semisextile geometric band is not the same parameter.
same-house-not-conjunction|directional-context|explicit_exclusion|IMG_4660.jpg|Shared house/sign occupancy alone does not establish conjunction.|A missing graph cannot prove no contact; test nuclear reach separately.
one-way-response|forced-contact|directional_rule|IMG_4662.jpg IMG_4665.jpg|A receiving body's response does not establish a reverse initiating edge when its own reach does not cover the sender.|Retain sender, receiver and ecosystem separately.
no-cross-ecosystem-radius-sum|directional-context|explicit_exclusion|IMG_4665.jpg|Two people's OOI radii must not be summed to manufacture a contact.|Do not reuse within-ecosystem Fringe merging across charts.
natal-no-sky-initiation|natal-transit-order|directional_exclusion|IMG_4666.jpg|In transit interpretation a natal body's response does not mean it initiates physical influence on the current sky.|Both reading perspectives do not imply two active physical edges.
fringe-interval-example|fringe-fca|worked_example_geometry|IMG_4663.jpg|For the printed Mars5:56 and Saturn15:32 example, the illustrated overlap is8:02 through9:56.|Retain approximate Saturn radius; do not elevate this interval to a universal Fringe catalog.
fringe-activation-pass-through|fringe-fca|activation_rule_description|IMG_4663.jpg|The transit Moon activates the illustrated Fringe by traversing its interval rather than extending its own OOI into it.|Exact endpoint equality and retrograde traversal conventions still require clarification.
fringe-sequential-not-merged|fringe-fca|meaning_and_exclusion|IMG_4663.jpg IMG_4664.jpg|The example treats non-nuclear Fringe as a lingering sequential influence rather than a merged conjunction.|Receiving conditions and the complete chain still matter.
vantage-two-perspectives|vantage-resolution|contextual_rule|IMG_4799.jpg IMG_4800.jpg|Vantage examines each participant's perspective and surroundings while preserving specific energy direction.|A symmetric label loses the sender/receiver sequence.
fca-five-percent|fringe-fca|formula_specification|IMG_4969.jpg|The stated spill fraction is five percent of sign, decan or degree scale.|No after-boundary strengths or complete retrograde/equality policy are supplied.
fca-degree-counterexample|fringe-fca|contradictory_worked_example|IMG_4969.jpg IMG_4971.jpg|The stated degree width is three arcminutes, but Mars5:56 is still labelled Aries FCA four arcminutes before6.|Preserve the numeric threshold and the conflicting printed example; author correction is required.
pluto-correct-original-arithmetic|forced-contact|compilation_correction|IMG_4814.jpg|The original's24:15 plus1:30 gives25:45, leaving Moon25:57 twelve arcminutes beyond reach.|The same original earlier gives24:42 as the Pluto coordinate; do not erase that residual conflict.
pluto-original-center-conflict|forced-contact|source_contradiction|IMG_4814.jpg|Earlier original prose gives24:42 while the figure and final interval start at24:15.|The two starting values produce different Moon reach; author/version clarification remains required.
chiron-original-degree|chiron|compilation_correction|IMG_5282.jpg IMG_5283.jpg|Original diagram19:18Rx agrees with rounded prose19; the compiled14:22 description is wrong.|This source correction is not an independent astronomical fixture.
chiron-original-aspect-conflict|chiron|source_contradiction|IMG_5282.jpg IMG_5283.jpg|The original calls the Saturn relationship sextile on687 and trine on688.|Preserve both; do not invent a chart epoch or use biography to choose an aspect.
eunomia-surviving-core|asteroid-eunomia|competing_meaning|IMG_5392.JPG IMG_5393.JPG|The main chapter describes an exposed resilient core surviving loss and explicitly rejects order/fairness as its meaning.|Competes with the original772 comparative entry; precedence is not established.
eunomia-functional-order|asteroid-eunomia|competing_meaning|IMG_5455.JPG|The comparative entry assigns Eunomia functional order and systems working by design.|Competes with the main chapter; do not silently combine the two.
elektra-hidden-complexity|asteroid-elektra|descriptive_meaning|IMG_5388.JPG IMG_5454.JPG|Elektra describes hidden coordination that holds many fragments together as a working system.|Do not substitute mythological tragedy; full participating conditions remain missing.
euphrosyne-divergent-continuity|asteroid-euphrosyne|descriptive_meaning|IMG_5394.jpg IMG_5395.JPG IMG_5455.JPG|Euphrosyne describes continuity and lineages formed through divergence from a shared plane.|A keyword alone does not replace ruler, forced-contact and retrograde context.
vesta-retrograde-inward|asteroid-vesta|contextual_meaning|IMG_5451.JPG|Retrograde Vesta turns commitment and purpose inward and can accompany isolation or overprotection in the source's interpretation.|This is conditional source language, not evidence of a user's trauma or diagnosis.
composite-joint-entity|composite|meaning_and_exclusion|IMG_5007.jpg IMG_5009.JPG|A composite describes the pair as a joint entity, distinct from reciprocal Synastry behavior or an electional relationship-event chart.|Do not fabricate when a relationship became official.
composite-midpoint-example|composite|worked_example_geometry|IMG_5007.jpg|Gemini21:16 and Pisces7:24 have the illustrated composite Sun at Aries29:20.|No antipodal midpoint choice, angular method or full context algorithm is specified.
composite-ac-priority|composite|context_dependency|IMG_5009.JPG|The original composite assessment prioritizes Ascendant and its ruler.|Still requires full ruler condition; a name alone is insufficient.
composite-fourth-priority|composite|context_dependency|IMG_5009.JPG|The original composite assessment explicitly includes fourth-house condition and its ruler.|Preserve the natural chart and all relevant conditions.
composite-fifth-priority|composite|context_dependency|IMG_5009.JPG|The original composite assessment explicitly includes fifth-house condition and its ruler.|No source-approved weighting algorithm follows from this priority list.
descendant-discernment|anchors|descriptive_meaning|IMG_5111.jpg IMG_5237.jpg|Descendant includes discerning what external contact is admitted into one's personal world.|Its coordinate alone does not implement the meaning; sign/ruler context remains required.
agency-personal-control|agency|explicit_caution|IMG_4942.jpg|The source distinguishes personal choice and action from control of the universe or other people.|Do not turn interpretation into a promise of control or guaranteed outcome.'''


def main():
    manifest = load_manifest()
    files = {r['name'].casefold():r for b in manifest['batches'] for r in b['files']
             if r['visual_review_status'] == 'TARGETED_ORIGINAL_VISUAL_REVIEW'}
    assertions = []
    for line in ROWS.splitlines():
        id, concept, kind, names, proposition, limit = line.split('|')
        witnesses = []
        for name in names.split():
            row = files[name.casefold()]
            witnesses.append(dict(file_id=row['file_id'], content_sha256=row['content_sha256'],
                original_printed_pages=row['printed_page_ids'], name=row['name']))
        assertions.append(dict(id=id, concept_id=concept, kind=kind, proposition=proposition,
            applicability='Listed original example or concept; complete chart context required for personal application.',
            exclusions_and_limits=[limit], witnesses=witnesses,
            authority='ORIGINAL_BATCH_SCAN_TARGETED_REVIEW',
            execution_status='NOT_EXECUTABLE_NOT_RUNTIME_APPROVED',
            interpretation_validation='SOURCE_FAITHFULNESS_ONLY_NOT_EMPIRICAL_VALIDATION',
            answer_use='NOT_APPROVED'))
    continuation=ROOT/'data/knowledge/source_review_continuation.json'
    if continuation.exists():
        assertions.extend(json.loads(continuation.read_text())['assertions'])
    data = dict(schema_version='1.0', scope='SELECTED_ATOMIC_ORIGINAL_SOURCE_ASSERTIONS_NOT_EXHAUSTIVE',
        all_important_knowledge_covered=False,
        required_competing_pairs=[['eunomia-surviving-core','eunomia-functional-order'],
            ['pluto-correct-original-arithmetic','pluto-original-center-conflict'],
            ['chiron-original-degree','chiron-original-aspect-conflict'],
            ['spark-original-sign-derivation','spark-original-house-procedure']], assertions=assertions)
    (ROOT / 'data/knowledge/original_assertions.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(selected_atomic_assertions=len(assertions), runtime_approved=0)))


if __name__ == '__main__':
    main()
