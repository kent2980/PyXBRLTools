import decimal
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.utils import Utils


class BaseTag(BaseModel):
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

    model_config = ConfigDict(coerce_numbers_to_str=True)


class SourceFile(BaseTag):
    """ソースファイル情報を格納するクラス"""

    id: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    xbrl_id: Optional[str] = Field(default=None)
    url: Optional[str] = Field(default=None)

    def __str__(self) -> str:
        return f"{self.name},{self.type},{self.xbrl_id},{self.url}"
