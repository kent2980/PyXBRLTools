from pathlib import Path
from typing import List, Optional

from app.ix_manager import BaseXbrlManager
from app.ix_parser import SchemaParser


class SchemaManager(BaseXbrlManager):
    """XBRLディレクトリの解析を行うクラス"""

    def __init__(
        self, directory_path, xbrl_id: Optional[str] = None
    ) -> None:
        super().__init__(directory_path, xbrl_id)

        self.__files = Path(directory_path).rglob("*.xsd")
        # self.__filesをリストに変換
        self.__files = list(self.__files)

        if len(self.__files) == 0:
            raise Exception("xsdファイルが見つかりません。")

        # プロパティの初期化
        self.__parsers: Optional[List[SchemaParser]] = None
        self.__elements = None
        self.__import_schemas = None
        self.__link_base_refs = None

        # 初期化メソッドを実行
        self.__init_parser()
        self.__init_manager()

    @property
    def parsers(self):
        return self.__parsers

    @property
    def elements(self):
        return self.__elements

    @property
    def import_schemas(self):
        return self.__import_schemas

    @property
    def link_base_refs(self):
        return self.__link_base_refs

    def __init_parser(self):
        """パーサーの初期化を行う"""
        self.__parsers = [
            SchemaParser(file.as_posix(), xbrl_id=self.xbrl_id)
            for file in self.__files
        ]

    def __init_manager(self):
        """マネージャーの初期化を行う"""
        self.set_source_file(self.parsers, class_name="sc")
        self._set_elements()
        self._set_import_schemas()
        self._set_link_base_refs(["lab-en", "gla"])

    def _set_elements(self):
        rows = []

        for parser in self.parsers:

            id = parser.source_file_id

            parser = parser.elements()

            data = parser.data

            rows.append(data)

            self._set_items(id=id, key="sc_elements", items=data)

        self.__elements = rows

    def _set_import_schemas(self):
        rows = []

        for parser in self.parsers:

            id = parser.source_file_id

            parser = parser.import_schemas()

            data = parser.data

            rows.append(data)

            self._set_items(id=id, key="sc_import", items=data)

        self.__import_schemas = rows

    def _set_link_base_refs(self, exclude: list = []):
        rows = []

        for parser in self.parsers:

            id = parser.source_file_id

            parser = parser.link_base_refs(exclude=exclude)

            data = parser.data

            rows.append(data)

            self._set_items(id=id, key="sc_linkbase_ref", items=data)

        self.__link_base_refs = rows
