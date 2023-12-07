import enum
from typing import Optional, Union
from uuid import UUID

from eth_typing import HexStr
from pydantic import BaseModel, Field

from ..utils.client import _force_get_global_client


class WalletType(enum.Enum):
    mnemonic = "mnemonic"  # generated via mnemonic index
    private_key = "private_key"  # custodial (KMS)
    enclave = "enclave"  # enclave
    noncustodial = "noncustodial"  # noncustodial


class WalletAppData(BaseModel):
    archived: bool = False
    notes: dict[str, Union[str, int]] = {}

    def __repr__(self):
        return f"<AppData| archived: {self.archived}, notes: {self.notes}>"

    __str__ = __repr__


class Wallet(BaseModel):
    """
    A wallet, which is able to make transactions.

    Wallets are owned by a specific user, and have individual permissions.
    """

    id: UUID
    name: str
    address: str
    type: WalletType
    private_key: Optional[HexStr] = Field(None, alias="privateKey")
    group_id: Optional[str] = Field(alias="groupId")
    owner_id: Optional[UUID] = Field(alias="ownerId")
    creator_app_id: Optional[UUID] = Field(alias="creatorAppId")
    data: WalletAppData = WalletAppData()

    def __repr__(self):
        return (
            f"<{self.type.value.capitalize()} {self.name}: '0x..{self.address[-4:]}'>"
        )

    @classmethod
    async def get_all(
        cls,
    ):
        client = _force_get_global_client()
        wallets = await client.wallet.get_app_wallets()
        return [cls(**w) for w in wallets]

    @classmethod
    async def create(
        cls,
        name: str,
        private_key: Optional[HexStr] = None,
        user_id: Optional[UUID] = None,
    ):
        client = _force_get_global_client()
        response = await client.wallet.make_app_wallet(
            name,
            private_key=private_key,
        )
        return Wallet(**response.json())

    @classmethod
    async def load(cls, address):
        """
        If you load a wallet by address, it will give a noncustodial wallet.
        This represents a wallet but has none of the capabilities of a wallet
        with a private key attached to it.
        """
        client = _force_get_global_client()
        wallet = await client.wallet.load(address)
        return cls(**wallet)

    async def load_private_key(self):
        client = _force_get_global_client()
        response = await client.wallet.info(self.id, with_private_key=True)
        return Wallet(**response)

    async def get_data(self):
        """
        Get app specific data associated with wallet.
        """
        client = _force_get_global_client()
        response = await client.wallet.get_wallet_data(self.id)
        return WalletAppData(**response.json())

    async def update_data(
        self, archive: bool = False, notes: dict[str, Union[int, str]] = {}
    ):
        client = _force_get_global_client()
        response = await client.wallet.update_wallet_data(self.id, archive, notes)
        return WalletAppData(**response.json())
