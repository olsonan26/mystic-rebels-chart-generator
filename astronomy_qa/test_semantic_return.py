"""Public structural check; real private-core tests are in local_integration_qa."""
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from semantic_return import Theme, return_base


def test_return_changes_semantic_role_not_original_expression_area():
    before=Theme('function','occupied-area')
    after=return_base(before,'represented-theme')
    assert after.function==before.function
    assert after.expressed_in==before.expressed_in
    assert after.qualified_by==('represented-theme',)
    assert after!=return_base(Theme('function','represented-theme'),'occupied-area')


