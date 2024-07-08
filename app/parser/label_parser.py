from pandas import DataFrame

from app.exception import TagNotFoundError, TypeOfXBRLIsDifferent
from app.tag import LabelArc, LabelLoc, LabelRoleRefs, LabelValue

from . import BaseXBRLParser


class LabelParser(BaseXBRLParser):
    """XBRLのラベル情報を取得するクラス
        このクラスはBaseXBRLParserを継承しています。
        XBRLのラベル情報を取得します。
        以下の機能を提供します。
        - ラベル情報取得

    Attributes:
    - xbrl_url: str
        XBRLのURL
    - output_path: str
        ファイルの保存先

    Properties:
    - data: list[dict]
        解析結果のデータ

    Methods:
    - link_labels
        link:label要素を取得する
    - link_locs
        link:loc要素を取得する
    - link_label_arcs
        link:labelArc要素を取得する
    - role_refs
        roleRef要素を取得する

    Examples:
        >>> from xbrl_parser.label_parser import LabelParser
        >>> parser = LabelParser.create(file_path)
        >>> print(parser.label().to_dataframe())
    """

    def __init__(self, xbrl_url, output_path=None):
        super().__init__(xbrl_url, output_path)

        # ファイル名がlab.xmlでない場合はエラーを発生
        if not self.basename().endswith(("lab.xml", "lab-en.xml")):
            raise TypeOfXBRLIsDifferent(f"{self.basename()} はlab.xmlではありません。")

    def link_labels(self):
        """link:label要素を取得するメソッド。

        returns:
            self: LabelParser
        """

        lists = []

        tags = self.soup.find_all(name=["link:label", "label"])
        for tag in tags:
            lv = LabelValue(
                xlink_type=tag.get("xlink:type"),
                xlink_label=tag.get("xlink:label"),
                xlink_role=tag.get("xlink:role"),
                xml_lang=tag.get("xml:lang"),
                label=tag.text,
            )
            lists.append(lv.__dict__)

        self.data = lists

        return self

    def link_label_locs(self):
        """link:loc要素を取得するメソッド。

        returns:
            self: LabelParser
        """
        lists = []

        tags = self.soup.find_all(name=["link:loc", "loc"])
        for tag in tags:

            # _____attr[xlink:href]
            if tag.get("xlink:href"):
                xlink_schema = tag.get("xlink:href").split("#")[0].split("/")[-1]
                xlink_href = tag.get("xlink:href").split("#")[-1:][0]
            else:
                xlink_schema = None
                xlink_href = None

            ll = LabelLoc(
                xlink_type=tag.get("xlink:type"),
                xlink_label=tag.get("xlink:label"),
                xlink_schema=xlink_schema,
                xlink_href=xlink_href,
            )
            lists.append(ll.__dict__)

        self.data = lists

        return self

    def link_label_arcs(self):
        """link:labelArc要素を取得するメソッド。

        returns:
            self: LabelParser
        """
        lists = []
        tags = self.soup.find_all(name=["link:labelArc", "labelArc"])
        for tag in tags:

            la = LabelArc(
                xlink_type=tag.get("xlink:type"),
                xlink_arcrole=tag.get("xlink:arcrole"),
                xlink_from=tag.get("xlink:from"),
                xlink_to=tag.get("xlink:to"),
            )
            lists.append(la.__dict__)

        self.data = lists

        return self

    def role_refs(self):
        """roleRef要素を取得するメソッド。

        returns:
            self: LabelParser

        Raises:
            TagNotFoundError: roleRef要素が存在しない場合に発生します。
        """
        lists = []
        tags = self.soup.find_all(name=["link:roleRef", "roleRef"])

        if len(tags) == 0:
            raise TagNotFoundError("roleRef要素が存在しません。")

        for tag in tags:
            # _____attr[xlink:href]
            if tag.get("xlink:href"):
                xlink_schema = tag.get("xlink:href").split("#")[0]
                xlink_href = tag.get("xlink:href").split("#")[-1:][0]
            else:
                xlink_schema = None
                xlink_href = None

            lrr = LabelRoleRefs(
                role_uri=tag.get("roleURI"),
                xlink_type=tag.get("xlink:type"),
                xlink_schema=xlink_schema,
                xlink_href=xlink_href,
            )

            lists.append(lrr.__dict__)

        self.data = lists

        return self
