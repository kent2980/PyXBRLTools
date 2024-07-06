from pathlib import Path

import pytest
from bs4 import BeautifulSoup as bs
from pandas import DataFrame

from PyXBRLTools.xbrl_manager.base_xbrl_manager import BaseXbrlManager
from PyXBRLTools.xbrl_parser.ixbrl_parser import IxbrlParser


@pytest.fixture
def base_xbrl_manager(get_current_path):
    # tests/data/edjpディレクトリのパスを取得
    test_dir = get_current_path / "data" / "xbrl" / "edjp"
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


def test_to_csv(base_xbrl_manager, get_current_path):
    file_path = get_current_path / "output" / "output.csv"
    base_xbrl_manager.data = {"column1": [1, 2, 3], "column2": ["a", "b", "c"]}
    base_xbrl_manager.to_csv(file_path.as_posix())
    # Add assertions to check if the CSV file is created successfully


def test_to_DataFrame(base_xbrl_manager):
    base_xbrl_manager.data = {"column1": [1, 2, 3], "column2": ["a", "b", "c"]}
    result = base_xbrl_manager.to_DataFrame()
    assert isinstance(result, DataFrame)
    assert len(result) > 0


def test_to_json(base_xbrl_manager, get_current_path):
    file_path = get_current_path / "output" / "output.json"
    base_xbrl_manager.data = {"column1": [1, 2, 3], "column2": ["a", "b", "c"]}
    base_xbrl_manager.to_json(file_path.as_posix())
    # Add assertions to check if the JSON file is created successfully


def test_to_dict(base_xbrl_manager):
    base_xbrl_manager.data = {"column1": [1, 2, 3], "column2": ["a", "b", "c"]}
    result = base_xbrl_manager.to_dict()
    assert isinstance(result, dict)
    assert len(result) > 0
