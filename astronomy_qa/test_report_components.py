"""The consumer can use cited vocabulary without blanket approval or guessing."""
import json,subprocess,sys
from pathlib import Path

import pytest

from knowledge_audit.report_components import usage_catalog,annotate_chart,render_markdown

ROOT=Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def catalog():
    def load(name):return json.loads((ROOT/'data/knowledge'/name).read_text())
    return usage_catalog(load('interpretive_inventory.json'),load('original_assertions.json'),load('source_blocker_findings.json'),load('source_meaning_profiles.json'))


def test_moon_house_and_juno_are_usable_without_approving_traits(catalog):
    output=annotate_chart({'chart_context':'natal','placements':[{'body':'Moon','house':7},{'body':'Juno'}]},catalog)
    assert {r['concept_id'] for r in output['annotations'][0]['source_vocabulary']}=={'meaning-moon','field-07'}
    assert output['annotations'][1]['source_vocabulary'][0]['concept_id']=='asteroid-juno'
    assert all(c['citations'] for a in output['annotations'] for c in a['source_vocabulary'])
    assert not output['personal_report_generated'] and not output['personal_traits_inferred']
    assert all(a['combined_personal_interpretation'] is None for a in output['annotations'])


def test_chiron_core_is_included_and_eunomia_alternatives_are_not_selected(catalog):
    output=annotate_chart({'chart_context':'natal','placements':[{'body':'Eunomia'},{'body':'Chiron'}]},catalog)
    assert not output['annotations'][0]['source_vocabulary']
    assert output['annotations'][1]['source_vocabulary'][0]['concept_id']=='chiron'
    assert {g['kind'] for g in output['gaps']}=={'UNRESOLVED_SOURCE_ALTERNATIVES'}
    eunomia=output['annotations'][0]['source_alternatives'][0]
    assert eunomia['findings'] and eunomia['selected_alternative_id'] is None
    assert {'eunomia-surviving-core','eunomia-functional-order'}=={a['id'] for a in eunomia['alternatives']}


def test_recovered_sign_vocabulary_is_used_without_personal_inference(catalog):
    output=annotate_chart({'chart_context':'natal','placements':[{'body':'Moon','sign':'Cancer'}]},catalog)
    assert output['annotations'][0]['chart_fact']['sign']=='Cancer'
    assert [c['concept_id'] for c in output['annotations'][0]['source_vocabulary']]==['meaning-moon','sign-cancer']
    assert not output['gaps'] and catalog['core_sign_entries_present']==12
    assert not output['astronomical_input_verified']


def test_unknown_body_and_null_house_do_not_trigger_fallback(catalog):
    output=annotate_chart({'chart_context':'natal','placements':[{'body':'Unknown','house':None}]},catalog)
    assert not output['annotations'][0]['source_vocabulary']
    assert output['gaps'][0]['kind']=='UNKNOWN_BODY'
    assert output['external_library_fallback_allowed'] is False


@pytest.mark.parametrize('placement',[{'body':'Moon','house':True},{'body':'Moon','house':0},
    {'body':'Moon','house':13},{'body':'Moon','sign':'Madeup'},{'body':'Moon','prediction':'famous'}])
def test_invalid_or_interpretive_inputs_are_rejected(catalog,placement):
    with pytest.raises(ValueError):annotate_chart({'chart_context':'natal','placements':[placement]},catalog)


def test_non_natal_context_and_duplicate_objects_are_rejected(catalog):
    with pytest.raises(ValueError):annotate_chart({'chart_context':'transit','placements':[{'body':'Moon'}]},catalog)
    with pytest.raises(ValueError):annotate_chart({'chart_context':'natal','placements':[{'body':'Moon'},{'body':'moon'}]},catalog)


def test_without_witnesses_even_reviewed_meaning_cannot_be_annotated():
    inv={'records':[dict(id='meaning-moon',title='Moon',kind='meaning',source_status='PASSAGE_REVIEWED',meaning_summary='Test meaning',requires_concepts=[])]}
    catalog=usage_catalog(inv,{'assertions':[]},{'findings':[]})
    row=catalog['components'][0]
    assert not row['source_excerpt_allowed'] and not row['chart_vocabulary_annotation_allowed']


def test_rendering_keeps_attribution_citations_and_missing_context(catalog):
    output=annotate_chart({'chart_context':'natal','placements':[{'body':'Moon','sign':'Cancer','house':7}]},catalog)
    text=render_markdown(output)
    assert 'In this source:' in text and 'PDF page' in text and 'printed 199' in text
    assert 'Required context:' in text and 'Unfinished synthesis:' in text
    assert 'you are' not in text.lower() and 'you will' not in text.lower()


def test_cli_returns_usable_json_and_markdown_without_extra_blank_lines():
    command=[sys.executable,str(ROOT/'scripts/annotate_chart_sources.py'),str(ROOT/'examples/report-source-input.json')]
    packet=json.loads(subprocess.check_output(command+['--format','json']))
    markdown=subprocess.check_output(command+['--format','markdown']).decode('utf-8')
    assert not packet['personal_report_generated']
    assert packet['annotations'][0]['chart_fact']['body']=='Moon'
    assert 'In this source:' in markdown and markdown.splitlines()[-1]


def test_all_twelve_signs_have_direct_original_citations(catalog):
    signs=[r for r in catalog['components'] if r['concept_id'].startswith('sign-')]
    assert len(signs)==12 and catalog['missing_sign_dictionary']==[]
    assert all(r['source_profile_id'] and r['chart_vocabulary_annotation_allowed'] for r in signs)
    assert all(any(c.get('original_printed_pages') and c.get('line_ranges') for c in r['citations']) for r in signs)


def test_chiron_held_out_examples_do_not_erase_supported_definition(catalog):
    chiron=next(r for r in catalog['components'] if r['concept_id']=='chiron')
    assert chiron['source_status']=='INCOMPLETE'
    assert chiron['chart_vocabulary_annotation_allowed']
    assert 'Fractured structures' in chiron['source_meaning']
    assert set(chiron['held_out_finding_ids'])=={'chiron-saturn-aspect','chiron685-orbit-wording'}
    assert any('Wounded Healer' in x for x in chiron['rejected_fallback_meanings'])


def test_rendered_eunomia_retains_both_definitions_instead_of_omission(catalog):
    output=annotate_chart({'chart_context':'natal','placements':[{'body':'Eunomia'}]},catalog)
    text=render_markdown(output)
    assert 'Refined Resilience' in text and 'Functional Order' in text
    assert 'printed 712' in text and 'printed 772' in text
    assert 'neither definition has been selected' in text
