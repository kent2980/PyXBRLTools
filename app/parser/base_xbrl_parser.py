import fcntl
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
from uuid import uuid4

import requests
from bs4 import BeautifulSoup as bs
from pandas import DataFrame

from app.tag import SourceFile


class BaseXBRLParser:
    """XBRLを解析する基底クラス"""

    def __init__(self, xbrl_url, output_path=None):

        # urlの検証を行います
        self.__assert_valid_url(xbrl_url, output_path)

        # プロパティの初期化
        self.__xbrl_url = xbrl_url  # XBRLのURL
        self.__output_path = output_path  # 出力先のパス
        self.__basename = Path(self.xbrl_url).name  # ファイル名
        self.__document_type = (
            "fr" if "fr" in self.basename else "sm"
        )  # ドキュメントタイプ
        self.__soup = None  # BeautifulSoup
        self.__data = None  # 解析結果のデータ
        self.__xbrl_id = str(uuid4())  # XBRLファイル固有のID
        self.__source_file = None  # XBRLのソースファイル

        # 初期化メソッド
        self._set_source_file(self.basename, self.xbrl_id)
        self.__init_parser()

    @property
    def basename(self):
        return self.__basename

    @property
    def data(self):
        return self.__data

    @property
    def document_type(self):
        return self.__document_type

    @property
    def output_path(self):
        return self.__output_path

    @output_path.setter
    def output_path(self, output_path: str):
        self.__output_path = output_path

    @property
    def source_file(self):
        return self.__source_file

    @property
    def soup(self):
        return self.__soup

    @property
    def xbrl_id(self):
        return self.__xbrl_id

    @xbrl_id.setter
    def xbrl_id(self, xbrl_id: str):
        self.__xbrl_id = xbrl_id

    @property
    def xbrl_url(self):
        return self.__xbrl_url

    @xbrl_url.setter
    def xbrl_url(self, xbrl_url: str):
        self.__xbrl_url = xbrl_url

    def __fetch_url(self):
        """URLからローカルにファイルを保存する"""
        if self.xbrl_url.startswith("http"):
            response = requests.get(self.xbrl_url)
            if response.status_code == 200:
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\
                    {self.xbrl_url} からXBRLを取得しました。"
                )
                # エンコーディングを自動検出
                response.encoding = response.apparent_encoding
                file_path = os.path.join(
                    self.output_path,
                    urlparse(self.xbrl_url).path.lstrip("/"),
                )
                if not os.path.exists(file_path.rsplit("/", 1)[0]):
                    os.makedirs(file_path.rsplit("/", 1)[0], exist_ok=True)
                with open(file_path, "w", encoding=response.encoding) as f:
                    f.write(response.text)
                time.sleep(2)
                return file_path
            else:
                raise Exception("Failed to fetch XBRL")

    def __is_url_in_local(self) -> tuple[bool, str]:
        """URLがローカルに存在するか判定する"""
        if self.xbrl_url.startswith("http"):
            file_path = Path(self.output_path) / Path(
                urlparse(self.xbrl_url).path
            ).relative_to("/")
            if os.path.exists(file_path):
                return True, file_path.as_posix()
            else:
                return False, None
        else:
            if os.path.exists(self.xbrl_url):
                return True, self.xbrl_url
            else:
                return False, None

    def __read_xbrl(self, xbrl_path):
        """XBRLをBeautifulSoup読み込む"""
        with open(xbrl_path, "r", encoding="utf-8") as f:
            # 読み取り専用でファイルをロック
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            self.__soup = bs(f, features="lxml-xml")
            # ファイルのロックを解除
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            return self.soup

    def __assert_valid_url(self, url: str, output_path: Optional[str]):
        """URLが有効かどうかを検証する"""

        if url.startswith("http"):
            if output_path is None:
                raise Exception("出力先のパスが指定されていません。")
        else:
            if not os.path.exists(url):
                raise FileNotFoundError(
                    f"ファイルが見つかりません。[{url}]"
                )

    def __init_parser(self):
        """解析用の初期化処理"""

        # ファイルが存在するか確認
        is_file, file_path = self.__is_url_in_local()
        # ファイルが存在しない場合は、URLから取得
        if is_file is False:
            file_path = self.__fetch_url()
        # XBRLを読み込む
        self.__read_xbrl(file_path)

    def _set_data(self, data):
        """解析結果のデータを設定する"""
        self.__data = data

    def _set_source_file(self, name: str, xbrl_id: str):
        """XBRLのソースファイルを取得する"""
        self.__source_file = SourceFile(name=name, xbrl_id=xbrl_id)

    def to_DataFrame(self):
        """DataFrame形式で出力する"""
        return DataFrame(self.data)

    def to_dict(self):
        """辞書形式で出力する"""
        return self.data
