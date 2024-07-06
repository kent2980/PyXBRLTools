import pandas as pd

from app.exception import XbrlListEmptyError
from app.manager import BaseXbrlManager
from app.parser import LabelParser


class LabelManager(BaseXbrlManager):
    """ labelLinkbaseデータの解析を行うクラス"""
    def __init__(self, directory_path, lang="jp") -> None:
        """
        LabelManagerクラスのコンストラクタです。

        Parameters:
            directory_path (str): XBRLファイルが格納されているディレクトリのパス

        Returns:
            None
        """
        super().__init__(directory_path)
        self.set_linkbase_files("labelLinkbaseRef")
        self.set_language(lang)
        self.label = None

        if len(self.files) == 0:
            raise XbrlListEmptyError("labelLinkbaseRefファイルが見つかりません。")

    def set_output_path(self, output_path):
        """
        出力先のパスを設定します。

        Parameters:
            output_path (str): 出力先のパス

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        self.output_path = output_path

        return self

    def set_language(self, lang):
        """
        言語を設定します。

        Parameters:
            lang (str): 言語の設定

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        self.lang = lang

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
            else:
                raise ValueError("言語の設定が不正です。[jp, en]を指定してください。")

        return self

    def set_link_labels(self, document_type=None):
        """
        label属性を設定します。
        ラベル情報を取得します。

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        output_path = self.output_path
        df = None
        files = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for index, row in files.iterrows():
            if df is None:
                df = (
                    LabelParser.create(row["xlink_href"], output_path)
                    .link_labels()
                    .to_DataFrame()
                )
            else:
                df = pd.concat(
                    [
                        df,
                        LabelParser.create(row["xlink_href"], output_path)
                        .link_labels()
                        .to_DataFrame(),
                    ],
                    ignore_index=True,
                )

        self.label = df
        self.data = self.label

        return self

    def set_link_label_locs(self, document_type=None):
        """
        loc属性を設定します。
        loc情報を取得します。

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        output_path = self.output_path
        df = None
        files = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for index, row in files.iterrows():
            if row["xlink_href"].endswith("lab.xml"):
                if df is None:
                    df = (
                        LabelParser.create(row["xlink_href"], output_path)
                        .link_label_locs()
                        .to_DataFrame()
                    )
                else:
                    df = pd.concat(
                        [
                            df,
                            LabelParser.create(row["xlink_href"], output_path)
                            .link_label_locs()
                            .to_DataFrame(),
                        ],
                        ignore_index=True,
                    )

        self.loc = df
        self.data = self.loc

        return self

    def set_link_label_arcs(self, document_type=None):
        """
        labelArc属性を設定します。
        labelArc情報を取得します。

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        output_path = self.output_path
        df = None
        files = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for index, row in files.iterrows():
            if row["xlink_href"].endswith("lab.xml"):
                if df is None:
                    df = (
                        LabelParser.create(row["xlink_href"], output_path)
                        .link_label_arcs()
                        .to_DataFrame()
                    )
                else:
                    df = pd.concat(
                        [
                            df,
                            LabelParser.create(row["xlink_href"], output_path)
                            .link_label_arcs()
                            .to_DataFrame(),
                        ],
                        ignore_index=True,
                    )

        self.label_arc = df
        self.data = self.label_arc

        return self

    def set_role_refs(self, document_type=None):
        """
        roleRef属性を設定します。
        roleRef情報を取得します。

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        output_path = self.output_path
        df = None
        files = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for index, row in files.iterrows():
            if row["xlink_href"].endswith("lab.xml"):
                if df is None:
                    df = (
                        LabelParser.create(row["xlink_href"], output_path)
                        .role_refs()
                        .to_DataFrame()
                    )
                else:
                    df = pd.concat(
                        [
                            df,
                            LabelParser.create(row["xlink_href"], output_path)
                            .role_refs()
                            .to_DataFrame(),
                        ],
                        ignore_index=True,
                    )

        self.role_ref = df
        self.data = self.role_ref

        return self
