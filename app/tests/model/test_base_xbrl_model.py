import pytest

from app.ix_models import BaseXbrlModel


@pytest.fixture
def base_xbrl_model(get_xbrl_edjp_zip, get_output_dir):
    output_path = get_output_dir / "base_xbrl_model"

    return BaseXbrlModel(get_xbrl_edjp_zip, output_path)


def test_base_xbrl_model_instance(base_xbrl_model):
    assert isinstance(base_xbrl_model, BaseXbrlModel)
