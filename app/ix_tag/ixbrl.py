from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from .base import BaseTag


@dataclass
class IxNonNumeric(BaseTag):
    """非数値タグの情報を格納するクラス"""

    xbrl_id: Optional[str] = field(default=None)
    context: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    xsi_nil: Optional[bool] = field(default=None)
    escape: Optional[bool] = field(default=None)
    format: Optional[str] = field(default=None)
    value: Optional[str] = field(default=None)
    report_type: Optional[str] = field(default=None)
    ixbrl_role: Optional[str] = field(default=None)
    source_file_id: Optional[str] = field(default=None)


@dataclass
class IxNonFraction(BaseTag):
    """非分数タグの情報を格納するクラス"""

    xbrl_id: Optional[str] = field(default=None)
    context: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    unit_ref: Optional[str] = field(default=None)
    xsi_nil: Optional[bool] = field(default=None)
    decimals: Optional[Decimal] = field(default=None)
    format: Optional[str] = field(default=None)
    scale: Optional[Decimal] = field(default=None)
    numeric: Optional[Decimal] = field(default=None)
    report_type: Optional[str] = field(default=None)
    ixbrl_role: Optional[str] = field(default=None)
    source_file_id: Optional[str] = field(default=None)


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
class IxContext(BaseTag):
    """コンテキスト情報を格納するクラス"""

    xbrl_id: Optional[str] = field(default=None)
    context_id: Optional[str] = field(default=None)
    period: Optional[dict] = field(default=None)
    scenario: Optional[list] = field(default=None)
    source_file_id: Optional[str] = field(default=None)
