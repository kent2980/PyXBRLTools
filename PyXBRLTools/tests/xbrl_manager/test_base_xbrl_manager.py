import pytest
from pandas import DataFrame
from PyXBRLTools.xbrl_parser.ixbrl_parser import IxbrlParser
from bs4 import BeautifulSoup as bs
from PyXBRLTools.xbrl_manager.base_xbrl_manager import BaseXbrlManager
from pathlib import Path

def get_current_dir():
    # 現在のディレクトリのパスを取得
    current_dir = Path(__file__).resolve().parent.parent
    return current_dir

@pytest.fixture
def base_xbrl_manager():
    # tests/data/edjpディレクトリのパスを取得
    test_dir = get_current_dir() / "data" / "edjp"
    return BaseXbrlManager(test_dir.as_posix())

def test_xbrl_type(base_xbrl_manager):
    result = base_xbrl_manager.xbrl_type()
    assert isinstance(result, tuple)
    assert len(result) == 2

def test_set_linkbase_files(base_xbrl_manager):
    result = base_xbrl_manager.set_linkbase_files()
    assert isinstance(result, BaseXbrlManager)
    assert isinstance(result.files, DataFrame)

def test_set_htmlbase_files(base_xbrl_manager):
    result = base_xbrl_manager.set_htmlbase_files()
    assert isinstance(result, BaseXbrlManager)
    assert isinstance(result.files, DataFrame)

def test_to_csv(base_xbrl_manager):
    file_path = get_current_dir() / "output" / "output.csv"
    base_xbrl_manager.data = {"column1": [1, 2, 3], "column2": ["a", "b", "c"]}
    base_xbrl_manager.to_csv(file_path.as_posix())
    # Add assertions to check if the CSV file is created successfully

def test_to_DataFrame(base_xbrl_manager):
    base_xbrl_manager.data = {"column1": [1, 2, 3], "column2": ["a", "b", "c"]}
    result = base_xbrl_manager.to_DataFrame()
    assert isinstance(result, DataFrame)
    assert len(result) > 0

def test_to_json(base_xbrl_manager):
    file_path = get_current_dir() / "output" / "output.json"
    base_xbrl_manager.data = {"column1": [1, 2, 3], "column2": ["a", "b", "c"]}
    base_xbrl_manager.to_json(file_path.as_posix())
    # Add assertions to check if the JSON file is created successfully

def test_to_dict(base_xbrl_manager):
    base_xbrl_manager.data = {"column1": [1, 2, 3], "column2": ["a", "b", "c"]}
    result = base_xbrl_manager.to_dict()
    assert isinstance(result, dict)
    assert len(result) > 0