from bs4 import BeautifulSoup as bs
from pandas import DataFrame
from abc import ABC, abstractmethod
import re
import os
from utils.utils import Utils
import logging
from log.py_xbrl_tools_loging import PyXBRLToolsLogging

class BaseXbrlIxbrlParser(ABC):
    """
    iXBRLファイルを解析するための抽象ベースクラスです。
    """

    def __init__(self, file_path) -> None:
        """
        コンストラクタ。iXBRLファイルを読み込んでBeautifulSoupオブジェクトを初期化します。

        Args:
            file_path (str): 解析するiXBRLファイルのパス。
        """
        self.file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as file:
            self.soup = bs(file, features='xml')

        self.__set_df()

        # ログ設定
        class_name = self.__class__.__name__
        self.logger = PyXBRLToolsLogging(log_level=logging.DEBUG)
        self.logger.set_log_file(f'Log/{class_name}.log')

    def __set_df(self):
        """データフレームを設定する内部メソッドです。"""
        self.__ix_non_fractions = self.get_ix_non_fractions()
        self.__ix_non_numerics = self.get_ix_non_numerics()
        self.__xbrli_contexts = self.get_xbrli_contexts()

    @property
    def ix_non_fractions(self):
        """非分数データを含むDataFrameを返します。"""
        return self.__ix_non_fractions

    @property
    def ix_non_numerics(self):
        """非数値データを含むDataFrameを返します。"""
        return self.__ix_non_numerics

    @property
    def xbrli_contexts(self):
        """文脈情報を含むDataFrameを返します。"""
        return self.__xbrli_contexts

    @abstractmethod
    def get_ix_non_fractions(self) -> DataFrame:
        """非分数データを取得するための抽象メソッドです。"""
        pass

    @abstractmethod
    def get_ix_non_numerics(self) -> DataFrame:
        """非数値データを取得するための抽象メソッドです。"""
        pass

    @abstractmethod
    def get_xbrli_contexts(self) -> DataFrame:
        """文脈情報を取得するための抽象メソッドです。"""
        pass

class XbrlIxbrlParser(BaseIxbrlParser):
    """
    iXBRLファイルを解析するための具象クラスです。
    """

    def get_ix_non_fractions(self):
        """非分数データを取得します。"""
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

        return DataFrame(lists)

    def get_ix_non_numerics(self):
        """非数値データを取得します。"""
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

        df = DataFrame(lists)

        return df

    def get_xbrli_contexts(self):
        """文脈情報を取得します。"""
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

        df = DataFrame(lists)

        return df