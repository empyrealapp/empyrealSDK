from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .wallet import Wallet
from .user import User


class Application(BaseModel):
    id: UUID = Field()
    name: str
    type: str
    transfer_fee: int = Field(alias="transferFee")
    swap_fee: int = Field(alias="swapFee")
    min_fee: int = Field(alias="minFee")
    max_fee: int = Field(alias="maxFee")
    fee_collection_amount: int = Field(alias="feeCollectionAmount")
    request_count: int = Field(alias="requestCount")
    limit_order_count: int = Field(alias="limitOrderCount")

    # types
    owner: Optional[User] = Field()
    app_wallet: Optional[Wallet] = Field(alias="appWallet")
