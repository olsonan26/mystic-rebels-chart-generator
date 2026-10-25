"""Line matches locate evidence; they cannot approve source meaning or fix OCR."""
import pytest
from knowledge_audit.line_reconciliation import reconcile,page_index,text_hash,validate_annotation
from knowledge_audit import source_pipeline


def test_reflow_mapping_keeps_numeric_change_and_unmatched_line_unapproved():
    pages={1:'The Moon nucleus is at 25:42 and remains beyond reach.',
           2:'This next sentence continues across the reflowed page.'}
    data={'lines':[{'text':'The Moon nucleus is at 25:57 and remains beyond reach.'},
        {'text':'This next sentence continues across the reflowed page.'},
        {'text':'A missing unique passage about an asteroid.'}]}
    public,private,ranked=reconcile(data,pages,page_index(pages),{p:text_hash(t) for p,t in pages.items()})
    assert public[0]['matched_tokens']<public[0]['tokens']
    assert public[0]['visual_transcription_status']=='PENDING'
    assert 'NUMERIC_OR_GLYPH_PRESENT' in public[0]['review_flags']
    assert public[1]['comparison_status']=='AUTO_MATCH_CANDIDATE'
    assert public[1]['pdf_spans'][0]['pdf_page']==2
    assert public[2]['comparison_status']=='NO_MATCH_CANDIDATE'
    assert all(l['visual_transcription_status']=='PENDING' for l in public)
    assert private[0]['source_text'].endswith('beyond reach.')
    assert 'source_text' not in public[0]


def test_visual_annotations_reject_wrong_source_or_nonexistent_lines():
    row={'content_sha256':'image','ocr_output_sha256':'ocr'}
    note=dict(image_sha256='image',ocr_output_sha256='ocr',line_ranges=[[1,1]],finding='checked',printed_header='687')
    validate_annotation(note,row,{'lines':[{}]})
    with pytest.raises(ValueError,match='drift'):
        validate_annotation(dict(note,image_sha256='other'),row,{'lines':[{}]})
    with pytest.raises(ValueError,match='outside'):
        validate_annotation(dict(note,line_ranges=[[1,2]]),row,{'lines':[{}]})


def test_checkpoint_recovers_transient_windows_lock_and_bounds_permanent_failure(tmp_path,monkeypatch):
    path=tmp_path/'state.json'; path.write_text('old')
    replace=source_pipeline.os.replace; calls=[]
    def locked_then_ok(src,dst):
        calls.append(1)
        assert path.read_text()=='old'
        if len(calls)<3: raise PermissionError('Transient indexing lock')
        replace(src,dst)
    monkeypatch.setattr(source_pipeline.os,'replace',locked_then_ok)
    monkeypatch.setattr(source_pipeline.time,'sleep',lambda n:None)
    source_pipeline.save_json(path,{'checkpoint':'complete'})
    assert len(calls)==3 and source_pipeline.load_state(path)=={'checkpoint':'complete'}
    def always_locked(src,dst): raise PermissionError('Permanent lock')
    monkeypatch.setattr(source_pipeline.os,'replace',always_locked)
    with pytest.raises(PermissionError): source_pipeline.save_json(path,{'checkpoint':'next'})
    assert source_pipeline.load_state(path)=={'checkpoint':'complete'}
    assert path.with_suffix('.json.tmp').exists()


def test_reinspection_retains_historical_and_new_chiron_counterevidence():
    from knowledge_audit.sources import original_witnesses
    from knowledge_audit.requirements import load_requirements,validate_requirements
    witnesses=[w for w in original_witnesses(['chiron']) if w['original_printed_page']=='687']
    assert len(witnesses)==2
    assert len({w['review_summary'] for w in witnesses})==2
    data=load_requirements()
    requirement=next(r for r in data['requirements'] if r['concept_ids']==['chiron'])
    assert all(w in requirement['original_scan_witnesses'] for w in witnesses)
    requirement['original_scan_witnesses'].remove(witnesses[0])
    with pytest.raises(ValueError,match='original counterevidence'):
        validate_requirements(data,check_files=False)


def test_printed_chart_geometry_distinguishes_competing_branches():
    # Check the actual arithmetic behind the new source findings, not an engine
    # output or an assumed epoch. The inputs are the inspected diagram labels.
    saturn=240*60+19*60+7
    chiron=300*60+19*60+18
    assert chiron-saturn==60*60+11
    moon=25*60+57; radius=90
    drawn_pluto=24*60+15; prose_pluto=24*60+42
    assert moon-(drawn_pluto+radius)==12
    assert (prose_pluto+radius)-moon==15
