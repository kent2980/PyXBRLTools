from dataclasses import dataclass, field
from typing import Optional

@dataclass
class LabelValue:
    """ラベル情報を格納するクラス"""
    xlink_type: Optional[str] = field(default=None)
    xlink_label: Optional[str] = field(default=None)
    xlink_role: Optional[str] = field(default=None)
    xml_lang: Optional[str] = field(default=None)
    id: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    xlink_schema: Optional[str] = field(default=None)

    @classmethod
    def keys(cls):
        return list(cls().__dict__.keys())

@dataclass
class LabelLoc:
    """loc要素情報を格納するクラス"""
    xlink_type: Optional[str] = field(default=None)
    xlink_label: Optional[str] = field(default=None)
    xlink_schema: Optional[str] = field(default=None)
    xlink_href: Optional[str] = field(default=None)

    @classmethod
    def keys(cls):
        return list(cls().__dict__.keys())

@dataclass
class LabelArc:
    """arc要素情報を格納するクラス"""
    xlink_type: Optional[str] = field(default=None)
    xlink_from: Optional[str] = field(default=None)
    xlink_to: Optional[str] = field(default=None)
    xlink_arcrole: Optional[str] = field(default=None)
    xlink_schema: Optional[str] = field(default=None)

    @classmethod
    def keys(cls):
        return list(cls().__dict__.keys())

@dataclass
class LabelRoleRefs:
    """roleRef要素情報を格納するクラス"""
    role_uri: Optional[str] = field(default=None)
    xlink_type: Optional[str] = field(default=None)
    xlink_schema: Optional[str] = field(default=None)
    xlink_href: Optional[str] = field(default=None)

    @classmethod
    def keys(cls):
        return list(cls().__dict__.keys())