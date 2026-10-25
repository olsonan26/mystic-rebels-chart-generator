"""Verify local witness retrieval and publish metadata-only validation evidence."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from knowledge_audit.sources import load_manifest, validate_manifest
from knowledge_audit.requirements import load_requirements, validate_requirements, requirement_packet
from knowledge_audit.semantics import concept_packet, profile_gaps


def main():
    manifest, requirements = load_manifest(), load_requirements()
    validate_manifest(manifest)
    validate_requirements(requirements)
    database = ROOT / 'reference/knowledge-index.sqlite'
    selected = [
        ('sophia', 'lunar-context'),
        ('asteroid-eunomia', 'asteroid-detail'),
        ('forced-contact', 'relationships-graph'),
        ('chiron', 'asteroid-detail'),
        ('core-trinity', 'dynamic-layers'),
        ('asteroid-flora', 'asteroid-detail'),
        ('asteroid-ixion', 'asteroid-detail'),
        ('asteroid-nessus', 'asteroid-detail'),
        ('asteroid-sedna', 'asteroid-detail'),
        ('lunar-arcs', 'lunar-context'),
        ('anchors', 'life-purpose'),
        ('spectrum-meanings', 'relationships-graph'),
        ('clusters', 'relationships-graph'),
        ('handoff', 'relationships-graph'),
        ('vantage-resolution', 'relationships-graph'),
        ('quadrants', 'pattern-resolution'),
        ('free-theory', 'pattern-resolution'),
        ('intra-house', 'pattern-resolution'),
        ('parans', 'locational-profile'),
        ('local-space', 'locational-profile'),
        ('epoch-imprint', 'special-contexts'),
        ('synastry', 'synastry-profile'),
        ('retrograde-meaning', 'retrograde-profile'),
        ('eclipse', 'special-contexts'),
        ('returns', 'return-phases'),
        ('parts-mechanics', 'parts-profile'),
    ]
    packets = []
    for concept, section in selected:
        packet = concept_packet(concept, database, section)
        packets.append(dict(concept=concept, section=section, use=packet['use'],
            personal_answer_generated=packet['personal_answer_generated'],
            pdf_witness_pages=[w['pdf_page'] for w in packet['witnesses']],
            original_scans=[{k: w[k] for k in ('file_id','name','original_printed_page','content_sha256','reconciliation_status')}
                            for w in packet['original_scan_witnesses']],
            compiled_source_sha256=packet['source_sha256'], witness_policy=packet['witness_policy']))
        packets[-1]['original_atomic_assertion_ids'] = [a['id'] for a in packet['original_atomic_assertions']]
        packets[-1]['original_line_finding_ids'] = [f['id'] for f in packet['original_line_reconciliation_findings']]
    findings = json.loads((ROOT / 'data/knowledge/source_blocker_findings.json').read_text(encoding='utf-8'))['findings']
    expected_findings = {finding['id'] for finding in findings}
    retrieved_findings = {identity for packet in packets for identity in packet['original_line_finding_ids']}
    missing_findings = expected_findings - retrieved_findings
    if missing_findings:
        raise ValueError('Named findings missing from retrieval probes: ' + ', '.join(sorted(missing_findings)))
    requirement = requirement_packet('M08-04-01', database)
    out = dict(status='VERIFIED_LOCAL_METADATA_AND_REVIEWED_SUMMARY_RETRIEVAL',
        source_file_records=manifest['file_record_denominator'],
        printed_page_denominator=None, exhaustive_semantic_coverage=False,
        packets=packets, named_findings_retrieved=sorted(retrieved_findings),
        atomic_requirement_retrieved=requirement['requirement']['id'],
        personal_answer_generated=False, deployed_retrieval_verified=False,
        limitation='Original OCR candidates remain separate from reviewed concept packets. Concept packets contain reviewed summaries/assertions and linked conflicting findings, never automatically promote candidate OCR, and retain every compiled witness. Neither path is deployed answering.')
    evidence = ROOT / 'evidence/source-continuation/retrieval-check.json'
    evidence.write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
    gaps = profile_gaps()
    (ROOT / 'evidence/semantic-audit/profile-gaps.json').write_text(json.dumps(gaps, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(status=out['status'], selected_concepts=len(packets),
        atomic_requirement=out['atomic_requirement_retrieved'], personal_answer_generated=False)))


if __name__ == '__main__':
    main()
