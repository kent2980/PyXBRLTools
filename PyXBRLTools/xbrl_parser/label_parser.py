from .base_xbrl_parser import BaseXBRLParser
from pandas import DataFrame

class LabelParser(BaseXBRLParser):
    """ XBRLのラベル情報を取得するクラス
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

    def link_labels(self):
        """link:label要素を取得するメソッド。

        returns:
            self: LabelParser

        example:
            >>> parser = XmlLabelParser("**-lab.xml")
            >>> df = parser.link_labels

            [取得するDataFrameの例]\n
            xlink_type (str): resource\n
            xlink_label (str): label_EquityClassOfShares\n
            xlink_role (str): http://www.xbrl.org/2003/role/label\n
            xml_lang (str): ja\n
            id (str): label_EquityClassOfShares\n
            label (str): 株式の種類
        """

        lists = []

        tags = self.soup.find_all(name=['link:label', 'label'])
        for tag in tags:
            # id属性が存在で分岐
            if tag.get('id') == None:
                dict = {
                    'xlink_type': tag.get('xlink:type'),
                    'xlink_label': tag.get('xlink:label'),
                    'xlink_role': tag.get('xlink:role'),
                    'xml_lang': tag.get('xml:lang'),
                    'id': tag.get('xlink:label'),
                    'label': tag.text
                }
            else:
                dict = {
                    'xlink_type': tag.get('xlink:type'),
                    'xlink_label': tag.get('xlink:label'),
                    'xlink_role': tag.get('xlink:role'),
                    'xml_lang': tag.get('xml:lang'),
                    'id': tag.get('id'),
                    'label': tag.text
                }
            lists.append(dict)

        df = DataFrame(lists)

        link_arcs = self.link_label_arcs().to_DataFrame()

        # self._link_labels(xlink_label)にlink_arcs(xlink_to)のxlink_schemaカラムを追加
        df = df.merge(link_arcs[['xlink_to', 'xlink_schema']],
                            left_on='xlink_label', right_on='xlink_to', how='left').drop(columns='xlink_to')

        self.data =  df.to_dict(orient='records')

        return self

    def link_locs(self):
        """link:loc要素を取得するメソッド。

        returns:
            self: LabelParser

        Example:
            >>> parser = XmlLabelParser("**-lab.xml")
            >>> df = parser.link_locs

            [取得するDataFrameの例]\n
            xlink_type (str): locator\n
            xlink_schema (str): http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2021-12-01/jppfs_cor_2023-12-01.xsd\n
            xlink_href (str): jppfs_cor_EquityClassOfShares\n
            xlink_label (str): label_EquityClassOfShares
        """
        lists = []

        tags = self.soup.find_all(name=['link:loc', 'loc'])
        for tag in tags:
            dict = {
                'xlink_type': tag.get('xlink:type'),
                'xlink_schema': tag.get('xlink:href').split('#')[0],
                'xlink_href': tag.get('xlink:href').split('#')[-1:][0],
                'xlink_label': tag.get('xlink:label'),
            }
            lists.append(dict)

        self.data =  lists

        return self

    def link_label_arcs(self):
        """link:labelArc要素を取得するメソッド。

        returns:
            self: LabelParser

        Example:
            >>> parser = XmlLabelParser("**-lab.xml")
            >>> df = parser.link_label_arcs

            [取得するDataFrameの例]\n
            xlink_type (str): arc\n
            xlink_arcrole (str): http://www.xbrl.org/2003/arcrole/concept-label\n
            xlink_from (str): EquityClassOfShares\n
            xlink_to (str): label_EquityClassOfShares
        """
        lists = []
        tags = self.soup.find_all(name=['link:labelArc', 'labelArc'])
        for tag in tags:
            dict = {
                'xlink_type': tag.get('xlink:type'),
                'xlink_arcrole': tag.get('xlink:arcrole'),
                'xlink_from': tag.get('xlink:from'),
                'xlink_to': tag.get('xlink:to'),
            }
            lists.append(dict)

        df = DataFrame(lists)

        link_locs = self.link_locs().to_DataFrame()

        # self._link_label_arcs(xlink_from)にlink_locs(xlink_label)のxlink_schemaカラムを追加
        df = df.merge(link_locs[['xlink_label', 'xlink_schema']],
                                left_on='xlink_from', right_on='xlink_label', how='left').drop(columns='xlink_label')

        self.data = df.to_dict(orient='records')

        return self

    def role_refs(self):
        """ roleRef要素を取得するメソッド。

        returns:
            self: LabelParser

        Example:
            >>> parser = XmlLabelParser("**-lab.xml")
            >>> df = parser.role_refs

            [取得するDataFrameの例]\n
            Role_URI (str): http://disclosure.edinet-fsa.go.jp/jpcrp/std/alt/role/label\n
            xlink_type (str): simple\n
            xlink_schema (str): jpcrp_rt_2023-12-01.xsd\n
            xlink_href (str): rol_std_altLabel
        """
        lists = []
        tags = self.soup.find_all(name=['link:roleRef', 'roleRef'])
        for tag in tags:
            dict = {
                'Role_URI': tag.get('roleURI'),
                'xlink_type': tag.get('xlink:type'),
                'xlink_schema': tag.get('xlink:href').split('#')[0] if tag.get('xlink:href') else None,
                'xlink_href': tag.get('xlink:href').split('#')[-1:][0] if tag.get('xlink:href') else None,
            }
            lists.append(dict)

        self.data = lists

        return self
