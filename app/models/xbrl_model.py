from app.exception import XbrlListEmptyError
from app.manager import (BaseXbrlManager, CalLinkManager, DefLinkManager,
                         IXBRLManager, LabelManager, PreLinkManager)

from .base_xbrl_model import BaseXbrlModel


class XBRLModel(BaseXbrlModel):
    """XBRLファイルを扱うためのクラス"""

    def __init__(self, xbrl_zip_path, output_path) -> None:
        super().__init__(xbrl_zip_path, output_path)
        self.__ixbrl_manager = IXBRLManager(self.directory_path)
        self.__label_manager = self._initialize_manager(
            LabelManager, output_path
        )
        self.__cal_link_manager = self._initialize_manager(
            CalLinkManager, output_path
        )
        self.__def_link_manager = self._initialize_manager(
            DefLinkManager, output_path
        )
        self.__pre_link_manager = self._initialize_manager(
            PreLinkManager, output_path
        )

    def _initialize_manager(
        self, manager_class: BaseXbrlManager, output_path
    ):
        try:
            return manager_class(self.directory_path, output_path)
        except XbrlListEmptyError:
            return None

    @property
    def ixbrl_manager(self):
        if self.__ixbrl_manager is None:
            raise XbrlListEmptyError(
                "ixbrlファイルが見つかりません。"
            )
        else:
            return self.__ixbrl_manager

    @property
    def label_manager(self):
        if self.__label_manager is None:
            raise XbrlListEmptyError(
                "labelLinkbaseファイルが見つかりません。"
            )
        else:
            return self.__label_manager

    @property
    def cal_link_manager(self):
        if self.__cal_link_manager is None:
            raise XbrlListEmptyError(
                "calculationLinkbaseファイルが見つかりません。"
            )
        else:
            return self.__cal_link_manager

    @property
    def def_link_manager(self):
        if self.__def_link_manager is None:
            raise XbrlListEmptyError(
                "definitionLinkbaseファイルが見つかりません。"
            )
        else:
            return self.__def_link_manager

    @property
    def pre_link_manager(self):
        if self.__pre_link_manager is None:
            raise XbrlListEmptyError(
                "presentationLinkbaseファイルが見つかりません。"
            )
        else:
            return self.__pre_link_manager

    def __del__(self):
        super().__del__()
        self.__ixbrl_manager = None
        self.__label_manager = None
        self.__cal_link_manager = None
        self.__def_link_manager = None
        self.__pre_link_manager = None
