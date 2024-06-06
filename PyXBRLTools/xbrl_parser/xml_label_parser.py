# 必要なライブラリのインポート
from bs4 import BeautifulSoup as bs
from pandas import DataFrame
from abc import ABC, abstractmethod
import re
import logging
from log.py_xbrl_tools_loging import PyXBRLToolsLogging

class BaseXmlLabelParser(ABC):
    """
    XMLラベルパーサの基底クラス。

    Attributes:
        file_path (str): パースするXMLファイルのパス。
        soup (BeautifulSoup): BeautifulSoupオブジェクト。
        _link_labels (DataFrame): link:label要素を含むDataFrame。
        _link_locs (DataFrame): link:loc要素を含むDataFrame。
        _link_label_arcs (DataFrame): link:labelArc要素を含むDataFrame。
        _role_refs (DataFrame): roleRef要素を含むDataFrame。
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

        if file_path is not None:
            # ファイル名が**lab**.xmlでない場合はエラーを出力する
            if not re.search(r'.*lab.*\.xml$', file_path):
                raise ValueError('ファイル名がlab**.xmlではありません。')

            # ファイルパスを設定
            self.__file_path = file_path

            # クラス変数の初期化
            self.__inictialize_class(file_path)


    @property
    def file_path(self) -> str| None:
        """file_path属性のゲッター。"""
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path: str) -> None:
        """file_path属性のセッター。

        Args:
            file_path (str): パースするXMLファイルのパス。
        """

        # ファイル名が**lab**.xmlでない場合はエラーを出力する
        if not re.search(r'.*lab.*\.xml$', file_path):
            raise ValueError('ファイル名がlab**.xmlではありません。')

        # ファイルパスを設定
        self.__file_path = file_path

        # クラス変数の初期化
        self.__inictialize_class(file_path)

    # クラス変数を初期化するメソッド
    def __inictialize_class(self, file_path: str):
        """クラス変数の初期化を行います。"""
        with open(file_path, 'r', encoding='utf-8') as file:
            self.soup = bs(file, features='xml')

        # DataFrameの初期化
        self._link_labels = None
        self._link_locs = None
        self._link_label_arcs = None
        self._role_refs = None

    @property
    @abstractmethod
    def link_labels(self) -> DataFrame:
        """link:label要素を取得する抽象メソッド。"""
        pass

    @property
    @abstractmethod
    def link_locs(self) -> DataFrame:
        """link:loc要素を取得する抽象メソッド。"""
        pass

    @property
    @abstractmethod
    def link_label_arcs(self) -> DataFrame:
        """link:labelArc要素を取得する抽象メソッド。"""
        pass

    @property
    @abstractmethod
    def role_refs(self) -> DataFrame:
        """roleRef要素を取得する抽象メソッド。"""
        pass

class XmlLabelParser(BaseXmlLabelParser):
    """ XMLラベルパーサの具象クラス。XMLラベルの情報を取得するクラス。"""

    @property
    def link_labels(self) -> DataFrame:
        """link:label要素を取得するメソッド。

        returns:


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

        if self._link_labels is None:

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

            self._link_labels = DataFrame(lists)

        return self._link_labels

    @property
    def link_locs(self) -> DataFrame:
        """link:loc要素を取得するメソッド。

        returns:
            DataFrame: link:loc要素を含むDataFrame。

        Example:
            >>> parser = XmlLabelParser("**-lab.xml")
            >>> df = parser.link_locs

            [取得するDataFrameの例]\n
            xlink_type (str): locator\n
            xlink_schema (str): http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2021-12-01/jppfs_cor_2023-12-01.xsd\n
            xlink_href (str): jppfs_cor_EquityClassOfShares\n
            xlink_label (str): label_EquityClassOfShares
        """
        if self._link_locs is None:

            lists = []
            tags = None

            tags = self.soup.find_all(name=['link:loc', 'loc'])
            for tag in tags:
                dict = {
                    'xlink_type': tag.get('xlink:type'),
                    'xlink_schema': tag.get('xlink:href').split('#')[0],
                    'xlink_href': tag.get('xlink:href').split('#')[-1:][0],
                    'xlink_label': tag.get('xlink:label'),
                }
                lists.append(dict)

            self._link_locs = DataFrame(lists)

        return self._link_locs

    @property
    def link_label_arcs(self) -> DataFrame:
        """link:labelArc要素を取得するメソッド。

        returns:
            DataFrame: link:labelArc要素を含むDataFrame。

        Example:
            >>> parser = XmlLabelParser("**-lab.xml")
            >>> df = parser.link_label_arcs

            [取得するDataFrameの例]\n
            xlink_type (str): arc\n
            xlink_arcrole (str): http://www.xbrl.org/2003/arcrole/concept-label\n
            xlink_from (str): EquityClassOfShares\n
            xlink_to (str): label_EquityClassOfShares
        """
        if self._link_label_arcs is None:

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

            self._link_label_arcs = DataFrame(lists)

        return self._link_label_arcs

    @property
    def role_refs(self) -> DataFrame:
        """ roleRef要素を取得するメソッド。

        returns:
            DataFrame: roleRef要素を含むDataFrame。

        Example:
            >>> parser = XmlLabelParser("**-lab.xml")
            >>> df = parser.role_refs

            [取得するDataFrameの例]\n
            Role_URI (str): http://disclosure.edinet-fsa.go.jp/jpcrp/std/alt/role/label\n
            xlink_type (str): simple\n
            xlink_schema (str): jpcrp_rt_2023-12-01.xsd\n
            xlink_href (str): rol_std_altLabel
        """
        if self._role_refs is None:

            lists = []
            tags = self.soup.find_all(name=['link:roleRef', 'roleRef'])
            for tag in tags:
                dict = {
                    'Role_URI': tag.get('roleURI'),
                    'xlink_type': tag.get('xlink:type'),
                    'xlink_schema': tag.get('xlink:href').split('#')[0].split('/')[-1:][0],
                    'xlink_href': tag.get('xlink:href').split('#')[-1:][0],
                }
                lists.append(dict)

            self._role_refs = DataFrame(lists)

        return self._role_refs