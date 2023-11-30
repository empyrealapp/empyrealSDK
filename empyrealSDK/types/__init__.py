# from enum import Enum, auto
from .application import Application
from .dex import DexFactory, DexPair
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
    "DexFactory",
    "DexPair",
    # "LimitOrderType",
    "Network",
    "Token",
    "TokenAmount",
    "User",
    "Wallet",
]
