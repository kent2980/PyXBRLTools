import pytest

from app.exception import (
    OutputPathNotFoundError,
    SetLanguageNotError,
    XbrlDirectoryNotFoundError,
    XbrlListEmptyError,
)


def test_XbrlListEmptyError():
    with pytest.raises(XbrlListEmptyError) as e:
        raise XbrlListEmptyError("test")
    assert (
        str(e.value)
        == "XBRLのリストが空です。処理を中断します。[詳細]: test"
    )


def test_XbrlDirectoryNotFoundError():
    with pytest.raises(XbrlDirectoryNotFoundError) as e:
        raise XbrlDirectoryNotFoundError("test")
    assert (
        str(e.value)
        == "XBRLディレクトリが見つかりません。処理を中断します。[詳細]: test"
    )


def test_OutputPathNotFoundError():
    with pytest.raises(OutputPathNotFoundError) as e:
        raise OutputPathNotFoundError("test")
    assert (
        str(e.value)
        == "出力先のパスが見つかりません。処理を中断します。[詳細]: test"
    )


def test_SetLanguageNotError():
    with pytest.raises(SetLanguageNotError) as e:
        raise SetLanguageNotError("test")
    assert (
        str(e.value)
        == "言語の設定が不正です。処理を中断します。[詳細]: test"
    )
