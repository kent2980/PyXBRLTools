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
        class_name = self.__class__.__name__
        self.logger = PyXBRLToolsLogging(log_level=logging.DEBUG)
        self.logger.set_log_file(f'Log/{class_name}.log')

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
    def link_roles(self) -> DataFrame:
        """link:role要素を取得するメソッド。"""
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
        """link:loc要素を取得するメソッド。"""

        # self.roleURIがNoneの場合はエラーを出力する
        if self.roleURI is None:
            raise ValueError('roleURIが設定されていません。')

        if self._link_locs is None:
            lists = []
            # link:calculationLink,link:definitionLink,link:presentationLinkタグからxlink:roleが一致するタグの子要素を取得
            link_tags = ['link:calculationLink', 'link:definitionLink', 'link:presentationLink']
            tags = self.soup.find_all(link_tags, attrs={'xlink:role': self.roleURI})
            tags = tags(['link:loc'])
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
        """link:labelArc要素を取得するメソッド。"""

        # self.roleURIがNoneの場合はエラーを出力する
        if self.roleURI is None:
            raise ValueError('roleURIが設定されていません。')

        if self._link_arcs is None:
            lists = []
            # link:calculationLink,link:definitionLink,link:presentationLinkタグからxlink:roleが一致するタグの子要素を取得
            link_tags = ['link:calculationLink', 'link:definitionLink', 'link:presentationLink']
            tags = self.soup.find_all(link_tags, attrs={'xlink:role': self.roleURI})
            ark_tags = ['link:calculationArc', 'link:definitionArc', 'link:presentationArc']
            tags = tags.find_all(ark_tags)
            for tag in tags:
                lists.append({
                    'xlink_type': tag.get('xlink:type'),
                    'xlink_from': tag.get('xlink:from'),
                    'xlink_to': tag.get('xlink:to'),
                    'xlink_arcrole': tag.get('xlink:arcrole'),
                    'xlink_order': tag.get('order'),
                    'xlink_weight': tag.get('weight'),
                })

            self._link_arcs = DataFrame(lists)

        return self._link_arcs

    @property
    def roleURI(self) -> str:
        """roleURI属性のゲッター。"""
        return self._roleURI

    @roleURI.setter
    def roleURI(self, roleURI: str) -> None:
        """roleURI属性のセッター。"""
        link_roles_df = self.link_roles

        # roleURIがlink_roles_dfのrole_uriに存在しない場合はエラーを出力する
        if roleURI not in link_roles_df['role_uri'].values:
            raise ValueError('roleURIが存在しません。')
        # roleURIがlink_roles_dfのrole_uriに存在する場合はroleURIを設定する
        else:
            self._roleURI = roleURI