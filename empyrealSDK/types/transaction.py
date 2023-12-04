from eth_typing import HexStr
from pydantic import BaseModel


class Transaction(BaseModel):
    hash: HexStr
