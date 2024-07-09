import pandas

from app.manager import BaseXbrlManager
from app.parser import (BaseLinkParser, CalLinkParser, DefLinkParser,
                        PreLinkParser)


class BaseLinkManager(BaseXbrlManager):
    """labelLinkbaseデータの解析を行うクラス"""

    def __init__(self, directory_path, output_path, document_type=None) -> None:
        super().__init__(directory_path)
        self._output_path = output_path
        self._document_type = document_type
        self.set_linkbase_files(self.get_role())
        self.parser = self.get_parser()

    @property
    def output_path(self):
        return self._output_path

    @property
    def document_type(self):
        return self._document_type

    @output_path.setter
    def output_path(self, output_path):
        """
        出力先のパスを設定します。

        Parameters:
            output_path (str): 出力先のパス

        Returns:
            self (LabelManager): 自身のインスタンス
        """
        self._output_path = output_path

    @document_type.setter
    def document_type(self, document_type):
        """
        document_typeを設定します。

        Parameters:
            document_type (str): document_typeの設定

        Returns:
            self (BaseLinkManager): 自身のインスタンス
        """
        self._document_type = document_type

    def get_parser(self) -> BaseLinkParser:
        raise NotImplementedError  # pragma: no cover

    def get_role(self):
        raise NotImplementedError  # pragma: no cover

    def get_link_roles(self):
        """link_rolesを設定します。"""
        output_path = self.output_path
        files = self.files
        if self.document_type is not None:
            files = files.query(f"document_type == '{self.document_type}'")
        for _, row in files.iterrows():

            parser = self.parser.create(row["xlink_href"], output_path).link_roles()

            data = parser.to_DataFrame()

            data["xbrl_id"] = self.xbrl_id

            yield data.to_dict(orient="records")

    def get_link_locs(self):
        output_path = self.output_path
        files = self.files
        if self.document_type is not None:
            files = files.query(f"document_type == '{self.document_type}'")
        for _, row in files.iterrows():
            parser = self.parser.create(row["xlink_href"], output_path).link_locs()

            data = parser.to_DataFrame()

            data["xbrl_id"] = self.xbrl_id

            yield data.to_dict(orient="records")

    def get_link_arcs(self):
        output_path = self.output_path
        files = self.files
        if self.document_type is not None:
            files = files.query(f"document_type == '{self.document_type}'")
        for _, row in files.iterrows():
            parser = self.parser.create(row["xlink_href"], output_path).link_arcs()

            data = parser.to_DataFrame()

            data["xbrl_id"] = self.xbrl_id

            yield data.to_dict(orient="records")

class CalLinkManager(BaseLinkManager):
    """calculationLinkbaseデータの解析を行うクラス"""

    def get_parser(self) -> BaseLinkParser:
        return CalLinkParser

    def get_role(self):
        role = "calculationLinkbaseRef"
        return role


class DefLinkManager(BaseLinkManager):
    """definitionLinkbaseデータの解析を行うクラス"""

    def get_parser(self) -> BaseLinkParser:
        return DefLinkParser

    def get_role(self):
        role = "definitionLinkbaseRef"
        return role


class PreLinkManager(BaseLinkManager):
    """presentationLinkbaseデータの解析を行うクラス"""

    def get_parser(self) -> BaseLinkParser:
        return PreLinkParser

    def get_role(self):
        role = "presentationLinkbaseRef"
        return role
