import pprint

import pytest

from app.ix_manager import CalLinkManager, DefLinkManager, PreLinkManager
from app.ix_tag import LinkArc, LinkLoc, LinkRole


@pytest.fixture
def cal_link_manager(get_xbrl_in_edjp, get_output_dir):
    output_dir = get_output_dir / "link"
    return CalLinkManager(get_xbrl_in_edjp, output_dir.as_posix())


@pytest.fixture
def def_link_manager(get_xbrl_in_edjp, get_output_dir):
    output_dir = get_output_dir / "link"
    return DefLinkManager(get_xbrl_in_edjp, output_dir.as_posix())


@pytest.fixture
def pre_link_manager(get_xbrl_in_edjp, get_output_dir):
    output_dir = get_output_dir / "link"
    return PreLinkManager(get_xbrl_in_edjp, output_dir.as_posix())


def test_cal_link_manager_is_instance(cal_link_manager):
    assert isinstance(cal_link_manager, CalLinkManager)


def test_def_link_manager_is_instance(def_link_manager):
    assert isinstance(def_link_manager, DefLinkManager)


def test_pre_link_manager_is_instance(pre_link_manager):
    assert isinstance(pre_link_manager, PreLinkManager)


def test_get_link_roles(cal_link_manager):
    for values in cal_link_manager.get_link_roles():
        assert isinstance(values, list)
        print("[test_get_link_roles]" + "*" * 80 + "\n")
        pprint.pprint(values)
        for value in values:
            assert isinstance(value, dict)
            assert sorted(value.keys()) == sorted(LinkRole.keys())


def test_get_link_locs(cal_link_manager):
    for values in cal_link_manager.get_link_locs():
        assert isinstance(values, list)
        print("[test_get_link_locs]" + "*" * 80 + "\n")
        pprint.pprint(values)
        for value in values:
            assert isinstance(value, dict)
            assert sorted(value.keys()) == sorted(LinkLoc.keys())


def test_get_link_arcs(cal_link_manager):
    for values in cal_link_manager.get_link_arcs():
        assert isinstance(values, list)
        print("[test_get_link_arcs]" + "*" * 80 + "\n")
        pprint.pprint(values)
        for value in values:
            assert isinstance(value, dict)
            assert sorted(value.keys()) == sorted(LinkArc.keys())


def test_change_output_path(cal_link_manager):
    output_path = "test"
    manager = cal_link_manager
    manager.output_path = output_path
    assert manager.output_path.__eq__(output_path)


def test_change_document_type(cal_link_manager):
    document_type = "test"
    manager = cal_link_manager
    manager.document_type = document_type
    assert manager.document_type.__eq__(document_type)
