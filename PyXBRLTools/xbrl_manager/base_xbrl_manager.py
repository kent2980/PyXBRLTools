import os
from abc import ABC

class BaseXbrlManager(ABC):
    """ XBRLファイルのパスを取得するための基底クラス。

    Attributes:\n
        dir_path (str): パースするディレクトリのパス。\n
        _ixbrl_files (list[dict[str: str]]): ixbrlファイルのパスと文書の種類を格納したリスト。\n
        _schema_files (list[dict[str: str]]): スキーマファイルのパスと文書の種類を格納したリスト。\n
        SUMMARY (str): 決算短信サマリー\n
        CASH_FLOW (str): キャッシュフロー計算書\n
        BARANCE_SHEET (str): 貸借対照表\n
        PROFIT_AND_LOSS (str): 損益計算書\n
        STATEMENT_OF_SHAREHOLDERS (str): 株主資本等変動計算書\n
        STATEMENT_OF_COMPREHENSIVE_INCOME (str): 包括利益計算書\n

    properties:\n
        dir_path (str): パースするディレクトリのパス。\n
        ixbrl_files (list[dict[str: str]]): ixbrlファイルのパスと文書の種類を格納したリスト。\n
        schema_files (list[dict[str: str]]): スキーマファイルのパスと文書の種類を格納したリスト。\n

    Methods:\n
        initialize_class: クラス変数の初期化を行うメソッド。\n
        search_ixbrl_files: ディレクトリパスから末尾(ixbrl.htm)で終わるファイルを検索するメソッド。\n
    """

    # クラス定数の宣言
    SUMMARY = "sm"
    CASH_FLOW = "cf"
    BARANCE_SHEET = "bs"
    PROFIT_AND_LOSS = "pl"
    STATEMENT_OF_SHAREHOLDERS = "ss"
    STATEMENT_OF_COMPREHENSIVE_INCOME = "pc"

    def __init__(self, dir_path: str):

        # ディレクトリパスを設定
        self._dir_path = dir_path

        # 初期化メソッドを実行
        self.initialize_class()

    @property
    def dir_path(self) -> str:
        """dir_path属性のゲッター。"""
        return self._dir_path

    @dir_path.setter
    def dir_path(self, dir_path: str) -> None:
        """dir_path属性のセッター。

        Args:
            dir_path (str): パースするディレクトリのパス。
        """
        # ディレクトリパスを設定
        self._dir_path = dir_path

        # 初期化メソッドを実行
        self.initialize_class()

    def initialize_class(self) -> None:
        """クラス変数の初期化を行うメソッド。"""

        # ixbrlファイルのパスを取得
        self.__ixbrl_files = self.search_ixbrl_files()

        # スキーマファイルのパスを取得
        self.__schema_files = self.search_schema_files()

    @property
    def ixbrl_files(self) -> dict[str: str]:
        """ixbrl_files属性のゲッター。"""
        return self.__ixbrl_files

    @property
    def schema_files(self) -> dict[str: str]:
        """schema_files属性のゲッター。"""
        return self.__schema_files

    def search_ixbrl_files(self) -> list[dict[str: str]]:
        """ ディレクトリパスから末尾(ixbrl.htm)で終わるファイルを検索するメソッド。

        Returns:
            list[dict[str: str]]: ファイルパスと文書の種類を格納したリスト。

        Raises:
            ValueError: ディレクトリパスが設定されていない場合。

        Example:
            >>> dir_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData"
            >>> link_manager = BaseLinkManager(dir_path)
            >>> link_manager.search_ixbrl_files()

            [取得したファイルパスと文書の種類のリスト]\n
            [{'document': 'sm', 'path': '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Summary/tse-acedjpsm-****-2024-03-31-01-2024-05-13-ixbrl.htm'},\n
            {'document': 'cf', 'path': '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/0304000-accf01-tse-acedjpfr-*****-2024-03-31-01-2024-05-13-ixbrl.htm'}]
        """
        # ディレクトリパスが設定されていない場合はエラーを出力する
        if self.dir_path is None:
            raise ValueError('ディレクトリパスが設定されていません。')

        lists = []
        # ディレクトリパスから末尾(ixbrl.htm)で終わるファイルを検索
        for file_path, file in self.search_file_path("ixbrl.htm"):
            if "sm" in file:
                lists.append({
                    'document': "sm",
                    'path': file_path
                    })
            elif "fr" in file:
                lists.append({
                    'document': file.split('-')[1][2:4],
                    'path': file_path})

        return lists

    def search_schema_files(self) -> list[dict[str: str]]:
        """ ディレクトリパスから末尾(xsd)で終わるファイルを検索するメソッド。

        Returns:
            list[dict[str: str]]: ファイルパスと文書の種類を格納したリスト。

        Raises:
            ValueError: ディレクトリパスが設定されていない場合。

        Example:
            >>> dir_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData"
            >>> link_manager = BaseLinkManager(dir_path)
            >>> link_manager.search_schema_files()

            [取得したファイルパスと文書の種類のリスト]\n
            [{'document': 'sm', 'path': '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Summary/tse-acedjpsm-****-2024-03-31-01-2024-05-13-ixbrl.htm'},\n
            {'document': 'cf', 'path': '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/0304000-accf01-tse-acedjpfr-*****-2024-03-31-01-2024-05-13-ixbrl.htm'}]
        """
        print("search_schema_files")
        # ディレクトリパスが設定されていない場合はエラーを出力する
        if self.dir_path is None:
            raise ValueError('ディレクトリパスが設定されていません。')

        lists = []
        # ディレクトリパスから末尾(xsd)で終わるファイルを検索
        for file_path, file in self.search_file_path("xsd"):
            if "sm" in file_path:
                lists.append({
                    'document': "sm",
                    'path': file_path
                    })
            elif "fr" in file_path:
                lists.append({
                    'document': "fr",
                    'path': file_path})

        return lists

    def search_file_path(self, search_word:str):
        """ ディレクトリパスからsearch_wordで終わるファイルを検索するメソッド。

        Args:
            search_word (str): 検索する文字列。

        Returns:
            str | None: ファイルパス。

        Example:
            >>> search_word = "ixbrl.htm"
            >>> search_file_path(search_word)

            "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Summary/tse-acedjpsm-****-2024-03-31-01-2024-05-13-ixbrl.htm"
        """
        # ディレクトリパスからsearch_wordで終わるファイルを検索して戻り値として返す
        for root, dirs, files in os.walk(self.dir_path):
            for file in files:
                if file.endswith(search_word):
                    file_path = os.path.join(root, file)
                    yield file_path, file