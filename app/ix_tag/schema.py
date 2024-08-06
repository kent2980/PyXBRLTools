from typing import Optional

from pydantic import Field

from .base import BaseTag


class SchemaImport(BaseTag):
    """Schema Import Dataclass"""

    schema_location: Optional[str] = Field(default=None)
    name_space: Optional[str] = Field(default=None)
    xbrl_type: Optional[str] = Field(default=None)
    xbrl_id: Optional[str] = Field(default=None)
    source_file_id: Optional[str] = Field(default=None)


class SchemaLinkBaseRef(BaseTag):
    """Schema Link Base Ref Dataclass"""

    xlink_type: Optional[str] = Field(default=None)
    xlink_href: Optional[str] = Field(default=None)
    xlink_role: Optional[str] = Field(default=None)
    xlink_arcrole: Optional[str] = Field(default=None)
    xbrl_type: Optional[str] = Field(default=None)
    xbrl_id: Optional[str] = Field(default=None)
    source_file_id: Optional[str] = Field(default=None)
    href_source_file_id: Optional[str] = Field(default=None)


class SchemaElement(BaseTag):
    """Schema Element Dataclass"""

    id: Optional[str] = Field(default=None)
    xbrli_balance: Optional[str] = Field(default=None)
    xbrli_period_type: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    nillable: Optional[str] = Field(default=None)
    substitution_group: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    abstract: Optional[str] = Field(default=None)
    xbrl_type: Optional[str] = Field(default=None)
    xbrl_id: Optional[str] = Field(default=None)
    source_file_id: Optional[str] = Field(default=None)
