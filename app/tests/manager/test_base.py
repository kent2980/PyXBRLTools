import uuid

import pytest
from pandas import DataFrame

from app.exception import XbrlDirectoryNotFoundError
from app.ix_manager import BaseXbrlManager


@pytest.fixture
def base_xbrl_manager(get_xbrl_in_edjp):
    return BaseXbrlManager(get_xbrl_in_edjp)


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


def test_xbrl_id(base_xbrl_manager):

    # マネージャーを取得
    manager = base_xbrl_manager
    result = manager.xbrl_id
    print(result)

    # テスト結果のアサーション
    assert isinstance(result, str)
    # uuidの形式かどうかをチェック
    assert len(result) == 36
    # uuidに変換可能かどうかをチェック
    try:
        uuid.UUID(result)
    except ValueError:
        assert False


def test_set_xbrl_id(base_xbrl_manager):

    # マネージャーを取得
    manager = base_xbrl_manager
    xbrl_id = uuid.uuid4().hex
    manager.set_xbrl_id(xbrl_id)
    result = manager.xbrl_id

    # テスト結果のアサーション
    assert result == xbrl_id


def test_not_directory_path(base_xbrl_manager):

    # マネージャーを取得
    manager = base_xbrl_manager
    try:
        manager.directory_path = "test"
        assert False
    except XbrlDirectoryNotFoundError:
        assert True


def test_set_linkbase_files(base_xbrl_manager):

    # マネージャーを取得
    manager = base_xbrl_manager
    manager.set_linkbase_files()
    files: DataFrame = manager.files

    assert isinstance(files, DataFrame)
    assert len(files) > 0
    for index, row in files.iterrows():
        assert row["xlink_arcrole"] == "linkbase"


def test_set_linkbase_files_with_xlink_role(base_xbrl_manager):

    # マネージャーを取得
    manager = base_xbrl_manager
    manager.set_linkbase_files("definitionLinkbaseRef")
    files: DataFrame = manager.files

    assert isinstance(files, DataFrame)
    assert len(files) > 0
    for index, row in files.iterrows():
        assert row["xlink_arcrole"] == "linkbase"
        assert row["xlink_role"] == "definitionLinkbaseRef"


def test_set_htmlbase_files(base_xbrl_manager):

    # マネージャーを取得
    manager = base_xbrl_manager
    manager.set_htmlbase_files()
    files = manager.files

    assert isinstance(files, DataFrame)
    assert len(files) > 0
    for index, row in files.iterrows():
        assert row["xlink_arcrole"] == "htmlbase"


def test_set_htmlbase_files_with_xlink_role(base_xbrl_manager):

    # マネージャーを取得
    manager = base_xbrl_manager
    manager.set_htmlbase_files("ixbrl")
    files = manager.files

    assert isinstance(files, DataFrame)
    assert len(files) > 0
    for _, row in files.iterrows():
        assert row["xlink_arcrole"] == "htmlbase"
        assert row["xlink_role"] == "ixbrl"


def test_to_output_type(base_xbrl_manager):

    # マネージャーを取得
    manager = base_xbrl_manager
    manager.set_htmlbase_files()

    # テスト結果のアサーション
    assert isinstance(manager.to_DataFrame(), DataFrame)
    assert isinstance(manager.to_dict(), dict)
