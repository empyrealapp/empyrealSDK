from typing import Optional

from pydantic import BaseModel, Field


class Security(BaseModel):
    anti_whale_modifiable: bool = Field(alias="antiWhaleModifiable")
    buy_tax: float = Field(alias="buyTax")
    sell_tax: float = Field(alias="sellTax")
    can_take_back_ownership: bool = Field(alias="canTakeBackOwnership")
    cannot_buy: bool = Field(alias="cannotBuy")
    cannot_sell_all: bool = Field(alias="cannotSellAll")
    creator_address: str = Field(alias="creatorAddress")
    creator_balance: int = Field(alias="creatorBalance")
    creator_percent: float = Field(alias="creatorPercent")
    holder_count: int = Field(alias="holderCount")
    honeypot_with_same_creator: bool = Field(alias="honeypotWithSameCreator")
    is_anti_whale: bool = Field(alias="isAntiWhale")
    is_blacklisted: bool = Field(alias="isBlacklisted")
    is_honeypot: bool = Field(alias="isHoneypot")
    is_mintable: bool = Field(alias="isMintable")
    is_open_source: bool = Field(alias="isOpenSource")
    is_proxy: bool = Field(alias="isProxy")
    is_whitelisted: bool = Field(alias="isWhitelisted")
    lp_holder_count: int = Field(alias="lpHolderCount")
    lp_total_supply: float = Field(alias="lpTotalSupply")
    owner_address: str = Field(alias="ownerAddress")
    owner_balance: int = Field(alias="ownerBalance")
    owner_change_balance: bool = Field(alias="ownerChangeBalance")
    owner_percent: float = Field(alias="ownerPercent")
    total_supply: Optional[float] = Field(None, alias="total_supply")
    trading_cooldown: bool = Field(alias="tradingCooldown")
    transfer_pausable: bool = Field(alias="transferPausable")
