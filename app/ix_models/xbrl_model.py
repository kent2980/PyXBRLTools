from app.exception import XbrlListEmptyError
from app.ix_manager import (
    BaseXbrlManager,
    CalLinkManager,
    DefLinkManager,
    IXBRLManager,
    LabelManager,
    PreLinkManager,
    QualitativeManager,
    SchemaManager,
)

from .base_xbrl_model import BaseXbrlModel


class XBRLModel(BaseXbrlModel):
    """XBRLファイルを扱うためのクラス"""

    def __init__(self, xbrl_zip_path, output_path) -> None:
        super().__init__(xbrl_zip_path, output_path)
        self.__ixbrl_manager: IXBRLManager = IXBRLManager(
            self.directory_path, xbrl_id=self.xbrl_id
        )
        self.__label_manager = self._init_manager(LabelManager)
        self.__cal_link_manager = self._init_manager(CalLinkManager)
        self.__def_link_manager = self._init_manager(DefLinkManager)
        self.__pre_link_manager = self._init_manager(PreLinkManager)
        self.__schema_manager: SchemaManager = SchemaManager(
            self.directory_path, xbrl_id=self.xbrl_id
        )
        self.__qualitative_manager = QualitativeManager(
            self.directory_path, xbrl_id=self.xbrl_id
        )

    def _init_manager(self, manager_class: BaseXbrlManager):
        try:
            return manager_class(
                self.directory_path, self.output_path, xbrl_id=self.xbrl_id
            )
        except XbrlListEmptyError as e:
            # print(e)
            pass

    @property
    def schema_manager(self):
        return self.__schema_manager

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

    @property
    def qualitative_manager(self):
        return self.__qualitative_manager

    def __del__(self):
        super().__del__()
        self.__ixbrl_manager = None
        self.__label_manager = None
        self.__cal_link_manager = None
        self.__def_link_manager = None
        self.__pre_link_manager = None
        self.__schema_manager = None
        self.__qualitative_manager = None

    def get_schema(self):
        return self.schema_manager

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

    def get_qualitative(self):
        return self.qualitative_manager

    def get_all_manager(self):
        all_data = {
            "ix": self.get_ixbrl(),
            "lab": self.get_label(),
            "cal": self.get_cal_link(),
            "def": self.get_def_link(),
            "pre": self.get_pre_link(),
            "schema": self.get_schema(),
            "qualitative": self.get_qualitative(),
        }
        # all_dataから値がNoneのものを削除
        return {k: v for k, v in all_data.items() if v is not None}

    def ixbrl_roles(self):
        for value in self.ixbrl_manager.ixbrl_roles():
            yield value

    def get_all_items(self):
        lists = []
        for _, manager in self.get_all_manager().items():
            for item in manager.items:
                # listsとitemsを結合
                lists.append(item)

        return lists

    def ix_header(self):
        return self.ixbrl_manager.ix_header

    def __str__(self) -> str:

        header = self.ix_header().__dict__

        return f" - [{header['securities_code']}] \
            {header['company_name']} <{header['document_name']}>"
