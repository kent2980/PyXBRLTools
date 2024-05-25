from bs4 import BeautifulSoup as bs
from pandas import DataFrame
from abc import ABC, abstractmethod
import re
import sys
import os

# 1つ上のディレクトリのパスを取得してsys.pathに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import Utils

class BaseIxbrlParser(ABC):

    def __init__(self, file_path) -> None:
        self.__file_path = file_path
        self.soup = bs(open(file_path), features='xml')

        self.__ix_non_fractions = None
        self.__ix_non_numerics = None

        self.__set_df()

    def __set_df(self):
        self.__ix_non_fractions = self.get_ix_non_fractions()
        self.__ix_non_numerics = self.get_ix_non_numerics()
        self.__xbrli_contexts = self.get_xbrli_contexts()

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path:str):
        self.__file_path = file_path
        self.soup = bs(open(file_path), features='xml')
        self.__set_df()

    @property
    def ix_non_fractions(self):
        return self.__ix_non_fractions

    @property
    def ix_non_numerics(self):
        return self.__ix_non_numerics

    @property
    def xbrli_contexts(self):
        return self.__xbrli_contexts

    @abstractmethod
    def get_ix_non_fractions(self):
        pass

    @abstractmethod
    def get_ix_non_numerics(self):
        pass

    @abstractmethod
    def get_xbrli_contexts(self):
        pass

class IxbrlParser(BaseIxbrlParser):

    def __init__(self, file_path) -> None:
        super().__init__(file_path)

    def get_ix_non_fractions(self):
        lists = []

        tags = self.soup.find_all(name='ix:nonFraction')
        for tag in tags:
            dict = {
                'context_ref': tag.get('contextRef'),
                'decimals': tag.get('decimals'),
                'format': tag.get('format'),
                'name': tag.get('name'),
                'scale': tag.get('scale'),
                'unit_ref': tag.get('unitRef'),
                'xsi_nil': tag.get('xsi:nil'),
                'ix_numeric': re.sub(',','',tag.text)
            }

            lists.append(dict)

        return DataFrame(lists)

    def get_ix_non_numerics(self):
        lists = []

        tags = self.soup.find_all(name='ix:nonNumeric')
        for tag in tags:
            dict = {
                'context_ref': tag.get('contextRef'),
                'name': tag.get('name'),
                'xsi_nil': tag.get('xsi:nil'),
                'escape': tag.get('escape'),
                'ix_text': Utils.zenkaku_space_trim(re.sub(r'（\d+）|\n| ', '', tag.text).split(' ')[0])
            }

            lists.append(dict)

        return DataFrame(lists)

    def get_xbrli_contexts(self):
        lists = []

        tags = self.soup.find_all(name='xbrli:context')
        for tag in tags:
            dict = {
                'context_id': tag.get('id'),
                'xbrli_entity': tag.find('xbrli:entity').text,
                'xbrli_period_start_date': Utils.is_element_text(tag.find('xbrli:period').find('xbrli:startDate')),
                'xbrli_period_end_date': Utils.is_element_text(tag.find('xbrli:period').find('xbrli:endDate')),
                'xbrli_instant': Utils.is_element_text(tag.find('xbrli:period').find('xbrli:instant'))
            }
            i = 1
            for ex_menbers in tag.find_all('xbrldi:explicitMember'):
                    dict['explicit_member_' + str(i)] = Utils.is_element_text(ex_menbers)
                    dict['explicit_member_' + str(i) + '_xmlns_xbrldi'] = ex_menbers.get('xmlns:xbrldi')
                    dict['explicit_member_' + str(i) + '_dimension'] = ex_menbers.get('dimension')
                    i = i + 1

            lists.append(dict)

        return DataFrame(lists)

if __name__ == '__main__':
    sr_file_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Summary/tse-acedjpsm-44440-20240502581623-ixbrl.htm"
    fr_file_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/0300000-acbs01-tse-acedjpfr-44440-2024-03-31-01-2024-05-14-ixbrl.htm"
    si = IxbrlParser(sr_file_path)
    print(si.ix_non_numerics)
    si.ix_non_fractions.to_csv('non_fractions.csv')
    si.ix_non_numerics.to_csv('non_numerics.csv')
    si.xbrli_contexts.to_csv('contexts.csv')