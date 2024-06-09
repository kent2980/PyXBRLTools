from bs4 import BeautifulSoup as bs
from pandas import DataFrame
from abc import ABC, abstractmethod
import re
from utils.utils import Utils
import logging
from log.py_xbrl_tools_loging import PyXBRLToolsLogging

class BaseXbrlIxbrlParser(ABC):
    """
    iXBRLファイルを解析するための抽象ベースクラスです。
    """

    def __init__(self, file_path:str = None) -> None:
        """
        コンストラクタ。iXBRLファイルを読み込んでBeautifulSoupオブジェクトを初期化します。

        Args:
            file_path (str): 解析するiXBRLファイルのパス。
        """
        # ログ設定
        class_name = self.__class__.__name__
        self.logger = PyXBRLToolsLogging(log_level=logging.DEBUG)
        self.logger.set_log_file(f'Log/{class_name}.log')

        if file_path is not None:
            # ファイル名が**ixbrl.htm出ない場合はエラーを出力する
            if not re.search(r'.*ixbrl\.htm$', file_path):
                raise ValueError('ファイル名がixbrl.htmではありません。')

            # ファイルパスを設定
            self.__file_path = file_path

            # クラス変数の初期化
            self.__inictialize_class(file_path)

    @property
    def file_path(self):
        """ファイルパスを返します。"""
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path):
        """ファイルパスを設定します。"""
        # ファイル名が**ixbrl.htm出ない場合はエラーを出力する
        if not re.search(r'.*ixbrl\.htm$', file_path):
            raise ValueError('ファイル名がixbrl.htmではありません。')

        # ファイルパスを設定
        self.__file_path = file_path

        # クラス変数の初期化
        self.__inictialize_class(file_path)

    def __inictialize_class(self, file_path: str):
        """クラス変数の初期化を行います。"""

        # beautifulsoupの初期化
        with open(file_path, 'r', encoding='utf-8') as file:
            self.soup = bs(file, features='xml')

        # DataFrameの初期化
        self._ix_non_fractions = None
        self._ix_non_numerics = None
        self._xbrli_contexts = None

    @property
    @abstractmethod
    def ix_non_fractions(self):
        """非分数データを含むDataFrameを返します。"""
        pass

    @property
    @abstractmethod
    def ix_non_numerics(self):
        """非数値データを含むDataFrameを返します。"""
        pass

    @property
    @abstractmethod
    def xbrli_contexts(self):
        """文脈情報を含むDataFrameを返します。"""
        pass

class XbrlIxbrlParser(BaseXbrlIxbrlParser):
    """
    iXBRLファイルを解析するための具象クラスです。
    """

    @property
    def ix_non_fractions(self):
        """非分数データを取得します。"""

        # DataFrameがNoneの場合は取得する
        if self._ix_non_fractions is None:

            lists = []
            tags = self.soup.find_all(name='ix:nonFraction')
            for tag in tags:
                lists.append({
                    'context_ref': tag.get('contextRef'),
                    'decimals': int(tag.get('decimals')) if tag.get('decimals') else None,
                    'format': tag.get('format'),
                    'name': tag.get('name').replace(":", "_"),
                    'scale': int(tag.get('scale')) if tag.get('scale') else None,
                    'sign': tag.get('sign'),
                    'unit_ref': tag.get('unitRef'),
                    'xsi_nil': True if tag.get('xsi:nil') == 'true' else False,
                    'numeric': float(re.sub(',','',tag.text)) if tag.text else None
                })

            self._ix_non_fractions = DataFrame(lists)

        return self._ix_non_fractions

    @property
    def ix_non_numerics(self):
        """非数値データを取得します。"""

        if self._ix_non_numerics is None:

            lists = []
            tags = self.soup.find_all(name='ix:nonNumeric')
            for tag in tags:
                lists.append({
                    'context_ref': tag.get('contextRef'),
                    'name': tag.get('name').replace(":", "_"),
                    'xsi_nil': True if tag.get('xsi:nil') == 'true' else False,
                    'escape': True if tag.get('escape') == 'true' else False,
                    'text': re.sub(r'[　 ]', '', tag.text) if tag.text else ''
                })

            self._ix_non_numerics = DataFrame(lists)

        return self._ix_non_numerics

    @property
    def xbrli_contexts(self):
        """文脈情報を取得します。"""

        if self._xbrli_contexts is None:

            lists = []
            tags = self.soup.find_all(name='xbrli:context')
            for tag in tags:
                context_dict = {
                    'context_id': tag.get('id'),
                    'xbrli_entity': re.sub(r'\r?\n',"",Utils.is_element_text(tag.find('xbrli:entity'))),
                    'xbrli_period_start_date': Utils.is_element_text(tag.find('xbrli:period').find('xbrli:startDate')),
                    'xbrli_period_end_date': Utils.is_element_text(tag.find('xbrli:period').find('xbrli:endDate')),
                    'xbrli_instant': Utils.is_element_text(tag.find('xbrli:period').find('xbrli:instant'))
                }
                explicit_members = {f'explicit_member_{i}': Utils.is_element_text(member)
                                    for i, member in enumerate(tag.find_all('xbrldi:explicitMember'), 1)}
                context_dict.update(explicit_members)
                lists.append(context_dict)

            self._xbrli_contexts = DataFrame(lists)

        return self._xbrli_contexts