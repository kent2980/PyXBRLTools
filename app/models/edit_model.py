from app.manager import (
    CalLinkManager,
    DefLinkManager,
    IxbrlManager,
    LabelManager,
    PreLinkManager,
    QualitativeManager,
)
from app.models import BaseXbrlModel


class EditModel(BaseXbrlModel):
    """決算短信(国際会計基準) ※IFRSタクソノミを利用する場合のXBRLファイルを扱うクラス"""

    pass
