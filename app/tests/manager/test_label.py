import pytest
from pandas import DataFrame

from app.exception import SetLanguageNotError
from app.manager import LabelManager


@pytest.fixture
def label_manager(set_xbrl_test_dir, get_output_dir):
    test_dir = set_xbrl_test_dir
    output_dir = get_output_dir / "label"
    return LabelManager(test_dir, output_dir.as_posix())

def test_set_language(label_manager):
    # マネージャーを取得
    manager = label_manager
    manager.set_language("en")
    # テスト結果のアサーション
    assert isinstance(manager, LabelManager)
    assert manager.lang == "en"
    try:
        manager.set_language("es")
        assert False
    except SetLanguageNotError:
        assert True

def test_set_link_labels(label_manager):
    # マネージャーを取得
    manager = label_manager
    manager.set_link_labels()
    df = manager.to_DataFrame()
    # テスト結果のアサーション
    assert isinstance(manager, LabelManager)
    assert isinstance(df, DataFrame)
    assert len(df) > 0
    manager.set_link_labels("sm")
    files = manager.files
    assert len(files) > 0
    assert "sm" in files["document_type"].values

def test_set_link_label_locs(label_manager):
    # マネージャーを取得
    manager = label_manager
    manager.set_link_label_locs()
    df = manager.to_DataFrame()
    # テスト結果のアサーション
    assert isinstance(manager, LabelManager)
    assert isinstance(df, DataFrame)
    assert len(df) > 0
    manager.set_link_label_locs("sm")
    files = manager.files
    assert len(files) > 0
    assert "sm" in files["document_type"].values

def test_set_link_label_arcs(label_manager):
    # マネージャーを取得
    manager = label_manager
    manager.set_link_label_arcs()
    df = manager.to_DataFrame()
    # テスト結果のアサーション
    assert isinstance(manager, LabelManager)
    assert isinstance(df, DataFrame)
    assert len(df) > 0
    manager.set_link_label_arcs("sm")
    files = manager.files
    assert len(files) > 0
    assert "sm" in files["document_type"].values

def test_set_role_refs(label_manager):
    # マネージャーを取得
    manager = label_manager
    manager.set_role_refs()
    df = manager.to_DataFrame()
    # テスト結果のアサーション
    assert isinstance(manager, LabelManager)
    assert isinstance(df, DataFrame)
    assert len(df) > 0
    manager.set_role_refs("sm")
    files = manager.files
    assert len(files) > 0
    assert "sm" in files["document_type"].values
