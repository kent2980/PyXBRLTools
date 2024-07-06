import pytest
from pandas import DataFrame

from app.manager import BaseXbrlManager


@pytest.fixture
def base_xbrl_manager(set_xbrl_test_dir):
    test_dir = set_xbrl_test_dir
    return BaseXbrlManager(test_dir)


def test_xbrl_type(base_xbrl_manager):

    # マネージャーを取得
    manager = base_xbrl_manager
    result = manager.xbrl_type()

    # テスト結果のアサーション
    assert isinstance(result, tuple)
    assert len(result) == 2

def test_Report_Type_const(base_xbrl_manager):

    # マネージャーを取得
    manager = base_xbrl_manager
    result = manager.REPORT_TYPE

    # テスト結果のアサーション
    assert isinstance(result, dict)
    assert len(result) > 0
    for key, value in result.items():
        assert isinstance(key, str)
        assert isinstance(value, str)
