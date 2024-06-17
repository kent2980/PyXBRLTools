from PyXBRLTools.xbrl_manager.base_xbrl_manager import BaseXbrlManager
from PyXBRLTools.xbrl_parser.label_parser import LabelParser
import pandas as pd

class LabelManager(BaseXbrlManager):
    def __init__(self, directory_path) -> None:
        """
        LabelManagerクラスのコンストラクタです。

        Parameters:
            directory_path (str): XBRLファイルが格納されているディレクトリのパス

        Returns:
            None
        """
        super().__init__(directory_path)
        self.set_linkbase_files("labelLinkbaseRef")
        self.label = None

    def set_link_labels(self, output_path, document_type=None):
        """
        label属性を設定します。
        ラベル情報を取得します。

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        df = None
        files = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for index, row in files.iterrows():
            if row["xlink_href"].endswith("lab.xml"):
                if df is None:
                    df = LabelParser.create(row["xlink_href"], output_path).link_labels().to_DataFrame()
                else:
                    df = pd.concat([df, LabelParser.create(row["xlink_href"], output_path).link_labels().to_DataFrame()], ignore_index=True)

        self.label = df
        self.data = self.label

        return self

    def set_link_locs(self, output_path, document_type=None):
        """
        loc属性を設定します。
        loc情報を取得します。

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        df = None
        files = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for index, row in files.iterrows():
            if row["xlink_href"].endswith("lab.xml"):
                if df is None:
                    df = LabelParser.create(row["xlink_href"], output_path).link_locs().to_DataFrame()
                else:
                    df = pd.concat([df, LabelParser.create(row["xlink_href"], output_path).link_locs().to_DataFrame()], ignore_index=True)

        self.loc = df
        self.data = self.loc

        return self

    def set_link_label_arcs(self, output_path, document_type=None):
        """
        labelArc属性を設定します。
        labelArc情報を取得します。

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        df = None
        files = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for index, row in files.iterrows():
            if row["xlink_href"].endswith("lab.xml"):
                if df is None:
                    df = LabelParser.create(row["xlink_href"], output_path).link_label_arcs().to_DataFrame()
                else:
                    df = pd.concat([df, LabelParser.create(row["xlink_href"], output_path).link_label_arcs().to_DataFrame()], ignore_index=True)

        self.label_arc = df
        self.data = self.label_arc

        return self

    def set_role_refs(self, output_path, document_type=None):
        """
        roleRef属性を設定します。
        roleRef情報を取得します。

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        df = None
        files = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for index, row in files.iterrows():
            if row["xlink_href"].endswith("lab.xml"):
                if df is None:
                    df = LabelParser.create(row["xlink_href"], output_path).role_refs().to_DataFrame()
                else:
                    df = pd.concat([df, LabelParser.create(row["xlink_href"], output_path).role_refs().to_DataFrame()], ignore_index=True)

        self.role_ref = df
        self.data = self.role_ref

        return self