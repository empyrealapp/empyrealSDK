from enum import Enum, auto
from typing import Optional

from eth_typing import ChecksumAddress, HexStr
from pydantic import BaseModel

from .token import Token
from .wallet import Wallet
from .network import Network
from ..utils.client import _force_get_global_client


class Liquidity(BaseModel):
    token0_balance: int
    token0_price: Optional[float] = None
    token1_balance: int
    token1_price: Optional[float] = None
    pair: "DexPair"

    @property
    def token0_value(self):
        # TODO: handle invalid prices
        if self.token0_price:
            return (
                self.token0_price
                * self.token0_balance
                / 10**self.pair.token0.decimals
            )
        return -0.5

    @property
    def token1_value(self):
        # TODO: handle invalid prices
        if self.token1_price:
            return (
                self.token1_price
                * self.token1_balance
                / 10**self.pair.token1.decimals
            )
        return -0.5

    @property
    def value(self):
        return round(self.token0_value * 2, 2)

    def __repr__(self):
        token0_symbol = self.pair.token0.symbol
        token1_symbol = self.pair.token1.symbol
        token0 = self.token0_balance / 10**self.pair.token0.decimals
        token1 = self.token1_balance / 10**self.pair.token1.decimals
        return f"<Liquidity: ${format(self.value, ',')} ({token0_symbol}: {token0}, {token1_symbol}: {token1})>"

    __str__ = __repr__


class DexFactory(Enum):
    UniswapV2 = auto()  # 0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f

    async def get_pairs(
        self,
        token: Token,
    ) -> list["DexPair"]:
        client = _force_get_global_client()
        return await client.prices.get_token_pairs(
            token_address=token.address,
            chain_id=token.network.value,
        )

    async def swap(
        self,
        wallet: Wallet,
        network: Network,
        path: list[ChecksumAddress],
        amount_in: int,
        slippage_percent: float,
        priority_fee: int,
        is_private: bool,
    ):
        raise NotImplementedError()


class DexPair(BaseModel):
    factory_address: ChecksumAddress
    token0: Token
    token1: Token
    address: ChecksumAddress
    index: int

    fee: Optional[float]

    network: Network
    block_number: int

    transaction_hash: HexStr

    async def get_liquidity(self, block_number: Optional[int] = None):
        client = _force_get_global_client()
        response = await client.prices.get_liquidity(
            token_address=self.address,
            chain_id=self.network.value,
            block_number=block_number,
        )
        return Liquidity(
            token0_balance=response["balances"]["token0"]["amount"],
            token0_price=response["balances"]["token0"]["price"],
            token1_balance=response["balances"]["token1"]["amount"],
            token1_price=response["balances"]["token1"]["price"],
            pair=self,
        )

    async def swap_history(self, start_time, end_time):
        raise NotImplementedError()

    async def swap(
        self,
        wallet: Wallet,
        amount: int,
        priority_fee: int,
        is_private: bool,
        use_token0: bool,
    ):
        raise NotImplementedError()

    async def buy_tax(self) -> float:
        raise NotImplementedError()

    async def sell_tax(self) -> float:
        raise NotImplementedError()

    async def honeypot(self) -> bool:
        raise NotImplementedError()

    def __repr__(self):
        return f"<DexPair: {self.token0.symbol}, {self.token1.symbol}>"

    __str__ = __repr__
