from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class GrantType(BaseModel):
    id: UUID
    grant_id: UUID
    wallet_id: UUID
    type: str

    arg1: Optional[str]
    arg2: Optional[str]
    arg3: Optional[str]
    arg4: Optional[str]

    status: str


class Grant(BaseModel):
    id: UUID
    app_id: UUID = Field(alias="appId")
    user_id: UUID = Field(alias="userId")
    status: str
    grant_types: list[GrantType] = Field(alias="grantTypes")
