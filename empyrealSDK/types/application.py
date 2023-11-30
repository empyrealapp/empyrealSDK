from functools import singledispatchmethod
from typing import Optional
from uuid import UUID

from eth_typing import ChecksumAddress
from pydantic import BaseModel, Field

from ..utils.client import _force_get_global_client, _set_global_client
from .wallet import Wallet
from .user import User


class Application(BaseModel):
    """
    This represents an Application, which allows a builder to use the SDK.
    """

    id: UUID = Field()
    name: str
    type: str
    tier: str
    api_key: str = Field(alias="apiKey")
    swap_fee: int = Field(alias="swapFee")
    fee_collection_amount: int = Field(alias="feeCollectionAmount")
    request_count: int = Field(alias="requestCount")

    # types
    owner: Optional[User] = Field()
    app_wallet: Optional[Wallet] = Field(alias="appWallet")

    @classmethod
    async def load(self, api_key: Optional[str] = None):
        """
        Loads an instance of the current empyrealSDK user's application.
        If an `api_key` is provided, this will create a new global client.
        Otherwise, the currently set application from the global context
        is loaded.

        Token :class:`empyrealSDK.types.Token`
        """
        from empyrealSDK import EmpyrealSDK

        if api_key:
            new_client = EmpyrealSDK(api_key)
            _set_global_client(new_client)
            return new_client

        client: EmpyrealSDK = _force_get_global_client()
        return await client.app.info()

    async def update_swap_fee(self, swap_fee: float):
        """
        Update your applications swap fee.
        Swap Fee must be set less than 2%.
        """

        client = _force_get_global_client()
        if swap_fee > 0.02:
            raise ValueError("Swap Fee must be less than 2%")
        response = await client.app.update(
            swap_fee=int(swap_fee * 1_000_000),
        )
        obj = response.json()
        for key in obj["updates"]:
            setattr(self, key, obj["updates"][key])
        return self

    @singledispatchmethod
    async def update_app_wallet(self, wallet: Wallet):
        """
        Update your applications swap fee.
        Swap Fee must be set less than 2%.
        """

        client = _force_get_global_client()
        return await client.app.update(
            app_wallet_id=wallet.id,
        )

    @update_app_wallet.register(str)
    async def _(self, wallet_address: ChecksumAddress):
        """
        Update your fee recipient wallet.
        """

        client = _force_get_global_client()
        wallet = await Wallet.load(wallet_address)

        return await client.app.update(
            app_wallet_id=wallet.id,
        )

    async def refresh_api_key(self):
        """
        Update your applications swap fee.
        Swap Fee must be set less than 2%.
        """

        client = _force_get_global_client()
        new_api_key = await client.app.update_api_key()
        self.api_key = new_api_key
        return self
