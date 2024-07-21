import pytest

from app.exception import SetLanguageNotError
from app.ix_manager import LabelManager
from app.ix_tag import LabelArc, LabelLoc, LabelValue


@pytest.fixture
def label_manager(get_xbrl_in_edjp, get_output_dir):
    test_dir = get_xbrl_in_edjp
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


def test_get_link_labels(label_manager):
    for values in label_manager.get_link_labels():
        for value in values:
            assert isinstance(value, dict)
            assert LabelValue.is_valid(value)


def test_get_link_label_locs(label_manager):
    for values in label_manager.get_link_label_locs():
        for value in values:
            assert isinstance(value, dict)
            assert LabelLoc.is_valid(value)


def test_get_link_label_arcs(label_manager):
    for values in label_manager.get_link_label_arcs():
        for value in values:
            assert isinstance(value, dict)
            assert LabelArc.is_valid(value)
