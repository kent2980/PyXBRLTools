import uuid
from dataclasses import dataclass, field
from typing import Optional


class BaseTag:
    """Base class for tags"""

    @classmethod
    def keys(cls):
        return list(cls().__dict__.keys())

    @classmethod
    def is_valid(cls, data: dict):
        # インスタンス化
        try:
            cls(**data)
            return True
        except TypeError:
            return False

    def __eq__(self, value: object) -> bool:
        return self.__dict__ == value.__dict__


@dataclass
class SourceFile(BaseTag):

    id: Optional[str] = field(default_factory=lambda: str(uuid.uuid4()))
    xbrl_id : Optional[str] = field(default=None)
    name: Optional[str]  = field(default=None)
