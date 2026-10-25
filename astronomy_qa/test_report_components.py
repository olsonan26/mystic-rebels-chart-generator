"""The consumer can use cited vocabulary without blanket approval or guessing."""
import json,subprocess,sys
from pathlib import Path

import pytest

from knowledge_audit.report_components import usage_catalog,annotate_chart,render_markdown

ROOT=Path(__file__).resolve().parents[1]


@pytest.fixture(scope='module')
def catalog():
    def load(name):return json.loads((ROOT/'data/knowledge'/name).read_text())
    return usage_catalog(load('interpretive_inventory.json'),load('original_assertions.json'),load('source_blocker_findings.json'))


def test_moon_house_and_juno_are_usable_without_approving_traits(catalog):
    output=annotate_chart({'chart_context':'natal','placements':[{'body':'Moon','house':7},{'body':'Juno'}]},catalog)
    assert {r['concept_id'] for r in output['annotations'][0]['source_vocabulary']}=={'meaning-moon','field-07'}
    assert output['annotations'][1]['source_vocabulary'][0]['concept_id']=='asteroid-juno'
    assert all(c['citations'] for a in output['annotations'] for c in a['source_vocabulary'])
    assert not output['personal_report_generated'] and not output['personal_traits_inferred']
    assert all(a['combined_personal_interpretation'] is None for a in output['annotations'])


def test_conflicting_eunomia_and_incomplete_chiron_are_not_selected(catalog):
    output=annotate_chart({'chart_context':'natal','placements':[{'body':'Eunomia'},{'body':'Chiron'}]},catalog)
    assert not any(a['source_vocabulary'] for a in output['annotations'])
    assert {g['kind'] for g in output['gaps']}=={'CONFLICT_REFERENCE_ONLY','INCOMPLETE_REFERENCE_ONLY'}
    eunomia=next(g for g in output['gaps'] if g['body']=='Eunomia')
    assert eunomia['findings']
    assert {'eunomia-surviving-core','eunomia-functional-order'} <= {
        c.get('assertion_id') for c in eunomia['reference_citations']}


def test_missing_sign_vocabulary_is_visible_and_not_fabricated(catalog):
    output=annotate_chart({'chart_context':'natal','placements':[{'body':'Moon','sign':'Cancer'}]},catalog)
    assert output['annotations'][0]['chart_fact']['sign']=='Cancer'
    assert [c['concept_id'] for c in output['annotations'][0]['source_vocabulary']]==['meaning-moon']
    assert output['gaps'][0]['kind']=='SIGN_VOCABULARY_NOT_COMPLETE'
    assert not output['astronomical_input_verified']


def test_unknown_body_and_null_house_do_not_trigger_fallback(catalog):
    output=annotate_chart({'chart_context':'natal','placements':[{'body':'Unknown','house':None}]},catalog)
    assert not output['annotations'][0]['source_vocabulary']
    assert output['gaps'][0]['kind']=='UNKNOWN_BODY'


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
    assert 'In this source:' in text and 'PDF page' in text and 'SIGN_VOCABULARY_NOT_COMPLETE' in text
    assert 'Required context:' in text and 'Unfinished synthesis:' in text
    assert 'you are' not in text.lower() and 'you will' not in text.lower()


def test_cli_returns_usable_json_and_markdown_without_extra_blank_lines():
    command=[sys.executable,str(ROOT/'scripts/annotate_chart_sources.py'),str(ROOT/'examples/report-source-input.json')]
    packet=json.loads(subprocess.check_output(command+['--format','json']))
    markdown=subprocess.check_output(command+['--format','markdown']).decode('utf-8')
    assert not packet['personal_report_generated']
    assert packet['annotations'][0]['chart_fact']['body']=='Moon'
    assert 'In this source:' in markdown and markdown.splitlines()[-1]
