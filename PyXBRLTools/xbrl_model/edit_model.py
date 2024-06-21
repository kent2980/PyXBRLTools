from PyXBRLTools.xbrl_model.base_xbrl_model import BaseXbrlModel
from PyXBRLTools.xbrl_exception.xbrl_model_exception import NotXbrlTypeException

class EditModel(BaseXbrlModel):
    """ 決算短信(国際会計基準) ※IFRSタクソノミを利用する場合のXBRLファイルを扱うクラス"""
    def __init__(self, xbrl_zip_path) -> None:
        super().__init__(xbrl_zip_path)
        if self.xbrl_type != "edit":
            raise NotXbrlTypeException("XBRLファイルの種類が異なります。")