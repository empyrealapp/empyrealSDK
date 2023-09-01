from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Wallet(BaseModel):
    id: UUID
    name: str
    address: str
    type: str
    group_id: Optional[str] = Field(alias="groupId")
    user_id: str = Field(alias="userId")
