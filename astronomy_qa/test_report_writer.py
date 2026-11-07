"""Writer cannot become an authority or an escape hatch for private data."""
from dataclasses import replace
from unittest.mock import Mock, patch
import pytest

from mystic_rebels.report_writer import (Claim, Section, Packet, synthetic_packet,
    deterministic, validate_selection, render, OpenRouterWriter, core_packet)


def test_report_functions_without_any_model_or_key(monkeypatch):
    monkeypatch.delenv('OPENROUTER_API_KEY', raising=False)
    packet = synthetic_packet()
    result = render(packet)
    assert not result['writer_used']
    assert result['fallback_reason'] == 'writer_disabled'
    assert not result['complete_personal_reading']


def test_writer_can_select_variants_and_order_but_not_omit_limits():
    packet = synthetic_packet()
    choice = {'sections': [{'id': 'overview', 'claims': [
        {'id': 'limit', 'variant': 1}, {'id': 'observation', 'variant': 1}]}]}
    writer = Mock(select=Mock(return_value=choice))
    result = render(packet, writer)
    assert result['writer_used']
    assert result['sections'][0]['sentences'][0]['text'] == packet.sections[0].claims[1].variants[1]
    assert result['evidence_digest'] == packet.digest


@pytest.mark.parametrize('mutation', ['prose', 'new_fact', 'drop_limit', 'duplicate', 'index', 'boolean', 'section', 'wrong_type'])
def test_any_unapproved_output_falls_back_exactly(mutation):
    packet = synthetic_packet()
    choice = deterministic(packet)
    if mutation == 'prose': choice['intro'] = 'You are destined for success.'
    elif mutation == 'new_fact': choice['sections'][0]['claims'][0]['text'] = 'You fear abandonment.'
    elif mutation == 'drop_limit': choice['sections'][0]['claims'].pop()
    elif mutation == 'duplicate': choice['sections'][0]['claims'][1] = choice['sections'][0]['claims'][0]
    elif mutation == 'index': choice['sections'][0]['claims'][0]['variant'] = 999
    elif mutation == 'boolean': choice['sections'][0]['claims'][0]['variant'] = True
    elif mutation == 'section': choice['sections'][0]['id'] = 'invented'
    else: choice = 'unrestricted text'
    writer = Mock(select=Mock(return_value=choice))
    result = render(packet, writer)
    expected = render(packet)
    assert result['sections'] == expected['sections']
    assert result['fallback_reason'] == 'invalid_selection'


def test_timeout_and_provider_failure_never_break_template():
    packet = synthetic_packet()
    result = render(packet, Mock(select=Mock(side_effect=TimeoutError('secret provider response'))))
    assert result['sections'] == render(packet)['sections']
    assert result['fallback_reason'] == 'provider_unavailable'
    assert 'secret' not in str(result)


def test_labels_flags_and_injection_do_not_authorize_egress():
    original = synthetic_packet()
    for packet in [replace(original, sections=(Section('overview', (Claim('new', ('private birth data',)),)),)),
                   replace(original, authority='invented_calibration_not_methodology_with_injection'),
                   replace(original, complete_personal_reading=True),
                   Packet(original.sections, 'private_core', external_egress=True)]:
        writer = Mock()
        result = render(packet, writer)
        writer.select.assert_not_called()
        assert not result['writer_used']


def test_transport_cannot_send_private_payload_even_if_called_directly():
    writer = OpenRouterWriter('not-a-real-token', 'replaceable/model')
    with patch('httpx.post') as network:
        with pytest.raises(ValueError):
            writer.select({'birth_name': 'private', 'book_excerpt': 'restricted'})
    network.assert_not_called()


def test_core_claims_are_recomputed_and_never_sent():
    try:
        from nadia_runtime import verified_core
        verified_core()
    except (OSError, ValueError, ImportError):
        with pytest.raises((OSError, ValueError, ImportError)):
            core_packet({}, 'synthetic question', 'synthetic owner')
        return
    bodies = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
    chart = {'ascendant': 0, 'positions': {b: {'longitude': i * 30 + 15,
        'retrograde': False, 'longitude_speed_deg_day': 1} for i, b in enumerate(bodies)}}
    packet = core_packet(chart, 'What are the chart components?', 'synthetic-owner')
    writer = Mock()
    result = render(packet, writer)
    writer.select.assert_not_called()
    assert not packet.external_egress and not result['complete_personal_reading']
    assert result['sections'][-1]['id'] == 'limitations'


def test_existing_report_generator_never_depends_on_writer():
    from mystic_rebels.models import BirthInput
    from mystic_rebels.profile_reports import ProfileRequest, generate_report
    birth = BirthInput(name='Synthetic integration fixture', local_date='2000-01-01', local_time='12:00:00',
                       timezone='Etc/UTC', latitude=51.4779, longitude=0)
    with patch.object(OpenRouterWriter, 'select', side_effect=AssertionError('Report must remain independent')) as writer:
        report = generate_report(ProfileRequest(birth=birth, synthetic=True))
    writer.assert_not_called()
    assert report['readiness']['technical_report_ready']
    assert not report['readiness']['complete_personal_reading']
