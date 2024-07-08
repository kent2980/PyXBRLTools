from dataclasses import dataclass, field
from typing import Optional

from .base import BaseTag


@dataclass
class IxNonNumeric(BaseTag):
    """非数値タグの情報を格納するクラス"""

    xbrl_id: Optional[str] = field(default=None)
    context_period: Optional[str] = field(default=None)
    context_entity: Optional[str] = field(default=None)
    context_category: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    xsi_nil: Optional[bool] = field(default=None)
    escape: Optional[bool] = field(default=None)
    format: Optional[str] = field(default=None)
    value: Optional[str] = field(default=None)
    document_type: Optional[str] = field(default=None)
    report_type: Optional[str] = field(default=None)

@dataclass
class IxNonFraction(BaseTag):
    """非分数タグの情報を格納するクラス"""

    xbrl_id: Optional[str] = field(default=None)
    context_period: Optional[str] = field(default=None)
    context_entity: Optional[str] = field(default=None)
    context_category: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    unit_ref: Optional[str] = field(default=None)
    xsi_nil: Optional[bool] = field(default=None)
    decimals: Optional[float] = field(default=None)
    format: Optional[str] = field(default=None)
    scale: Optional[float] = field(default=None)
    numeric: Optional[float] = field(default=None)
    document_type: Optional[str] = field(default=None)
    report_type: Optional[str] = field(default=None)


@dataclass
class IxHeader(BaseTag):
    """iXBRLのヘッダー情報を格納するクラス"""

    company_name: Optional[str] = field(default=None)
    securities_code: Optional[str] = field(default=None)
    document_name: Optional[str] = field(default=None)
    reporting_date: Optional[str] = field(default=None)
    current_period: Optional[str] = field(default=None)
    xbrl_id: Optional[str] = field(default=None)
    report_type: Optional[str] = field(default=None)


@dataclass
class IxSummary(BaseTag):
    """iXBRLのサマリー情報を格納するクラス"""

    context_period: Optional[str] = field(default=None)
    context_entity: Optional[str] = field(default=None)
    context_category: Optional[str] = field(default=None)
    net_sales: Optional[str] = field(default=None)

