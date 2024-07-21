from typing import Optional

from app.manager import BaseXbrlManager
from app.parser import (
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
        is_child=False,
        xbrl_id: Optional[str] = None,
    ) -> None:
        super().__init__(directory_path, xbrl_id=xbrl_id)
        self._output_path = output_path
        self._document_type = document_type
        if is_child:
            self.set_linkbase_files(self.get_role())
            self.parser = self.get_parser()

        self.link_roles = None
        self.link_locs = None
        self.link_arcs = None

        self.set_source_file(self.xbrl_id, output_path=output_path)
        self.set_link_roles()
        self.set_link_locs()
        self.set_link_arcs()

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
        raise NotImplementedError

    def get_role(self):
        raise NotImplementedError

    def set_link_roles(self):
        """link_rolesを設定します。"""
        if self.link_roles:
            return self.link_roles

        rows = []

        output_path = self.output_path
        files = self.files
        if self.document_type is not None:
            files = files.query(f"document_type == '{self.document_type}'")
        for _, row in files.iterrows():

            parser = self.parser(
                row["xlink_href"], output_path, xbrl_id=self.xbrl_id
            ).link_roles()

            data = parser.to_DataFrame()

            data["xbrl_id"] = self.xbrl_id

            rows.append(data.to_dict(orient="records"))

        self._set_items("link_roles", rows)

        self.link_roles = rows

    def set_link_locs(self):
        """link_locsを設定します。"""

        if self.link_locs:
            return self.link_locs

        rows = []

        output_path = self.output_path
        files = self.files
        if self.document_type is not None:
            files = files.query(f"document_type == '{self.document_type}'")
        for _, row in files.iterrows():
            parser = self.parser(
                row["xlink_href"], output_path, xbrl_id=self.xbrl_id
            ).link_locs()

            data = parser.to_DataFrame()

            data["xbrl_id"] = self.xbrl_id

            rows.append(data.to_dict(orient="records"))

        self._set_items("link_locs", rows)

        self.link_locs = rows

    def set_link_arcs(self):
        """link_arcsを設定します。"""

        if self.link_arcs:
            return self.link_arcs

        rows = []

        output_path = self.output_path
        files = self.files
        if self.document_type is not None:
            files = files.query(f"document_type == '{self.document_type}'")
        for _, row in files.iterrows():
            parser = self.parser(
                row["xlink_href"], output_path, xbrl_id=self.xbrl_id
            ).link_arcs()

            data = parser.to_DataFrame()

            data["xbrl_id"] = self.xbrl_id

            rows.append(data.to_dict(orient="records"))

        self._set_items("link_arcs", rows)

        self.link_arcs = rows


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
    ) -> None:
        super().__init__(
            directory_path,
            output_path,
            document_type,
            is_child=True,
            xbrl_id=xbrl_id,
        )

    def get_parser(self) -> BaseLinkParser:
        return CalLinkParser

    def get_role(self):
        role = "calculationLinkbaseRef"
        return role


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
    ) -> None:
        super().__init__(
            directory_path,
            output_path,
            document_type,
            is_child=True,
            xbrl_id=xbrl_id,
        )

    def get_parser(self) -> BaseLinkParser:
        return DefLinkParser

    def get_role(self):
        role = "definitionLinkbaseRef"
        return role


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
    ) -> None:
        super().__init__(
            directory_path,
            output_path,
            document_type,
            is_child=True,
            xbrl_id=xbrl_id,
        )

    def get_parser(self) -> BaseLinkParser:
        return PreLinkParser

    def get_role(self):
        role = "presentationLinkbaseRef"
        return role
