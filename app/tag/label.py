from dataclasses import dataclass, field
from typing import Optional

from .base import BaseTag


@dataclass
class LabelValue(BaseTag):
    """ラベル情報を格納するクラス"""

    xlink_type: Optional[str] = field(default=None)
    xlink_label: Optional[str] = field(default=None)
    xlink_role: Optional[str] = field(default=None)
    xml_lang: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    source_file_id: Optional[str] = field(default=None)


@dataclass
class LabelLoc(BaseTag):
    """loc要素情報を格納するクラス"""

    xlink_type: Optional[str] = field(default=None)
    xlink_label: Optional[str] = field(default=None)
    xlink_schema: Optional[str] = field(default=None)
    xlink_href: Optional[str] = field(default=None)
    source_file_id: Optional[str] = field(default=None)


@dataclass
class LabelArc(BaseTag):
    """arc要素情報を格納するクラス"""

    xlink_type: Optional[str] = field(default=None)
    xlink_from: Optional[str] = field(default=None)
    xlink_to: Optional[str] = field(default=None)
    xlink_arcrole: Optional[str] = field(default=None)
    source_file_id: Optional[str] = field(default=None)


@dataclass
class LabelRoleRefs(BaseTag):
    """roleRef要素情報を格納するクラス"""

    role_uri: Optional[str] = field(default=None)
    xlink_type: Optional[str] = field(default=None)
    xlink_schema: Optional[str] = field(default=None)
    xlink_href: Optional[str] = field(default=None)
