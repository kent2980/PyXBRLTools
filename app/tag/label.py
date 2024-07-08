from dataclasses import dataclass, field
from typing import Optional

@dataclass
class LabelValue:
    """ラベル情報を格納するクラス"""
    xlink_type: Optional[str] = None
    xlink_label: Optional[str] = None
    xlink_role: Optional[str] = None
    xml_lang: Optional[str] = None
    id: Optional[str] = None
    label: Optional[str] = None
    xlink_schema: Optional[str] = None

    @classmethod
    def keys(cls):
        return list(cls().__dict__.keys())


@dataclass
class LabelLoc:
    """loc要素情報を格納するクラス"""
    xlink_type: Optional[str] = None
    xlink_label: Optional[str] = None
    xlink_schema: Optional[str] = None
    xlink_href: Optional[str] = None

    @classmethod
    def keys(cls):
        return list(cls().__dict__.keys())


@dataclass
class LabelArc:
    """arc要素情報を格納するクラス"""
    xlink_type: Optional[str] = None
    xlink_from: Optional[str] = None
    xlink_to: Optional[str] = None
    xlink_arcrole: Optional[str] = None
    xlink_schema: Optional[str] = None

    @classmethod
    def keys(cls):
        return list(cls().__dict__.keys())


@dataclass
class LabelRoleRefs:
    """roleRef要素情報を格納するクラス"""
    role_uri: Optional[str] = None
    xlink_type: Optional[str] = None
    xlink_schema: Optional[str] = None
    xlink_href: Optional[str] = None

    @classmethod
    def keys(cls):
        return list(cls().__dict__.keys())