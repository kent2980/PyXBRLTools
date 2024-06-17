import pytest
from pandas import DataFrame
from PyXBRLTools.xbrl_manager.label_manager import LabelManager
from PyXBRLTools.xbrl_parser.label_parser import LabelParser
from pathlib import Path

def get_current_dir():
    # Get the current directory path
    current_dir = Path(__file__).resolve().parent.parent
    return current_dir

def get_output_dir():
    # Get the output directory path
    output_dir = get_current_dir() / "data" / "label"
    return output_dir.as_posix()

@pytest.fixture
def label_manager() ->  LabelManager:
    # Get the test directory path
    test_dir = get_current_dir() / "data" / "edjp"
    return LabelManager(test_dir.as_posix())

def test_set_label(label_manager):
    result = label_manager.set_label(get_output_dir())
    result.to_json(str(get_current_dir() / "output" / "label.json"))
    assert isinstance(result, LabelManager)
    assert isinstance(result.to_DataFrame(), DataFrame)
    assert len(result.to_dict()) > 0
    assert result.to_DataFrame().iloc[0].to_dict() == {
            "xlink_type": "resource",
            "xlink_label": "label_CostForTheMeetingOfShareholdersEL",
            "xlink_role": "http://www.xbrl.org/2003/role/label",
            "xml_lang": "ja",
            "id": "label_CostForTheMeetingOfShareholdersEL",
            "label": "株主提案対応費用",
            "xlink_schema": "tse-acedjpfr-58200-2024-03-31-01-2024-05-14.xsd"
        }

def test_set_label_with_document_type(label_manager):
    result = label_manager.set_label(get_output_dir(), document_type="sm")
    assert isinstance(result, LabelManager)
    assert isinstance(result.to_DataFrame(), DataFrame)
    assert len(result.to_DataFrame()) > 0

def test_set_label_with_invalid_document_type(label_manager):
    result = label_manager.set_label(get_output_dir(), document_type="bs")
    assert isinstance(result, LabelManager)
    assert isinstance(result.to_DataFrame(), DataFrame)
    assert len(result.to_DataFrame()) == 0

def test_set_label_with_html_files(label_manager):
    # Add test cases to check if the label is set correctly for HTML files
    pass

def test_set_label_with_non_html_files(label_manager):
    # Add test cases to check if the label is set correctly for non-HTML files
    pass