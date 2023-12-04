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
            amount=allowance,
            decimals=self.decimals,
            token=self,
        )

    async def approve(
        self,
        from_wallet: Wallet,
        spender: Union[Wallet, ChecksumAddress],
        amount: int = int(2**256 - 1),
        priority_fee: Optional[int] = None,
    ) -> HexStr:
        """
        Approve a spender to use a token.
        :param from_wallet: :class:`empyrealSDK.Wallet` making the approval
        :param spender: A checksummed ethereum address
        :return: HexStr

        """
        client = _force_get_global_client()
        if isinstance(spender, Wallet):
            return await client.token.approve(
                self.id,
                from_wallet.id,
                spender.address,
                chain_id=self.network.chain_id,
                amount=amount,
                priority_fee=priority_fee,
            )
        return await client.token.approve(
            self.id,
            from_wallet.id,
            spender,
            chain_id=self.network.chain_id,
            amount=amount,
            priority_fee=priority_fee,
        )

    async def transfer(
        self,
        from_wallet: Wallet,
        recipient: Union[Wallet, ChecksumAddress],
        amount: "TokenAmount",
        gas_price: Optional[int] = None,
    ) -> HexStr:
        """
        Transfer a token amount to a target address

        :param wallet: :class:`empyrealSDK.Wallet`
        :param recipient: The recipient of the transfer
        :param amount: Amount of tokens to transfer
        :return: HexStr of the transaction
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
        return TokenAmount(amount=balance, decimals=self.decimals, token=self)

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
        return TokenAmount(
            amount=balance,
            decimals=self.decimals,
            token=self,
        )

    def __repr__(self):
        return f"<'{self.symbol}' on {self.network.name}>"

    __str__ = __repr__


class TokenAmount(BaseModel):
    """An abstraction on a token amount"""

    amount: int
    """The raw amount of tokens, ignoring the decimal"""

    decimals: int = 18
    """The number of decimals used onchain to represent the token amount"""

    token: Optional["Token"] = None
    """The token associated with the amount"""

    def format(self, num_decimals=2):
        """Format the token to a decimal string, with respect to the token decimals"""
        return round(self.amount / 10**self.decimals, num_decimals)

    def __truediv__(self, other):
        """Divide the token by either another TokenAmount or an integer value"""
        return self._div_by_other(other)

    def __mul__(self, other):
        """Multiply the token by either another TokenAmount or an integer value"""
        return self._mul_other(other)

    @singledispatchmethod
    def _mul_other(self, other: int):
        return TokenAmount(
            amount=self.amount // other,
            decimals=self.decimals,
            token=self.token,
        )

    @singledispatchmethod
    def _div_by_other(self, other: int):
        return TokenAmount(
            amount=self.amount // other,
            decimals=self.decimals,
            token=self.token,
        )

    def __repr__(self):
        if self.token:
            return f"<{self.token.name}: {self.amount / 10**self.decimals}>"
        return f"<Amount: {self.amount / 10**self.decimals}>"

    __str__ = __repr__


@TokenAmount._div_by_other.register(TokenAmount)  # type: ignore
def _(self: TokenAmount, other: TokenAmount):
    return TokenAmount(
        amount=int(self.amount / (other.amount / 10**other.decimals)),
        decimals=self.decimals,
        token=self.token,
    )


@TokenAmount._mul_other.register(TokenAmount)  # type: ignore
def _(self: TokenAmount, other: TokenAmount):
    return TokenAmount(
        amount=int(int(self.amount * other.amount) / 10**other.decimals),
        decimals=self.decimals,
        token=self.token,
    )
