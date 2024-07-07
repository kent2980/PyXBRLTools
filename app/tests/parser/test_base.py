import os
import uuid
from pathlib import Path

import pytest
from pandas import DataFrame

from app.parser import BaseXBRLParser


@pytest.fixture
def get_parser(set_xbrl_test_dir, get_output_dir):
    test_dir: str = set_xbrl_test_dir
    output_path = get_output_dir / "test"
    xbrl_file: Path = None
    # test_dirからXBRLファイルパスを再起的にfor文で取得
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.endswith("ixbrl.htm"):
                xbrl_file = Path(root) / file
                break
    return BaseXBRLParser(xbrl_file.as_posix(), output_path.as_posix())

@pytest.fixture
def get_create_parser(set_xbrl_test_dir, get_output_dir):
    test_dir: str = set_xbrl_test_dir
    output_path = get_output_dir / "test"
    xbrl_file: Path = None
    # test_dirからXBRLファイルパスを再起的にfor文で取得
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.endswith("ixbrl.htm"):
                xbrl_file = Path(root) / file
                break
    return BaseXBRLParser.create(xbrl_file.as_posix(), output_path.as_posix())

def test_xbrl_id(get_parser):
    # パーサーを取得
    parser = get_parser
    result = parser.xbrl_id

    # テスト結果のアサーション
    assert isinstance(result, str)
    # uuidの形式かどうかをチェック
    assert len(result) == 36
    # 設定したuuidと一致するかどうかをチェック
    xbrl_id = uuid.uuid4().hex
    parser.xbrl_id = xbrl_id
    assert parser.xbrl_id == xbrl_id

def test_not_output_path():
    try:
        # パーサーを取得
        dummy_url = "http://example.com"
        BaseXBRLParser(dummy_url, output_path=None)
    except Exception:
        assert True

def test_output_path(get_create_parser):
    parser = get_create_parser
    output_path = "test"
    parser.output_path = output_path
    assert parser.output_path == output_path

def test_dummy_file_path():
    try:
        # パーサーを取得
        dummy_file = "dummy_file"
        BaseXBRLParser(dummy_file)
    except FileNotFoundError:
        assert True

def test_fetch_url(get_parser):
    # 有効なURLのテスト
    url = "http://disclosure.edinet-fsa.go.jp/taxonomy/jpcrp/2023-12-01/label/jpcrp_2023-12-01_lab.xml"
    parser = get_parser
    parser.xbrl_url = url
    file_path = parser._fetch_url()
    assert os.path.exists(file_path)
    # 無効なURLのテスト
    url = "http://exampletest.com"
    parser.xbrl_url = url
    try:
        parser._fetch_url()
    except Exception:
        assert True

def test_is_url_in_local(get_parser, get_output_dir):
    # パーサーを取得
    parser = get_parser
    # タイプ:URL
    url = "http://example.com/test.xml"
    parser.xbrl_url = url
    is_url, path = parser._is_url_in_local()
    assert is_url == False
    assert path is None
    # タイプ:ローカル
    local = Path(get_output_dir) / "test.xml"
    parser.xbrl_url = local.as_posix()
    is_url, path = parser._is_url_in_local()
    assert is_url == False
    assert path is None

def test_to_data(get_create_parser):
    parser = get_create_parser
    df = parser.to_DataFrame()
    assert isinstance(df, DataFrame)
    dict_data = parser.to_dict()
    assert isinstance(dict_data, list)
    assert isinstance(dict_data[0], dict)

def test_create(get_output_dir):
    url = "http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2023-12-01/label/jppfs_2023-12-01_lab.xml"
    output_path = get_output_dir / "test"
    parser = BaseXBRLParser.create(url, output_path.as_posix())
    assert isinstance(parser, BaseXBRLParser)
