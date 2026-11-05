"""Optional presentation specialist; never an interpretation authority.

Current output contract deliberately permits selection of approved wording only.
Arbitrary paraphrases cannot be certified by string/keyword or model-based checks.
Core packets are recomputed on the server and are NEVER eligible for external
egress in this prototype. Only hard-coded, invented calibration packets can leave.
No route accepts writer packets, provider names, approval flags or API keys.
"""
from dataclasses import dataclass
import hashlib
import json
from typing import Protocol


@dataclass(frozen=True)
class Claim:
    id: str
    variants: tuple[str, ...]


@dataclass(frozen=True)
class Section:
    id: str
    claims: tuple[Claim, ...]


@dataclass(frozen=True)
class Packet:
    sections: tuple[Section, ...]
    authority: str
    external_egress: bool = False
    complete_personal_reading: bool = False

    @property
    def digest(self):
        return hashlib.sha256(json.dumps(self.payload(), sort_keys=True).encode()).hexdigest()

    def payload(self):
        return {'contract': 'approved-wording-selection/1', 'sections': [
            {'id': s.id, 'claims': [{'id': c.id, 'variants': list(c.variants)} for c in s.claims]}
            for s in self.sections], 'complete_personal_reading': False}


class Writer(Protocol):
    def select(self, payload: dict) -> object: ...


def synthetic_packet(case='balanced'):
    """Invented engineering calibration, no astrology or user/source material."""
    if case not in {'balanced', 'limited', 'reflection'}:
        raise ValueError('Unknown synthetic benchmark case')
    text = {
        'balanced': ('This demonstration contains three approved observations.',
                     'Three approved observations are included in this demonstration.'),
        'limited': ('Some information is unavailable in this demonstration.',
                    'This demonstration leaves unavailable information open.'),
        'reflection': ('You may choose which topic to discuss first.',
                       'The choice of which topic to discuss first is yours.'),
    }
    return Packet((Section('overview', (
        Claim('observation', text[case]),
        Claim('limit', ('This is an invented writing test, not a personal interpretation.',
                        'This invented example tests writing only; it is not a personal interpretation.')),
    )),), authority='invented_calibration_not_methodology', external_egress=True)


def core_packet(chart, question, owner_id, *, motion=None):
    """Independent core calculation/approval precedes any presentation operation.

    No candidate packet or approval boolean can substitute for recomputation.
    Core sentences receive no model-authored alternatives. Existing reading gates
    and source limitations remain intact. This packet can only render locally.
    """
    from nadia_runtime import verified_core
    core = verified_core()
    from nadia_core.synthesis import compose, validate_composition
    evidence = compose(core, chart, question, owner_id, motion=motion)
    validation = validate_composition(core, evidence, chart, question, owner_id, motion=motion)
    if (not validation['valid'] or evidence['personal_reading_allowed'] is not False
            or evidence['complete_question_answer'] is not False):
        raise ValueError('Core authority validation failed')
    claims = tuple(Claim(c['claim_id'], (c['sentence'],)) for c in evidence['claims'])
    # All output limitations travel with every rendered result, rather than being
    # left to a model to remember. Raw provenance/chart/source data never leaves.
    limits = tuple(dict.fromkeys(str(v) for c in evidence['claims']
                                for v in tuple(c['missing_dependencies']) + tuple(c['exceptions'])))
    mandatory = Claim('complete-reading-limit', (
        'Scoped chart components only. Complete personal interpretation is unavailable.',))
    detail = Claim('unresolved-dependencies', ('Unresolved dependencies: ' + ', '.join(limits),))
    return Packet((Section('components', claims), Section('limitations', (mandatory, detail))),
                  authority='recomputed_private_core:' + core.version, external_egress=False)


def validate_selection(packet, candidate):
    """Closed schema; every claim exactly once, approved wording index only.

    Section order is fixed to protect assessment/scope. Claim order within a
    section may change for readability; qualifications cannot be dropped.
    No semantic-entailment claim is made for arbitrary generated prose.
    """
    if not isinstance(candidate, dict) or set(candidate) != {'sections'}:
        return False
    sections = candidate['sections']
    if not isinstance(sections, list) or len(sections) != len(packet.sections):
        return False
    for section, actual in zip(packet.sections, sections):
        if not isinstance(actual, dict) or set(actual) != {'id', 'claims'} or actual['id'] != section.id:
            return False
        claims = actual['claims']
        approved = {c.id: c for c in section.claims}
        if not isinstance(claims, list) or len(claims) != len(approved):
            return False
        seen = set()
        for choice in claims:
            if not isinstance(choice, dict) or set(choice) != {'id', 'variant'}:
                return False
            identity, index = choice['id'], choice['variant']
            if not isinstance(identity, str) or identity not in approved or identity in seen:
                return False
            if type(index) is not int or not 0 <= index < len(approved[identity].variants):
                return False
            seen.add(identity)
    return True


def deterministic(packet):
    return {'sections': [{'id': s.id, 'claims': [{'id': c.id, 'variant': 0} for c in s.claims]}
                         for s in packet.sections]}


def render(packet, writer: Writer | None = None):
    selection = deterministic(packet)
    accepted = False
    reason = 'writer_disabled' if writer is None else 'external_egress_prohibited'
    if writer is not None and packet.external_egress and packet == synthetic_packet_for(packet):
        try:
            proposed = writer.select(packet.payload())
            if validate_selection(packet, proposed):
                selection, accepted, reason = proposed, True, 'approved_wording_only'
            else:
                reason = 'invalid_selection'
        except Exception:
            # Do not log credentials, prompts, private evidence or provider bodies.
            reason = 'provider_unavailable'
    by_section = {s.id: {c.id: c for c in s.claims} for s in packet.sections}
    return {'sections': [{'id': s['id'], 'sentences': [
        {'claim_id': c['id'], 'text': by_section[s['id']][c['id']].variants[c['variant']]}
        for c in s['claims']]} for s in selection['sections']],
        'writer_used': accepted, 'fallback_reason': None if accepted else reason,
        'evidence_digest': packet.digest, 'complete_personal_reading': False,
        'validation_scope': 'exact_approved_wording_not_arbitrary_prose_entailment'}


def synthetic_packet_for(packet):
    # Exact immutable fixture equality is the egress boundary. Caller-set labels,
    # flags or extra user text do not confer authorization to transmit anything.
    return next((p for p in (synthetic_packet(c) for c in ('balanced', 'limited', 'reflection'))
                 if p == packet), None)


class OpenRouterWriter:
    """Replaceable transport, bounded requests; credential held only in memory."""
    def __init__(self, api_key, model, *, timeout=20.0):
        if not isinstance(model, str) or not model or len(model) > 150:
            raise ValueError('Explicit model identifier required')
        self._key, self.model, self.timeout = api_key, model, timeout

    def select(self, payload):
        # Defense in depth: reject any payload except the three exact synthetic
        # fixtures even if a caller invokes this transport directly.
        if payload not in [synthetic_packet(c).payload() for c in ('balanced', 'limited', 'reflection')]:
            raise ValueError('Only invented calibration packets may be transmitted')
        self.last_usage, self.last_http_status, self.last_finish_reason = {}, None, None
        import httpx
        response = httpx.post('https://openrouter.ai/api/v1/chat/completions',
            headers={'Authorization': 'Bearer ' + self._key}, timeout=self.timeout,
            json=provider_request(self.model, payload))
        self.last_http_status = response.status_code
        response.raise_for_status()
        data = response.json()
        finish = data.get('choices', [{}])[0].get('finish_reason')
        self.last_finish_reason = finish if finish in ('stop', 'length', 'content_filter', 'tool_calls', 'error') else None
        usage = data.get('usage', {})
        self.last_usage = {k: usage[k] for k in ('prompt_tokens', 'completion_tokens', 'total_tokens', 'cost')
                           if type(usage.get(k)) in (int, float)}
        return json.loads(data['choices'][0]['message']['content'])


def provider_request(model, payload):
    return {'model': model, 'temperature': 0, 'max_tokens': 384,
            'provider': {'data_collection': 'deny', 'zdr': True, 'require_parameters': True},
            'response_format': {'type': 'json_object'},
            'messages': [{'role': 'system', 'content':
                'You are an optional presentation specialist, never an interpretation engine. '
                'Select approved wording variants and order claims for clarity, gentle tone and readability. '
                'Return ONLY {"sections":[{"id":"section id","claims":[{"id":"claim id","variant":0}]}]}. '
                'Preserve section order and EVERY claim exactly once. Use zero-based integer variant indexes. '
                'Add no prose, facts, conclusions, predictions, psychology, explanations or keys.'},
                {'role': 'user', 'content': json.dumps(payload, sort_keys=True)}]}
