from enum import IntEnum, auto
from typing import Any, Optional, Union
from uuid import UUID

from eth_typing import HexStr
from pydantic import BaseModel, Field

from ..utils.client import _force_get_global_client
from .wallet import Wallet


class UserType(IntEnum):
    telegram = auto()
    unclassified = auto()


class User(BaseModel):
    """
    A User of an application.  This is mainly used to organize wallets
    and actions to a single owner.  Currently the telegram id identity is
    used to manage users, but they can be created without an originating
    telegram account, and it is mainly used as a convenience for tracking.
    """

    id: UUID
    type: Optional[UserType] = None
    name: str
    telegram_id: Optional[str] = Field(alias="telegramId")
    is_new_user: bool = Field(alias="isNewUser")
    metadata: dict[Any, Any] = Field(default={})

    @classmethod
    async def load(cls, telegram_id: Union[str, int]):
        client = _force_get_global_client()
        response = await client.user.get_from_telegram(telegram_id)
        return cls(**response.json())

    @classmethod
    async def create(cls, name: str):
        raise NotImplementedError()

    async def get_app_wallets(self):
        client = _force_get_global_client()
        response = await client.wallet.get_app_wallets(self.id)
        return [Wallet(**row) for row in response.json()]

    async def make_wallet(self, name: str, private_key: Optional[HexStr] = None):
        client = _force_get_global_client()
        response = await client.wallet.make_wallet(
            self.id,
            name,
            private_key=private_key,
        )
        return Wallet(**response.json())

    def __repr__(self):
        return f"<User: {self.name}>"

    __str__ = __repr__
