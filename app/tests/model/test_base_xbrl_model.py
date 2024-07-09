import random
from pathlib import Path

import pytest

from app.models import BaseXbrlModel


@pytest.fixture
def base_xbrl_model(get_xbrl_zip_dir, get_output_dir):
    zip_files = list(Path(get_xbrl_zip_dir).rglob("*.zip"))
    # zip_filesからランダムに1つ取得
    zip_file = random.choice(zip_files)
    output_path = get_output_dir / "base_xbrl_model"

    return BaseXbrlModel(zip_file, output_path)

def test_base_xbrl_model_instance(base_xbrl_model):
    assert isinstance(base_xbrl_model, BaseXbrlModel)
