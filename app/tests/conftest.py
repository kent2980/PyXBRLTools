import random
import shutil
import zipfile
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def get_current_path():
    """ 現在のディレクトリを取得"""

    current_path = Path(__file__).resolve().parent
    return current_path

@pytest.fixture(scope="session")
def get_test_dir(get_current_path) -> Path:
    """ テスト用のディレクトリを取得"""

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

# テスト終了後にテスト用のディレクトリを削除する
@pytest.fixture(scope="session", autouse=True)
def remove_test_dir(request, get_test_dir):
    """ テスト用のディレクトリとディレクトリ配下のファイルを再起的に削除する """

    test_dire = get_test_dir.as_posix()

    def cleanup():
        shutil.rmtree(test_dire, ignore_errors=True)

    request.addfinalizer(cleanup)

