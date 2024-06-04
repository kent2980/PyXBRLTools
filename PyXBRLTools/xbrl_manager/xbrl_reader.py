from exceptions import *
from utils import Utils
from label_manager import LabelManager
from link_managers import CalculationLinkManager, DefinitionLinkManager, PresentationLinkManager


class XbrlRead:
    def __init__(self, xbrl_zip_path: str = None):
        ...

    def get_company_code(self):
        ...

    def company_explain_df(self):
        ...

    def to_dataframe(self):
        ...

    # add_label_df() の中身は LabelManager を使用するように変更
    def add_label_df(self):
        ...

    # to_cal_link_df() の中身は CalculationLinkManager を使用するように変更
    def to_cal_link_df(self):
        ...

    # to_def_link_df() の中身は DefinitionLinkManager を使用するように変更
    def to_def_link_df(self):
        ...

    # to_pre_link_df() の中身は PresentationLinkManager を使用するように変更
    def to_pre_link_df(self):
        ...