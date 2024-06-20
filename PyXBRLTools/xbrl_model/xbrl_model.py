from PyXBRLTools.xbrl_model.base_xbrl_model import BaseXbrlModel

class XbrlEdjpModel(BaseXbrlModel):
    """ 決算短信(日本基準)のXBRLファイルを扱うクラス """
    def __init__(self, xbrl_zip_path) -> None:
        super().__init__(xbrl_zip_path)
        if self.xbrl_type != "edjp":
            raise Exception("XBRLファイルの種類が異なります。")

class XbrlEdusModel(BaseXbrlModel):
    """ 決算短信(米国基準)のXBRLファイルを扱うクラス """
    def __init__(self, xbrl_zip_path) -> None:
        super().__init__(xbrl_zip_path)
        if self.xbrl_type != "edus":
            raise Exception("XBRLファイルの種類が異なります。")

class XbrlEdifModel(BaseXbrlModel):
    """ 決算短信(国際会計基準)のXBRLファイルを扱うクラス """
    pass

class XbrlEditModel(BaseXbrlModel):
    """ 決算短信(国際会計基準) ※IFRSタクソノミを利用する場合のXBRLファイルを扱うクラス"""
    pass

class XbrlRvdfModel(BaseXbrlModel):
    """ 配当予想修正に関するお知らせのXBRLファイルを扱うクラス """
    pass

class XbrlRvfcModel(BaseXbrlModel):
    """ 業績予想修正に関するお知らせのXBRLファイルを扱うクラス """
    pass

class XbrlRejpModel(BaseXbrlModel):
    """ REIT決算短信(日本基準)のXBRLファイルを扱うクラス """
    pass

class XbrlRrdfModel(BaseXbrlModel):
    """ 分配予想の修正に関するお知らせのXBRLファイルを扱うクラス """
    pass

class XbrlRrfcModel(BaseXbrlModel):
    """ 運用状況の予想の修正に関するお知らせのXBRLファイルを扱うクラス"""
    pass

class XbrlEfjpModel(BaseXbrlModel):
    """ その他のXBRLファイルを扱うクラス"""
    pass