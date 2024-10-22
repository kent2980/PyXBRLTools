from typing import List, Optional

from app.exception import XbrlListEmptyError
from app.ix_manager import BaseXbrlManager
from app.ix_parser import QualitativeParser
from app.ix_tag import QualitativeDocument


class QualitativeManager(BaseXbrlManager):
    """qualitativeデータの解析を行うクラス

    raise   - XbrlListEmptyError("qualitative.htmが見つかりません。")
    """

    def __init__(
        self, directory_path, xbrl_id: Optional[str] = None
    ) -> None:
        super().__init__(directory_path, xbrl_id=xbrl_id)
        # self._set_htmlbase_files("qualitative")

        # if len(self.related_files) == 0:
        #     raise XbrlListEmptyError("qualitative.htmが見つかりません。")

        # プロパティの初期化
        self.__ix_qualitative_info = None

        # 初期化メソッドを実行
        self.__init_parser()
        self.__init_manager()
        self._set_source_file_ids()

    @property
    def ix_qualitative_info(self):
        return self.__ix_qualitative_info

    def __init_parser(self):
        """QualitativeParserの初期化"""
        parsers: List[QualitativeParser] = []
        for file in self.files:
            if file.endswith("qualitative.htm"):
                parser = QualitativeParser(
                    xbrl_url=file, xbrl_id=self.xbrl_id
                )
                parsers.append(parser)

        self._set_parsers(parsers)

    def __init_manager(self):
        """QualitativeManagerの初期化"""
        self.__set_qualitative_info()

    def __set_qualitative_info(self):
        """Qualitative情報を設定する"""

        rows: List[List[QualitativeDocument]] = []

        for parser in self.parsers:

            id = parser.source_file_id

            parser: QualitativeParser = parser.set_qualitative_info()

            parser.set_photo_info()  # 写真情報を設定

            data = parser.data

            rows.append(data)

            self._set_items(id=id, key="qualitative_info", items=data)

        self.__ix_qualitative_info = rows
