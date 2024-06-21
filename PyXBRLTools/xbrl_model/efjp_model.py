from PyXBRLTools.xbrl_model.base_xbrl_model import BaseXbrlModel
from PyXBRLTools.xbrl_exception.xbrl_model_exception import NotXbrlTypeException

class EfjpModel(BaseXbrlModel):
    """ ETF決算短信(日本基準)のXBRLファイルを扱うクラス """
    def __init__(self, xbrl_zip_path) -> None:
        super().__init__(xbrl_zip_path)
        if self.xbrl_type != "efjp":
            raise NotXbrlTypeException("XBRLファイルの種類が異なります。")