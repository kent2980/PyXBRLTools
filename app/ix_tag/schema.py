from dataclasses import dataclass, field
from typing import Optional

from .base import BaseTag


@dataclass
class SchemaImport(BaseTag):
    """Schema Import Dataclass"""

    schema_location: Optional[str] = field(default=None)
    name_space: Optional[str] = field(default=None)
    xbrl_type: Optional[str] = field(default=None)
    xbrl_id: Optional[str] = field(default=None)
    source_file_id: Optional[str] = field(default=None)


@dataclass
class SchemaLinkBaseRef(BaseTag):
    """Schema Link Base Ref Dataclass"""

    xlink_type: Optional[str] = field(default=None)
    xlink_href: Optional[str] = field(default=None)
    xlink_role: Optional[str] = field(default=None)
    xlink_arcrole: Optional[str] = field(default=None)
    xbrl_type: Optional[str] = field(default=None)
    xbrl_id: Optional[str] = field(default=None)
    source_file_id: Optional[str] = field(default=None)


@dataclass
class SchemaElement(BaseTag):
    """Schema Element Dataclass"""

    id: Optional[str] = field(default=None)
    xbrli_balance: Optional[str] = field(default=None)
    xbrli_period_type: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    nillable: Optional[str] = field(default=None)
    substitution_group: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)
    abstract: Optional[str] = field(default=None)
    xbrl_type: Optional[str] = field(default=None)
    xbrl_id: Optional[str] = field(default=None)
    source_file_id: Optional[str] = field(default=None)
