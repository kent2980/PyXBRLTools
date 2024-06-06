from xbrl_manager.base_xbrl_manager import BaseXbrlManager
from xbrl_parser.xml_link_parser import XmlLinkParser
from abc import abstractmethod
import os

class BaseLinkManager(BaseXbrlManager):
    """ linkファイルの情報を取得するクラス。

    Args:
        BaseXbrlManager (class): XBRLデータの基底クラス。

    Attributes:
        link_path (str): linkファイルのパス。
        link_parser (XmlLinkParser): linkファイルのパーサ。

    Properties:
        link_path (str): linkファイルのパスを取得するプロパティ。
        link_parser (XmlLinkParser): linkファイルのパーサを取得するプロパティ。

    Methods:
        _get_link_path: linkファイルのパスを取得する抽象メソッド。
        _search_link_path: linkファイルのパスを検索するメソッド。
    """

    def __init__(self, dir_path: str):
        """ コンストラクタ """
        super().__init__(dir_path)
        self.__link_path = self._get_link_path()
        self.__link_parser = XmlLinkParser(self.link_path)

    @property
    def link_path(self):
        """ linkファイルのパスを取得するプロパティ。"""
        return self.__link_path

    @property
    def link_parser(self):
        """ linkファイルのパーサを取得するプロパティ。"""
        return self.__link_parser

    @abstractmethod
    def _get_link_path(self):
        """ linkファイルのパスを取得する抽象メソッド。"""
        pass

    def _search_link_path(self, search_word: str) -> str | None:
        """ linkファイルのパスを検索するメソッド。

        Args:
            search_word (str): 検索する文字列。

        Returns:
            str | None: linkファイルのパス。

        Examples:
            >>> _search_link_path("cal.xml")
            "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/tse-acedjpfr-57210-2024-03-31-01-2024-05-13-cal.xml"
        """
        # ディレクトリパスからsearch_wordで終わるファイルを検索して戻り値として返す
        for root, dirs, files in os.walk(self.dir_path):
            for file in files:
                if file.endswith(search_word):
                    file_path = os.path.join(root, file)
                    return file_path

class CalLinkManager(BaseLinkManager):
    """ cal.xmlファイルの情報を取得するクラス。

    Args:
        BaseLinkManager (class): linkファイルの基底クラス。

    Attributes:
        link_path (str): cal.xmlファイルのパス。
        link_parser (XmlLinkParser): cal.xmlファイルのパーサ。

    Properties:
        link_path (str): cal.xmlファイルのパスを取得するプロパティ。
        link_parser (XmlLinkParser): cal.xmlファイルのパーサを取得するプロパティ。

    Methods:
        _get_link_path: cal.xmlファイルのパスを取得するメソッド。
    """

    def _get_link_path(self) -> str | None:
        """ cal.xmlファイルのパスを取得するメソッド。

        Returns:
            str | None: cal.xmlファイルのパス。

        Examples:
            >>> _get_link_path()
            "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/tse-acedjpfr-57210-2024-03-31-01-2024-05-13-cal.xml"
        """
        # ディレクトリパスからcal.xmlで終わるファイルを検索して戻り値として返す
        return self._search_link_path("cal.xml")

class DefLinkManager(BaseLinkManager):
    """ def.xmlファイルの情報を取得するクラス。

    Args:
        BaseLinkManager (class): linkファイルの基底クラス。

    Attributes:
        link_path (str): def.xmlファイルのパス。
        link_parser (XmlLinkParser): def.xmlファイルのパーサ。

    Properties:
        link_path (str): def.xmlファイルのパスを取得するプロパティ。
        link_parser (XmlLinkParser): def.xmlファイルのパーサを取得するプロパティ。

    Methods:
        _get_link_path: def.xmlファイルのパスを取得するメソッド。
    """

    def _get_link_path(self) -> str | None:
        """ def.xmlファイルのパスを取得するメソッド。

        Args:
            search_word (str): 検索する文字列。

        Returns:
            str | None: def.xmlファイルのパス。

        Examples:
            >>> _get_link_path()
            "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/tse-acedjpfr-57210-2024-03-31-01-2024-05-13-def.xml"
        """
        # ディレクトリパスからdef.xmlで終わるファイルを検索して戻り値として返す
        return self._search_link_path("def.xml")

class PreLinkManager(BaseLinkManager):
    """ pre.xmlファイルの情報を取得するクラス。

    Args:
        BaseLinkManager (class): linkファイルの基底クラス。

    Attributes:
        link_path (str): pre.xmlファイルのパス。
        link_parser (XmlLinkParser): pre.xmlファイルのパーサ。

    Properties:
        link_path (str): pre.xmlファイルのパスを取得するプロパティ。
        link_parser (XmlLinkParser): pre.xmlファイルのパーサを取得するプロパティ。

    Methods:
        _get_link_path: pre.xmlファイルのパスを取得するメソッド。
    """

    def _get_link_path(self) -> str | None:
        """ pre.xmlファイルのパスを取得するメソッド。

        Args:
            search_word (str): 検索する文字列。

        Returns:
            str | None: pre.xmlファイルのパス。

        Examples:
            >>> _get_link_path()
            "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData/Attachment/tse-acedjpfr-57210-2024-03-31-01-2024-05-13-pre.xml"
        """
        # ディレクトリパスからpre.xmlで終わるファイルを検索して戻り値として返す
        return self._search_link_path("pre.xml")
