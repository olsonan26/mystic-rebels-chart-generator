"""Packaging integrity: no approval, context, or conflicting source is lost."""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('report_export',ROOT/'scripts/export_report_knowledge.py')
export=importlib.util.module_from_spec(spec)
spec.loader.exec_module(export)


def test_bundle_preserves_every_canonical_document_and_gate():
    outputs=export.build()
    bundle=json.loads(outputs['data/knowledge/report_knowledge_bundle.json'])
    for key,name in export.SOURCES.items():
        assert bundle['documents'][key]==json.loads((ROOT/'data/knowledge'/name).read_text())
    assert bundle['contract']['personal_answer_approved'] is False
    assert bundle['contract']['all_important_knowledge_covered'] is False
    assert not bundle['contract']['private_originals_pdf_ocr_indexes_included']


def test_topic_packets_keep_matching_conflicts_and_dependencies():
    outputs=export.build()
    manifest=json.loads(outputs['data/knowledge/report_knowledge_manifest.json'])
    source=json.loads(outputs['data/knowledge/report_knowledge_bundle.json'])['documents']
    for entry in manifest['topic_packets'].values():
        raw=outputs[entry['path']]
        packet=json.loads(raw)
        ids=set(packet['transitive_concept_ids'])
        assert set(packet['initial_concept_ids'])<=ids
        assert {r['id'] for r in packet['concepts']}==ids
        assert all(set(r['requires_concepts'])<=ids for r in packet['concepts'])
        assert packet['assertions']==[a for a in source['assertions']['assertions'] if a['concept_id'] in ids]
        assert packet['findings']==[f for f in source['findings']['findings'] if ids.intersection(f['concept_ids'])]
        assert packet['contract']['personal_answer_approved'] is False
        assert len(raw)<1000000


def test_export_check_rejects_stale_canonical_meaning(tmp_path,monkeypatch):
    for name in export.SOURCES.values():
        p=tmp_path/'data/knowledge'/name
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes((ROOT/'data/knowledge'/name).read_bytes())
    monkeypatch.setattr(export,'ROOT',tmp_path)
    monkeypatch.setattr(sys,'argv',['export_report_knowledge.py'])
    export.main()
    monkeypatch.setattr(sys,'argv',['export_report_knowledge.py','--check'])
    export.main()
    p=tmp_path/'data/knowledge/interpretive_inventory.json'
    data=json.loads(p.read_text())
    data['records'][0]['meaning_summary']+=' Changed source summary in isolated fixture.'
    p.write_text(json.dumps(data))
    with pytest.raises(SystemExit,match='Stale/missing knowledge export'):
        export.main()


def test_generated_outputs_are_deterministic_and_current():
    first=export.build()
    assert first==export.build()
    assert all((ROOT/p).read_bytes()==raw for p,raw in first.items())


def test_export_survives_git_checkout_line_ending_changes(tmp_path,monkeypatch):
    baseline=export.build()
    for index,name in enumerate(export.SOURCES.values()):
        path=tmp_path/'data/knowledge'/name
        path.parent.mkdir(parents=True,exist_ok=True)
        raw=(ROOT/'data/knowledge'/name).read_bytes().replace(b'\r\n',b'\n')
        path.write_bytes(raw if index%2 else raw.replace(b'\n',b'\r\n'))
    monkeypatch.setattr(export,'ROOT',tmp_path)
    assert export.build()==baseline
