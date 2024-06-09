# 必要なライブラリのインポート
from bs4 import BeautifulSoup as bs
from pandas import DataFrame
from abc import ABC, abstractmethod
import re
import logging
from log.py_xbrl_tools_loging import PyXBRLToolsLogging

class BaseXmlLinkParser(ABC):
    """
    XMLラベルパーサの基底クラス。

    Attributes:\n
        file_path (str): パースするXMLファイルのパス。\n

    Properties:\n
        link_roles (DataFrame): link:role要素を取得するプロパティ。\n
        link_locs (dict[str, DataFrame]): link:loc要素を取得するプロパティ。\n
        link_arcs (dict[str, DataFrame]): link:labelArc要素を取得するプロパティ。\n
        link_base (DataFrame): link:base要素を取得するプロパティ。\n
        link (DataFrame): link要素を取得するプロパティ。\n

    Methods:
        __init__: 初期化メソッド。
        __inicialize_class: クラス変数の初期化を行うメソッド。
    """

    def __init__(self, file_path: str = None) -> None:
        """初期化メソッド。

        Args:
            file_path (str): XMLファイルのパス。
        """
        # ログ設定
        class_name = self.__class__.__name__
        self.logger = PyXBRLToolsLogging(log_level=logging.DEBUG)
        self.logger.set_log_file(f'Log/{class_name}.log')

        self.logger.logger.debug(f'{class_name} を初期化中、file_path: {file_path}')

        if file_path is not None:

            # ファイル名が**cal.xml,**def.xml,**pre.xmlでない場合はエラーを出力する
            if not re.search(r'.*cal\.xml$|.*def\.xml$|.*pre\.xml$', file_path):
                self.logger.error('無効なファイル名です。 ファイル名は cal.xml, def.xml, pre.xml である必要があります。')
                raise ValueError('ファイル名がcal.xml,def.xml,pre.xmlではありません。')

            # ファイルパスを設定
            self.__file_path = file_path

            # クラス変数の初期化
            self.__inicialize_class(file_path)

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
        self.logger.logger.debug(f'file_pathを設定中: {file_path}')

        # ファイル名が**cal.xml,**def.xml,**pre.xmlでない場合はエラーを出力する
        if not re.search(r'.*cal\.xml$|.*def\.xml$|.*pre\.xml$', file_path):
            self.logger.error('無効なファイル名です。 ファイル名は cal.xml, def.xml, pre.xml である必要があります。')
            raise ValueError('ファイル名がcal.xml,def.xml,pre.xmlではありません。')

        # ファイルパスを設定
        self.__file_path = file_path

        # クラス変数の初期化
        self.__inicialize_class(file_path)

    # クラス変数を初期化するメソッド
    def __inicialize_class(self, file_path: str):
        """クラス変数の初期化を行います。"""

        # BeautifulSoupの初期化
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self._soup = bs(file, features='xml')
        except Exception as e:
            self.logger.error(f'BeautifulSoupの初期化に失敗しました。: {e}')
            raise e

        # DataFrameの初期化
        self._role_refs = None
        self._link_locs = None
        self._link_arcs = None
        self._link_base = None
        self._link = None

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

class XmlLinkParser(BaseXmlLinkParser):
    """ BaseXmlLabelParserを継承して具体的な実装を行うクラス。

    Attributes:\n
        file_path (str): パースするXMLファイルのパス。\n

    Properties:\n
        link_roles (DataFrame): link:role要素を取得するプロパティ。\n
        link_locs (dict[str, DataFrame]): link:loc要素を取得するプロパティ。\n
        link_arcs (dict[str, DataFrame]): link:labelArc要素を取得するプロパティ。\n
        link_base (DataFrame): link:base要素を取得するプロパティ。\n
        link (DataFrame): link要素を取得するプロパティ。\n

    Methods:\n
        get_selected_link_locs: 指定したroleに対応するlink:loc要素を取得するメソッド。\n
        get_selected_link_arcs: 指定したroleに対応するlink:labelArc要素を取得するメソッド。\n
        is_role_exist: linkのxlink_roleにroleが存在するか確認するメソッド。\nß
    """

    @property
    def link_roles(self) -> DataFrame:
        """ link:role要素を取得するメソッド。

        Returns:
            DataFrame: link:role要素を含むDataFrame。

        Examples:
            >>> parser = XmlLinkParser('data/abc-20130331_cal.xml')
            >>> parser.link_roles

            [取得するDataFrameの例]\n
            xlink_type (str): simple\n
            xlink_href (str): http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2023-12-01/jppfs_cor_2023-12-01.xsd\n
            role_uri (str): http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet
        """
        if self._role_refs is None:

            self.logger.logger.debug('link:role要素を取得中。')

            lists = []
            tags = self._soup.find_all(['link:role', 'roleRef'])
            for tag in tags:
                lists.append({
                    'xlink_type': tag.get('xlink:type'),
                    'xlink_href': tag.get('xlink:href'),
                    'role_uri': tag.get('roleURI'),
                })

            self._role_refs = DataFrame(lists)

        return self._role_refs

    @property
    def link_locs(self) -> dict[str, DataFrame]:
        """ link:loc要素を取得するメソッド。

        Returns:
            dict[str, DataFrame]: link:loc要素を含むDataFrame。

        Examples:
            >>> parser = XmlLinkParser('data/abc-20130331_cal.xml')
            >>> parser.link_locs

            [取得する辞書データの例]\n
            http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet: DataFrame\n

            [取得するDataFrameの例]\n
            xlink_type (str): locator\n
            xlink_href (str): jppfs_cor_2023-12-01.xsd\n
            xlink_label (str): jppfs_cor_EquityClassOfShares
        """

        # link_locsがNoneの場合は取得する
        if self._link_locs is None:

            self.logger.logger.debug('link:loc要素を取得中。')

            dict = {}

            # link:calculationLink,link:definitionLink,link:presentationLinkタグからxlink:roleが一致するタグの子要素を取得
            link_tag_names = ['link:calculationLink', 'link:definitionLink', 'link:presentationLink']
            link_tags = self._soup.find_all(link_tag_names)

            for link_tag in link_tags:
                tag_lists = []

                attr_value = link_tag.get('xlink:role')

                tags = link_tag.find_all(['link:loc'])
                for tag in tags:
                    tag_lists.append({
                        'xlink_type': tag.get('xlink:type'),
                        'xlink_href': tag.get('xlink:href').split('#')[0],
                        'xlink_label': tag.get('xlink:label'),
                    })

                dict[attr_value] = DataFrame(tag_lists)

            self._link_locs = dict

        return self._link_locs

    @property
    def link_arcs(self) -> dict[str, DataFrame]:
        """ link:labelArc要素を取得するメソッド。

        Returns:
            dict[str, DataFrame]: link:labelArc要素を含むDataFrame。

        Examples:
            >>> parser = XmlLinkParser('data/abc-20130331_cal.xml')
            >>> parser.link_arcs

            [取得する辞書データの例]
            http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet: DataFrame\n

            [取得するDataFrameの例]\n
            xlink_type (str): arc\n
            xlink_from (str): jppfs_cor_AccountsPayableOther\n
            xlink_to (str): jppfs_lab_AccountsPayableOther\n
            xlink_arcrole (str): http://www.xbrl.org/2003/arcrole/concept-label\n
            xlink_order (int): 1\n
            xlink_weight (int): 1
        """
        # link_arcsがNoneの場合は取得する
        if self._link_arcs is None:

            self.logger.logger.debug('link:labelArc要素を取得中。')

            dict = {}

            # link:calculationLink,link:definitionLink,link:presentationLinkタグからxlink:roleが一致するタグの子要素を取得
            link_tag_names = ['link:calculationLink', 'link:definitionLink', 'link:presentationLink']
            link_tags = self._soup.find_all(link_tag_names)

            for link_tag in link_tags:
                tag_lists = []

                attr_value = link_tag.get('xlink:role')

                arc_tag_names = ['link:calculationArc', 'link:definitionArc', 'link:presentationArc']
                tags = link_tag.find_all(arc_tag_names)
                for tag in tags:
                    tag_lists.append({
                        'xlink_type': tag.get('xlink:type'),
                        'xlink_from': tag.get('xlink:from'),
                        'xlink_to': tag.get('xlink:to'),
                        'xlink_arcrole': tag.get('xlink:arcrole'),
                        'xlink_order': tag.get('order'),
                        'xlink_weight': tag.get('weight'),
                    })

                dict[attr_value] = DataFrame(tag_lists)

            self._link_arcs = dict

        return self._link_arcs

    @property
    def link_base(self) -> DataFrame:
        """ link:base要素を取得するメソッド。

        Returns:
            DataFrame: link:base要素を含むDataFrame。

        Examples:
            >>> parser = XmlLinkParser('data/abc-20130331_cal.xml')
            >>> parser.link_base

            [取得するDataFrameの例]\n
            xmlns_xlink (str): http://www.w3.org/1999/xlink\n
            xmlns_xsi (str): http://www.w3.org/2001/XMLSchema-instance\n
            xmlns_link (str): http://www.xbrl.org/2003/linkbase
        """
        if self._link_base is None:

            self.logger.logger.debug('link:base要素を取得中。')

            lists = []
            tags = self._soup.find_all(name='link:linkbase')
            for tag in tags:
                lists.append({
                    'xmlns_xlink': tag.get('xmlns:xlink'),
                    'xmlns_xsi': tag.get('xmlns:xsi'),
                    'xmlns_link': tag.get('xmlns:link'),
                })

            self._link_base = DataFrame(lists)

        return self._link_base

    @property
    def link(self) -> DataFrame:
        """ link要素を取得するメソッド

        Returns:
            DataFrame: link要素を含むDataFrame。

        Examples:
            >>> parser = XmlLinkParser('data/abc-20130331_cal.xml')
            >>> df = parser.link

            [取得するDataFrameの例]\n
            xlink_type (str) : extended\n
            xlink_role (str) : http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet
        """
        if self._link is None:

            self.logger.logger.debug('link要素を取得中。')

            lists = []
            tag_names = ["link:calculationLink", "link:definitionLink", "link:presentationLink"]
            tags = self._soup.find_all(name=tag_names)
            for tag in tags:
                lists.append({
                    'xlink_type': tag.get('xlink:type'),
                    'xlink_role': tag.get('xlink:role'),
                })

            self._link = DataFrame(lists)

        return self._link

    def get_selected_link_locs(self, role: str) -> DataFrame:
        """指定したroleに対応するlink:loc要素を取得するメソッド。

        Args:
            role (str): 取得したいrole。

        Returns:
            DataFrame: 指定したroleに対応するlink:loc要素を含むDataFrame。

        Examples:
            >>> parser = XmlLinkParser('data/abc-20130331_cal.xml')
            >>> parser.get_selected_link_locs('http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet')

            [取得するDataFrameの例]\n
            xlink_type (str): locator\n
            xlink_href (str): jppfs_cor_2023-12-01.xsd\n
            xlink_label (str): jppfs_cor_EquityClassOfShares
        """

        loc = self.link_locs

        # locにroleが存在しない場合はエラーを出力する
        if role not in loc:
            self.logger.logger.error(f'role: {role} は存在しません。')
            raise ValueError(f'role: {role} は存在しません。')

        return loc[role]

    def get_selected_link_arcs(self, role: str) -> DataFrame:
        """指定したroleに対応するlink:labelArc要素を取得するメソッド。

        Args:
            role (str): 取得したいrole。

        Returns:
            DataFrame: 指定したroleに対応するlink:labelArc要素を含むDataFrame。

        Examples:
            >>> parser = XmlLinkParser('data/abc-20130331_cal.xml')
            >>> parser.get_selected_link_arcs('http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet')

            [取得するDataFrameの例]\n
            xlink_type (str): arc\n
            xlink_from (str): jppfs_cor_AccountsPayableOther\n
            xlink_to (str): jppfs_lab_AccountsPayableOther\n
            xlink_arcrole (str): http://www.xbrl.org/2003/arcrole/concept-label\n
            xlink_order (int): 1\n
            xlink_weight (int): 1
        """

        arcs = self.link_arcs

        # arcsにroleが存在しない場合はエラーを出力する
        if role not in arcs:
            self.logger.logger.error(f'role: {role} は存在しません。')
            raise ValueError(f'role: {role} は存在しません。')

        return arcs[role]

    # linkのxlink_roleにroleが存在するか確認するメソッド
    def is_role_exist(self, role: str) -> bool:
        """linkのxlink_roleにroleが存在するか確認するメソッド。

        Args:
            role (str): 確認したいrole。

        Returns:
            bool: roleが存在する場合はTrue、存在しない場合はFalse。

        Examples:
            >>> parser = XmlLinkParser('data/abc-20130331_cal.xml')
            >>> parser.check_role_exist('http://disclosure.edinet-fsa.go.jp/role/jppfs/rol_ConsolidatedBalanceSheet')
            True
        """
        roles = self.link['xlink_role'].values
        return role in roles