import pytest
from pandas import DataFrame
from PyXBRLTools.xbrl_parser.ixbrl_parser import IxbrlParser
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs
@pytest.fixture
def ixbrl_parser():
    xbrl_url = "/Users/user/Vscode/python/PyXBRLTools/PyXBRLTools/tests/data/edjp/Attachment/0101010-acbs01-tse-acedjpfr-58200-2024-03-31-01-2024-05-14-ixbrl.htm"
    return IxbrlParser.create(xbrl_url)

def test_ix_non_numeric(ixbrl_parser):
    # Create a dummy iXBRL file locally
    result = ixbrl_parser.ix_non_numeric()
    # Check if the result is a BeautifulSoup object
    assert isinstance(result, IxbrlParser)
    # Check if the data attribute is populated with the expected values
    assert len(result.data) > 0
    # Check if the data attribute is a list
    assert isinstance(result.data, list)

def test_ix_non_fractions(ixbrl_parser):
    # Create a dummy iXBRL file locally
    result = ixbrl_parser.ix_non_fractions()
    # Check if the result is a BeautifulSoup object
    assert isinstance(result, IxbrlParser)
    # Check if the data attribute is populated with the expected values
    assert len(result.data) > 0
    # Check if the data attribute is a list
    assert isinstance(result.data, list)

def test_to_DataFrame(ixbrl_parser):
    result = ixbrl_parser.ix_non_fractions().to_DataFrame()
    assert isinstance(result, DataFrame)
    assert len(result) > 0