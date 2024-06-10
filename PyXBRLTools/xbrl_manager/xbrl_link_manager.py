from abc import ABC, abstractmethod
import logging
from xbrl_parser.xml_link_parser import XmlLinkParser
from xbrl_manager.xbrl_path_manager import XbrlPathManager
from log.py_xbrl_tools_loging import PyXBRLToolsLogging

class XbrlLinkType:
    CAL = 'cal'
    DEF = 'def'
    PRE = 'pre'

class BaseXbrlLinkManager(ABC):
    def __init__(self, xbrl_directory_path):
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

        # リンクパスを初期化
        self.__link_path = None

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

    @property
    def xbrl_path_manager(self):
        return self.__xbrl_path_manager

    @property
    def link_path(self):
        return self.__link_path

class XbrlLinkManager(BaseXbrlLinkManager):

    def __init__(self, xbrl_directory_path, link_type = None):
        """ コンストラクタ
        Args:
            xbrl_directory_path (str): xbrlディレクトリのパス
        """
        super().__init__(xbrl_directory_path)
        if link_type is not None:
            # link_typeをXbrlLinkTypeクラスの定数でなければエラー
            if link_type != XbrlLinkType.CAL and link_type != XbrlLinkType.DEF and link_type != XbrlLinkType.PRE:
                self.logger.logger.error('link_typeの値が不正です。')
                raise ValueError('link_typeの値が不正です。')

            self.__link_type = link_type

            # リンクタイプによってリンクパスを設定
            if link_type == XbrlLinkType.CAL:
                self._BaseXbrlLinkManager__link_path = self.xbrl_path_manager.cal_path[0]['file_path']
            elif link_type == XbrlLinkType.DEF:
                self._BaseXbrlLinkManager__link_path = self.xbrl_path_manager.def_path[0]['file_path']
            elif link_type == XbrlLinkType.PRE:
                self._BaseXbrlLinkManager__link_path = self.xbrl_path_manager.pre_path[0]['file_path']
            else:
                self.logger.logger.error('link_typeの値が不正です。')
                raise ValueError('link_typeの値が不正です。')

            # リンクパーサーを設定
            self.__link_parser = XmlLinkParser(self.link_path)

    @property
    def link_type(self):
        return self.__link_type

    @link_type.setter
    def link_type(self, value):
        self.__link_type = value

        # リンクタイプによってリンクパスを設定
        if value == XbrlLinkType.CAL:
            self._BaseXbrlLinkManager__link_path = self.xbrl_path_manager.cal_path[0]['file_path']
        elif value == XbrlLinkType.DEF:
            self._BaseXbrlLinkManager__link_path = self.xbrl_path_manager.def_path[0]['file_path']
        elif value == XbrlLinkType.PRE:
            self._BaseXbrlLinkManager__link_path = self.xbrl_path_manager.pre_path[0]['file_path']
        else:
            self.logger.logger.error('link_typeの値が不正です。')
            raise ValueError('link_typeの値が不正です。')

        # リンクパーサーを設定
        self.__link_parser = XmlLinkParser(self.link_path)

    def get_link_arcs(self, xlink_href: list[str] = None):
        link_arcs = self.__link_parser.link_arcs
        if link_arcs is not None:
            link_arcs = link_arcs[link_arcs['xlink_to'].isin(xlink_href)]
        return self.__link_parser.link_arcs

    def get_link_roles(self):
        return self.__link_parser.link_roles

    def get_link_base(self):
        return self.__link_parser.link_base

    def get_link_locs(self, label_names: list[str] = None):
        link_locs = self.__link_parser.link_arcs
        if label_names is not None:
            link_locs = link_locs[link_locs['xlink_href'].isin(label_names)]
        return link_locs

    def get_selected_link_arcs(self, role_uri):
        return self.__link_parser.get_selected_link_arcs(role_uri)

    def get_selected_link_locs(self, role_uri):
        return self.__link_parser.get_selected_link_locs(role_uri)

# テストコード
if __name__ == "__main__":
    print("Test sample")

    dir_path = "/Users/user/Vscode/python/PyXBRLTools/doc/extract_to_dir/XBRLData"
    link_manager = XbrlLinkManager(dir_path, XbrlLinkManager.LINK_TYPE_CAL)
    print(link_manager.link_path)