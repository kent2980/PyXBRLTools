import pytest

from app.ix_manager import IXBRLManager
from app.ix_tag import IxHeader, IxNonFraction, IxNonNumeric


@pytest.fixture
def ixbrl_manager(get_xbrl_in_edjp):
    return IXBRLManager(get_xbrl_in_edjp)


def test_def_manager_instance(ixbrl_manager):
    assert isinstance(ixbrl_manager, IXBRLManager)


def test_get_non_fraction(ixbrl_manager):
    print("非分数のIXBRLデータを取得します。")
    for values in ixbrl_manager.get_ix_non_fraction():
        for value in values:
            assert isinstance(value, dict)
            # IxNonFractionに格納可能なデータか確認
            assert IxNonFraction.is_valid(value)


def test_get_non_numeric(ixbrl_manager):
    print("非数値のIXBRLデータを取得します。")
    for values in ixbrl_manager.get_ix_non_numeric():
        for value in values:
            assert isinstance(value, dict)
            # IxNonNumericに格納可能なデータか確認
            assert IxNonNumeric.is_valid(value)


def test_get_header(ixbrl_manager):
    print("ヘッダー情報を取得します。")
    value = ixbrl_manager.get_ix_header()
    assert isinstance(value, dict)
    # IxHeaderに格納可能なデータか確認
    assert IxHeader.is_valid(value)
    print(value)


def test_get_summary(ixbrl_manager):
    print("サマリー情報を取得します。")
    for value in ixbrl_manager.get_ix_summary():
        # assert isinstance(value, dict)
        # IxSummaryに格納可能なデータか確認
        # assert IxSummary.is_valid(value)
        # print(value)
        print(value)
