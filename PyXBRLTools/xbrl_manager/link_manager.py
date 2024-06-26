from PyXBRLTools.xbrl_manager.base_xbrl_manager import BaseXbrlManager
from PyXBRLTools.xbrl_parser.link_parser import (BaseLinkParser, CalLinkParser, DefLinkParser,
    PreLinkParser)
import pandas
from PyXBRLTools.xbrl_exception.xbrl_manager_exception import XbrlListEmptyError

class BaseLinkManager(BaseXbrlManager):
    def __init__(self, directory_path) -> None:
        super().__init__(directory_path)
        self.set_linkbase_files(self.get_role())
        self.label = None
        self.parser = self.get_parser()

        if len(self.files) == 0:
            raise XbrlListEmptyError(f"{self.get_role()}ファイルが見つかりません。")

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

    def get_parser(self) -> BaseLinkParser:
        raise NotImplementedError

    def get_role(self):
        raise NotImplementedError

    def set_link_roles(self, document_type = None):
        output_path = self.output_path
        df = None
        files = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for index, row in files.iterrows():
            if df is None:
                df = self.parser.create(row["xlink_href"], output_path).link_roles().to_DataFrame()
            else:
                df = pandas.concat([df, self.parser.create(row["xlink_href"], output_path).link_roles().to_DataFrame()], ignore_index=True)

        self.label = df
        self.data = self.label

        return self

    def set_link_locs(self, document_type = None):
        output_path = self.output_path
        df = None
        files = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for index, row in files.iterrows():
            if df is None:
                df = self.parser.create(row["xlink_href"], output_path).link_locs().to_DataFrame()
                df['document_type'] = row['document_type']
            else:
                new_df = self.parser.create(row["xlink_href"], output_path).link_locs().to_DataFrame()
                new_df['document_type'] = row['document_type']
                df = pandas.concat([df, new_df], ignore_index=True)
        print(df)
        self.label = df
        self.data = self.label

        return self

    def set_link_arcs(self, document_type = None):
        output_path = self.output_path
        df = None
        files = self.files
        if document_type is not None:
            files = files.query(f"document_type == '{document_type}'")
        for index, row in files.iterrows():
            if df is None:
                df = self.parser.create(row["xlink_href"], output_path).link_arcs().to_DataFrame()
                df['document_type'] = row['document_type']
            else:
                new_df = self.parser.create(row["xlink_href"], output_path).link_arcs().to_DataFrame()
                new_df['document_type'] = row['document_type']
                df = pandas.concat([df, new_df], ignore_index=True)

        print(df)
        self.label = df
        self.data = self.label

        return self

class CalLinkManager(BaseLinkManager):
    def get_parser(self) -> BaseLinkParser:
        return CalLinkParser

    def get_role(self):
        role = "calculationLinkbaseRef"
        return role

class DefLinkManager(BaseLinkManager):
    def get_parser(self) -> BaseLinkParser:
        return DefLinkParser

    def get_role(self):
        role = "definitionLinkbaseRef"
        return role

class PreLinkManager(BaseLinkManager):
    def get_parser(self) -> BaseLinkParser:
        return PreLinkParser

    def get_role(self):
        role = "presentationLinkbaseRef"
        return role
