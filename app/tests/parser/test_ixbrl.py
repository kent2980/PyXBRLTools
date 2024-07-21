import pandas as pd
import pytest

from app.exception import TypeOfXBRLIsDifferent
from app.ix_parser import IxbrlParser
from app.ix_tag import IxNonFraction, IxNonNumeric


@pytest.fixture
def get_parser(get_xbrl_test_ixbrl, get_output_dir):
    output_path = get_output_dir / "test"
    parser = IxbrlParser.create(
        get_xbrl_test_ixbrl, output_path.as_posix()
    )
    return parser


def test_create_ixbrl_parser(get_parser):
    assert isinstance(get_parser, IxbrlParser)


def test_not_file_path():
    url = "http://www.example.com/lab.xml"
    parser = None
    try:
        parser = IxbrlParser.create(url, "output")
    except TypeOfXBRLIsDifferent:
        assert True
    assert parser is None


def test_set_document(get_parser):
    parser = get_parser
    url = "http://www.example.com/sm_lab.xml"
    result = parser._set_document(url)
    assert result == "sm"


def test_report_type(get_parser):
    parser = get_parser
    # pattern1
    url = "http://www.example.com/tse-acedjpsm-67500-20240401564502-ixbrl.htm"
    result = parser._set_report_type(url)
    assert result == "edjp"
    # pattern2
    url = "http://www.example.com/tse-rrfc-29710-20240531516514-ixbrl.htm"
    result = parser._set_report_type(url)
    assert result == "rrfc"


def test_non_numeric(get_parser):
    parser = get_parser
    parser = parser.ix_non_numeric()
    result = parser.to_DataFrame()
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    # column check
    assert sorted(IxNonNumeric.keys()) == sorted(result.columns.tolist())


def test_non_fraction(get_parser):
    parser = get_parser
    parser = parser.ix_non_fractions()
    result = parser.to_DataFrame()
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    # column check
    assert sorted(IxNonFraction.keys()) == sorted(result.columns.tolist())
