import pytest

from app.manager import (BaseLinkManager, CalLinkManager, DefLinkManager,
                         PreLinkManager)


@pytest.fixture
def link_manager(set_xbrl_test_dir, get_output_dir):
    try:
        test_dir = set_xbrl_test_dir
        output_dir = get_output_dir / "link"
        return BaseLinkManager(test_dir, output_dir.as_posix())
    except NotImplementedError:
        return None

@pytest.fixture
def cal_link_manager(set_xbrl_test_dir, get_output_dir):
    test_dir = set_xbrl_test_dir
    output_dir = get_output_dir / "link"
    return CalLinkManager(test_dir, output_dir.as_posix())

@pytest.fixture
def def_link_manager(set_xbrl_test_dir, get_output_dir):
    test_dir = set_xbrl_test_dir
    output_dir = get_output_dir / "link"
    return DefLinkManager(test_dir, output_dir.as_posix())

@pytest.fixture
def pre_link_manager(set_xbrl_test_dir, get_output_dir):
    test_dir = set_xbrl_test_dir
    output_dir = get_output_dir / "link"
    return PreLinkManager(test_dir, output_dir.as_posix())

def test_base_manager_not_instance(link_manager):
    # マネージャーを取得
    manager = link_manager
    assert manager is None

def test_cal_manager_instance(cal_link_manager):
    # マネージャーを取得
    manager = cal_link_manager
    assert isinstance(manager, CalLinkManager)
    manager.set_link_roles()
    df = manager.to_DataFrame()
    assert len(df) > 0
    manager.set_link_locs()
    df = manager.to_DataFrame()
    assert len(df) > 0
    manager.set_link_arcs()
    df = manager.to_DataFrame()
    assert len(df) > 0

def test_def_manager_instance(def_link_manager):
    # マネージャーを取得
    manager = def_link_manager
    assert isinstance(manager, DefLinkManager)

def test_pre_manager_instance(pre_link_manager):
    # マネージャーを取得
    manager = pre_link_manager
    assert isinstance(manager, PreLinkManager)

def test_set_document_type(cal_link_manager):
    # マネージャーを取得
    manager:CalLinkManager = cal_link_manager
    manager.set_document_type("fr")
    assert manager.document_type == "fr"

    manager.set_link_roles()
    df = manager.to_DataFrame()
    assert len(df) > 0
    manager.set_link_locs()
    df = manager.to_DataFrame()
    assert len(df) > 0
    manager.set_link_arcs()
    df = manager.to_DataFrame()
    assert len(df) > 0

def test_output_path(cal_link_manager, get_output_dir):
    # マネージャーを取得
    manager:CalLinkManager = cal_link_manager
    output_path = get_output_dir / "link"
    manager.output_path = output_path.as_posix()
    assert manager.output_path == output_path.as_posix()
