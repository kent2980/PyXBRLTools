from app.exception import TypeOfXBRLIsDifferent
from app.tag import LinkArc, LinkBase, LinkLoc, LinkRole, LinkTag

from . import BaseXBRLParser


class BaseLinkParser(BaseXBRLParser):
    """BaseLinkParserのクラス"""

    def __init__(self, xbrl_url, output_path=None, is_child=False):
        super().__init__(xbrl_url, output_path)

        # プロパティの初期化
        self.link_tag_name = None
        self.arc_tag_name = None

        # link要素とarc要素のタグ名を設定
        if is_child:
            self.set_link_tag_name()
            self.set_arc_tag_name()

    def set_link_tag_name(self):
        raise NotImplementedError   

    def set_arc_tag_name(self):
        raise NotImplementedError   

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
            lists.append(lrr.__dict__)

        self.data = lists

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
                )

                lists.append(ll.__dict__)

        self.data = lists

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

            tags = link_tag.find_all(self.arc_tag_name)
            for tag in tags:
                # _____attr[xlink:order]
                xlink_order = (
                    float(tag.get("order")) if tag.get("order") is not None else None
                )

                # _____attr[xlink:weight]
                xlink_weight = (
                    float(tag.get("weight")) if tag.get("weight") is not None else None
                )

                la = LinkArc(
                    xbrl_id=self.xbrl_id,
                    attr_value=attr_value,
                    xlink_type=tag.get("xlink:type"),
                    xlink_from=tag.get("xlink:from"),
                    xlink_to=tag.get("xlink:to"),
                    xlink_arcrole=tag.get("arcrole"),
                    xlink_order=xlink_order,
                    xlink_weight=xlink_weight,
                )
                lists.append(la.__dict__)

        self.data = lists

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
            lists.append(lb.__dict__)

        self.data = lists

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
            lists.append(lt.__dict__)

        self.data = lists

        return self


class CalLinkParser(BaseLinkParser):
    """CalculationLinkのParserクラス"""

    def __init__(self, xbrl_url, output_path=None):
        super().__init__(xbrl_url, output_path, is_child=Ture)

        # cal.xmlでない場合はエラーを出力
        if not self.basename().endswith("cal.xml"):
            raise TypeOfXBRLIsDifferent(f"{self.basename()} はcal.xmlではありません。")

    def set_link_tag_name(self):
        self.link_tag_name = "link:calculationLink"

    def set_arc_tag_name(self):
        self.arc_tag_name = "link:calculationArc"


class DefLinkParser(BaseLinkParser):
    """DefinitionLinkのParserクラス"""

    def __init__(self, xbrl_url, output_path=None):
        super().__init__(xbrl_url, output_path, is_child=Ture)

        # def.xmlでない場合はエラーを出力
        if not self.basename().endswith("def.xml"):
            raise TypeOfXBRLIsDifferent(f"{self.basename()} はdef.xmlではありません。")     # pragma: no cover

    def set_link_tag_name(self):
        self.link_tag_name = ["link:definitionLink", "definitionLink"]

    def set_arc_tag_name(self):
        self.arc_tag_name = ["link:definitionArc", "definitionArc"]


class PreLinkParser(BaseLinkParser):
    """PresentationLinkのParserクラス"""

    def __init__(self, xbrl_url, output_path=None):
        super().__init__(xbrl_url, output_path, is_child=Ture)

        # pre.xmlでない場合はエラーを出力
        if not self.basename().endswith("pre.xml"):
            raise TypeOfXBRLIsDifferent(f"{self.basename()} はpre.xmlではありません。")     # pragma: no cover

    def set_link_tag_name(self):
        self.link_tag_name = "link:presentationLink"

    def set_arc_tag_name(self):
        self.arc_tag_name = "link:presentationArc"