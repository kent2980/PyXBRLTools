import pytest
from pandas import DataFrame
from PyXBRLTools.xbrl_manager.label_manager import LabelManager
from PyXBRLTools.xbrl_parser.label_parser import LabelParser
from pathlib import Path

def get_current_dir():
    # Get the current directory path
    current_dir = Path(__file__).resolve().parent.parent
    return current_dir

@pytest.fixture
def label_manager():
    # Get the test directory path
    test_dir = get_current_dir() / "data" / "edjp"
    return LabelManager(test_dir.as_posix())

def test_set_label(label_manager):
    result = label_manager.set_label()
    assert isinstance(result, LabelManager)
    assert isinstance(result.label, DataFrame)
    assert len(result.label) > 0

def test_set_label_with_document_type(label_manager):
    result = label_manager.set_label(document_type="document_type")
    assert isinstance(result, LabelManager)
    assert isinstance(result.label, DataFrame)
    assert len(result.label) > 0

def test_set_label_with_invalid_document_type(label_manager):
    result = label_manager.set_label(document_type="invalid_document_type")
    assert isinstance(result, LabelManager)
    assert isinstance(result.label, DataFrame)
    assert len(result.label) == 0

def test_set_label_with_html_files(label_manager):
    # Add test cases to check if the label is set correctly for HTML files
    pass

def test_set_label_with_non_html_files(label_manager):
    # Add test cases to check if the label is set correctly for non-HTML files
    pass