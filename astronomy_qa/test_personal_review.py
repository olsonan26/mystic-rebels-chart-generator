"""Public export-boundary tests; NOT interpretation-quality tests."""
import importlib.util
from pathlib import Path
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('personal_review',ROOT/'scripts/personal_review.py')
review=importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


def test_report_escapes_identity_and_displays_unapproved_scope():
    packet={'report':{'profile':{'name':'<script>private</script>'}},'claims':[],
            'draft':{'recognition':'Hypothesis only','explanation':'Incomplete condition.', 'practical_application':[]}}
    result=review.render(packet)
    assert '<script>private</script>' not in result
    assert '&lt;script&gt;' in result
    assert 'Unapproved interpretation hypothesis' in result
    assert 'Do not publish' in result


def test_private_output_cannot_be_written_into_public_source(monkeypatch):
    monkeypatch.setattr(sys,'argv',['personal_review','--input','not-read.json','--output',str(ROOT/'docs/leaked-review')])
    with pytest.raises(ValueError,match='ignored consumer tmp'):
        review.main()
