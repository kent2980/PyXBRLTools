from dataclasses import dataclass, field
from typing import Optional

from app.utils import Utils


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
    """ソースファイル情報を格納するクラス"""

    id: Optional[str] = field(default=None)
    name: str = field(default=None)
    type: Optional[str] = field(default=None)
    xbrl_id: str = field(default=None)
    url: str = field(default=None)

    # def __post_init__(self):
    #     if self.url:
    #         self.id = str(Utils.string_to_uuid(self.url))
    #     else:
    #         self.id = str(Utils.string_to_uuid(f"{self.xbrl_id}{self.name}"))

    def __str__(self) -> str:
        return f"{self.name},{self.type},{self.xbrl_id},{self.url}"
