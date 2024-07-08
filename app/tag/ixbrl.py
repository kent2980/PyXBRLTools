from dataclasses import dataclass, field
from typing import Optional

@dataclass
class IxNonNumeric:
    """ 非数値タグの情報を格納するクラス """
    xbrl_id: Optional[str] = field(default=None)
    context_period: Optional[str] = field(default=None)
    context_entity: Optional[str] = field(default=None)
    context_category: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    xsi_nil: Optional[bool] = field(default=None)
    escape: Optional[str] = field(default=None)
    format: Optional[str] = field(default=None)
    text: Optional[str] = field(default=None)
    document_type: Optional[str] = field(default=None)
    report_type: Optional[str] = field(default=None)

    @classmethod
    def keys(cls):
        return list(cls().__dict__.keys())

@dataclass
class IxNonFraction:
    """ 非分数タグの情報を格納するクラス """
    xbrl_id: Optional[str] = field(default=None)
    context_period: Optional[str] = field(default=None)
    context_entity: Optional[str] = field(default=None)
    context_category: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    unit_ref: Optional[str] = field(default=None)
    xsi_nil: Optional[bool] = field(default=None)
    decimals: Optional[str] = field(default=None)
    format: Optional[str] = field(default=None)
    scale: Optional[str] = field(default=None)
    sign: Optional[str] = field(default=None)
    numeric: Optional[str] = field(default=None)
    document_type: Optional[str] = field(default=None)
    report_type: Optional[str] = field(default=None)

    @classmethod
    def keys(cls):
        return list(cls().__dict__.keys())