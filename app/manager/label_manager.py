import pandas as pd

from app.exception import SetLanguageNotError
from app.manager import BaseXbrlManager
from app.parser import LabelParser


class LabelManager(BaseXbrlManager):
    """labelLinkbaseデータの解析を行うクラス"""

    def __init__(self, directory_path, output_path, lang="jp") -> None:
        """
        LabelManagerクラスのコンストラクタです。

        Parameters:
            directory_path (str): XBRLファイルが格納されているディレクトリのパス

        Returns:
            None
        """
        super().__init__(directory_path)
        self.set_linkbase_files("labelLinkbaseRef")
        self.output_path = output_path
        self.set_language(lang)
        self.label = None

    def set_language(self, lang):
        """
        言語を設定します。

        Parameters:
            language (str): 言語の設定

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        self.lang = lang

        if not lang in ["jp", "en"]:
            raise SetLanguageNotError(
                "言語の設定が不正です。[jp, en]を指定してください。"
            )

        if len(self.files) > 0:
            if lang == "jp":
                # self.filesのxlink_hrefの末尾が"lab.xml"であるものを抽出
                self.files = self.files[
                    self.files["xlink_href"].str.endswith("lab.xml")
                ]
            elif lang == "en":
                # self.filesのxlink_hrefの末尾が"lab-en.xml"であるものを抽出
                self.files = self.files[
                    self.files["xlink_href"].str.endswith("lab-en.xml")
                ]

        return self

    def get_link_labels(self, document_type=None):
        """
        label属性を設定します。
        ラベル情報を取得します。

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        output_path = self.output_path
        files = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for _, row in files.iterrows():
            parser = LabelParser.create(row["xlink_href"], output_path).link_labels()

            df = parser.to_DataFrame()

            yield df.to_dict(orient="records")

    def get_link_label_locs(self, document_type=None):
        """
        loc属性を設定します。
        loc情報を取得します。

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        output_path = self.output_path
        files = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for _, row in files.iterrows():
            parser = LabelParser.create(row["xlink_href"], output_path).link_label_locs()

            df = parser.to_DataFrame()

            yield df.to_dict(orient="records")

    def get_link_label_arcs(self, document_type=None):
        """
        labelArc属性を設定します。
        labelArc情報を取得します。

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        output_path = self.output_path
        files = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for _, row in files.iterrows():
            parser = LabelParser.create(row["xlink_href"], output_path).link_label_arcs()

            df = parser.to_DataFrame()

            yield df.to_dict(orient="records")
