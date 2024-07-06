import time
from pathlib import Path

import pytest

from PyXBRLTools.db_connector.postgre_sql_connector import PostgreSqlConnector
from PyXBRLTools.xbrl_model.edif_model import EdifModel
from PyXBRLTools.xbrl_model.edit_model import EditModel
from PyXBRLTools.xbrl_model.edjp_model import EdjpModel
from PyXBRLTools.xbrl_model.edus_model import EdusModel
from PyXBRLTools.xbrl_model.efjp_model import EfjpModel
from PyXBRLTools.xbrl_model.rejp_model import RejpModel
from PyXBRLTools.xbrl_model.rrdf_model import RrdfModel
from PyXBRLTools.xbrl_model.rrfc_model import RrfcModel
from PyXBRLTools.xbrl_model.rvdf_model import RvdfModel
from PyXBRLTools.xbrl_model.rvfc_model import RvfcModel
from PyXBRLTools.xbrl_reader.xbrl_reader import XbrlReader


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
    assert xbrl_type in [
        "edjp",
        "edus",
        "edif",
        "edit",
        "rvdf",
        "rvfc",
        "rejp",
        "rrdf",
        "rrfc",
        "efjp",
    ]


def test_get_model(xbrl_reader):
    model = xbrl_reader.get_model()
    assert isinstance(
        model,
        (
            EdifModel,
            EditModel,
            EdjpModel,
            EdusModel,
            EfjpModel,
            RejpModel,
            RrdfModel,
            RrfcModel,
            RvdfModel,
            RvfcModel,
        ),
    )


def test_dict_key(xbrl_reader):
    model = xbrl_reader.get_model()
    dict = model.get_all_data()
    # assert isinstance(dict, dict | None)
    assert all([key in dict for key in ["ixbrl", "label", "cal", "def", "pre"]])


def test_ixbrl(get_current_path):
    output_path = get_current_path / "data" / "output"
    output_error_text_path = get_current_path / "output" / "error_txt"
    zip_path = "/Users/user/Documents/tdnet/tdnet"
    # ディレクトリ内のzipファイルを再起的に取得
    zip_files = [file for file in Path(zip_path).rglob("*.zip")]
    # sqlコネクターを作成
    connector = PostgreSqlConnector(
        "localhost", 5432, "fsstock", "postgres", "changethis"
    )
    connector.connect()
    ix = True
    label = True
    cal = True
    def_link = True
    pre_link = True
    for zip_file in zip_files:
        # 実行時間を計測
        start_time = time.time()

        xbrl_reader = XbrlReader(zip_file.as_posix(), output_path)
        model = xbrl_reader.get_model()
        if not model is None:
            try:
                dict = model.get_all_data()
                if not dict is None:
                    if "ixbrl" in dict:
                        dict_value = dict["ixbrl"]
                        # テーブルが存在するか確認
                        if ix:
                            connector.create_table_from_df(
                                "ix_non_fraction", dict_value[0]
                            )
                            connector.create_table_from_df(
                                "ix_non_numeric", dict_value[1]
                            )
                            connector.create_table_from_df("ix_header", dict_value[2])
                            ix = False
                        else:
                            connector.add_data_from_df("ix_non_fraction", dict_value[0])
                            connector.add_data_from_df("ix_non_numeric", dict_value[1])
                            connector.add_data_from_df("ix_header", dict_value[2])
                    if "label" in dict:
                        dict_value = dict["label"]
                        if label:
                            connector.create_table_from_df(
                                "link_label_locs", dict_value[0]
                            )
                            connector.set_unique_key(
                                "link_label_locs", ["xlink_schema", "xlink_label"]
                            )
                            connector.create_table_from_df(
                                "link_label_arcs", dict_value[1]
                            )
                            connector.set_unique_key(
                                "link_label_arcs",
                                ["xlink_from", "xlink_to", "xlink_schema"],
                            )
                            connector.create_table_from_df("link_labels", dict_value[2])
                            connector.set_unique_key(
                                "link_labels", ["xlink_label", "xlink_role", "xml_lang"]
                            )
                            label = False
                        else:
                            connector.add_data_from_df_ignore_duplicate(
                                "link_label_locs", dict_value[0]
                            )
                            connector.add_data_from_df_ignore_duplicate(
                                "link_label_arcs", dict_value[1]
                            )
                            connector.add_data_from_df_ignore_duplicate(
                                "link_labels", dict_value[2]
                            )
                    if "def" in dict:
                        dict_value = dict["def"]
                        if def_link:
                            connector.create_table_from_df(
                                "def_link_locs", dict_value[0]
                            )
                            connector.create_table_from_df(
                                "def_link_arcs", dict_value[1]
                            )
                            def_link = False
                        else:
                            connector.add_data_from_df("def_link_locs", dict_value[0])
                            connector.add_data_from_df("def_link_arcs", dict_value[1])
                    if "cal" in dict:
                        dict_value = dict["cal"]
                        if cal:
                            connector.create_table_from_df(
                                "cal_link_locs", dict_value[0]
                            )
                            connector.create_table_from_df(
                                "cal_link_arcs", dict_value[1]
                            )
                            cal = False
                        else:
                            connector.add_data_from_df("cal_link_locs", dict_value[0])
                            connector.add_data_from_df("cal_link_arcs", dict_value[1])
                    if "pre" in dict:
                        dict_value = dict["pre"]
                        if pre_link:
                            connector.create_table_from_df(
                                "pre_link_locs", dict_value[0]
                            )
                            connector.create_table_from_df(
                                "pre_link_arcs", dict_value[1]
                            )
                            pre_link = False
                        else:
                            connector.add_data_from_df("pre_link_locs", dict_value[0])
                            connector.add_data_from_df("pre_link_arcs", dict_value[1])
            except Exception as e:
                # エラーが発生したファイル名とエラーメッセージとエラー発生箇所をテキストファイルに出力
                with open(output_error_text_path / "error.txt", "a") as f:
                    f.write(f"{zip_file}: {e}\n")
        # 実行時間を取得
        elapsed_time = time.time() - start_time
        # 実行時間をテキストファイルに出力
        with open(output_error_text_path / "time.txt", "a") as f:
            f.write(f"{zip_file}: {elapsed_time}\n")
    connector.disconnect()
