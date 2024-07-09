import random

import pytest

from app.models import XBRLModel
from app.tag import IxHeader


@pytest.fixture
def xbrl_model(get_xbrl_zip_dir, get_output_dir):
    xbrl_files = list(get_xbrl_zip_dir.rglob("*.zip"))
    xbrl_file = random.choice(xbrl_files)
    return XBRLModel(xbrl_file, get_output_dir)

def test_xbrl_model_instance(xbrl_model):
    assert isinstance(xbrl_model, XBRLModel)

def test_ixbrl_manager(xbrl_model):
    assert xbrl_model.ixbrl_manager is not None
    manager = xbrl_model.ixbrl_manager
    if not manager is None:
        header = manager.get_ix_header()
        assert sorted(header.keys()) == sorted(IxHeader.keys())
