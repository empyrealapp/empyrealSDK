from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class User(BaseModel):
    id: UUID
    name: str
    telegram_id: str = Field(alias="telegramId")
    is_new_user: bool = Field(alias="isNewUser")
    metadata: dict[Any, Any]
