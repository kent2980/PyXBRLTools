import random
import shutil
import zipfile
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


@pytest.fixture(scope="module")
def set_xbrl_test_dir(get_current_path, get_test_dir) -> str:

    # zipファイルをランダムで取得
    xbrl_zip_dir = get_current_path / ".xbrl"
    xbrl_zip_files = list(Path(xbrl_zip_dir).rglob("*.zip"))
    # Pathをstrに変換
    xbrl_zip_files = [str(xbrl_zip_file) for xbrl_zip_file in xbrl_zip_files]
    target_path = random.choice(xbrl_zip_files)

    # testディレクトリにzipファイルを解凍
    with zipfile.ZipFile(target_path) as z:
        z.extractall(get_test_dir.as_posix())

    return get_test_dir.as_posix()

@pytest.fixture(scope="module")
def get_xbrl_in_edjp(get_current_path, get_test_dir):
    keyword = "edjp"
    xbrl_path = get_xbrl_zip_in_keyword(get_current_path, keyword)

    with zipfile.ZipFile(xbrl_path) as z:
        z.extractall(get_test_dir.as_posix())

    return get_test_dir.as_posix()

@pytest.fixture(scope="module")
def get_xbrl_test_ixbrl(get_xbrl_in_edjp):
    """テスト用のixbrlファイルを取得"""

    xbrl_files = list(Path(get_xbrl_in_edjp).rglob("*ixbrl.htm"))
    xbrl_file = random.choice(xbrl_files)
    return xbrl_file.as_posix()


@pytest.fixture(scope="module")
def get_xbrl_test_label(get_xbrl_in_edjp):
    """テスト用のラベルファイルを取得"""

    # lab.xml or lab-en.xmlを取得
    label_files = list(Path(get_xbrl_in_edjp).rglob("*lab.xml"))
    label_file = random.choice(label_files)
    return label_file.as_posix()


# テスト終了後にテスト用のディレクトリを削除する
@pytest.fixture(scope="session", autouse=True)
def remove_test_dir(request, get_test_dir, get_output_dir):
    """テスト用のディレクトリとディレクトリ配下のファイルを再起的に削除する"""

    test_dir: Path = get_test_dir
    test_output_dir = get_output_dir / "test"
    test_create_output_dir = get_output_dir / "test_create"

    def cleanup():
        shutil.rmtree(test_dir.as_posix(), ignore_errors=True)
        shutil.rmtree(test_output_dir.as_posix(), ignore_errors=True)
        shutil.rmtree(test_create_output_dir.as_posix(), ignore_errors=True)

    request.addfinalizer(cleanup)

def get_xbrl_zip_in_keyword(get_current_path, keyword):
    dir_path = get_current_path / ".xbrl"
    # 全てのファイルを取得
    files = list(dir_path.rglob("*.zip"))
    for file in files:
        for name in zipfile.ZipFile(file).namelist():
            if keyword in name:
                return file.as_posix()