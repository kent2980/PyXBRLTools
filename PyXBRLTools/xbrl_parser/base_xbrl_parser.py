from bs4 import BeautifulSoup as bs
import requests
from pandas import DataFrame
import os
from urllib.parse import urlparse

class BaseXBRLParser:
    """ XBRLを解析する基底クラス
        このクラスを継承して、各XBRLの解析クラスを作成する。
        以下の機能を提供します。
        - XBRLのダウンロード
        - XBRLの解析
        - XBRLの情報取得
        - 出力形式の選択

    Attributes:
    - xbrl_url: str
        XBRLのURL
    - output_path: str
        ファイルの保存先

    Properties:
    - data: list[dict]
        解析結果のデータ

    Methods:
    - read_xbrl
        XBRLを読み込む
    - parse_xbrl
        XBRLを解析する
    - fetch_url
        URLからXBRLを取得する
    - is_url_in_local
        URLがローカルに存在するか判定する
    -create
        BaseXBRLParserの初期化を行うクラスメソッド
    - to_csv
        CSV形式で出力する
    - to_DataFrame
        DataFrame形式で出力する
    - to_json
        JSON形式で出力する
    - to_dict
        辞書形式で出力する
    """
    def __init__(self, xbrl_url, output_path = None):
        # URLが指定されている場合は出力先を指定する
        if xbrl_url.startswith('http') and output_path is None:
            raise Exception('Please specify the output path')

        # プロパティの初期化
        self.xbrl_url = xbrl_url
        self.output_path = output_path
        self.soup:bs | None = None
        self.data = []

    def _read_xbrl(self, xbrl_path):
        """ XBRLをBeautifulSoup読み込む """
        with open(xbrl_path, 'r', encoding='utf-8') as f:
            self.soup = bs(f, features='xml')
            return self.soup

    def _fetch_url(self):
        """ URLからローカルにファイルを保存する """
        if self.xbrl_url.startswith('http'):
            response = requests.get(self.xbrl_url)
            if response.status_code == 200:
                file_path = os.path.join(self.output_path, urlparse(self.xbrl_url).path.lstrip('/'))
                # 保存ディレクトリが存在しない場合は作成する
                if not os.path.exists(file_path.rsplit('/', 1)[0]):
                    os.makedirs(file_path.rsplit('/', 1)[0])
                with open(file_path, 'w') as f:
                    f.write(response.text)
                return file_path
            else:
                raise Exception('Failed to fetch XBRL')

    def _is_url_in_local(self) -> tuple[bool, str]:
        """ URLがローカルに存在するか判定する

        Returns:
        - bool: ファイルが存在するか
        - str: ファイルのパス
        """
        if self.xbrl_url.startswith('http'):
            file_path = os.path.join(self.output_path, self.xbrl_url.split('/')[-1])
            if os.path.exists(file_path):
                return True, file_path
            else:
                return False, None
        else:
            if os.path.exists(self.xbrl_url):
                return True, self.xbrl_url
            else:
                return False, None

    @classmethod
    def create(cls, xbrl_url, output_path = None):
        """ BaseXBRLParserの初期化を行うクラスメソッド
            xbrl_urlがローカルパスの場合は、output_pathは不要です。

        Args:
        - xbrl_url: str
            XBRLのURL
        - output_path: str
            ファイルの保存先

        Returns:
        - cls: BaseXBRLParser
            BaseXBRLParserのインスタンス

        Examples:
            >>> from xbrl_parser.base_xbrl_parser import BaseXBRLParser
            >>> instance = BaseXBRLParser.create(xbrl_url, output_path)
        """
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