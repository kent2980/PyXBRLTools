from pathlib import Path

import pytest

from PyXBRLTools.xbrl_model.base_xbrl_model import BaseXbrlModel


@pytest.fixture
def xbrl_model(get_current_path):
    zip_dir = get_current_path / "data" / "xbrl_zip"
    zip_name = "edjp.zip"
    zip_path = zip_dir / zip_name
    output_path = get_current_path / "data" / "output"
    return BaseXbrlModel(zip_path.as_posix(), output_path.as_posix())


def test_xbrl_zip_path(xbrl_model, get_current_path):
    zip_dir = get_current_path / "data" / "xbrl_zip"
    zip_name = "edjp.zip"
    zip_path = zip_dir / zip_name
    assert xbrl_model.xbrl_zip_path == zip_path.as_posix()


# 解凍したディレクトリのパスを取得するメソッドをテストする
def test_directory_path(xbrl_model):
    assert isinstance(xbrl_model.directory_path, str)


# zipファイルを解凍するメソッドをテストする
def test_unzip_xbrl(xbrl_model):
    directory_path = xbrl_model._BaseXbrlModel__unzip_xbrl()
    assert isinstance(directory_path, str)
    assert Path(directory_path).exists()


def test_xbrl_type(xbrl_model):
    xbrl_type = xbrl_model.xbrl_type
    assert xbrl_type in [
        "edjp",
        "edus",
        "edif",
        "edit",
        "rvdf",
        "rvfc",
        "rejp",
        "rrdf",
        "rrfc",
        "efjp",
    ]


def test__check_xbrl_files_in_dir(xbrl_model):
    assert xbrl_model._BaseXbrlModel__check_xbrl_files_in_dir("ixbrl.htm")
    assert xbrl_model._BaseXbrlModel__check_xbrl_files_in_dir("lab")
    assert xbrl_model._BaseXbrlModel__check_xbrl_files_in_dir("pre")
    assert xbrl_model._BaseXbrlModel__check_xbrl_files_in_dir("cal")
    assert xbrl_model._BaseXbrlModel__check_xbrl_files_in_dir("def")
    key = ("pre", "cal", "def")
    assert xbrl_model._BaseXbrlModel__check_xbrl_files_in_dir(*key)
