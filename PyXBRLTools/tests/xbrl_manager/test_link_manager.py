import pytest
from PyXBRLTools.xbrl_parser.link_parser import PreLinkParser
from PyXBRLTools.xbrl_manager.link_manager import PreLinkManager

@pytest.fixture
def pre_link_manager() -> PreLinkManager:
    directory_path = "/Users/user/Vscode/python/PyXBRLTools/PyXBRLTools/tests/data/xbrl/edjp"
    return PreLinkManager(directory_path)

def test_get_parser(pre_link_manager):
    # Test get_parser method
    result = pre_link_manager.get_parser()
    assert result == PreLinkParser

def test_get_role(pre_link_manager):
    # Test get_role method
    result = pre_link_manager.get_role()
    assert result == "presentationLinkbaseRef"

def test_set_link_roles(pre_link_manager):
    # Test set_link_roles method
    output_path = "/Users/user/Vscode/python/PyXBRLTools/PyXBRLTools/tests/data/link"
    result = pre_link_manager.set_link_roles(output_path)
    assert isinstance(result, PreLinkManager)
    print(result.to_DataFrame())
    assert result.label is not None
    assert result.data is not None

def test_set_link_locs(pre_link_manager):
    # Test set_link_locs method
    output_path = "/Users/user/Vscode/python/PyXBRLTools/PyXBRLTools/tests/data/link"
    result = pre_link_manager.set_link_locs(output_path)
    print(result.to_DataFrame())
    assert isinstance(result, PreLinkManager)
    assert result.label is not None
    assert result.data is not None
    assert result.label.equals(result.data)

def test_set_link_arcs(pre_link_manager):
    # Test set_link_arcs method
    output_path = "/Users/user/Vscode/python/PyXBRLTools/PyXBRLTools/tests/data/link"
    result = pre_link_manager.set_link_arcs(output_path)
    print(result.to_DataFrame())
    assert isinstance(result, PreLinkManager)
    assert result.label is not None
    assert result.data is not None
    assert result.label.equals(result.data)