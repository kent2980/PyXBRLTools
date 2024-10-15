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


@pytest.fixture(scope="module")
def get_api_url():

    url_base = "/api/v1/xbrl"

    urls = {
        "ix_head_title": f"{url_base}/ix/head/list/",
        "ix_source_file": f"{url_base}/source/list/",
        "ix_non_numeric": f"{url_base}/ix/non_numeric/list/",
        "ix_non_fraction": f"{url_base}/ix/non_fraction/list/",
        # 'ix_context': f'{url_base}/ix/context/',
        "lab_source_file": f"{url_base}/source/list/",
        "lab_link_locs": f"{url_base}/link/lab/loc/list/",
        "lab_link_arcs": f"{url_base}/link/lab/arc/list/",
        "lab_link_values": f"{url_base}/link/lab/value/list/",
        "cal_source_file": f"{url_base}/source/list/",
        # 'cal_link_roles': f'{url_base}/link/cal/role/',
        "cal_link_locs": f"{url_base}/link/cal/loc/list/",
        "cal_link_arcs": f"{url_base}/link/cal/arc/list/",
        "def_source_file": f"{url_base}/source/list/",
        # 'def_link_roles': f'{url_base}/link/def/role/',
        "def_link_locs": f"{url_base}/link/def/loc/list/",
        "def_link_arcs": f"{url_base}/link/def/arc/list/",
        "pre_source_file": f"{url_base}/source/list/",
        # 'pre_link_roles': f'{url_base}/link/pre/role/',
        "pre_link_locs": f"{url_base}/link/pre/loc/list/",
        "pre_link_arcs": f"{url_base}/link/pre/arc/list/",
        "sc_source_file": f"{url_base}/source/list/",
        # "sc_link_elements": f"{url_base}/schema/elements/list/",
        # "sc_link_import": f"{url_base}/schema/imports/list/",
        "sc_linkbase_ref": f"{url_base}/schema/linkbase/list/",
        "qualitative_info": f"{url_base}/qualitative/list/",
    }

    return urls


@pytest.fixture(scope="module")
def get_api_is():
    """APIに登録されているかを確認するためのsource_file_idを取得"""

    url_base = "/api/v1/xbrl"

    urls = {
        "ix_head_title": f"{url_base}/ix/head/is/",
        "ix_source_file": f"{url_base}/source/is/",
        "ix_non_numeric": f"{url_base}/ix/non_numeric/is/",
        "ix_non_fraction": f"{url_base}/ix/non_fraction/is/",
        # "ix_context": f"{url_base}/ix/context/is/",
        "lab_source_file": f"{url_base}/source/is/",
        "lab_link_locs": f"{url_base}/link/lab/loc/is/",
        "lab_link_arcs": f"{url_base}/link/lab/arc/is/",
        "lab_link_values": f"{url_base}/link/lab/value/is/",
        "cal_source_file": f"{url_base}/source/is/",
        "cal_link_locs": f"{url_base}/link/cal/loc/is/",
        "cal_link_arcs": f"{url_base}/link/cal/arc/is/",
        "def_source_file": f"{url_base}/source/is/",
        "def_link_locs": f"{url_base}/link/def/loc/is/",
        "def_link_arcs": f"{url_base}/link/def/arc/is/",
        "pre_source_file": f"{url_base}/source/is/",
        "pre_link_locs": f"{url_base}/link/pre/loc/is/",
        "pre_link_arcs": f"{url_base}/link/pre/arc/is/",
        "sc_source_file": f"{url_base}/source/is/",
        "sc_linkbase_ref": f"{url_base}/schema/linkbase/is/",
        "qualitative_info": f"{url_base}/qualitative/is/",
    }

    return urls
