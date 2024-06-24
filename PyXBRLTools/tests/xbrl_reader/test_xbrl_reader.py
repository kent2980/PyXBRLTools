import pytest
from PyXBRLTools.xbrl_reader.xbrl_reader import XbrlReader
from PyXBRLTools.xbrl_model.edif_model import EdifModel
from PyXBRLTools.xbrl_model.edit_model import EditModel
from PyXBRLTools.xbrl_model.edjp_model import EdjpModel
from PyXBRLTools.xbrl_model.edus_model import EdusModel
from PyXBRLTools.xbrl_model.efjp_model import EfjpModel
from PyXBRLTools.xbrl_model.rejp_model import RejpModel
from PyXBRLTools.xbrl_model.rrdf_model import RrdfModel
from PyXBRLTools.xbrl_model.rrfc_model import RrfcModel
from PyXBRLTools.xbrl_model.rvfc_model import RvfcModel
from PyXBRLTools.xbrl_model.rvdf_model import RvdfModel
from pathlib import Path
from PyXBRLTools.db_connector.postgre_sql_connector import PostgreSqlConnector

@pytest.fixture
def xbrl_reader(get_current_path):
    zip_dir = get_current_path / "data" / "xbrl_zip"
    zip_name = "edif.zip"
    zip_path = zip_dir / zip_name
    output_path = get_current_path / "data" / "output"
    return XbrlReader(zip_path.as_posix(), output_path.as_posix())

def test_xbrl_zip_path(xbrl_reader, get_current_path):
    zip_dir = get_current_path / "data" / "xbrl_zip"
    zip_name = "edif.zip"
    zip_path = zip_dir / zip_name
    assert xbrl_reader.xbrl_zip_path == zip_path.as_posix()

def test_xbrl_type(xbrl_reader):
    xbrl_type = xbrl_reader.xbrl_type
    assert xbrl_type in ["edjp", "edus", "edif", "edit", "rvdf", "rvfc", "rejp", "rrdf", "rrfc", "efjp"]

def test_get_model(xbrl_reader):
    model = xbrl_reader.get_model()
    assert isinstance(model, (EdifModel, EditModel, EdjpModel, EdusModel, EfjpModel, RejpModel, RrdfModel, RrfcModel, RvdfModel, RvfcModel))

def test_ixbrl(get_current_path):
    output_path = get_current_path / "data" / "output"
    output_error_text_path = get_current_path / "output" / "error_txt"
    zip_path = "/Users/user/Documents/tdnet/tdnet"
    # ディレクトリ内のzipファイルを再起的に取得
    zip_files = [file for file in Path(zip_path).rglob("*.zip")]
    # sqlコネクターを作成
    connector = PostgreSqlConnector("localhost", 5432, "fsstock", "postgres", "full6839")
    connector.connect()
    count = 0
    for zip_file in zip_files:
        xbrl_reader = XbrlReader(zip_file.as_posix(), output_path)
        model = xbrl_reader.get_model()
        if not model is  None:
            try:
                ix_non_fraction, ix_non_numeric, ix_header = model.get_ixbrl()
                assert not ix_non_fraction.empty
                assert not ix_non_numeric.empty
                assert not ix_header.empty
                # zip_fileのファイル名を取得
                if count == 0:
                    connector.create_table_from_df("aix_non_fraction", ix_non_fraction)
                    connector.create_table_from_df("aix_non_numeric", ix_non_numeric)
                    connector.create_table_from_df("aix_title_header", ix_header)
                else:
                    connector.add_data_from_df("aix_non_fraction", ix_non_fraction)
                    connector.add_data_from_df("aix_non_numeric", ix_non_numeric)
                    connector.add_data_from_df("aix_title_header", ix_header)
                count += 1
            except Exception as e:
                # エラーが発生したファイル名とエラーメッセージをテキストファイルに出力
                with open(output_error_text_path / "error.txt", "a") as f:
                    f.write(f"{zip_file}: {e}\n")
    connector.disconnect()