import uuid
from typing import Optional

from pydantic import Field

from .base import BaseTag


class QualitativeDocument(BaseTag):
    """定性的情報を格納するデータクラス"""

    currentId: str = Field(
        max_length=36,
        description="ID",
        default_factory=lambda: str(uuid.uuid4()),
    )
    parentId: Optional[str] = Field(
        default=None, max_length=36, description="親ID"
    )
    type: Optional[str] = Field(default=None, description="タイプ")
    order: Optional[int] = Field(default=None, description="順番")
    xbrl_id: Optional[str] = Field(
        default=None, max_length=36, description="XBRLの固有ID"
    )
    source_file_id: Optional[str] = Field(
        default=None, max_length=36, description="XBRLのソースファイルID"
    )
    content: Optional[str] = Field(
        default=None, description="タイトル,本文"
    )
    photo_url: Optional[str] = Field(default=None, description="画像URL")
