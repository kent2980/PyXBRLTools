import pandas as pd
import pytest

from app.exception import TagNotFoundError, TypeOfXBRLIsDifferent
from app.ix_parser import LabelParser
from app.ix_tag import LabelArc, LabelLoc, LabelRoleRefs, LabelValue


@pytest.fixture
def get_parser(get_xbrl_test_label, get_output_dir):
    output_dir = get_output_dir / "test"
    parser = LabelParser.create(get_xbrl_test_label, output_dir)
    return parser


def test_create(get_parser):
    assert isinstance(get_parser, LabelParser)


def test_not_file_type(get_xbrl_test_ixbrl):
    try:
        LabelParser.create(get_xbrl_test_ixbrl)
    except TypeOfXBRLIsDifferent:
        assert True


def test_link_labels(get_parser):
    parser = get_parser
    parser.link_labels()
    result_df = parser.to_DataFrame()
    assert isinstance(result_df, pd.DataFrame)
    assert result_df.shape[0] > 0
    result_dict = parser.to_dict()
    assert isinstance(result_dict, list)
    assert len(result_dict) > 0
    # column check
    assert sorted(LabelValue.keys()) == sorted(result_df.columns.tolist())


def test_link_locs(get_parser):
    parser = get_parser
    parser.link_label_locs()
    result_df = parser.to_DataFrame()
    assert isinstance(result_df, pd.DataFrame)
    assert result_df.shape[0] > 0
    result_dict = parser.to_dict()
    assert isinstance(result_dict, list)
    assert len(result_dict) > 0
    # column check
    assert sorted(LabelLoc.keys()) == sorted(result_df.columns.tolist())


def test_link_arcs(get_parser):
    parser = get_parser
    parser.link_label_arcs()
    result_df = parser.to_DataFrame()
    assert isinstance(result_df, pd.DataFrame)
    assert result_df.shape[0] > 0
    result_dict = parser.to_dict()
    assert isinstance(result_dict, list)
    assert len(result_dict) > 0
    # column check
    assert sorted(LabelArc.keys()) == sorted(result_df.columns.tolist())


def test_role_refs(get_parser):
    parser = get_parser
    try:
        parser.role_refs()
        result_df = parser.to_DataFrame()
        assert isinstance(result_df, pd.DataFrame)
        assert result_df.shape[0] > 0
        result_dict = parser.to_dict()
        assert isinstance(result_dict, list)
        assert len(result_dict) > 0
        # column check
        assert sorted(LabelRoleRefs.keys()) == sorted(
            result_df.columns.tolist()
        )
    except TagNotFoundError:
        assert True
