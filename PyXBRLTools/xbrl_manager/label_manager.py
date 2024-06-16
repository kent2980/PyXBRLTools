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

    def set_label(self, document_type=None):
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
                    df = LabelParser.create(row["xlink_href"]).link_labels().to_DataFrame()
                else:
                    df = pd.concat([df, LabelParser.create(row["xlink_href"]).link_labels().to_DataFrame()], ignore_index=True)

        self.label = df.to_dict(orient="records")
        self.data = self.label

        return self