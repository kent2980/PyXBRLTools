from typing import List, Optional

from app.exception import SetLanguageNotError
from app.ix_manager import BaseXbrlManager
from app.ix_parser import LabelParser


class LabelManager(BaseXbrlManager):
    """labelLinkbaseデータの解析を行うクラス"""

    def __init__(
        self,
        directory_path,
        output_path,
        lang="jp",
        xbrl_id: Optional[str] = None,
    ):
        super().__init__(directory_path, xbrl_id=xbrl_id)
        self.__output_path = output_path
        self.__lang = None
        self.__link_labels = None
        self.__link_label_locs = None
        self.__link_label_arcs = None

        self._set_linkbase_files("labelLinkbaseRef")
        self.__init_language(lang)
        self.__init_parser()
        self.__init_manager()
        self._set_source_file_ids()

    @property
    def output_path(self):
        return self.__output_path

    @property
    def lang(self):
        return self.__lang

    @property
    def link_labels(self):
        return self.__link_labels

    @property
    def link_label_locs(self):
        return self.__link_label_locs

    @property
    def link_label_arcs(self):
        return self.__link_label_arcs

    def __init_language(self, lang):
        """言語を設定します。"""
        self.__lang = lang

        if lang not in ["jp", "en"]:
            raise SetLanguageNotError(
                "言語の設定が不正です。[jp, en]を指定してください。"
            )

        if len(self.related_files) > 0:
            if lang == "jp":
                # self.related_filesのxlink_hrefの末尾が"lab.xml"であるものを抽出
                self.related_files = self.related_files[
                    self.related_files["xlink_href"].str.endswith(
                        "lab.xml"
                    )
                ]
            elif lang == "en":
                # self.related_filesのxlink_hrefの末尾が"lab-en.xml"であるものを抽出
                self.related_files = self.related_files[
                    self.related_files["xlink_href"].str.endswith(
                        "lab-en.xml"
                    )
                ]

    def __init_parser(self):
        """パーサーを設定します。"""
        parsers: List[LabelParser] = []
        for _, row in self.related_files.iterrows():
            parser = LabelParser(
                row["xlink_href"], self.output_path, xbrl_id=self.xbrl_id
            )
            parsers.append(parser)

        self._set_parsers(parsers)

    def __init_manager(self):
        self.set_source_file(self.parsers, class_name="lab")
        self.__set_link_labels()
        self.__set_link_label_locs()
        self.__set_link_label_arcs()

        self.items.sort(key=lambda x: x["sort_position"])

    def __set_link_labels(self):
        """
        label属性を設定します。
        ラベル情報を取得します。

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        if self.link_labels:
            return self.link_labels

        rows = []

        for parser in self.parsers:

            id = parser.source_file_id

            parser = parser.link_labels()

            data = parser.data

            rows.append(data)

            self._set_items(
                id=id, key="lab_link_values", items=data, sort_position=3
            )

        self.__link_labels = rows

    def __set_link_label_locs(self):
        """
        loc属性を設定します。
        loc情報を取得します。

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        if self.link_label_locs:
            return self.link_label_locs

        rows = []

        for parser in self.parsers:

            id = parser.source_file_id

            parser = parser.link_label_locs()

            data = parser.data

            rows.append(data)

            self._set_items(
                id=id, key="lab_link_locs", items=data, sort_position=1
            )

        self.__link_label_locs = rows

    def __set_link_label_arcs(self):
        """
        labelArc属性を設定します。
        labelArc情報を取得します。

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        if self.link_label_arcs:
            return self.link_label_arcs

        rows = []

        for parser in self.parsers:

            id = parser.source_file_id

            parser = parser.link_label_arcs()

            data = parser.data

            rows.append(data)

            self._set_items(
                id=id, key="lab_link_arcs", items=data, sort_position=2
            )

        self.__link_label_arcs = rows
