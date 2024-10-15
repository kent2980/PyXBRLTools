import fcntl
import os
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse
from uuid import uuid4

import requests
from bs4 import BeautifulSoup as bs
from pandas import DataFrame

from app.exception import TypeOfXBRLIsDifferent
from app.ix_tag import BaseTag, SourceFile
from app.utils.utils import Utils


class BaseXBRLParser:
    """XBRLを解析する基底クラス"""

    def __init__(
        self, xbrl_url, output_path=None, xbrl_id: Optional[str] = None
    ):

        # urlの検証を行います
        self.__assert_valid_url(xbrl_url, output_path)

        # プロパティの初期化
        self.__xbrl_url = xbrl_url  # XBRLのURL
        self.__output_path = output_path  # 出力先のパス
        self.__basename = Path(self.xbrl_url).name  # ファイル名
        self.__xbrl_type = None  # XbrlType(fr or sm)
        self.__soup = None  # BeautifulSoup
        self.__data: Optional[List[BaseTag]] = None  # 解析結果のデータ
        self.__xbrl_id = xbrl_id  # XBRLファイル固有のID
        self.__source_file_id = None  # XBRLのソースファイルID
        self.__source_file: Optional[SourceFile] = (
            None  # XBRLのソースファイル
        )

        # 初期化メソッド
        self.__init_xbrl_id()
        self.__init_xbrl_type()
        self.__init_parser()
        self.__init_source_file_id()
        self._set_source_file(self.basename)

    @property
    def basename(self):
        return self.__basename

    @property
    def data(self):
        return self.__data

    @property
    def xbrl_type(self):
        return self.__xbrl_type

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
    def source_file_id(self):
        return self.__source_file_id

    @property
    def soup(self):
        return self.__soup

    @property
    def xbrl_id(self):
        return self.__xbrl_id

    @xbrl_id.setter
    def xbrl_id(self, xbrl_id: str):
        self.__xbrl_id = xbrl_id

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

    def __init_xbrl_id(self):
        """XBRLファイル固有のIDを設定する"""
        if self.xbrl_id is None:
            self.__xbrl_id = str(uuid4())

    def __init_source_file_id(self):
        """XBRLのソースファイルIDを設定する"""

        if self.xbrl_url is None:
            raise Exception("XBRLのURLが指定されていません。")

        if self.xbrl_id is None:
            raise Exception("XBRLのIDが指定されていません。")

        if self.xbrl_url.startswith("http"):
            self.__source_file_id = str(
                Utils.string_to_uuid(self.xbrl_url)
            )
        else:
            self.__source_file_id = str(
                Utils.string_to_uuid(f"{self.xbrl_id}{self.basename}")
            )

    def __init_xbrl_type(self):
        """XBRLの種類を設定する"""
        if "fr" in self.basename:
            self.__xbrl_type = "fr"
        else:
            self.__xbrl_type = "sm"

    def _assert_valid_basename(self, *keywords: str):
        """ファイル名が有効かどうかを検証する"""
        if not self.basename.endswith(keywords):
            raise TypeOfXBRLIsDifferent(
                f"{self.basename} は{keywords}ではありません。"
            )

    def _set_data(self, data: List[BaseTag]):
        """解析結果のデータを設定する"""
        self.__data = data

    def _set_source_file(self, name: str):
        """XBRLのソースファイルを取得する"""
        if self.xbrl_url.startswith("http"):
            type = "url"
            xbrl_id = None
            url = self.xbrl_url
        else:
            type = "local"
            xbrl_id = self.xbrl_id
            url = None
        self.__source_file = SourceFile(
            name=name,
            type=type,
            url=url,
            xbrl_id=xbrl_id,
            id=self.source_file_id,
        )

    def to_DataFrame(self):
        """DataFrame形式で出力する"""

        lists = []

        for _, item in enumerate(self.data):
            if isinstance(item, BaseTag):
                item = item.__dict__
                lists.append(item)
            elif isinstance(item, list):
                return DataFrame(item)
            elif isinstance(item, dict):
                lists.append(item)
            else:
                print(type(item))
                raise Exception("itemがBaseTagクラスではありません。")

        return DataFrame(lists)

    def to_dict(self):
        """辞書形式で出力する"""
        return self.to_DataFrame().to_dict(orient="records")
