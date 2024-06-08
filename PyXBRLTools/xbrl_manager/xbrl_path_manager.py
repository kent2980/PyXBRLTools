from abc import ABC, abstractmethod
import os
from xbrl_parser.xml_schema_parser import XmlSchemaParser

class BaseXbrlPathManager(ABC):
    """
    XBRLディレクトリ内のパスを管理するための基底クラス。

    Attributes:
        xbrl_directory_path (str): XBRLディレクトリへのパス
        _ixbrl_path (list[dict[str, str]]): iXBRLファイルへのパス
        _xsd_path (list[dict[str, str]]): XSDファイルへのパス
        _lab_path (list[dict[str, str]]): LABファイルへのパス
        _cal_path (list[dict[str, str]]): CALファイルへのパス
        _def_path (list[dict[str, str]]): DEFファイルへのパス
        _pre_path (list[dict[str, str]]): PREファイルへのパス
        _schema_parser (XmlSchemaParser): XMLスキーマパーサ

    Properties:
        ixbrl_path (list[dict[str, str]]): iXBRLファイルへのパス
        xsd_path (list[dict[str, str]]): XSDファイルへのパス
        lab_path (list[dict[str, str]]): LABファイルへのパス
        cal_path (list[dict[str, str]]): CALファイルへのパス
        def_path (list[dict[str, str]]): DEFファイルへのパス
        pre_path (list[dict[str, str]]): PREファイルへのパス

    Methods:
        __init__: 初期化メソッド
    """
    def __init__(self, xbrl_directory_path):
        """
        BaseXbrlPathManagerをディレクトリパスで初期化します。

        :param xbrl_directory_path: XBRLディレクトリへのパス
        :type xbrl_directory_path: str
        """
        # ディレクトリパスが有効かどうかを確認
        if not os.path.isdir(xbrl_directory_path):
            raise ValueError(f"{xbrl_directory_path}は有効なディレクトリパスではありません")

        # ディレクトリパスをインスタンス変数に格納
        self.xbrl_directory_path = xbrl_directory_path

        # iXBRLファイルへのパスを初期化
        self._ixbrl_path = None
        self._xsd_path = None
        self._lab_path = None
        self._cal_path = None
        self._def_path = None
        self._pre_path = None

        # パーサーを初期化
        self._schema_parser = XmlSchemaParser()

    @property
    @abstractmethod
    def ixbrl_path(self):
        """
        iXBRLファイルへのパスを取得するための抽象メソッド。
        """
        pass

    @property
    @abstractmethod
    def xsd_path(self):
        """
        XSDファイルへのパスを取得するための抽象メソッド。
        """
        pass

    @property
    @abstractmethod
    def lab_path(self):
        """
        LABファイルへのパスを取得するための抽象メソッド。
        """
        pass

    @property
    @abstractmethod
    def cal_path(self):
        """
        CALファイルへのパスを取得するための抽象メソッド。
        """
        pass

    @property
    @abstractmethod
    def def_path(self):
        """
        DEFファイルへのパスを取得するための抽象メソッド。
        """
        pass

    @property
    @abstractmethod
    def pre_path(self):
        """
        PREファイルへのパスを取得するための抽象メソッド。
        """
        pass

class XbrlPathManager(BaseXbrlPathManager):
    """
    XBRLディレクトリ内のパスを管理するためのクラス。

    Attributes:
        xbrl_directory_path (str): XBRLディレクトリへのパス

    Properties:
        ixbrl_path (list[dict[str, str]]): iXBRLファイルへのパス
        xsd_path (list[dict[str, str]]): XSDファイルへのパス
        lab_path (list[dict[str, str]]): LABファイルへのパス
        cal_path (list[dict[str, str]]): CALファイルへのパス
        def_path (list[dict[str, str]]): DEFファイルへのパス
        pre_path (list[dict[str, str]]): PREファイルへのパス

    Methods:
        __search_file: XBRLディレクトリ内で指定された拡張子のファイルを検索するメソッド
        __select_search_file: XBRLディレクトリ内で指定されたファイル名を検索するメソッド
    """

    @property
    def ixbrl_path(self) -> list[dict[str, str]]:
        """
        iXBRLファイルへのパスを取得します。

        Returns:
            list[dict[str, str]]: iXBRLファイルへのパス

        Example:
            [
                {
                    'document': 'sm',
                    'file_path': '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/ixbrl.htm'
                },
                {
                    'document': 'fr',
                    'file_path': '/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/ixbrl.htm'
                }
            ]
        """
        if self._ixbrl_path is not None:
            return self._ixbrl_path
        else:
            lists = []
            for file_path, file_name in self.__search_file("ixbrl.htm"):
                if "sm" in file_name:
                    lists.append({
                        'document': 'sm',
                        'file_path': file_path
                    })
                elif "fr" in file_name:
                    lists.append({
                        'document': file_name.split("-")[1][2:4],
                        'file_path': file_path
                    })

            self._ixbrl_path = lists

            return self._ixbrl_path

    @property
    def xsd_path(self) -> list[dict[str, str]]:
        """
        XSDファイルへのパスを取得します。

        :return: XSDファイルへのパス
        :rtype: str
        """
        if self._xsd_path is not None:
            return self._xsd_path
        else:
            lists = []
            for file_path, file_name in self.__search_file("xsd"):
                if "sm" in file_name:
                    lists.append({
                        'document': 'sm',
                        'file_path': file_path
                    })
                elif "fr" in file_name:
                    lists.append({
                        'document': "fr",
                        'file_path': file_path
                    })

            self._xsd_path = lists

            return self._xsd_path

    @property
    def lab_path(self):
        """
        LABファイルへのパスを取得します。

        :return: LABファイルへのパス
        :rtype: str
        """
        if self._lab_path is not None:
            return self._lab_path
        else:
            lists = []
            xsd_paths = self.xsd_path
            for xsd_path in xsd_paths:
                self._schema_parser.file_path = xsd_path["file_path"]
                link_base_refs = self._schema_parser.link_base_refs
                for index, row in link_base_refs.iterrows():
                    if row["xlink_role"] == "http://www.xbrl.org/2003/role/labelLinkbaseRef":
                        file_path = row["xlink_href"]
                        path_type = "global"
                        if "http" not in file_path:
                            file_path = self.__select_search_file(file_path)
                            path_type = "local"
                        if xsd_path["document"] == "sm":
                            lists.append({
                                'document': 'sm',
                                'path_type': path_type,
                                'file_path': file_path
                            })
                        elif xsd_path["document"] == "fr":
                            lists.append({
                                'document': 'fr',
                                'path_type': path_type,
                                'file_path': file_path
                            })

            self._lab_path = lists

            return self._lab_path

    @property
    def cal_path(self):
        """
        CALファイルへのパスを取得します。

        :return: CALファイルへのパス
        :rtype: str
        """
        if self._cal_path is not None:
            return self._cal_path
        else:
            lists = []
            xsd_paths = self.xsd_path
            for xsd_path in xsd_paths:
                self._schema_parser.file_path = xsd_path["file_path"]
                link_base_refs = self._schema_parser.link_base_refs
                for index, row in link_base_refs.iterrows():
                    if row["xlink_role"] == "http://www.xbrl.org/2003/role/calculationLinkbaseRef":
                        file_path = row["xlink_href"]
                        path_type = "global"
                        if "http" not in file_path:
                            file_path = self.__select_search_file(file_path)
                            path_type = "local"
                        if xsd_path["document"] == "sm":
                            lists.append({
                                'document': 'sm',
                                'path_type': path_type,
                                'file_path': file_path
                            })
                        elif xsd_path["document"] == "fr":
                            lists.append({
                                'document': 'fr',
                                'path_type': path_type,
                                'file_path': file_path
                            })

            self._cal_path = lists

            return self._cal_path

    @property
    def def_path(self):
        """
        DEFファイルへのパスを取得します。

        :return: DEFファイルへのパス
        :rtype: str
        """
        if self._def_path is not None:
            return self._def_path
        else:
            lists = []
            xsd_paths = self.xsd_path
            for xsd_path in xsd_paths:
                self._schema_parser.file_path = xsd_path["file_path"]
                link_base_refs = self._schema_parser.link_base_refs
                for index, row in link_base_refs.iterrows():
                    if row["xlink_role"] == "http://www.xbrl.org/2003/role/definitionLinkbaseRef":
                        file_path = row["xlink_href"]
                        path_type = "global"
                        if "http" not in file_path:
                            file_path = self.__select_search_file(file_path)
                            path_type = "local"
                        if xsd_path["document"] == "sm":
                            lists.append({
                                'document': 'sm',
                                'path_type': path_type,
                                'file_path': file_path
                            })
                        elif xsd_path["document"] == "fr":
                            lists.append({
                                'document': 'fr',
                                'path_type': path_type,
                                'file_path': file_path
                            })

            self._def_path = lists

            return self._def_path

    @property
    def pre_path(self):
        """
        PREファイルへのパスを取得します。

        :return: PREファイルへのパス
        :rtype: str
        """
        if self._pre_path is not None:
            return self._pre_path
        else:
            lists = []
            xsd_paths = self.xsd_path
            for xsd_path in xsd_paths:
                self._schema_parser.file_path = xsd_path["file_path"]
                link_base_refs = self._schema_parser.link_base_refs
                for index, row in link_base_refs.iterrows():
                    if row["xlink_role"] == "http://www.xbrl.org/2003/role/presentationLinkbaseRef":
                        file_path = row["xlink_href"]
                        path_type = "global"
                        if "http" not in file_path:
                            file_path = self.__select_search_file(file_path)
                            path_type = "local"
                        if xsd_path["document"] == "sm":
                            lists.append({
                                'document': 'sm',
                                'path_type': path_type,
                                'file_path': file_path
                            })
                        elif xsd_path["document"] == "fr":
                            lists.append({
                                'document': 'fr',
                                'path_type': path_type,
                                'file_path': file_path
                            })

            self._pre_path = lists

            return self._pre_path

    def __search_file(self, file_extension) -> tuple[str, str]:
        """
        XBRLディレクトリ内で指定された拡張子のファイルを検索します。

        :param file_extension: 検索するファイルの拡張子
        :type file_extension: str
        :return: 検索されたファイルのパス
        :rtype: str
        """
        # XBRLディレクトリ内のファイルを検索
        for root, _, files in os.walk(self.xbrl_directory_path):
            for file in files:
                if file.endswith(file_extension):
                    yield os.path.join(root, file), file
        return None

    def __select_search_file(self, file_name:str) -> str:
        """
        XBRLディレクトリ内で指定されたファイル名を検索します。

        :param file_name: 検索するファイル名
        :type file_name: str
        :return: 検索されたファイルのパス
        :rtype: str
        """
        # XBRLディレクトリ内のファイルを検索
        for root, _, files in os.walk(self.xbrl_directory_path):
            for file in files:
                if file == file_name:
                    return os.path.join(root, file)
        return None
