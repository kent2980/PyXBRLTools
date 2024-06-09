from bs4 import BeautifulSoup as bs
from pandas import DataFrame
import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import Utils
import logging
from log.py_xbrl_tools_loging import PyXBRLToolsLogging

class XbrlQualitativeParser:
    """
    "qualitative.htm"から情報を解析して抽出するためのクラスです。
    """

    def __init__(self, file_path: str = None) -> None:
        """
        QualitativeParserクラスのコンストラクタです。
        """
        # ログ設定
        class_name = self.__class__.__name__
        self.logger = PyXBRLToolsLogging(log_level=logging.DEBUG)
        self.logger.set_log_file(f'Log/{class_name}.log')

        if file_path is not None:
            # ファイル名がqualitative.htmでない場合はエラーを出力する
            if not re.search(r'.*qualitative\.htm$', file_path):
                raise ValueError('ファイル名がqualitative.htmではありません。')

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
        self.__smt_head = None

    @property
    def file_path(self):
        """ファイルパスを返します。"""
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path):
        """ファイルパスを設定します。"""
        # ファイル名が**qualitative.htmでない場合はエラーを出力する
        if not re.search(r'.*qualitative\.htm$', file_path):
            raise ValueError('ファイル名がqualitative.htmではありません。')

        # ファイルパスを設定
        self.__file_path = file_path

        # クラス変数の初期化
        self.__inictialize_class(file_path)

    @property
    def smt_head(self) -> DataFrame:
        """
        HTMLファイルから見出しとテキストデータを抽出してDataFrameとして返すメソッドです。
        """

        if self.__smt_head is None:

            lists = []
            head1_title = ""
            head2_title = ""

            for tag in self.soup.find_all(class_=True):
                class_ = tag["class"][0]

                if class_ == "smt_head1":
                    head1_title = Utils.normalize_text(tag.text)
                elif class_ == "smt_head2":
                    head2_title = Utils.normalize_text(tag.text)
                elif "smt_text" in class_:
                    text = Utils.normalize_text(tag.text)
                    if not lists or head1_title != lists[-1]['title'] or head2_title != lists[-1]['sub_title']:
                        lists.append({'title': head1_title, 'sub_title': head2_title, 'text': text})
                    else:
                        lists[-1]['text'] += text

            lists = [row for row in lists if re.search(r'\d', row['title'])]

            self.__smt_head = DataFrame(lists)

        return self.__smt_head