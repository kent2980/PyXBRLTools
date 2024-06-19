from pathlib import Path
import pytest
from PyXBRLTools.xbrl_manager.qualitative_manager import QualitativeManager
from PyXBRLTools.xbrl_exception.xbrl_manager_exception import XbrlListEmptyError
from PyXBRLTools.tests.xbrl_manager.test_base_xbrl_manager import get_current_dir

def get_current_dir ():
    # Get the current directory path
    current_dir = Path(__file__).resolve().parent.parent
    return current_dir

@pytest.fixture
def qualitative_manager():
    directory_path = "/path/to/directory"
    test_dir = get_current_dir() / "data" / "xbrl" / "edjp"
    manager = QualitativeManager(test_dir)
    return manager

def test_qualitative_manager_init(qualitative_manager):
    assert qualitative_manager.directory_path == "/path/to/directory"
    assert qualitative_manager.htmlbase_files == "qualitative"

def test_qualitative_manager_init_empty_files():
    with pytest.raises(XbrlListEmptyError):
        directory_path = "/path/to/empty/directory"
        QualitativeManager(directory_path)

def test_qualitative_manager_qualitative_infos(qualitative_manager):
    result = qualitative_manager.qualitative_infos()
    assert isinstance(result.data, list)
    # Add more assertions based on the expected behavior of the method