import pprint
from pathlib import Path

import pytest

from app.exception import TypeOfXBRLIsDifferent
from app.ix_parser import (
    BaseLinkParser,
    CalLinkParser,
    DefLinkParser,
    PreLinkParser,
)
from app.ix_tag import LinkArc, LinkBase, LinkLoc, LinkRole, LinkTag


@pytest.fixture
def cal_link_parser(get_xbrl_in_edjp, get_output_dir):
    # ディレクトリからXBRLファイルパスのリストを取得
    xbrl_files = Path(get_xbrl_in_edjp).rglob("*cal.xml")
    xbrl_file = next(xbrl_files)
    output_path = get_output_dir / "link"

    return CalLinkParser.create(
        xbrl_file.as_posix(), output_path.as_posix()
    )


@pytest.fixture
def def_link_parser(get_xbrl_in_edjp, get_output_dir):
    # ディレクトリからXBRLファイルパスのリストを取得
    xbrl_files = Path(get_xbrl_in_edjp).rglob("*def.xml")
    xbrl_file = next(xbrl_files)
    output_path = get_output_dir / "link"

    return DefLinkParser.create(
        xbrl_file.as_posix(), output_path.as_posix()
    )


@pytest.fixture
def pre_link_parser(get_xbrl_in_edjp, get_output_dir):
    # ディレクトリからXBRLファイルパスのリストを取得
    xbrl_files = Path(get_xbrl_in_edjp).rglob("*pre.xml")
    xbrl_file = next(xbrl_files)
    output_path = get_output_dir / "link"

    return PreLinkParser.create(
        xbrl_file.as_posix(), output_path.as_posix()
    )


def test_Base_link_parser_is_instance_Error(
    get_xbrl_in_edjp, get_output_dir
):
    xbrl_files = Path(get_xbrl_in_edjp).rglob("*cal.xml")
    xbrl_file = next(xbrl_files)
    output_path = get_output_dir / "link"

    try:
        BaseLinkParser(xbrl_file.as_posix(), output_path.as_posix())
    except NotImplementedError:
        assert True


def test_cal_link_parser_is_instance(cal_link_parser):
    assert isinstance(cal_link_parser, CalLinkParser)


def test_def_link_parser_is_instance(def_link_parser):
    assert isinstance(def_link_parser, DefLinkParser)


def test_pre_link_parser_is_instance(pre_link_parser):
    assert isinstance(pre_link_parser, PreLinkParser)


def test_cal_link_parser_not_url(get_xbrl_in_edjp):
    xbrl_files = Path(get_xbrl_in_edjp).rglob("*def.xml")
    xbrl_file = next(xbrl_files)
    try:
        CalLinkParser.create(xbrl_file.as_posix(), None)
    except TypeOfXBRLIsDifferent:
        assert True


def test_link_roles(cal_link_parser):
    values = cal_link_parser.link_roles().to_dict()
    assert sorted(values[0].keys()) == sorted(LinkRole.keys())
    # 取得したデータをテスト出力
    print("[test_link_roles]" + "*" * 80 + "\n")
    pprint.pprint(values)


def test_link_locs(cal_link_parser):
    values = cal_link_parser.link_locs().to_dict()
    assert sorted(values[0].keys()) == sorted(LinkLoc.keys())
    # 取得したデータをテスト出力
    print("[test_link_locs]" + "*" * 80 + "\n")
    pprint.pprint(values)


def test_link_arcs(cal_link_parser):
    values = cal_link_parser.link_arcs().to_dict()
    assert sorted(values[0].keys()) == sorted(LinkArc.keys())
    # 取得したデータをテスト出力
    print("[test_link_arcs]" + "*" * 80 + "\n")
    pprint.pprint(values)


def test_link_base(cal_link_parser):
    values = cal_link_parser.link_base().to_dict()
    assert sorted(values[0].keys()) == sorted(LinkBase.keys())
    # 取得したデータをテスト出力
    print("[test_link_base]" + "*" * 80 + "\n")
    pprint.pprint(values)


def test_link_tags(cal_link_parser):
    values = cal_link_parser.link_tags().to_dict()
    assert sorted(values[0].keys()) == sorted(LinkTag.keys())
    # 取得したデータをテスト出力
    print("[test_link_tags]" + "*" * 80 + "\n")
    pprint.pprint(values)
