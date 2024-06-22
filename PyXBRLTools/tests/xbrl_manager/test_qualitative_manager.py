from pathlib import Path
import pytest
from PyXBRLTools.xbrl_manager.qualitative_manager import QualitativeManager
from PyXBRLTools.xbrl_exception.xbrl_manager_exception import XbrlDirectoryNotFoundError

@pytest.fixture
def qualitative_manager(get_current_path):
    test_dir = get_current_path / "data" / "xbrl" / "edjp"
    manager = QualitativeManager(test_dir)
    return manager

def test_qualitative_manager_init(qualitative_manager, get_current_path):
    assert qualitative_manager.directory_path == get_current_path / "data" / "xbrl" / "edjp"
    assert qualitative_manager.files["xlink_href"].iloc[0].split("/")[-1] == "qualitative.htm"

# ディレクトリ内にファイルが存在しない場合
def test_qualitative_manager_init_empty_files():
    with pytest.raises(XbrlDirectoryNotFoundError) as e:
        directory_path = "/path/to/empty/directory"
        QualitativeManager(directory_path)
    assert e.type == XbrlDirectoryNotFoundError