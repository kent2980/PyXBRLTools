from abc import ABC, abstractmethod
import os

class BaseXbrlPathManager(ABC):
    """
    XBRLディレクトリ内のパスを管理するための基底クラス。
    """
    def __init__(self, xbrl_directory_path):
        """
        BaseXbrlPathManagerをディレクトリパスで初期化します。

        :param xbrl_directory_path: XBRLディレクトリへのパス
        :type xbrl_directory_path: str
        """
        if not os.path.isdir(xbrl_directory_path):
            raise ValueError(f"{xbrl_directory_path}は有効なディレクトリパスではありません")
        self.xbrl_directory_path = xbrl_directory_path
        self.ixbrl_path = None
        self.xsd_path = None
        self.lab_path = None
        self.cal_path = None
        self.def_path = None
        self.pre_path = None

    @abstractmethod
    def get_ixbrl_path(self):
        """
        iXBRLファイルへのパスを取得するための抽象メソッド。
        """
        pass

    @abstractmethod
    def get_xsd_path(self):
        """
        XSDファイルへのパスを取得するための抽象メソッド。
        """
        pass

    @abstractmethod
    def get_lab_path(self):
        """
        LABファイルへのパスを取得するための抽象メソッド。
        """
        pass

    @abstractmethod
    def get_cal_path(self):
        """
        CALファイルへのパスを取得するための抽象メソッド。
        """
        pass

    @abstractmethod
    def get_def_path(self):
        """
        DEFファイルへのパスを取得するための抽象メソッド。
        """
        pass

    @abstractmethod
    def get_pre_path(self):
        """
        PREファイルへのパスを取得するための抽象メソッド。
        """
        pass