from uuid import UUID

from eth_typing import ChecksumAddress
from pydantic import BaseModel, Field


class Token(BaseModel):
    id: UUID = Field()
    address: ChecksumAddress
    name: str
    symbol: str
    decimals: int
    chain_name: str = Field(alias="chain")
    chain_id: int = Field(alias="chainId")
    type: str
