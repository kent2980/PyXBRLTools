# 必要なライブラリのインポート
from bs4 import BeautifulSoup as bs
from pandas import DataFrame
from abc import ABC, abstractmethod
import re
import logging
# from log.py_xbrl_tools_loging import PyXBRLToolsLogging

class BaseXmlLinkParser(ABC):
    """
    XMLラベルパーサの基底クラス。

    Attributes:
        file_path (str): パースするXMLファイルのパス。
        soup (BeautifulSoup): BeautifulSoupオブジェクト。
        __link_labels (DataFrame): link:label要素を含むDataFrame。
        __link_locs (DataFrame): link:loc要素を含むDataFrame。
        __link_arcs (DataFrame): link:labelArc要素を含むDataFrame。
    """

    def __init__(self, file_path: str) -> None:
        """初期化メソッド。

        Args:
            file_path (str): XMLファイルのパス。
        """
        # ファイル名が**cal.xml,**def.xml,**pre.xmlでない場合はエラーを出力する
        if not re.search(r'.*cal\.xml$|.*def\.xml$|.*pre\.xml$', file_path):
            raise ValueError('ファイル名がcal.xml,def.xml,pre.xmlではありません。')

        # ファイル名を設定
        self.__file_path = file_path

        # クラス変数の初期化
        self.__inicialize_class(file_path)

        # ログ設定
        # class_name = self.__class__.__name__
        # self.logger = PyXBRLToolsLogging(log_level=logging.DEBUG)
        # self.logger.set_log_file(f'Log/{class_name}.log')

    @property
    def file_path(self) -> str:
        """file_path属性のゲッター。"""
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path: str) -> None:
        """file_path属性のセッター。

        Args:
            file_path (str): パースするXMLファイルのパス。
        """

        # ファイル名が**cal.xml,**def.xml,**pre.xmlでない場合はエラーを出力する
        if not re.search(r'.*cal\.xml$|.*def\.xml$|.*pre\.xml$', file_path):
            raise ValueError('ファイル名がcal.xml,def.xml,pre.xmlではありません。')

        # ファイルパスを設定
        self.__file_path = file_path

        # クラス変数の初期化
        self.__inicialize_class(file_path)

    # クラス変数を初期化するメソッド
    def __inicialize_class(self, file_path: str):
        """クラス変数の初期化を行います。"""

        # BeautifulSoupの初期化
        with open(file_path, 'r', encoding='utf-8') as file:
            self.soup = bs(file, features='xml')

        # DataFrameの初期化
        self._role_refs = None
        self._link_locs = None
        self._link_arcs = None
        self._link_base = None
        self._link = None

        # 変数の初期化
        self._roleURI = None

    @property
    @abstractmethod
    def link_roles(self):
        """link:role要素を含むDataFrameを返すプロパティ。"""
        pass

    @property
    @abstractmethod
    def link_locs(self):
        """link:loc要素を含むDataFrameを返すプロパティ。"""
        pass

    @property
    @abstractmethod
    def link_arcs(self):
        """link:labelArc要素を含むDataFrameを返すプロパティ。"""
        pass

    @property
    @abstractmethod
    def link_base(self):
        """link:base要素を含むDataFrameを返すプロパティ。"""
        pass

    @property
    @abstractmethod
    def link(self):
        """link要素を含むDataFrameを返すプロパティ。"""
        pass

    @property
    @abstractmethod
    def roleURI(self):
        """roleURI属性のゲッター。"""
        pass

    @roleURI.setter
    @abstractmethod
    def roleURI(self, roleURI: str):
        """roleURI属性のセッター。"""
        pass

class XmlLinkParser(BaseXmlLinkParser):
    """BaseXmlLabelParserを継承して具体的な実装を行うクラス。"""

    @property
    def roleURI(self) -> str:
        """roleURI属性のゲッター。"""
        return self._roleURI

    @roleURI.setter
    def roleURI(self, roleURI: str) -> None:
        """roleURI属性のセッター。"""
        self._roleURI = roleURI

    @property
    def link_roles(self) -> DataFrame:
        """ link:role要素を取得するメソッド。

        Returns:
            DataFrame: link:role要素を含むDataFrame。

        Examples:
            >>> parser = XmlLinkParser('data/abc-20130331_cal.xml')
            >>> parser.link_roles
            [取得するDataFrameの例]
            xlink_type: simple
            xlink_href: http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2023-12-01/jppfs_cor_2023-12-01.xsd
            role_uri: http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet
        """
        if self._role_refs is None:
            lists = []
            tags = self.soup.find_all(['link:role', 'roleRef'])
            for tag in tags:
                lists.append({
                    'xlink_type': tag.get('xlink:type'),
                    'xlink_href': tag.get('xlink:href'),
                    'role_uri': tag.get('roleURI'),
                })

            self._role_refs = DataFrame(lists)

        return self._role_refs

    @property
    def link_locs(self) -> DataFrame:
        """ link:loc要素を取得するメソッド。

        Returns:
            DataFrame: link:loc要素を含むDataFrame。

        Examples:
            >>> parser = XmlLinkParser('data/abc-20130331_cal.xml')
            >>> parser.roleURI = 'http://www.xbrl.org/2003/role/link'
            >>> parser.link_locs
            [取得するDataFrameの例]
            xlink_type: locator
            xlink_href: http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2023-12-01/jppfs_cor_2023-12-01.xsd#jppfs_cor_AccountsPayableOther
            xlink_label: jppfs_cor_AccountsPayableOther
        """

        # # self.roleURIがNoneの場合はエラーを出力する
        # if self.roleURI is None:
        #     raise ValueError('roleURIが設定されていません。')

        # link_locsがNoneの場合は取得する
        if self._link_locs is None:
            lists = []
            # link:calculationLink,link:definitionLink,link:presentationLinkタグからxlink:roleが一致するタグの子要素を取得
            link_tag_names = ['link:calculationLink', 'link:definitionLink', 'link:presentationLink']
            tags = self.soup.find(link_tag_names, attrs={'xlink:role': self.roleURI})

            # link:locタグからxlink:roleが一致するタグの子要素を取得
            tags = tags.find_all(['link:loc'])

            # link:loc要素を取得
            for tag in tags:
                lists.append({
                    'xlink_type': tag.get('xlink:type'),
                    'xlink_href': tag.get('xlink:href').split('#')[0],
                    'xlink_label': tag.get('xlink:label'),
                })

            self._link_locs = DataFrame(lists)

        return self._link_locs

    @property
    def link_arcs(self) -> DataFrame:
        """ link:labelArc要素を取得するメソッド。

        Returns:
            DataFrame: link:labelArc要素を含むDataFrame。

        Examples:
            >>> parser = XmlLinkParser('data/abc-20130331_cal.xml')
            >>> parser.roleURI = 'http://www.xbrl.org/2003/role/link'
            >>> parser.link_arcs
            [取得するDataFrameの例]
            xlink_type: arc
            xlink_from: jppfs_cor_AccountsPayableOther
            xlink_to: jppfs_cor_AccountsPayableOther
            xlink_arcrole: http://www.xbrl.org/2003/arcrole/concept-label
            xlink_order: 1
            xlink_weight: 1
        """
        # # self.roleURIがNoneの場合はエラーを出力する
        # if self.roleURI is None:
        #     raise ValueError('roleURIが設定されていません。')

        # link_arcsがNoneの場合は取得する
        if self._link_arcs is None:
            lists = []

            # link:calculationLink,link:definitionLink,link:presentationLinkタグからxlink:roleが一致するタグの子要素を取得
            link_tag_names = ['link:calculationLink', 'link:definitionLink', 'link:presentationLink']
            link_tags = self.soup.find_all(link_tag_names)

            for link_tag in link_tags:
                tag_lists = []

                attr_value = link_tag.get('xlink:role')

                arc_tag_names = ['link:caculationArc', 'link:definitionArc', 'link:presentationArc']
                tags = link_tag.find_all(arc_tag_names, attrs={'xlink:arcrole': attr_value})
                for tag in tags:
                    tag_lists.append({
                        'xlink_type': tag.get('xlink:type'),
                        'xlink_from': tag.get('xlink:from'),
                        'xlink_to': tag.get('xlink:to'),
                        'xlink_arcrole': tag.get('xlink:arcrole'),
                        'xlink_order': tag.get('order'),
                        'xlink_weight': tag.get('weight'),
                    })
                lists.append({
                    attr_value: tag_lists
                })
                print(tag_lists)

            print(lists)

    def link_base(self) -> DataFrame:
        """ link:base要素を取得するメソッド。

        Returns:
            DataFrame: link:base要素を含むDataFrame。

        Examples:
            >>> parser = XmlLinkParser('data/abc-20130331_cal.xml')
            >>> parser.link_base

            [取得するDataFrameの例]
            xmlns_xlink: http://www.w3.org/1999/xlink
            xmlns_xsi: http://www.w3.org/2001/XMLSchema-instance
            xmlns_link: http://www.xbrl.org/2003/linkbase
        """
        if self._link_base is None:
            lists = []
            tags = self.soup.find_all(name='link:linkbase')
            for tag in tags:
                lists.append({
                    'xmlns_xlink': tag.get('xmlns:xlink'),
                    'xmlns_xsi': tag.get('xmlns:xsi'),
                    'xmlns_link': tag.get('xmlns:link'),
                })

            self._link_base = DataFrame(lists)

        return self._link_base

    def link(self) -> DataFrame:
        """ link要素を取得するメソッド。

        Returns:
            DataFrame: link要素を含むDataFrame。

        Examples:
            >>> parser = XmlLinkParser('data/abc-20130331_cal.xml')
            >>> parser.link

            [取得するDataFrameの例]
            xlink_type: extended
            xlink_role: http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet
        """
        if self._link is None:
            lists = []
            tag_names = ["link:calculationLink", "link:definitionLink", "link:presentationLink"]
            tags = self.soup.find_all(name=tag_names)
            for tag in tags:
                lists.append({
                    'xlink_type': tag.get('xlink:type'),
                    'xlink_role': tag.get('xlink:role'),
                })

            self._link = DataFrame(lists)

        return self._link

# テストコード
if __name__ == '__main__':
    xml_path = '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/tse-acedjpfr-57210-2024-03-31-01-2024-05-13-cal.xml'
    parser = XmlLinkParser(xml_path)
    # print(parser.link_roles)
    # print(parser.link_locs)
    print(parser.link_arcs)
    # print(parser.link_base)
    # print(parser.link())
    # print(parser.roleURI)
    # parser.roleURI = 'http://www.xbrl.org/2003/role/link'
    # print(parser.roleURI)
    # print(parser.link_locs)