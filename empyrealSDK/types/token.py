from functools import singledispatchmethod
from typing import Literal, Optional, Union
from uuid import UUID

from eth_typing import ChecksumAddress, HexStr
from pydantic import BaseModel, Field

from .network import Network
from .wallet import Wallet
from ..utils.client import _force_get_global_client


class Token(BaseModel):
    """An abstraction of an ERC20 token instance"""

    id: UUID = Field()
    address: ChecksumAddress
    name: str
    symbol: str
    decimals: int
    network: Network = Field(alias="chainId")

    @classmethod
    async def load(
        cls,
        address: ChecksumAddress,
        network: Network = Network.Ethereum,
    ):
        client = _force_get_global_client()
        response = await client.token.lookup(address, network.value)
        return cls(**response.json())

    async def allowance(
        self,
        owner: ChecksumAddress,
        spender: ChecksumAddress,
        block_num: Optional[Union[int, Literal["latest"]]] = "latest",
    ) -> "TokenAmount":
        """
        Gets the allowance allocated to an address from a spender


        :param owner: A checksummed ethereum address
        :param spender: A checksummed ethereum address
        :return: :class:`.TokenAmount`
        """
        client = _force_get_global_client()
        allowance = await client.token.allowance(
            self.address,
            owner,
            spender,
            self.network.value,
            block_num=block_num,
        )
        return TokenAmount(
            raw_amount=allowance,
            decimals=self.decimals,
            token=self,
        )

    async def approve(
        self,
        from_wallet: Wallet,
        recipient: Union[Wallet, ChecksumAddress],
        amount: int,
        gas_price: Optional[int] = None,
    ) -> HexStr:
        raise NotImplementedError()

    async def transfer(
        self,
        from_wallet: Wallet,
        recipient: Union[Wallet, ChecksumAddress],
        amount: int,
        gas_price: Optional[int] = None,
    ) -> HexStr:
        """
        Transfer a token amount to a target address

        :param wallet: :class:`empyrealSDK.Wallet`
        :param spender: A checksummed ethereum address
        :return: :class:`.TokenAmount`
        """
        client = _force_get_global_client()
        if isinstance(recipient, Wallet):
            recipient_address = recipient.address
        else:
            recipient_address = recipient
        return await client.token.transfer(
            self.id,
            from_wallet.id,
            recipient_address,
            amount,
            gas_price=gas_price,
        )

    @singledispatchmethod
    async def balance_of(
        self,
        wallet: Wallet,
        block: Union[int, Literal["latest"]] = "latest",
    ) -> "TokenAmount":
        """
        Gets the balance of a wallet at a particular block.
        Defaults to latest block.

        :param wallet: :class:`empyrealSDK.Wallet`
        :param block: A block number of defaults to latest block
        :return: :class:`.TokenAmount` of the current balance
        """

        client = _force_get_global_client()
        balance = await client.token.balance_of(
            self.address,
            wallet.address,
            self.network.value,
            block,
        )
        return TokenAmount(raw_amount=balance, decimals=self.decimals, token=self)

    @balance_of.register(str)
    async def _(
        self,
        wallet_address: ChecksumAddress,
        network: Network = Network.Ethereum,
        block: Union[int, Literal["latest"]] = "latest",
    ):
        """
        Gets the balance of a wallet at a particular block,
        given a Checksum Address.

        :param wallet: :class:`empyrealSDK.Wallet`
        :param block: A block number of defaults to latest block
        :return: :class:`.TokenAmount` of the current balance
        """

        client = _force_get_global_client()
        balance = await client.token.balance_of(
            self.address,
            wallet_address,
            network.value,
            block,
        )
        return TokenAmount(raw_amount=balance, decimals=self.decimals, token=self)

    def __repr__(self):
        return f"<'{self.symbol}' on {self.network.name}>"

    __str__ = __repr__


class TokenAmount(BaseModel):
    """An abstraction on a token amount"""

    raw_amount: int
    decimals: int
    token: "Token"
    price: Optional[int] = None

    @singledispatchmethod
    def __div__(self, other_amount: int):
        return self.raw_amount / other_amount

    def __repr__(self):
        return f"<{self.token.name}: {self.raw_amount / 10**self.decimals}>"

    __str__ = __repr__
