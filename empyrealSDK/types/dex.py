from collections.abc import Sequence
from datetime import datetime
from enum import Enum
from functools import singledispatchmethod
from typing import Optional, Literal, Union

from eth_typing import ChecksumAddress, HexAddress, HexStr
from pydantic import BaseModel

from .token import Token, TokenAmount
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


class DexRoute(BaseModel):
    path: list[ChecksumAddress]
    fees: list[int] = []
    pair_addresses: list[ChecksumAddress]
    eth_price: TokenAmount
    usdc_price: TokenAmount
    factory: "DexFactory"
    network: Network

    def __repr__(self):
        return f"<DexRoute | path={self.path} | eth_price: {self.eth_price.format(8)}, usdc_price: ${self.usdc_price.format(6)}>"

    async def simulate(
        self,
        amount_in: int,
        sender: ChecksumAddress,
        use_eth: bool = True,
    ) -> TokenAmount:
        """
        Simulate a swap for a specific route
        """
        return await self.factory.simulate_swap(
            self.path,
            amount_in,
            sender,
            fees=self.fees,
            use_eth=use_eth,
            network=self.network,
        )

    __str__ = __repr__


class DexFactory(Enum):
    UniswapV2 = "uniswap"  # 0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f

    def __init__(self, *args):
        self.network = Network.Ethereum

    def __getitem__(self, network: Network):
        self.network = network

    @property
    def weth(self):
        # TODO: handle by chain_id
        return "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

    async def get_taxes(
        self,
        token0_address,
        token1_address=None,
        chain_id: int = 1,
    ):
        """
        Get swap taxes for a token
        """
        if not token1_address:
            token1_address = self.weth
        client = _force_get_global_client()
        taxes = await client.prices.get_taxes(
            token0_address,
            token1_address,
            chain_id=chain_id,
        )
        return taxes

    @singledispatchmethod
    async def get_price(
        self,
        token_address: ChecksumAddress,
    ):
        """
        Get the price for a token using the best route to WETH/USDC
        """
        client = _force_get_global_client()
        routes = await client.prices.get_routes(token_address)
        return [
            DexRoute(
                path=row["path"],
                pair_addresses=row["pair_addresses"],
                eth_price=TokenAmount(
                    amount=int(row["eth_price"] * 1e18),
                ),
                usdc_price=TokenAmount(
                    amount=int(row["usdc_price"] * 1e6),
                    decimals=6,
                ),
                factory=self,
                network=self.network,
            )
            for row in routes
        ]

    @get_price.register(Token)
    async def _(
        self,
        token: Token,
    ):
        return await self.get_price(token.address)

    async def get_pair_info(
        self,
        pair_address: HexAddress,
        force_checksum: bool = True,
        chain_id: int = 1,
    ):
        """
        Get metadata for a particular LP Pair.
        """
        client = _force_get_global_client()
        pair_info = await client.prices.get_pair_info(
            pair_address,
            force_checksum=force_checksum,
            chain_id=chain_id,
        )
        token0 = Token(**pair_info["token0"])
        token1 = Token(**pair_info["token1"])
        return DexPair(
            factory_address=pair_info["factoryAddress"],
            token0=token0,
            token1=token1,
            address=pair_info["pairAddress"],
            index=pair_info["index"],
            fee=pair_info["feePercentage"],
            network=Network(pair_info["chainId"]),
            block_number=pair_info["blockNumber"],
            transaction_hash=pair_info["transactionHash"],
            factory=self,
        )

    async def get_pairs(
        self,
        token: Token,
    ) -> list["DexPair"]:
        """
        A simple function get all pairs with a token.

        :return: A list of all pairs associated with a token
        """
        client = _force_get_global_client()
        pairs = await client.prices.get_token_pairs(
            token_address=token.address,
            chain_id=token.network.value,
        )
        return [
            DexPair(
                factory_address=row["factoryAddress"],
                token0=Token(**row["token0"]),
                token1=Token(**row["token1"]),
                address=row["pairAddress"],
                index=row["index"],
                fee=row["feePercentage"],
                network=Network(row["chainId"]),
                block_number=row["blockNumber"],
                transaction_hash=row["transactionHash"],
                factory=self,
            )
            for row in pairs
        ]

    async def simulate_swap(
        self,
        path: Sequence[Literal["eth"] | ChecksumAddress],
        amount_in: int,
        sender: ChecksumAddress,
        fees: list[int] = [],
        use_eth: bool = True,
        network: Network = Network.Ethereum,
    ) -> TokenAmount:
        """
        Simulate a swap on a given path
        """
        client = _force_get_global_client()
        result = await client.swap.simulate(
            path,
            amount_in,
            sender,
            fees,
            dex=self.value,
            chain_id=network.chain_id,
            use_eth=use_eth,
        )
        token = Token(**result["token"])

        return TokenAmount(
            amount=int(result["amountOut"]),
            decimals=token.decimals,
            token=token,
        )

    async def swap(
        self,
        path: list[ChecksumAddress],
        wallet: Wallet,
        amount_in: Union[TokenAmount, int],
        slippage_percent: float,
        priority_fee: int = 0,
        is_private: bool = False,
        fees: list[int] = [],
        use_eth: bool = True,
        network: Network = Network.Ethereum,
    ) -> HexStr:
        """
        :param path: swap path, consisting of the token addresses to swap through
        :param from_wallet: :class:`empyrealSDK.Wallet` executing the swap
        :param amount_in: :class:`empyrealSDK.TokenAmount` tokens being spent
        :param fees: only used for uniswapV3, ignore for more pairs
        :return: Transaction Hash
        """
        client = _force_get_global_client()
        raw_amount_in: int = (
            amount_in.amount if isinstance(amount_in, TokenAmount) else amount_in
        )
        result = await client.swap.swap(
            path,
            raw_amount_in,
            wallet.id,
            slippage_percent=slippage_percent,
            priority_fee=priority_fee,
            is_private=is_private,
            chain_id=network.chain_id,
            use_eth=use_eth,
            fees=fees,
            dex=self.value,
        )
        return result


class SwapInterval(BaseModel):
    start_time: datetime
    open: float
    close: float
    tx_count: int
    min: float
    max: float
    prev_close: float


class SwapHistory(BaseModel):
    pair: "DexPair"
    intervals: list[SwapInterval]

    @property
    def timestamps(self):
        return [s.start_time for s in self.intervals]

    @property
    def opens(self):
        return [s.open for s in self.intervals]

    @property
    def closes(self):
        return [s.close for s in self.intervals]

    @property
    def mins(self):
        return [s.min for s in self.intervals]

    @property
    def maxs(self):
        return [s.max for s in self.intervals]

    def __repr__(self):
        return f"<SwapHistory: {self.pair.address}>"

    __str__ = __repr__


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
    factory: DexFactory

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

    async def get_taxes(self):
        return await self.factory.get_taxes(
            self.token0.address,
            self.token1.address,
        )

    async def swap_history(
        self, use_token0: bool = True, start_time=None, end_time=None
    ):
        client = _force_get_global_client()
        feed = await client.prices.load_feed(
            self.address,
            use_token0=use_token0,
        )
        response = []
        for row in sorted(feed.split("\n"))[1:]:
            (
                interval,
                open,
                close,
                min,
                max,
                min_block,
                max_block,
                num_tx,
                prev_close,
            ) = row.split(",")
            response.append(
                SwapInterval(
                    start_time=datetime.strptime(interval, "%Y-%m-%d %H:%M:%S+00:00"),
                    open=float(open),
                    close=float(close),
                    min=float(min),
                    max=float(max),
                    tx_count=int(num_tx),
                    prev_close=float(prev_close if prev_close != "None" else open),
                )
            )
        return SwapHistory(pair=self, intervals=response)

    async def swap(
        self,
        wallet: Wallet,
        amount: int,
        priority_fee: int,
        is_private: bool,
        use_token0: bool,
    ):
        raise NotImplementedError()

    async def honeypot(self) -> bool:
        raise NotImplementedError()

    def __repr__(self):
        return f"<DexPair: {self.token0.symbol}, {self.token1.symbol}>"

    __str__ = __repr__
