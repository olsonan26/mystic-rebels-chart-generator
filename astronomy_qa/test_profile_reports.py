"""Real chart -> private source gates -> ephemeral report contract regressions."""
from copy import deepcopy
import json
from unittest.mock import patch

from fastapi.testclient import TestClient
import pytest

from mystic_rebels.api import app
from mystic_rebels.models import BirthInput
from mystic_rebels.profile_reports import ProfileRequest, generate_report
from site_access import SitePasswordGate


def sample(**changes):
    return BirthInput(name='Synthetic Nadia Example', local_date='2000-01-01', local_time='12:00:00',
                      timezone='Etc/UTC', latitude=51.4779, longitude=0,
                      location_name='Greenwich reference location (synthetic)', **changes)


def test_real_calculation_and_private_source_components():
    # Public CI intentionally has no proprietary wheel. Missing core yields facts
    # with an explicit gate, not invented meanings. Protected preflight tests the
    # same contract against the installed immutable private wheel.
    report = generate_report(ProfileRequest(birth=sample(), synthetic=True))
    assert report['synthetic']
    assert report['readiness']['technical_report_ready']
    assert not report['readiness']['complete_personal_reading']
    assert report['lead']['personalized_answer'] is None
    assert report['chart']['configuration']['zodiac'] == 'tropical'
    assert len(report['chart']['points']) == 12
    if report['readiness']['knowledge_status'] == 'verified':
        vocab = [r for r in report['sections'] if r['status'] == 'source_vocabulary']
        assert len(vocab) == 10
        assert all(r['source_refs'] and r['rule_ids'] for r in vocab)
        assert all(not r['personal_interpretation_approved'] for r in vocab)
        moon = next(r for r in vocab if r['id'] == 'placement-moon')
        assert any(f['label'] == 'Ruled house and occupants' for f in moon['facts'])
    else:
        assert all(r['status'] != 'source_vocabulary' for r in report['sections'])
    assert len([s for s in report['sections'] if s['status'] == 'unavailable']) == (15 if report['readiness']['knowledge_status'] == 'verified' else 18)


def test_missing_core_preserves_facts_without_legacy_fallback():
    with patch('mystic_rebels.profile_reports.verified_core', side_effect=ValueError('bad private integrity')):
        report = generate_report(ProfileRequest(birth=sample()))
    assert report['readiness']['knowledge_status'] == 'unavailable'
    assert report['core_identity'] is None
    assert not any(s['status'] == 'source_vocabulary' for s in report['sections'])
    assert report['sections'][0]['facts']
    assert report['lead']['source_refs'] == []


@pytest.mark.parametrize('accuracy,clock,uncertainty', [('unknown', None, None), ('approximate', '20:01:00', 600)])
def test_uncertain_time_suppresses_house_derived_output(accuracy, clock, uncertainty):
    birth = sample(time_accuracy=accuracy, uncertainty_seconds=uncertainty).model_copy(update={'local_time': clock})
    report = generate_report(ProfileRequest(birth=birth))
    assert not report['chart']['angles'] and not report['chart']['whole_sign_cusps']
    assert all(p.get('house') is None and p.get('field') is None for p in report['chart']['points'])
    assert not any(f['label'] == 'Ruled house and occupants' for s in report['sections'] for f in s['facts'])
    assert not report['readiness']['complete_personal_reading']


def test_report_identity_and_json_are_deterministic():
    request = ProfileRequest(birth=sample(), synthetic=True)
    first, second = generate_report(request), generate_report(request)
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
    assert first['report_id'] != generate_report(request.model_copy(update={'tier': 'premium'}))['report_id']
    assert 'created_at_utc' not in first['chart']


@pytest.mark.parametrize('url', ['', 'javascript:alert(1)', 'http://example.com/book', 'https://user:pass@example.com'])
def test_booking_has_no_invented_or_unsafe_destination(monkeypatch, url):
    from mystic_rebels.profile_reports import booking_url
    monkeypatch.setenv('NADIA_BOOKING_URL', url)
    assert booking_url() is None


def test_booking_uses_only_explicit_https_configuration(monkeypatch):
    from mystic_rebels.profile_reports import booking_url
    monkeypatch.setenv('NADIA_BOOKING_URL', 'https://example.com/owner-supplied-booking')
    assert booking_url() == 'https://example.com/owner-supplied-booking'


def test_route_recalculates_and_does_not_accept_injected_interpretation():
    client = TestClient(app)
    request = {'birth': sample().model_dump(), 'tier': 'essential', 'synthetic': True}
    response = client.post('/api/profile-reports', json=request)
    assert response.status_code == 200
    assert response.headers['cache-control'] == 'private, no-store'
    assert response.json()['readiness']['complete_personal_reading'] is False
    injected = dict(request, chart={'positions': 'injected'}, interpretation='complete')
    assert client.post('/api/profile-reports', json=injected).status_code == 422
    assert client.post('/api/profile-reports', json=request, headers={'Origin': 'https://other.example'}).status_code == 403


def test_existing_access_boundary_protects_report_birth_data(monkeypatch):
    monkeypatch.setenv('SITE_ACCESS_SECRET', 'x' * 40)
    monkeypatch.setenv('SITE_ACCESS_HASH', 'configured')
    client = TestClient(SitePasswordGate(app))
    response = client.post('/api/profile-reports', json={'birth': sample().model_dump()})
    assert response.status_code == 401
    assert 'Synthetic Nadia' not in response.text


def test_dual_chart_cannot_be_mislabeled_natal():
    from mystic_rebels.errors import ChartError
    with pytest.raises(ChartError):
        generate_report(ProfileRequest(birth=sample().model_copy(update={'chart_type': 'dual'})))


def test_bounded_sections_preserve_ruler_channels_unknown_contacts_and_scope():
    report = generate_report(ProfileRequest(birth=sample(), synthetic=True))
    # Public CI has no private release; verify fail-closed fallback there.
    if report['readiness']['knowledge_status'] == 'unavailable':
        assert not any(s['status'] == 'source_context' for s in report['sections'])
        return
    sections = {s['id']: s for s in report['sections']}
    houses = sections['house-condition']
    assert len(houses['calculation_evidence']['houses']) == 12
    assert any(h['empty_of_ruling_planets'] for h in houses['calculation_evidence']['houses'])
    motion = sections['retrograde-profile']
    assert len(motion['calculation_evidence']['channels']) == 10
    assert all(not r['inherited_occupant_retrograde'] for r in motion['calculation_evidence']['channels'])
    contacts = sections['relationships-graph']['calculation_evidence']
    assert sum(contacts['classification_counts'].values()) == 315
    assert contacts['classification_counts'].get('SOURCE LIMIT UNKNOWN', 0) > 0
    assert contacts['complete_contact_catalog'] is False
    for identity in ('house-condition', 'retrograde-profile', 'relationships-graph'):
        assert sections[identity]['status'] == 'source_context'
        assert sections[identity]['source_refs'] and sections[identity]['rule_ids']
        assert not sections[identity]['personal_interpretation_approved']
        assert sections[identity]['blockers']


def test_unverified_component_rule_cannot_authorize_report_context():
    try:
        from nadia_runtime import verified_core
        core = verified_core()
    except (OSError, ValueError, ImportError):
        with patch('mystic_rebels.profile_reports.verified_core', side_effect=ValueError('unavailable')):
            report = generate_report(ProfileRequest(birth=sample()))
    else:
        core.rules['phase5:condition-channels']['status'] = 'disputed'
        with patch('mystic_rebels.profile_reports.verified_core', return_value=core):
            report = generate_report(ProfileRequest(birth=sample()))
    assert not report['readiness']['complete_personal_reading']
    assert not any(s['status'] == 'source_context' for s in report['sections'])
