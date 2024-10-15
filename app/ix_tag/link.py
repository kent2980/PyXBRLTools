from typing import Optional

from pydantic import Field

from .base import BaseTag


class LinkSchemaImport(BaseTag):
    """
    リンクスキーマのインポートを表すデータクラスです。
    """

    xbrl_id: Optional[str] = Field(default=None)
    schema_location: Optional[str] = Field(default=None)
    name_space: Optional[str] = Field(default=None)
    document_type: Optional[str] = Field(default=None)


class LinkBaseRef(BaseTag):
    """
    リンクベースの参照を表すデータクラスです。
    """

    xbrl_id: Optional[str] = Field(default=None)
    xlink_type: Optional[str] = Field(default=None)
    xlink_href: Optional[str] = Field(default=None)
    xlink_role: Optional[str] = Field(default=None)
    xlink_arcrole: Optional[str] = Field(default=None)
    document_type: Optional[str] = Field(default=None)


class LinkElement(BaseTag):
    """
    リンク要素を表すデータクラスです。
    """

    xbrl_id: Optional[str] = Field(default=None)
    id: Optional[str] = Field(default=None)
    xbrli_balance: Optional[str] = Field(default=None)
    xbrli_period_type: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    nillable: Optional[str] = Field(default=None)
    substitution_group: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    abstract: Optional[str] = Field(default=None)
    document_type: Optional[str] = Field(default=None)


class LinkRole(BaseTag):
    """
    リンクロールを表すデータクラスです。
    """

    xbrl_id: Optional[str] = Field(default=None)
    xlink_type: Optional[str] = Field(default=None)
    xlink_schema: Optional[str] = Field(default=None)
    xlink_href: Optional[str] = Field(default=None)
    role_uri: Optional[str] = Field(default=None)


class LinkLoc(BaseTag):
    """
    リンクロケーションを表すデータクラスです。
    """

    xbrl_id: Optional[str] = Field(default=None)
    attr_value: Optional[str] = Field(default=None)
    xlink_type: Optional[str] = Field(default=None)
    xlink_schema: Optional[str] = Field(default=None)
    xlink_href: Optional[str] = Field(default=None)
    xlink_label: Optional[str] = Field(default=None)
    source_file_id: Optional[str] = Field(default=None)


class LinkArc(BaseTag):
    """
    リンクアークを表すデータクラスです。
    """

    xbrl_id: Optional[str] = Field(default=None)
    attr_value: Optional[str] = Field(default=None)
    xlink_type: Optional[str] = Field(default=None)
    xlink_from: Optional[str] = Field(default=None)
    xlink_to: Optional[str] = Field(default=None)
    xlink_arcrole: str = Field(default=None)
    xlink_order: Optional[float] = Field(default=None)
    xlink_weight: Optional[float] = Field(default=None)
    source_file_id: Optional[str] = Field(default=None)


class LinkBase(BaseTag):
    """
    リンクベースを表すデータクラスです。
    """

    xbrl_id: Optional[str] = Field(default=None)
    xmlns_xlink: Optional[str] = Field(default=None)
    xmlns_xsi: Optional[str] = Field(default=None)
    xmlns_link: Optional[str] = Field(default=None)


class LinkTag(BaseTag):
    """
    リンクタグを表すデータクラスです。
    """

    xbrl_id: Optional[str] = Field(default=None)
    xlink_type: Optional[str] = Field(default=None)
    xlink_role: Optional[str] = Field(default=None)
