from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def get_current_path():
    current_path = Path(__file__).resolve().parent
    return current_path
