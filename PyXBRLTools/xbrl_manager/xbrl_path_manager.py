from abc import ABC, abstractmethod
import os

class BaseXbrlPathManager(ABC):
    def __init__(self, xbrl_directory_path):
        if not os.path.isdir(xbrl_directory_path):
            raise ValueError(f"{xbrl_directory_path} is not a valid directory path")
        self.xbrl_directory_path = xbrl_directory_path
        self.ixbrl_path = None
        self.xsd_path = None
        self.lab_path = None
        self.cal_path = None
        self.def_path = None
        self.pre_path = None

    @abstractmethod
    def get_ixbrl_path(self):
        pass

    @abstractmethod
    def get_xsd_path(self):
        pass

    @abstractmethod
    def get_lab_path(self):
        pass

    @abstractmethod
    def get_cal_path(self):
        pass

    @abstractmethod
    def get_def_path(self):
        pass

    @abstractmethod
    def get_pre_path(self):
        pass