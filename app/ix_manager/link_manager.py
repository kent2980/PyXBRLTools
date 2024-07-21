from typing import List, Optional

from app.ix_manager import BaseXbrlManager
from app.ix_parser import (
    BaseLinkParser,
    CalLinkParser,
    DefLinkParser,
    PreLinkParser,
)


class BaseLinkManager(BaseXbrlManager):
    """labelLinkbaseデータの解析を行うクラス"""

    def __init__(
        self,
        directory_path,
        output_path,
        document_type=None,
        xbrl_id: Optional[str] = None,
    ):
        super().__init__(directory_path, xbrl_id=xbrl_id)

        # プロパティの初期化
        self.__output_path = output_path
        self.__document_type = document_type
        self.__parser = None
        self.__parsers: Optional[List[BaseLinkParser]] = None
        self.__role = None
        self.__link_roles = None
        self.__link_locs = None
        self.__link_arcs = None

    @property
    def document_type(self):
        return self.__document_type

    @property
    def output_path(self):
        return self.__output_path

    @property
    def parser(self):
        return self.__parser

    @parser.setter
    def parser(self, parser):
        self.__parser = parser

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, role):
        self.__role = role

    @property
    def parsers(self):
        return self.__parsers

    @property
    def link_roles(self):
        return self.__link_roles

    @property
    def link_locs(self):
        return self.__link_locs

    @property
    def link_arcs(self):
        return self.__link_arcs

    def _init_parser(self):
        """パーサーを設定します。"""
        parsers: List[BaseLinkParser] = []
        for _, row in self.files.iterrows():
            parser = self.parser(
                row["xlink_href"], self.output_path, xbrl_id=self.xbrl_id
            )
            parsers.append(parser)
        self.__parsers = parsers

    def _init_manager(self):
        self.set_source_file(self.parsers)
        self.__set_link_roles()
        self.__set_link_locs()
        self.__set_link_arcs()

    def __set_link_roles(self):
        """link_rolesを設定します。"""
        if self.__link_roles:
            return self.__link_roles

        rows = []

        files = self.files
        if self.document_type is not None:
            files = files.query(f"document_type == '{self.document_type}'")
        for parser in self.parsers:

            parser = parser.link_roles()

            data = parser.data

            rows.append(data)

        self._set_items("link_roles", rows)

        self.__link_roles = rows

    def __set_link_locs(self):
        """link_locsを設定します。"""

        if self.__link_locs:
            return self.__link_locs

        rows = []

        files = self.files
        if self.document_type is not None:
            files = files.query(f"document_type == '{self.document_type}'")
        for parser in self.parsers:
            parser = parser.link_locs()

            data = parser.data

            rows.append(data)

        self._set_items("link_locs", rows)

        self.__link_locs = rows

    def __set_link_arcs(self):
        """link_arcsを設定します。"""
        if self.__link_arcs:
            return self.__link_arcs

        rows = []

        files = self.files
        if self.document_type is not None:
            files = files.query(f"document_type == '{self.document_type}'")
        for parser in self.parsers:
            parser = parser.link_arcs()

            data = parser.data

            rows.append(data)

        self._set_items("link_arcs", rows)

        self.__link_arcs = rows


class CalLinkManager(BaseLinkManager):
    """calculationLinkbaseデータの解析を行うクラス

    raise   - NotImplementedError: [description]
            - XbrlListEmptyError: [description]
    """

    def __init__(
        self,
        directory_path,
        output_path,
        document_type=None,
        xbrl_id: Optional[str] = None,
    ):
        super().__init__(
            directory_path,
            output_path,
            document_type,
            xbrl_id=xbrl_id,
        )
        self.role = "calculationLinkbaseRef"
        self.parser = CalLinkParser

        # 初期化メソッドを実行
        self._set_linkbase_files(self.role)
        self._init_parser()
        self._init_manager()


class DefLinkManager(BaseLinkManager):
    """definitionLinkbaseデータの解析を行うクラス

    raise   - NotImplementedError: [description]
            - XbrlListEmptyError: [description]
    """

    def __init__(
        self,
        directory_path,
        output_path,
        document_type=None,
        xbrl_id: Optional[str] = None,
    ):
        super().__init__(
            directory_path, output_path, document_type, xbrl_id=xbrl_id
        )
        self.role = "definitionLinkbaseRef"
        self.parser = DefLinkParser

        # 初期化メソッドを実行
        self._set_linkbase_files(self.role)
        self._init_parser()
        self._init_manager()


class PreLinkManager(BaseLinkManager):
    """presentationLinkbaseデータの解析を行うクラス

    raise   - NotImplementedError: [description]
            - XbrlListEmptyError: [description]
    """

    def __init__(
        self,
        directory_path,
        output_path,
        document_type=None,
        xbrl_id: Optional[str] = None,
    ):
        super().__init__(
            directory_path, output_path, document_type, xbrl_id=xbrl_id
        )
        self.role = "presentationLinkbaseRef"
        self.parser = PreLinkParser

        # 初期化メソッドを実行
        self._set_linkbase_files(self.role)
        self._init_parser()
        self._init_manager()
