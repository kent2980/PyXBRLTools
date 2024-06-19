from PyXBRLTools.xbrl_exception.xbrl_parser_exception import TypeOfXBRLIsDifferent
from .base_xbrl_parser import BaseXBRLParser

class BaseLinkParser(BaseXBRLParser):
    """ BaseLinkParserのクラス"""
    def __init__(self, xbrl_url, output_path=None):
        super().__init__(xbrl_url, output_path)

        # プロパティの初期化
        self.link_tag_name = None
        self.arc_tag_name = None

        # link要素とarc要素のタグ名を設定
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

        example:
            >>> parser = XmlLabelParser("**-lab.xml")
            >>> df = parser.link_roles().to_DataFrame()

            [取得するDataFrameの例]\n
            xlink_type (str): simple\n
            xlink_href (str): http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2023-12-01/jppfs_cor_2023-12-01.xsd\n
            role_uri (str): http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet
        """

        lists = []

        tags = self.soup.find_all(name=['link:role', 'roleRef'])
        for tag in tags:
            dict = {
                    'xlink_type': tag.get('xlink:type'),
                    'xlink_href': tag.get('xlink:href'),
                    'role_uri': tag.get('roleURI'),
            }
            lists.append(dict)

        self.data = lists

        return self

    def link_locs(self):
        """link:loc要素を取得するメソッド。

        returns:
            DataFrame: link:loc要素を含むDataFrame。

        example:
            >>> parser = XmlLabelParser("**-lab.xml")
            >>> df = parser.link_locs().to_DataFrame()

            [取得するDataFrameの例]\n
            xlink_type (str): locator\n
            xlink_href (str): jppfs_cor_2023-12-01.xsd\n
            xlink_label (str): jppfs_cor_EquityClassOfShares
        """
        link_tags = self.soup.find_all(self.link_tag_name)

        lists = []
        for link_tag in link_tags:

            attr_value = link_tag.get('xlink:role')

            tags = link_tag.find_all(['link:loc'])
            for tag in tags:
                lists.append({
                    'attr_value': attr_value,
                    'xlink_type': tag.get('xlink:type'),
                    'xlink_schema': tag.get('xlink:href').split('#')[0],
                    'xlink_href': tag.get('xlink:href').split('#')[1],
                    'xlink_label': tag.get('xlink:label'),
                })

        self.data = lists

        return self

    def link_arcs(self):
        """link:arc要素を取得するメソッド。

        returns:
            DataFrame: link:arc要素を含むDataFrame。

        example:
            >>> parser = XmlLabelParser("**-lab.xml")
            >>> df = parser.link_arcs().to_DataFrame()

            [取得するDataFrameの例]\n
            xlink_type (str): arc\n
            xlink_from (str): jppfs_cor_AccountsPayableOther\n
            xlink_to (str): jppfs_lab_AccountsPayableOther\n
            xlink_arcrole (str): http://www.xbrl.org/2003/arcrole/concept-label\n
            xlink_order (int): 1\n
            xlink_weight (int): 1
        """
        link_tags = self.soup.find_all(self.link_tag_name)

        lists = []
        for link_tag in link_tags:

            attr_value = link_tag.get('xlink:role')

            tags = link_tag.find_all('link:calculationArc')
            tags = link_tag.find_all(self.arc_tag_name)
            for tag in tags:
                lists.append({
                    'attr_value': attr_value,
                    'xlink_type': tag.get('xlink:type'),
                    'xlink_from': tag.get('xlink:from'),
                    'xlink_to': tag.get('xlink:to'),
                    'xlink_arcrole': tag.get('xlink:arcrole'),
                    'xlink_order': float(tag.get('order')) if tag.get('order') is not None else None,
                    'xlink_weight': float(tag.get('weight')) if tag.get('weight') is not None else None,
                })

        self.data = lists

        return self

    def link_base(self):
        """link:base要素を取得するメソッド。

        returns:
            DataFrame: link:base要素を含むDataFrame。

        example:
            >>> parser = XmlLabelParser("**-lab.xml")
            >>> df = parser.link_base().to_DataFrame()

            [取得するDataFrameの例]\n
            xmlns_xlink (str): http://www.w3.org/1999/xlink\n
            xmlns_xsi (str): http://www.w3.org/2001/XMLSchema-instance\n
            xmlns_link (str): http://www.xbrl.org/2003/linkbase
        """

        lists = []

        tags = self.soup.find_all(name='link:linkbase')
        for tag in tags:
            dict = {
                'xmlns_xlink': tag.get('xmlns:xlink'),
                'xmlns_xsi': tag.get('xmlns:xsi'),
                'xmlns_link': tag.get('xmlns:link'),
            }
            lists.append(dict)

        self.data = lists

        return self

    def link(self):
        """link要素を取得するメソッド。

        returns:
            DataFrame: link要素を含むDataFrame。

        example:
            >>> parser = XmlLabelParser("**-lab.xml")
            >>> df = parser.calculationLink().to_DataFrame()

            [取得するDataFrameの例]\n
            xlink_type (str) : extended\n
            xlink_role (str) : http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet
        """

        lists = []

        tags = self.soup.find_all(self.link_tag_name)
        for tag in tags:
            dict = {
                    'xlink_type': tag.get('xlink:type'),
                    'xlink_role': tag.get('xlink:role'),
            }
            lists.append(dict)

        self.data = lists

        return self

class CalLinkParser(BaseLinkParser):
    """ CalculationLinkのParserクラス"""
    def __init__(self, xbrl_url, output_path=None):
        super().__init__(xbrl_url, output_path)

        # cal.xmlでない場合はエラーを出力
        if not self.basename().endswith("cal.xml"):
            raise TypeOfXBRLIsDifferent(f"{self.basename()} はcal.xmlではありません。")

    def set_link_tag_name(self):
        self.link_tag_name = 'link:calculationLink'

    def set_arc_tag_name(self):
        self.arc_tag_name = 'link:calculationArc'
class DefLinkParser(BaseLinkParser):
    """ DefinitionLinkのParserクラス"""
    def __init__(self, xbrl_url, output_path=None):
        super().__init__(xbrl_url, output_path)

        # def.xmlでない場合はエラーを出力
        if not self.basename().endswith("def.xml"):
            raise TypeOfXBRLIsDifferent(f"{self.basename()} はdef.xmlではありません。")

    def set_link_tag_name(self):
        self.link_tag_name = 'link:definitionLink'

    def set_arc_tag_name(self):
        self.arc_tag_name = 'link:definitionArc'
class PreLinkParser(BaseLinkParser):
    """ PresentationLinkのParserクラス"""
    def __init__(self, xbrl_url, output_path=None):
        super().__init__(xbrl_url, output_path)

        # pre.xmlでない場合はエラーを出力
        if not self.basename().endswith("pre.xml"):
            raise TypeOfXBRLIsDifferent(f"{self.basename()} はpre.xmlではありません。")

    def set_link_tag_name(self):
        self.link_tag_name = 'link:presentationLink'

    def set_arc_tag_name(self):
        self.arc_tag_name = 'link:presentationArc'