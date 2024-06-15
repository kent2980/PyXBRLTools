import pytest
from pandas import DataFrame
from PyXBRLTools.xbrl_parser.ixbrl_parser import IxbrlParser
import os

@pytest.fixture
def ixbrl_parser():
    xbrl_url = "/doc/XBRLData/Summary/tse-qcedjpsm-00000-20240613331210-ixbrl.htm"
    return IxbrlParser(xbrl_url)

def test_ix_non_numeric(ixbrl_parser):
    # Create a dummy iXBRL file locally
    ixbrl_content = """<ix:nonNumeric contextRef="context_1" name="name_1" xsi:nil="true" escape="true" format="format_1">text_1</ix:nonNumeric>
    <ix:nonNumeric contextRef="context_2" name="name_2" xsi:nil="false" escape="false" format="format_2">text_2</ix:nonNumeric>"""
    ixbrl_path = "sample_ixbrl.xml"
    with open(ixbrl_path, "w") as f:
        f.write(ixbrl_content)
    # Test parsing the dummy iXBRL file
    ixbrl_parser._read_xbrl(ixbrl_path)
    result = ixbrl_parser.ix_non_numeric()
    # Check if the result is a BeautifulSoup object
    assert isinstance(result, IxbrlParser)
    # Remove the dummy iXBRL file
    os.remove(ixbrl_path)

def test_ix_non_fractions(ixbrl_parser):
    # Create a dummy iXBRL file locally
    ixbrl_content = """<ix:nonFraction contextRef="context_1" name="name_1" xsi:nil="true" decimals="2" format="format_1" scale="3" sign="-" unitRef="unit_1">1234</ix:nonFraction>
    <ix:nonFraction contextRef="context_2" name="name_2" xsi:nil="false" decimals="0" format="format_2" scale="1" sign="+" unitRef="unit_2">5678</ix:nonFraction>"""
    ixbrl_path = "sample_ixbrl.xml"
    with open(ixbrl_path, "w") as f:
        f.write(ixbrl_content)
    # Test parsing the dummy iXBRL file
    ixbrl_parser._read_xbrl(ixbrl_path)
    result = ixbrl_parser.ix_non_fractions()
    # Check if the result is a BeautifulSoup object
    assert isinstance(result, IxbrlParser)
    # Remove the dummy iXBRL file
    os.remove(ixbrl_path)

def test_to_DataFrame(ixbrl_parser):
    ixbrl_parser.data = [{"key1": "value1"}, {"key2": "value2"}]
    result = ixbrl_parser.to_DataFrame()
    assert isinstance(result, DataFrame)
    assert len(result) > 0