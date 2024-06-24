import pytest
from pandas import DataFrame
from PyXBRLTools.xbrl_manager.label_manager import LabelManager
from pathlib import Path

@pytest.fixture
def get_output_dir(get_current_path):
    # Get the output directory path
    output_dir = get_current_path / "data" / "label"
    return output_dir.as_posix()

@pytest.fixture
def label_manager(get_current_path, get_output_dir) ->  LabelManager:
    # Get the test directory path
    test_dir = get_current_path / "data" / "xbrl" / "edjp"
    return LabelManager(test_dir.as_posix()).set_output_path(get_output_dir)

def test_set_link_labels(label_manager, get_current_path):
    result = label_manager.set_link_labels()
    result.to_json(str(get_current_path / "output" / "label.json"))
    assert isinstance(result, LabelManager)
    assert isinstance(result.to_DataFrame(), DataFrame)
    assert len(result.to_dict()) > 0
    # assert result.to_DataFrame().iloc[0].to_dict() == {
    #         "xlink_type": "resource",
    #         "xlink_label": "label_CostForTheMeetingOfShareholdersEL",
    #         "xlink_role": "http://www.xbrl.org/2003/role/label",
    #         "xml_lang": "ja",
    #         "id": "label_CostForTheMeetingOfShareholdersEL",
    #         "label": "株主提案対応費用",
    #         "xlink_schema": "tse-acedjpfr-58200-2024-03-31-01-2024-05-14.xsd"
    #     }

def test_set_label_with_document_type(label_manager):
    result = label_manager.set_link_labels(document_type="sm")
    assert isinstance(result, LabelManager)
    assert isinstance(result.to_DataFrame(), DataFrame)
    assert len(result.to_DataFrame()) > 0

def test_set_label_with_invalid_document_type(label_manager):
    result = label_manager.set_link_labels(document_type="bs")
    assert isinstance(result, LabelManager)
    assert isinstance(result.to_DataFrame(), DataFrame)
    assert len(result.to_DataFrame()) == 0

def test_set_link_locs(label_manager):
    result = label_manager.set_link_locs()
    print(result.to_DataFrame().iloc[0].to_dict())
    assert isinstance(result, LabelManager)
    assert isinstance(result.to_DataFrame(), DataFrame)
    assert len(result.to_DataFrame()) > 0
    # assert result.to_DataFrame().iloc[0].to_dict() == {
    #     'xlink_type': 'locator',
    #     'xlink_schema': 'tse-acedjpfr-58200-2024-03-31-01-2024-05-14.xsd',
    #     'xlink_href': 'tse-acedjpfr-58200_CostForTheMeetingOfShareholdersEL',
    #     'xlink_label': 'CostForTheMeetingOfShareholdersEL'
    #     }

def test_set_link_locs_with_document_type(label_manager):
    result = label_manager.set_link_locs(document_type="sm")
    assert isinstance(result, LabelManager)
    assert isinstance(result.to_DataFrame(), DataFrame)
    assert len(result.to_DataFrame()) > 0

def test_set_link_label_arcs(label_manager):
    result = label_manager.set_link_label_arcs()
    assert isinstance(result, LabelManager)
    assert isinstance(result.to_DataFrame(), DataFrame)
    assert len(result.to_DataFrame()) > 0
    # assert result.to_DataFrame().iloc[0].to_dict() == {
    #     'xlink_type': 'arc',
    #     'xlink_arcrole': 'http://www.xbrl.org/2003/arcrole/concept-label',
    #     'xlink_from': 'CostForTheMeetingOfShareholdersEL',
    #     'xlink_to': 'label_CostForTheMeetingOfShareholdersEL',
    #     'xlink_schema': 'tse-acedjpfr-58200-2024-03-31-01-2024-05-14.xsd'
    #             }

def test_set_link_label_arcs_with_document_type(label_manager):
    result = label_manager.set_link_label_arcs(document_type="sm")
    assert isinstance(result, LabelManager)
    assert isinstance(result.to_DataFrame(), DataFrame)
    assert len(result.to_DataFrame()) > 0

def test_set_role_refs(label_manager):
    result = label_manager.set_role_refs()
    assert isinstance(result, LabelManager)
    assert isinstance(result.to_DataFrame(), DataFrame)
    assert len(result.to_DataFrame()) > 0
    # assert result.to_DataFrame().iloc[0].to_dict() == {
    #     'Role_URI': 'http://disclosure.edinet-fsa.go.jp/jpcrp/std/alt/Consolidated/role/label',
    #     'xlink_type': 'simple',
    #     'xlink_schema': '../jpcrp_rt_2023-12-01.xsd',
    #     'xlink_href': 'rol_std_altConsolidatedLabel'
    #     }