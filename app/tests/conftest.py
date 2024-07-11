from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def get_current_path():
    """現在のディレクトリを取得"""

    current_path = Path(__file__).resolve().parent
    return current_path


@pytest.fixture(scope="session")
def get_output_dir(get_current_path):
    """出力ディレクトリを取得"""

    output_dir = get_current_path / ".output"
    return output_dir


@pytest.fixture(scope="session")
def get_test_dir(get_current_path) -> Path:
    """テスト用のディレクトリを取得"""

    test_dir = get_current_path / ".data" / "test"
    return test_dir


@pytest.fixture(scope="session")
def get_xbrl_zip_dir(get_current_path) -> Path:
    """XBRLファイルのディレクトリを取得"""

    xbrl_dir = get_current_path / ".xbrl"
    return xbrl_dir


@pytest.fixture(scope="module")
def get_xbrl_in_edjp(get_test_dir):
    """テスト用のXBRL(edjp)ファイルを取得"""
    test_dir = get_test_dir / "edjp"
    return test_dir.as_posix()


@pytest.fixture(scope="module")
def get_xbrl_edjp_zip(get_xbrl_zip_dir):
    """テスト用のXBRL(edjp)ファイル(zip)を取得"""
    zip_file = get_xbrl_zip_dir / "edjp.zip"
    return zip_file.as_posix()


@pytest.fixture(scope="module")
def get_xbrl_rvfc_zip(get_xbrl_zip_dir):
    """テスト用のXBRL(rvfc)ファイル(zip)を取得"""
    zip_file = get_xbrl_zip_dir / "rvfc.zip"
    return zip_file.as_posix()


@pytest.fixture(scope="module")
def get_xbrl_test_ixbrl(get_xbrl_in_edjp):
    """テスト用のixbrlファイルを取得"""

    xbrl_files = Path(get_xbrl_in_edjp).rglob("*ixbrl.htm")
    xbrl_file = next(xbrl_files)
    return xbrl_file.as_posix()


@pytest.fixture(scope="module")
def get_xbrl_test_label(get_xbrl_in_edjp):
    """テスト用のラベルファイルを取得"""

    # lab.xml or lab-en.xmlを取得
    label_files = Path(get_xbrl_in_edjp).rglob("*lab.xml")
    label_file = next(label_files)
    return label_file.as_posix()
