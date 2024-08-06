from typing import Optional

from pydantic import Field

from .base import BaseTag


class LabelValue(BaseTag):
    """ラベル情報を格納するクラス"""

    xlink_type: Optional[str] = Field(default=None)
    xlink_label: Optional[str] = Field(default=None)
    xlink_role: Optional[str] = Field(default=None)
    xml_lang: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    source_file_id: Optional[str] = Field(default=None)


class LabelLoc(BaseTag):
    """loc要素情報を格納するクラス"""

    xlink_type: Optional[str] = Field(default=None)
    xlink_label: Optional[str] = Field(default=None)
    xlink_schema: Optional[str] = Field(default=None)
    xlink_href: Optional[str] = Field(default=None)
    source_file_id: Optional[str] = Field(default=None)


class LabelArc(BaseTag):
    """arc要素情報を格納するクラス"""

    xlink_type: Optional[str] = Field(default=None)
    xlink_from: Optional[str] = Field(default=None)
    xlink_to: Optional[str] = Field(default=None)
    xlink_arcrole: Optional[str] = Field(default=None)
    source_file_id: Optional[str] = Field(default=None)


class LabelRoleRefs(BaseTag):
    """roleRef要素情報を格納するクラス"""

    role_uri: Optional[str] = Field(default=None)
    xlink_type: Optional[str] = Field(default=None)
    xlink_schema: Optional[str] = Field(default=None)
    xlink_href: Optional[str] = Field(default=None)
