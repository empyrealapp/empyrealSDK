from uuid import UUID

from eth_typing import ChecksumAddress

from empyrealSDK.exc import handle_response_error
from empyrealSDK.utils import RequestHelpers


class SwapResource(RequestHelpers):
    async def swap(
        self,
        path: list[ChecksumAddress],
        amount_in: int,
        wallet_id: UUID,
        slippage_percent: float = 0.01,
        priority_fee: int = 0,
        is_private: bool = False,
        chain_id: int = 1,
        use_eth: bool = True,
        fees: list[ChecksumAddress] = [],
        dex: str = "uniswap",
    ):
        response = await self._post(
            "dex/swap",
            json={
                "path": path,
                "amountIn": amount_in,
                "walletId": wallet_id,
                "slippage": slippage_percent,
                "priorityFee": priority_fee,
                "isPrivate": is_private,
                "chainId": chain_id,
                "useEth": use_eth,
                "fees": fees,
                "dex": dex,
            },
        )
        handle_response_error(response)
        return response.json()

    async def simulate(
        self,
        path: list[ChecksumAddress],
        amount_in: int,
        sender: ChecksumAddress,
        fees: list[ChecksumAddress] = [],
        dex: str = "uniswap",
        chain_id: int = 1,
        use_eth: bool = True,
    ):
        response = await self._put(
            "dex/simulate",
            json={
                "dex": dex,
                "path": path,
                "fees": fees,
                "amountIn": str(amount_in),
                "sender": sender,
                "chainId": chain_id,
                "useEth": use_eth,
            },
        )
        handle_response_error(response)
        return response.json()
