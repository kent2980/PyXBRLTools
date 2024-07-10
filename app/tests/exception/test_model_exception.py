import pytest

from app.exception import NotXbrlDirectoryException, NotXbrlTypeException


def test_NotXbrlDirectoryException():
    with pytest.raises(NotXbrlDirectoryException) as e:
        raise NotXbrlDirectoryException("test")
    assert str(e.value) == "無効なXBRLファイルです。[詳細]:test"


def test_NotXbrlTypeException():
    with pytest.raises(NotXbrlTypeException) as e:
        raise NotXbrlTypeException("test")
    assert str(e.value) == "XBRLファイルの種類が不正です。[詳細]:test"
