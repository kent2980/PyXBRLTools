from pathlib import Path
from typing import List, Optional
from uuid import uuid4

import pandas as pd

from app.exception import XbrlDirectoryNotFoundError, XbrlListEmptyError
from app.ix_parser import BaseXBRLParser, SchemaParser
from app.utils import Utils


class BaseXbrlManager:
    """XBRLディレクトリの解析を行う基底クラス"""

    def __init__(
        self, directory_path, xbrl_id: Optional[str] = None
    ) -> None:
        self.directory_path = Path(directory_path)
        self.files = None
        self.__items = None
        self.__xbrl_id = xbrl_id if xbrl_id else str(uuid4())

    @property
    def items(self):
        return self.__items

    @property
    def xbrl_id(self):
        return self.__xbrl_id

    @xbrl_id.setter
    def xbrl_id(self, xbrl_id):
        self.__xbrl_id = xbrl_id

    def _set_items(self, key: str, value):
        """アイテムを設定する"""
        if self.__items is None:
            self.__items = {}
            self.__items[key] = value
        else:
            self.__items[key] = value

    @property
    def directory_path(self):
        return self.__directory_path

    @directory_path.setter
    def directory_path(self, directory_path):
        directory_path = Path(directory_path)
        if not directory_path.exists():
            raise XbrlDirectoryNotFoundError(
                f"無効なパス[{directory_path} ]"
            )
        self.__directory_path = directory_path

    def __to_filelist(self):
        """ディレクトリ内のファイル一覧を取得する"""
        return [
            file.as_posix()
            for file in self.directory_path.glob("**/*")
            if file.is_file() and not file.name.startswith(".")
        ]

    def xbrl_type(self):
        """書類品種を取得します"""
        files = self.__to_filelist()
        for file_str in files:
            file = Path(file_str)
            if file.suffix == ".xsd" and "fr" not in file.name:
                type_str = file.name.split("-")[1]
                code = (
                    type_str[:4] if len(type_str) == 4 else type_str[2:6]
                )
                return code, Utils.read_const_json["report"][code]

    def _set_linkbase_files(self, xlink_role=None):
        """関係ファイルのリストを取得する"""
        files = self.__to_filelist()
        xsd_files = [file for file in files if Path(file).suffix == ".xsd"]

        data_frames = [
            SchemaParser(file).link_base_refs().to_DataFrame()
            for file in xsd_files
        ]
        df = pd.concat(data_frames, ignore_index=True)

        href_map = {
            row["xlink_href"]: file
            for file in files
            for index, row in df.iterrows()
            if not row["xlink_href"].startswith("http")
            and row["xlink_href"] in file
        }

        df["xlink_href"] = (
            df["xlink_href"]
            .astype(str)
            .apply(lambda href: href_map.get(href, href))
        )

        # dfのxlink_roleカラムを整形
        df["xlink_role"] = df["xlink_role"].apply(
            lambda role: (
                role.split("/")[-1] if isinstance(role, str) else role
            )
        )
        # dfのxlink_arcroleカラムを整形
        df["xlink_arcrole"] = df["xlink_arcrole"].apply(
            lambda arcrole: (
                arcrole.split("/")[-1]
                if isinstance(arcrole, str)
                else arcrole
            )
        )

        if xlink_role:
            query = f"xlink_role == '{xlink_role}'"
            df = df.query(query)

        # ファイルが見つからない場合はエラーを発生させる
        if len(df) == 0 and xlink_role:
            raise XbrlListEmptyError(
                f"{xlink_role}ファイルが見つかりません。"
            )

        self.files = df
        return self

    def _set_htmlbase_files(self, xlink_role=None):
        """HTMLベースのファイルリストを取得する"""
        lists = []
        files = self.__to_filelist()
        for file_str in files:
            file = Path(file_str)
            if file.suffix == ".htm" or file.suffix == ".html":
                document_type = (
                    file.name.split("-")[1][2:4]
                    if "fr" in file.name
                    else "sm"
                )

                href = file.as_posix()
                role = file.name.split("-")[-1].split(".")[0]

                lists.append(
                    {
                        "xlink_type": "simple",
                        "xlink_href": href,
                        "xlink_role": role,
                        "xlink_arcrole": "htmlbase",
                        "document_type": document_type,
                    }
                )

        df = pd.DataFrame(lists)

        if xlink_role:
            query = f"xlink_role == '{xlink_role}'"
            df = df.query(query)

        # ファイルが見つからない場合はエラーを発生させる
        if len(df) == 0 and xlink_role:
            raise XbrlListEmptyError(
                f"{xlink_role}ファイルが見つかりません。"
            )

        self.files = df

        return self

    def set_source_file(self, parsers: List[BaseXBRLParser]):
        """ソースファイルを設定する"""
        items = []
        for parser in parsers:
            sources = parser.source_file
            items.append(sources.__dict__)
        self._set_items("source_files", [items])
