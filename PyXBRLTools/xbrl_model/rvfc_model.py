from PyXBRLTools.xbrl_model.base_xbrl_model import BaseXbrlModel
from PyXBRLTools.xbrl_exception.xbrl_model_exception import NotXbrlTypeException

class RvfcModel(BaseXbrlModel):
    """ 業績予想修正に関するお知らせのXBRLファイルを扱うクラス """
    def __init__(self, xbrl_zip_path) -> None:
        super().__init__(xbrl_zip_path)
        if self.xbrl_type != "rvfc":
            raise NotXbrlTypeException("XBRLファイルの種類が異なります。")