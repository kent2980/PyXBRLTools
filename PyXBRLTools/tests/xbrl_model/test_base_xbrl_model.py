import pytest
from pathlib import Path
from PyXBRLTools.xbrl_model.base_xbrl_model import BaseXbrlModel
from PyXBRLTools.tests.xbrl_manager.test_base_xbrl_manager import test_xbrl_type

def get_current_path() -> Path:
    return Path(__file__).resolve().parent.parent

@pytest.fixture
def xbrl_model():
    zip_dir = get_current_path() / "data" / "xbrl_zip"
    zip_name = "081220240327560965.zip"
    zip_path = zip_dir / zip_name
    return BaseXbrlModel(zip_path.as_posix())

def test_xbrl_zip_path(xbrl_model):
    zip_dir = get_current_path() / "data" / "xbrl_zip"
    zip_name = "081220240327560965.zip"
    zip_path = zip_dir / zip_name
    assert xbrl_model.xbrl_zip_path == zip_path.as_posix()

# 解凍したディレクトリのパスを取得するメソッドをテストする
def test_directory_path(xbrl_model):
    assert isinstance(xbrl_model.directory_path, str)

# zipファイルを解凍するメソッドをテストする
def test_unzip_xbrl(xbrl_model):
    directory_path = xbrl_model.unzip_xbrl()
    assert isinstance(directory_path, str)
    assert Path(directory_path).exists()

def test_xbrl_type(xbrl_model):
    xbrl_type = xbrl_model.xbrl_type
    assert xbrl_type in ["edjp", "edus", "edif", "edit", "rvdf", "rvfc", "rejp", "rrdf", "rrfc", "efjp"]

