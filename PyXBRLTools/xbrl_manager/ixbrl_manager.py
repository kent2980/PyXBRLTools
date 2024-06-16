from xbrl_manager.base_xbrl_manager import BaseXbrlManager
from xbrl_parser.ixbrl_parser import IxbrlParser
import pandas as pd

class IxbrlManager(BaseXbrlManager):
    def __init__(self, directory_path) -> None:
        """
        IxbrlManagerクラスのコンストラクタです。

        Parameters:
            directory_path (str): XBRLファイルが格納されているディレクトリのパス

        Returns:
            None
        """
        super().__init__(directory_path)
        self.set_htmlbase_files("ixbrl")
        self.ix_non_fraction = None
        self.ix_non_numeric = None

    def set_ix_non_fraction(self):
        """
        ix_non_fraction属性を設定します。

        Returns:
            self (IxbrlManager): 自身のインスタンス
        """
        df = None
        files = self.files
        if self.document_type is not None:
            files = files.query(f"document_type == '{self.document_type}'")
        for index, row in files.iterrows():
            if row["xlink_href"].endswith(".htm"):
                if df is None:
                    df = IxbrlParser.create(row["xlink_href"]).ix_non_fractions().to_DataFrame()
                else:
                    df = pd.concat([df, IxbrlParser.create(row["xlink_href"]).ix_non_fractions().to_DataFrame()], ignore_index=True)

        self.ix_non_fraction = df
        self.data = df

        return self

    def set_ix_non_numeric(self):
        """
        ix_non_numeric属性を設定します。

        Returns:
            self (IxbrlManager): 自身のインスタンス
        """
        df = None
        files = self.files
        if self.document_type is not None:
            files = files.query(f"document_type == '{self.document_type}'")
        for index, row in files.iterrows():
            if row["xlink_href"].endswith(".htm"):
                if df is None:
                    df = IxbrlParser.create(row["xlink_href"]).ix_non_numeric().to_DataFrame()
                else:
                    df = pd.concat([df, IxbrlParser.create(row["xlink_href"]).ix_non_numeric().to_DataFrame()], ignore_index=True)

        self.ix_non_numeric = df
        self.data = df

        return self