from bs4 import BeautifulSoup as bs
import requests
from pandas import DataFrame
import os
import time
from urllib.parse import urlparse
from pathlib import Path
from uuid import UUID, uuid4

class BaseXBRLParser:
    """ XBRLを解析する基底クラス """

    def __init__(self, xbrl_url, output_path=None):
        if xbrl_url.startswith('http'):
            if output_path is None:
                raise Exception('Please specify the output path')
        if not xbrl_url.startswith('http') and not os.path.exists(xbrl_url):
            raise FileNotFoundError(f'ファイルが見つかりません。[{xbrl_url}]')

        file_name = os.path.basename(xbrl_url)
        self.__document_type = "fr" if "fr" in file_name else "sm"
        self.xbrl_url = xbrl_url
        self.output_path = output_path
        self.soup: bs | None = None
        self.data = []
        self.__xbrl_id = str(uuid4())

    @property
    def xbrl_id(self):
        return self.__xbrl_id

    @xbrl_id.setter
    def xbrl_id(self, xbrl_id: str):
        self.__xbrl_id = xbrl_id

    @property
    def document_type(self):
        return self.__document_type

    def _read_xbrl(self, xbrl_path):
        """ XBRLをBeautifulSoup読み込む """
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            self.soup = bs(f, features='lxml-xml')
            return self.soup

    def _fetch_url(self):
        """ URLからローカルにファイルを保存する """
        if self.xbrl_url.startswith('http'):
            response = requests.get(self.xbrl_url)
            if response.status_code == 200:
                # エンコーディングを自動検出
                response.encoding = response.apparent_encoding
                file_path = os.path.join(self.output_path, urlparse(self.xbrl_url).path.lstrip('/'))
                if not os.path.exists(file_path.rsplit('/', 1)[0]):
                    os.makedirs(file_path.rsplit('/', 1)[0])
                with open(file_path, 'w', encoding=response.encoding) as f:
                    f.write(response.text)
                time.sleep(2)
                return file_path
            else:
                raise Exception('Failed to fetch XBRL')

    def _is_url_in_local(self) -> tuple[bool, str]:
        """ URLがローカルに存在するか判定する """
        if self.xbrl_url.startswith('http'):
            file_path = Path(self.output_path) / Path(urlparse(self.xbrl_url).path).relative_to('/')
            if os.path.exists(file_path):
                return True, file_path.as_posix()
            else:
                return False, None
        else:
            if os.path.exists(self.xbrl_url):
                return True, self.xbrl_url
            else:
                return False, None

    @classmethod
    def create(cls, xbrl_url, output_path=None):
        instance = cls(xbrl_url, output_path)
        is_file, file_path = instance._is_url_in_local()
        if is_file is False:
            file_path = instance._fetch_url()
        instance._read_xbrl(file_path)
        return instance

    def to_csv(self, file_path):
        """ CSV形式で出力する """
        df = self.to_DataFrame()
        df.to_csv(file_path, index=False)

    def to_DataFrame(self):
        """ DataFrame形式で出力する """
        return DataFrame(self.data)

    def to_json(self, file_path):
        """ JSON形式で出力する """
        df = self.to_DataFrame()
        df.to_json(file_path, orient='records')

    def to_dict(self):
        """ 辞書形式で出力する """
        return self.data

    def basename(self):
        """ URLからファイル名を取得する """
        if self.xbrl_url.startswith('http'):
            base_name = urlparse(self.xbrl_url).path.split('/')[-1]
            return str(base_name)
        else:
            return str(Path(self.xbrl_url).name)
