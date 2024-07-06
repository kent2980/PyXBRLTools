import os
from pathlib import Path

import pytest
from bs4 import BeautifulSoup as bs
from pandas import DataFrame

from PyXBRLTools.xbrl_parser.base_xbrl_parser import BaseXBRLParser


@pytest.fixture
def xbrl_parser():
    xbrl_url = "http://disclosure.edinet-fsa.go.jp/taxonomy/jpcrp/2022-11-01/jpcrp_cor_2022-11-01.xsd"
    output_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/TEST"
    return BaseXBRLParser(xbrl_url, output_path)


def test_read_xbrl(xbrl_parser):
    # ダミーのxmlをローカルに作成する
    xbrl_content = """<xbrl>
    <context>
        <entity>
            <identifier scheme="scheme">identifier</identifier>
        </entity>
        <period>
            <startDate>2021-01-01</startDate>
            <endDate>2021-12-31</endDate>
        </period>
    </context>
    </xbrl>"""
    # xbrl_contentをファイルに保存する
    xbrl_path = "sample_xbrl.xml"
    with open(xbrl_path, "w") as f:
        f.write(xbrl_content)
    # ファイルパスからダミーのXMLを読み込んで解析するテスト
    result = xbrl_parser._read_xbrl(xbrl_path)
    # 戻り値がBeautifulSoupオブジェクトであることを確認する
    assert isinstance(result, bs)
    # 戻り値が空でないことを確認する
    assert len(result) > 0
    # ファイルを削除する
    os.remove(xbrl_path)


def test_fetch_url(xbrl_parser):
    result = xbrl_parser._fetch_url()
    assert isinstance(result, str)
    assert len(result) > 0


def test_is_url_in_local(xbrl_parser):
    result = xbrl_parser._is_url_in_local()
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], bool)
    assert isinstance(result[1], str) or result[1] is None


def test_to_csv(xbrl_parser):
    file_path = "output.csv"
    xbrl_parser.data = [{"key1": "value1"}, {"key2": "value2"}]
    xbrl_parser.to_csv(file_path)
    assert os.path.exists(file_path)
    os.remove(file_path)


def test_to_dataframe(xbrl_parser):
    xbrl_parser.data = [{"key1": "value1"}, {"key2": "value2"}]
    result = xbrl_parser.to_DataFrame()
    assert isinstance(result, DataFrame)
    assert len(result) > 0


def test_to_json(xbrl_parser):
    file_path = "output.json"
    xbrl_parser.data = [{"key1": "value1"}, {"key2": "value2"}]
    xbrl_parser.to_json(file_path)
    assert os.path.exists(file_path)
    os.remove(file_path)


def test_to_dict(xbrl_parser):
    xbrl_parser.data = [{"key1": "value1"}, {"key2": "value2"}]
    result = xbrl_parser.to_dict()
    assert isinstance(result, list)
    assert len(result) > 0
