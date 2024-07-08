from dataclasses import dataclass
from typing import List, Optional

@dataclass
class RoleTag:
    xbrl_id: str
    xlink_type: Optional[str]
    xlink_href: Optional[str]
    role_uri: Optional[str]

@dataclass
class LocTag:
    xbrl_id: str
    attr_value: Optional[str]
    xlink_type: Optional[str]
    xlink_schema: Optional[str]
    xlink_href: Optional[str]
    xlink_label: Optional[str]

@dataclass
class ArcTag:
    xbrl_id: str
    attr_value: Optional[str]
    xlink_type: Optional[str]
    xlink_from: Optional[str]
    xlink_to: Optional[str]
    xlink_arcrole: Optional[str]
    xlink_order: Optional[float]
    xlink_weight: Optional[float]

@dataclass
class LinkBaseTag:
    xbrl_id: str
    xmlns_xlink: Optional[str]
    xmlns_xsi: Optional[str]
    xmlns_link: Optional[str]

@dataclass
class LinkTag:
    xbrl_id: str
    xlink_type: Optional[str]
    xlink_role: Optional[str]