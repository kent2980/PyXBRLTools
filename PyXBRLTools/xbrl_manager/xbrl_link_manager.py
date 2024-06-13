from abc import ABC, abstractmethod
import logging
from pandas import DataFrame
import pandas as pd
from xbrl_parser.xml_link_parser import XmlLinkParser
from xbrl_manager.xbrl_path_manager import XbrlPathManager
from log.py_xbrl_tools_loging import PyXBRLToolsLogging
from xbrl_manager.xbrl_download_manager import XBRLDownloadManager

class XbrlLinkType:
    CAL = 'cal'
    DEF = 'def'
    PRE = 'pre'

class BaseXbrlLinkManager(ABC):
    def __init__(self, xbrl_directory_path, load_link_directory):
        # ログ設定
        class_name = self.__class__.__name__
        self.logger = PyXBRLToolsLogging(log_level=logging.DEBUG)
        self.logger.set_log_file(f'Log/{class_name}.log')

        # XBRLディレクトリのパスを設定
        self.__xbrl_directory_path = xbrl_directory_path

        # XBRLディレクトリマネージャを設定
        try:
            self.__xbrl_path_manager = XbrlPathManager(xbrl_directory_path)
        except ValueError as e:
            self.logger.logger.error(f"エラーが発生しました。[{e}]")
            raise ValueError(f"エラーが発生しました。[{e}]")

        # Linkファイルをダウンロードするローカルディレクトリのパスを設定
        self.__load_link_directory = load_link_directory

        # ダウンロードマネージャーを設定
        self.__xbrl_download_manager = XBRLDownloadManager(load_link_directory)

        # リンクパスを初期化
        self.__link_path = None

        # プロパティを初期化
        self.__link_arcs = None
        self.__link_roles = None
        self.__link_base = None
        self.__link_locs = None

    @property
    def xbrl_directory_path(self):
        return self.__xbrl_directory_path

    @xbrl_directory_path.setter
    def xbrl_directory_path(self, value):
        self.__xbrl_directory_path = value

        try:
            self.__xbrl_path_manager = XbrlPathManager(value)
        except ValueError as e:
            self.logger.logger.error(f"エラーが発生しました。[{e}]")
            raise ValueError(f"エラーが発生しました。[{e}]")

        # プロパティを初期化
        self.__link_arcs = None
        self.__link_roles = None
        self.__link_base = None
        self.__link_locs = None
    @property
    def load_link_directory(self):
        return self.__load_link_directory

    @load_link_directory.setter
    def load_link_directory(self, value):
        # 保存ディレクトリを設定
        self.__load_link_directory = value
        # ダウンロードマネージャーの保存ディレクトリを設定
        self.xbrl_download_manager.Xbrl_save_dir = value

    @property
    def xbrl_path_manager(self):
        return self.__xbrl_path_manager

    @property
    def xbrl_download_manager(self):
        return self.__xbrl_download_manager

    @property
    def link_path(self):
        return self.__link_path

    @link_path.setter
    def link_path(self, value):
        self.__link_path = value

    @property
    @abstractmethod
    def link_arcs(self):
        pass

    @property
    @abstractmethod
    def link_roles(self):
        pass

    @property
    @abstractmethod
    def link_base(self):
        pass

    @property
    @abstractmethod
    def link_locs(self):
        pass

class XbrlLinkManager(BaseXbrlLinkManager):
    """XBRLリンクマネージャークラス

    XBRLファイルのリンク情報を管理するクラスです。

    Attributes:
        xbrl_directory_path (str): XBRLディレクトリのパス
        link_type (XbrlLinkType): リンクタイプ
        link_parser (XmlLinkParser): リンクパーサー
    """

    def __init__(self, xbrl_directory_path, load_link_directory, link_type = None):
        """コンストラクタ

        Args:
            xbrl_directory_path (str): XBRLディレクトリのパス
            link_type (XbrlLinkType, optional): リンクタイプ
        """
        super().__init__(xbrl_directory_path, load_link_directory)
        if link_type is not None:
            # link_typeをXbrlLinkTypeクラスの定数でなければエラー
            if link_type != XbrlLinkType.CAL and link_type != XbrlLinkType.DEF and link_type != XbrlLinkType.PRE:
                self.logger.logger.error('link_typeの値が不正です。')
                raise ValueError('link_typeの値が不正です。')

            self.__link_type = link_type

            # 計算リンクの場合
            if link_type == XbrlLinkType.CAL:
                self.link_path = DataFrame(self.xbrl_path_manager.cal_path)
            # 定義リンクの場合
            elif link_type == XbrlLinkType.DEF:
                self.link_path = DataFrame(self.xbrl_path_manager.def_path)
            # 表示リンクの場合
            elif link_type == XbrlLinkType.PRE:
                self.link_path = DataFrame(self.xbrl_path_manager.pre_path)
            # それ以外の場合
            else:
                self.logger.logger.error('link_typeの値が不正です。')
                raise ValueError('link_typeの値が不正です。')

            # リンクファイルをローカルにダウンロード
            self.link_path = self.__load_link_files(self.link_path)

        # リンクパーサーを設定
        self.__link_parser = XmlLinkParser()

    def __load_link_files(self, link_path: DataFrame) -> DataFrame:

        # ローカルにリンクファイルをダウンロード
        for url_path, local_path in self.xbrl_download_manager.load_xbrl_files_from_list(link_path['file_path'].to_list()):
            link_path['file_path'] = link_path['file_path'].replace(url_path, local_path)

        # link_pathのpath_typeをlocalに変更
        link_path['path_type'] = 'local'

        return link_path

    @property
    def link_parser(self):
        return self.__link_parser

    @property
    def link_type(self):
        """リンクタイプを取得します。

        Returns:
            XbrlLinkType: リンクタイプ
        """
        return self.__link_type

    @link_type.setter
    def link_type(self, value):
        """リンクタイプを設定します。

        Args:
            value (XbrlLinkType): リンクタイプ
        """
        self.__link_type = value

        # プロパティを初期化
        self._BaseXbrlLinkManager__link_arcs = None
        self._BaseXbrlLinkManager__link_roles = None
        self._BaseXbrlLinkManager__link_base = None
        self._BaseXbrlLinkManager__link_locs = None

        # リンクタイプによってリンクパスを設定
        if value == XbrlLinkType.CAL:
            self.link_path = DataFrame(self.xbrl_path_manager.cal_path)
        # 定義リンクの場合
        elif value == XbrlLinkType.DEF:
            self.link_path = DataFrame(self.xbrl_path_manager.def_path)
        # 表示リンクの場合
        elif value == XbrlLinkType.PRE:
            self.link_path = DataFrame(self.xbrl_path_manager.pre_path)
        else:
            self.logger.logger.error('link_typeの値が不正です。')
            raise ValueError('link_typeの値が不正です。')

        # リンクファイルをローカルにダウンロード
        self.link_path = self.__load_link_files(self.link_path)

    @property
    def link_arcs(self):
        """指定されたxlink_hrefに一致するリンクアークを取得します。

        Args:
            xlink_href (list[str], optional): 取得するリンクアークのxlink_hrefリスト

        Returns:
            pd.DataFrame: リンクアークのデータフレーム
        """
        if self._BaseXbrlLinkManager__link_arcs is not None:
            return self._BaseXbrlLinkManager__link_arcs

        link_arcs = None
        for index, row in self.link_path.iterrows():
            self.link_parser.file_path = row['file_path']
            if link_arcs is None:
                link_arcs = self.__link_parser.link_arcs
            else:
                link_arcs = pd.concat([link_arcs, self.link_parser.link_arcs])

        self._BaseXbrlLinkManager__link_arcs = link_arcs.drop_duplicates()

        return self._BaseXbrlLinkManager__link_arcs

    @property
    def link_roles(self):
        """リンクロールを取得します。

        Returns:
            list[str]: リンクロールのリスト
        """
        if self._BaseXbrlLinkManager__link_roles is not None:
            return self._BaseXbrlLinkManager__link_roles

        link_roles = None
        for index, row in self.link_path.iterrows():
            self.link_parser.file_path = row['file_path']
            if link_roles is None:
                link_roles = self.__link_parser.link_roles
            else:
                link_roles = pd.concat([link_roles, self.link_parser.link_roles])

        self._BaseXbrlLinkManager__link_roles = link_roles.drop_duplicates()

        return self._BaseXbrlLinkManager__link_roles

    @property
    def link_base(self):
        """リンクベースを取得します。

        Returns:
            str: リンクベース
        """
        if self._BaseXbrlLinkManager__link_base is not None:
            return self._BaseXbrlLinkManager__link_base

        link_base = None
        for index, row in self.link_path.iterrows():
            self.link_parser.file_path = row['file_path']
            if link_base is None:
                link_base = self.__link_parser.link_base
            else:
                link_base = pd.concat([link_base, self.link_parser.link_base])

        self._BaseXbrlLinkManager__link_base = link_base.drop_duplicates()

        return self._BaseXbrlLinkManager__link_base

    @property
    def link_locs(self):
        """指定されたlabel_namesに一致するリンクロケーションを取得します。

        Args:
            label_names (list[str], optional): 取得するリンクロケーションのlabel_namesリスト

        Returns:
            pd.DataFrame: リンクロケーションのデータフレーム
        """
        if self._BaseXbrlLinkManager__link_locs is not None:
            return self._BaseXbrlLinkManager__link_locs

        link_locs = None
        for index, row in self.link_path.iterrows():
            self.link_parser.file_path = row['file_path']
            if link_locs is None:
                link_locs = self.__link_parser.link_locs
            else:
                link_locs = pd.concat([link_locs, self.link_parser.link_locs])

        self._BaseXbrlLinkManager__link_locs = link_locs.drop_duplicates()

        return self._BaseXbrlLinkManager__link_locs

    def get_selected_link_arcs(self, role_uri):
        """指定されたrole_uriに一致する選択されたリンクアークを取得します。

        Args:
            role_uri (str): 取得するリンクアークのrole_uri

        Returns:
            pd.DataFrame: 選択されたリンクアークのデータフレーム
        """
        return self.__link_parser.get_selected_link_arcs(role_uri).drop_duplicates()

    def get_selected_link_locs(self, role_uri):
        """指定されたrole_uriに一致する選択されたリンクロケーションを取得します。

        Args:
            role_uri (str): 取得するリンクロケーションのrole_uri

        Returns:
            pd.DataFrame: 選択されたリンクロケーションのデータフレーム
        """
        return self.__link_parser.get_selected_link_locs(role_uri).drop_duplicates()

# テストコード
if __name__ == "__main__":
    print("Test sample")

    dir_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData"
    # link_manager = XbrlLinkManager(dir_path, XbrlLinkManager.LINK_TYPE_CAL)
    # print(link_manager.link_path)