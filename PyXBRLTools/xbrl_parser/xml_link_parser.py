# 必要なライブラリのインポート
from bs4 import BeautifulSoup as bs
from pandas import DataFrame
from abc import ABC, abstractmethod
import os
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
        self.file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as file:
            self.soup = bs(file, features='xml')
        self.__set_df()

        # ログ設定
        class_name = self.__class__.__name__
        self.logger = PyXBRLToolsLogging(log_level=logging.DEBUG)
        self.logger.set_log_file(f'Log/{class_name}.log')

    @property
    def link_locs(self):
        """link:loc要素を含むDataFrameを返すプロパティ。"""
        return self.__link_locs

    @property
    def link_arcs(self):
        """link:labelArc要素を含むDataFrameを返すプロパティ。"""
        return self.__link_arcs

    def __set_df(self):
        """プライベートメソッド。DataFrameを設定する。"""
        if self.file_path:
            self.__link_locs = self.get_link_locs()
            self.__link_arcs = self.get_link_arcs()

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

    @abstractmethod
    def get_link_locs(self) -> DataFrame:
        """link:loc要素を取得する抽象メソッド。"""
        pass

    @abstractmethod
    def get_link_arcs(self) -> DataFrame:
        """link:labelArc要素を取得する抽象メソッド。"""
        pass

class XmlLinkParser(BaseXmlLinkParser):
    """BaseXmlLabelParserを継承して具体的な実装を行うクラス。"""

    def get_link_locs(self) -> DataFrame:
        """link:loc要素を取得するメソッド。"""
        return self._get_tags_to_dataframe(['link:loc', 'loc'])

    def get_link_arcs(self) -> DataFrame:
        """link:labelArc要素を取得するメソッド。"""
        tag_list = ['link:calculationArc','link:definitionArc','link:presentationArc']
        return self._get_tags_to_dataframe(tag_list)