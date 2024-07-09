import pytest

from app.tag import BaseTag


def test_base_tag_instance():
    base_tag = BaseTag()
    assert isinstance(base_tag, BaseTag)

    try:
        BaseTag.is_valid("test")
    except TypeError:
        assert True

    base_tag2 = BaseTag()

    assert base_tag.__eq__(base_tag2)
