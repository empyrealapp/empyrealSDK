# from enum import Enum, auto
from .application import Application
from .dex import Liquidity, DexFactory, DexPair, DexRoute, SwapHistory
from .network import Network
from .token import Token, TokenAmount
from .user import User
from .wallet import Wallet


# class LimitOrderType(Enum):
#     TrailingStopLoss = auto()
#     StopLoss = auto()
#     TakeProfit = auto()


# class Dex(Enum):
#     Camelot = auto()
#     Uniswap = auto()
#     UniswapV3 = auto()
#     SushiSwap = auto()


__all__ = [
    "Application",
    # "Dex",
    "Liquidity",
    "DexFactory",
    "DexPair",
    "DexRoute",
    # "LimitOrderType",
    "Network",
    "SwapHistory",
    "Token",
    "TokenAmount",
    "User",
    "Wallet",
]
