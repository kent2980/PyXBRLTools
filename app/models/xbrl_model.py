from app.exception import XbrlListEmptyError
from app.manager import (
    BaseXbrlManager,
    CalLinkManager,
    DefLinkManager,
    IXBRLManager,
    LabelManager,
    PreLinkManager,
)

from .base_xbrl_model import BaseXbrlModel


class XBRLModel(BaseXbrlModel):
    """XBRLファイルを扱うためのクラス"""

    def __init__(self, xbrl_zip_path, output_path) -> None:
        super().__init__(xbrl_zip_path, output_path)
        self.__ixbrl_manager = IXBRLManager(self.directory_path)
        self.__label_manager = self._init_manager(LabelManager)
        self.__cal_link_manager = self._init_manager(CalLinkManager)
        self.__def_link_manager = self._init_manager(DefLinkManager)
        self.__pre_link_manager = self._init_manager(PreLinkManager)

    def _init_manager(self, manager_class: BaseXbrlManager):
        try:
            return manager_class(self.directory_path, self.output_path)
        except XbrlListEmptyError:
            return None

    @property
    def ixbrl_manager(self):
        return self.__ixbrl_manager

    @property
    def label_manager(self):
        return self.__label_manager

    @property
    def cal_link_manager(self):
        return self.__cal_link_manager

    @property
    def def_link_manager(self):
        return self.__def_link_manager

    @property
    def pre_link_manager(self):
        return self.__pre_link_manager

    def __del__(self):
        super().__del__()
        self.__ixbrl_manager = None
        self.__label_manager = None
        self.__cal_link_manager = None
        self.__def_link_manager = None
        self.__pre_link_manager = None

    def get_ixbrl(self):
        return self.ixbrl_manager

    def get_label(self):
        return self.label_manager

    def get_cal_link(self):
        return self.cal_link_manager

    def get_def_link(self):
        return self.def_link_manager

    def get_pre_link(self):
        return self.pre_link_manager

    def get_all_manager(self):
        all_data = {
            "ixbrl": self.get_ixbrl(),
            "label": self.get_label(),
            "cal_link": self.get_cal_link(),
            "def_link": self.get_def_link(),
            "pre_link": self.get_pre_link(),
        }
        # all_dataから値がNoneのものを削除
        return {k: v for k, v in all_data.items() if v is not None}
