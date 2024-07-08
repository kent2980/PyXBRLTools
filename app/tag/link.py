from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class SchemaImport:
    schema_location: Optional[str] = field(default=None)
    name_space: Optional[str] = field(default=None)
    document_type: Optional[str] = field(default=None)

@dataclass
class LinkBaseRef:
    xlink_type: Optional[str] = field(default=None)
    xlink_href: Optional[str] = field(default=None)
    xlink_role: Optional[str] = field(default=None)
    xlink_arcrole: Optional[str] = field(default=None)
    document_type: Optional[str] = field(default=None)

@dataclass
class Element:
    id: Optional[str] = field(default=None)
    xbrli_balance: Optional[str] = field(default=None)
    xbrli_period_type: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    nillable: Optional[str] = field(default=None)
    substitution_group: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)
    abstract: Optional[str] = field(default=None)
    document_type: Optional[str] = field(default=None)

@dataclass
class RoleTag:
    xbrl_id: str
    xlink_type: Optional[str] = field(default=None)
    xlink_href: Optional[str] = field(default=None)
    role_uri: Optional[str] = field(default=None)

@dataclass
class LocTag:
    xbrl_id: str
    attr_value: Optional[str] = field(default=None)
    xlink_type: Optional[str] = field(default=None)
    xlink_schema: Optional[str] = field(default=None)
    xlink_href: Optional[str] = field(default=None)
    xlink_label: Optional[str] = field(default=None)

@dataclass
class ArcTag:
    xbrl_id: str
    attr_value: Optional[str] = field(default=None)
    xlink_type: Optional[str] = field(default=None)
    xlink_from: Optional[str] = field(default=None)
    xlink_to: Optional[str] = field(default=None)
    xlink_arcrole: Optional[str] = field(default=None)
    xlink_order: Optional[float] = field(default=None)
    xlink_weight: Optional[float] = field(default=None)

@dataclass
class LinkBaseTag:
    xbrl_id: str
    xmlns_xlink: Optional[str] = field(default=None)
    xmlns_xsi: Optional[str] = field(default=None)
    xmlns_link: Optional[str] = field(default=None)

@dataclass
class LinkTag:
    xbrl_id: str
    xlink_type: Optional[str] = field(default=None)
    xlink_role: Optional[str] = field(default=None)