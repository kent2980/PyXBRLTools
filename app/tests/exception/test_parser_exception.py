import pytest

from app.exception import TagNotFoundError, TypeOfXBRLIsDifferent


def test_TypeOfXBRLIsDifferent():
    with pytest.raises(TypeOfXBRLIsDifferent) as e:
        raise TypeOfXBRLIsDifferent("test")
    assert (
        str(e.value)
        == "XBRLの種類が異なります。処理を中断します。[詳細]: test"
    )


def test_TagNotFoundError():
    with pytest.raises(TagNotFoundError) as e:
        raise TagNotFoundError("test")
    assert (
        str(e.value)
        == "タグが見つかりません。処理を中断します。[詳細]: test"
    )
