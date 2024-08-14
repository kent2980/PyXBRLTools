import hashlib
import json
import os
import re
import shutil
import unicodedata
import uuid
import zipfile
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlparse

import requests
from datetimejp import JDate


class Utils:
    """ユーティリティクラス"""

    def extract_zip(zip_path, extract_to=None):
        """
        ZIPファイルを指定されたディレクトリに展開します。

        Args:
            zip_path (str): ZIPファイルのパス。
            extract_to (str, optional): ファイルを展開するディレクトリ。デフォルトはZIPファイルと同じディレクトリ。

        Raises:
            FileNotFoundError: ZIPファイルが存在しない場合に発生。
            Exception: 展開に失敗した場合に発生。
        """
        if not os.path.exists(zip_path):
            raise FileNotFoundError(
                f"ZIPファイル {zip_path} が存在しません。"
            )

        if extract_to is None:
            extract_to = os.path.dirname(zip_path)

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)
        except Exception as e:
            raise Exception(
                f"ZIPファイル {zip_path} の展開に失敗しました: {e}"
            )

    def format_date(date_str):
        """
        日付文字列を受け取り、統一的なフォーマット 'YYYY-MM-DD' に変換する。

        Args:
            date_str (str): "令和4年10月3日"、
            "2023年10月3日"、"2023-10-3" のいずれかの形式の日付文字列。

        Returns:
            str: 'YYYY-MM-DD' 形式の日付文字列。

        Raises:
            ValueError: 引数がサポートされていない形式の日付文字列の場合。

        Examples:
            >>> format_date('令和4年10月3日')
            '2022-10-03'
            >>> format_date('2023年10月3日')
            '2023-10-03'
            >>> format_date('2023-10-3')
            '2023-10-03'
        """

        # "元号yy年MM月DD日"のフォーマット
        try:
            jd = JDate.strptime(date_str, "%g%e年%m月%d日")
            result = jd.strftime("%Y-%m-%d")
            date_obj = result

        except ValueError:
            try:
                # "YYYY年MM月DD日"のフォーマット
                date_obj = datetime.strptime(
                    date_str, "%Y年%m月%d日"
                ).strftime("%Y-%m-%d")
            except ValueError:
                # "YYYY-MM-DD"のフォーマット
                date_obj = datetime.strptime(
                    date_str, "%Y-%m-%d"
                ).strftime("%Y-%m-%d")

        return date_obj

    def initialize_directory(directory_path: str):
        """
        指定されたディレクトリ内のすべてのファイルとサブディレクトリを削除します。

        :param directory_path: 初期化するディレクトリのパス
        """
        if not os.path.exists(directory_path):
            # ディレクトリが存在しない場合は作成
            os.makedirs(directory_path)
        else:
            # ディレクトリが存在する場合は、中身を全て削除
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(
                        file_path
                    ):
                        os.unlink(
                            file_path
                        )  # ファイルまたはシンボリックリンクを削除
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # ディレクトリを削除
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")

    def find_filename_with_keyword(directory_path, keyword):
        """
        指定されたディレクトリから再帰的にファイルを検索し、
        ファイル名にキーワードを含むファイルのパスをリストとして返します。

        :param directory_path: 検索対象のディレクトリのパス
        :param keyword: 検索するキーワード
        :return: キーワードを含むファイル名のパスのリスト
        """
        matching_files = []

        for root, dirs, files in os.walk(directory_path):
            for filename in files:
                if keyword in filename:
                    file_path = os.path.join(root, filename)
                    matching_files.append(file_path)

        return matching_files

    import os
    import re

    def find_filename_with_regex(directory_path, pattern):
        """
        指定されたディレクトリから再帰的にファイルを検索し、
        ファイル名が指定された正規表現パターンにマッチするファイルのパスをリストとして返します。

        :param directory_path: 検索対象のディレクトリのパス
        :param pattern: 正規表現パターン
        :return: パターンにマッチするファイル名のパスのリスト
        """
        matching_files = []
        regex = re.compile(pattern)

        for root, dirs, files in os.walk(directory_path):
            for filename in files:
                if regex.search(filename):
                    file_path = os.path.join(root, filename)
                    matching_files.append(file_path)

        return matching_files

    def download_file_to_dir(url, directory):
        """
        URLからファイルをダウンロードし、指定されたディレクトリにそのファイル名で保存します。

        :param url: ダウンロードしたいファイルのURL
        :param directory: 保存するディレクトリのパス
        """
        # URLからファイル名を取得
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # 完全なファイルパスを作成
        file_path = os.path.join(directory, filename)

        # ディレクトリが存在しない場合は作成
        if not os.path.exists(directory):
            os.makedirs(directory)

        # ファイルをダウンロードして保存
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

        return file_path  # ダウンロードしたファイルのパスを返す

    def is_element_text(element):
        if element is not None:
            return element.text
        return None

    def zenkaku_space_trim(str: str):
        return str.replace("　", "")

    def normalize_text(text: str) -> str:
        """
        テキストを正規化します。
        """
        # テキストをNFKC正規化
        return re.sub(" ", "", unicodedata.normalize("NFKC", text))

    def date_str_to_format(text, format_str):
        if "dateyearmonthdaycjk" in format_str:
            # textの「yyyy年mm月dd日」を「yyyy-mm-dd」に変換
            text = (
                text.replace("年", "-")
                .replace("月", "-")
                .replace("日", "")
            )
            # textの数字部分を0埋め
            text = re.sub(r"(\d+)", lambda x: x.group(0).zfill(2), text)
            format_str = "dateyearmonthday"
            return text, format_str
        elif "dateerayearmonthdayjp" in format_str:
            jd = JDate.strptime(text, "%g%e年%m月%d日")
            text = jd.strftime("%Y-%m-%d")
            # textの数字部分を0埋め
            text = re.sub(r"(\d+)", lambda x: x.group(0).zfill(2), text)
            format_str = "dateyearmonthday"
            return text, format_str
        if text:
            # textが「yyyy-mm-dd」の場合
            if re.match(r"^\d{4}-\d{2}-\d{2}$", text):
                format_str = "dateyearmonthday"
        return text, format_str

    def read_const_json():
        """const.jsonを読み込む関数"""
        # 現在のディレクトリを取得
        current_dir = Path(os.path.dirname(__file__)).parent
        const_path = current_dir / "const" / "const.json"
        with open(const_path) as f:
            const = json.load(f)
        return const

    def string_to_uuid(name: str):
        # SHA-1ハッシュを生成
        hash = hashlib.sha1(name.encode("utf-8")).hexdigest()
        # 最初の32文字を取り出してUUIDに変換
        return uuid.UUID(hash[:32])

    def decimal_encoder(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(
            f"Object of type {obj.__class__.__name__} is not JSON serializable"
        )
