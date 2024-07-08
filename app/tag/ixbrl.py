from dataclasses import dataclass
from typing import Optional

@dataclass
class IxNonNumeric:
    """ 非数値タグの情報を格納するクラス """
    xbrl_id: Optional[str] = None
    context_period: Optional[str] = None
    context_entity: Optional[str] = None
    context_category: Optional[str] = None
    name: Optional[str] = None
    xsi_nil: Optional[bool] = None
    escape: Optional[str] = None
    format: Optional[str] = None
    text: Optional[str] = None
    document_type: Optional[str] = None
    report_type: Optional[str] = None

    @classmethod
    def keys(cls):
        return list(cls().__dict__.keys())

@dataclass
class IxNonFraction:
    """ 非分数タグの情報を格納するクラス """
    xbrl_id: Optional[str] = None
    context_period: Optional[str] = None
    context_entity: Optional[str] = None
    context_category: Optional[str] = None
    name: Optional[str] = None
    unit_ref: Optional[str] = None
    xsi_nil: Optional[bool] = None
    decimals: Optional[str] = None
    format: Optional[str] = None
    scale: Optional[str] = None
    sign: Optional[str] = None
    numeric: Optional[str] = None
    document_type: Optional[str] = None
    report_type: Optional[str] = None

    @classmethod
    def keys(cls):
        return list(cls().__dict__.keys())