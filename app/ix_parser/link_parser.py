from typing import Optional

from app.ix_tag import LinkArc, LinkBase, LinkLoc, LinkRole, LinkTag

from . import BaseXBRLParser


class BaseLinkParser(BaseXBRLParser):
    """BaseLinkParserのクラス"""

    def __init__(
        self, xbrl_url, output_path=None, xbrl_id: Optional[str] = None
    ):
        super().__init__(xbrl_url, output_path, xbrl_id)

        # プロパティの初期化
        self.__link_tag_name = None
        self.__arc_tag_name = None

    @property
    def link_tag_name(self):
        return self.__link_tag_name

    @property
    def arc_tag_name(self):
        return self.__arc_tag_name

    def _set_link_tag_name(self, tag_name):
        self.__link_tag_name = tag_name

    def _set_arc_tag_name(self, tag_name):
        self.__arc_tag_name = tag_name

    def link_roles(self):
        """link:role要素を取得するメソッド。

        returns:
            DataFrame: link:role要素を含むDataFrame。
        """

        lists = []

        tags = self.soup.find_all(name=["link:role", "roleRef"])
        for tag in tags:
            xlink_schema = tag.get("xlink:href").split("#")[0]
            xlink_href = tag.get("xlink:href").split("#")[1]
            lrr = LinkRole(
                xbrl_id=self.xbrl_id,
                xlink_type=tag.get("xlink:type"),
                xlink_schema=xlink_schema,
                xlink_href=xlink_href,
                role_uri=tag.get("roleURI"),
            )
            lists.append(lrr)

        self._set_data(lists)

        return self

    def link_locs(self):
        """link:loc要素を取得するメソッド。

        returns:
            DataFrame: link:loc要素を含むDataFrame。
        """
        link_tags = self.soup.find_all(self.link_tag_name)

        lists = []

        for link_tag in link_tags:

            attr_value = link_tag.get("xlink:role").split("_")[-1]

            # httpが含まれている場合は、attr_valueを変更
            if "http" in attr_value:
                attr_value = attr_value.split("/Role")[-1]

            tags = link_tag.find_all(["link:loc", "loc"])
            for tag in tags:

                # _____attr[xlink:href]
                xlink_schema = tag.get("xlink:href").split("#")[0]
                xlink_href = tag.get("xlink:href").split("#")[1]

                ll = LinkLoc(
                    xbrl_id=self.xbrl_id,
                    attr_value=attr_value,
                    xlink_type=tag.get("xlink:type"),
                    xlink_schema=xlink_schema,
                    xlink_href=xlink_href,
                    xlink_label=tag.get("xlink:label"),
                    source_file_id=self.source_file_id,
                )

                lists.append(ll)

        self._set_data(lists)

        return self

    def link_arcs(self):
        """link:arc要素を取得するメソッド。

        returns:
            DataFrame: link:arc要素を含むDataFrame。
        """
        link_tags = self.soup.find_all(self.link_tag_name)

        lists = []
        for link_tag in link_tags:

            attr_value = link_tag.get("xlink:role").split("_")[-1]

            # httpが含まれている場合は、attr_valueを変更
            if "http" in attr_value:
                attr_value = attr_value.split("/Role")[-1]


            tags = link_tag.find_all(self.arc_tag_name)
            for tag in tags:
                # _____attr[xlink:order]
                xlink_order = (
                    float(tag.get("order"))
                    if tag.get("order") is not None
                    else None
                )

                # _____attr[xlink:weight]
                xlink_weight = (
                    float(tag.get("weight"))
                    if tag.get("weight") is not None
                    else None
                )

                la = LinkArc(
                    xbrl_id=self.xbrl_id,
                    attr_value=attr_value,
                    xlink_type=tag.get("xlink:type"),
                    xlink_from=tag.get("xlink:from"),
                    xlink_to=tag.get("xlink:to"),
                    xlink_arcrole=tag.get("xlink:arcrole"),
                    xlink_order=xlink_order,
                    xlink_weight=xlink_weight,
                    source_file_id=self.source_file_id,
                )
                lists.append(la)

        self._set_data(lists)

        return self

    def link_base(self):
        """link:base要素を取得するメソッド。

        returns:
            DataFrame: link:base要素を含むDataFrame。
        """

        lists = []

        tags = self.soup.find_all(name=["link:linkbase", "linkbase"])
        for tag in tags:

            lb = LinkBase(
                xbrl_id=self.xbrl_id,
                xmlns_xlink=tag.get("xmlns:xlink"),
                xmlns_xsi=tag.get("xmlns:xsi"),
                xmlns_link=tag.get("xmlns:link"),
            )
            lists.append(lb)

        self._set_data(lists)

        return self

    def link_tags(self):
        """link要素を取得するメソッド。

        returns:
            DataFrame: link要素を含むDataFrame。
        """

        lists = []

        tags = self.soup.find_all(self.link_tag_name)
        for tag in tags:

            lt = LinkTag(
                xbrl_id=self.xbrl_id,
                xlink_type=tag.get("xlink:type"),
                xlink_role=tag.get("xlink:role"),
            )
            lists.append(lt)

        self._set_data(lists)

        return self


class CalLinkParser(BaseLinkParser):
    """CalculationLinkのParserクラス"""

    def __init__(
        self, xbrl_url, output_path=None, xbrl_id: Optional[str] = None
    ):
        super().__init__(xbrl_url, output_path, xbrl_id)

        # ファイル名の検証
        self._assert_valid_basename("cal.xml")

        # 初期化メソッド
        self._set_link_tag_name(
            ["link:calculationLink", "calculationLink"]
        )
        self._set_arc_tag_name(["link:calculationArc", "calculationArc"])


class DefLinkParser(BaseLinkParser):
    """DefinitionLinkのParserクラス"""

    def __init__(
        self, xbrl_url, output_path=None, xbrl_id: Optional[str] = None
    ):
        super().__init__(xbrl_url, output_path, xbrl_id)

        # ファイル名の検証
        self._assert_valid_basename("def.xml")

        # 初期化メソッド
        self._set_link_tag_name(["link:definitionLink", "definitionLink"])
        self._set_arc_tag_name(["link:definitionArc", "definitionArc"])


class PreLinkParser(BaseLinkParser):
    """PresentationLinkのParserクラス"""

    def __init__(
        self, xbrl_url, output_path=None, xbrl_id: Optional[str] = None
    ):
        super().__init__(xbrl_url, output_path, xbrl_id)

        # ファイル名の検証
        self._assert_valid_basename("pre.xml")

        # 初期化メソッド
        self._set_link_tag_name(
            ["link:presentationLink", "presentationLink"]
        )
        self._set_arc_tag_name(["link:presentationArc", "presentationArc"])
