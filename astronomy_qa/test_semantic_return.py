"""Synthetic-only checks of the offline claim protocol, not personal validation."""
from copy import deepcopy
from pathlib import Path
import sys
import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from personal_review import BirthInput, build_review
from semantic_return import ReviewSession, Theme, return_base
from nadia_runtime import verified_core


@pytest.fixture(scope='module')
def packet():
    # Public CI must not receive the proprietary core. These are real local
    # integration checks, not a mocked substitute for source-backed evidence.
    private=Path(__file__).resolve().parents[1]/'.nadia-private'
    if not (private/'nadia_knowledge_core-0.7.0-py3-none-any.whl').is_file():
        pytest.skip('Local integration requires the pinned private core wheel; no public upload')
    return build_review(BirthInput(name='Synthetic semantic fixture',
        local_date='1984-05-15',local_time='06:30:00',timezone='Australia/Sydney',
        latitude=-33.8688,longitude=151.2093,location_name='Synthetic fixture'),
        'synthetic-protocol',synthetic=True)


def test_return_changes_semantic_role_not_original_expression_area():
    before=Theme('function','occupied-area')
    after=return_base(before,'represented-theme')
    assert after.function==before.function
    assert after.expressed_in==before.expressed_in
    assert after.qualified_by==('represented-theme',)
    assert after!=return_base(Theme('function','represented-theme'),'occupied-area')


def test_candidate_can_only_select_prevalidated_claims(packet):
    session=ReviewSession(verified_core(),packet)
    evidence=session.evidence()
    assert evidence['claims']
    candidate={'snapshot_id':session.snapshot_id,'claim_ids':list(evidence['claims'])}
    assert session.render_selection(candidate)==next(iter(evidence['claims'].values()))
    for update in [{'text':'invented personal reading'}, {'house':1},
                   {'snapshot_id':'different-chart'}, {'claim_ids':['new-aspect']}]:
        with pytest.raises(ValueError):
            session.render_selection({**candidate,**update})
    assert evidence['personal_readings_approved'] is False


def test_caller_mutation_cannot_rewrite_accepted_snapshot(packet):
    copy=deepcopy(packet)
    session=ReviewSession(verified_core(),copy)
    expected=session.evidence()
    copy['owner_id']='different-owner'
    assert session.evidence()==expected
    with pytest.raises(ValueError):
        ReviewSession(verified_core(),copy)


def test_untrusted_component_change_is_rejected(packet):
    changed=deepcopy(packet)
    changed['components'][0]['placement']['house']=12
    with pytest.raises(ValueError):
        ReviewSession(verified_core(),changed)
