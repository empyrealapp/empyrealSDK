from enum import IntEnum, auto
from uuid import UUID

from pydantic import BaseModel, Field

from .token import Token


class VaultType(IntEnum):
    bank = auto()
    vault = auto()


class Vault(BaseModel):
    app_id: UUID = Field(alias="appId")
    wallet_id: UUID = Field(alias="walletId")
    token: Token
    name: str
    description: str
    type: str
    balance: float
    shares: float
