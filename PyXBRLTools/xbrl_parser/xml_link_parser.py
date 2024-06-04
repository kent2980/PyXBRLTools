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
        self.__link_locs = None
        self.__link_arcs = None

    def _get_tags_to_dataframe(self, tag_names: list) -> DataFrame:
        """タグ名のリストからDataFrameを生成するヘルパーメソッド。

        Args:
            tag_names (list): タグ名のリスト。

        Returns:
            DataFrame: 生成されたDataFrame。
        """
        tags = self.soup.find_all(name=tag_names)
        data_list = [
            {key: tag.get(key) for key in tag.attrs.keys()} | {'text': tag.text}
            for tag in tags
        ]
        return DataFrame(data_list)

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

class XmlLinkParser(BaseXmlLinkParser):
    """BaseXmlLabelParserを継承して具体的な実装を行うクラス。"""

    @property
    def link_locs(self) -> DataFrame:
        """link:loc要素を取得するメソッド。"""
        return self._get_tags_to_dataframe(['link:loc', 'loc'])

    @property
    def link_arcs(self) -> DataFrame:
        """link:labelArc要素を取得するメソッド。"""
        tag_list = ['link:calculationArc','link:definitionArc','link:presentationArc']
        return self._get_tags_to_dataframe(tag_list)