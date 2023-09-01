from enum import Enum, auto


class Network(Enum):
    Ethereum = 1
    Arbitrum = 42161


class LimitOrderType(Enum):
    TrailingStopLoss = auto()
    StopLoss = auto()
    TakeProfit = auto()


class Dex(Enum):
    Camelot = auto()
    Uniswap = auto()
    UniswapV3 = auto()
    SushiSwap = auto()
