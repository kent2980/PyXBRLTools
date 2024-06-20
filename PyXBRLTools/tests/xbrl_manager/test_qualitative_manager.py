from pathlib import Path
import pytest
from PyXBRLTools.xbrl_manager.qualitative_manager import QualitativeManager
from PyXBRLTools.xbrl_exception.xbrl_manager_exception import XbrlDirectoryNotFoundError

def get_current_dir ():
    # Get the current directory path
    current_dir = Path(__file__).resolve().parent.parent
    return current_dir

@pytest.fixture
def qualitative_manager():
    test_dir = get_current_dir() / "data" / "xbrl" / "edjp"
    manager = QualitativeManager(test_dir)
    return manager

def test_qualitative_manager_init(qualitative_manager):
    assert qualitative_manager.directory_path == get_current_dir() / "data" / "xbrl" / "edjp"
    assert qualitative_manager.files["xlink_href"].iloc[0].split("/")[-1] == "qualitative.htm"

# ディレクトリ内にファイルが存在しない場合
def test_qualitative_manager_init_empty_files():
    with pytest.raises(XbrlDirectoryNotFoundError) as e:
        directory_path = "/path/to/empty/directory"
        QualitativeManager(directory_path)
    assert e.type == XbrlDirectoryNotFoundError