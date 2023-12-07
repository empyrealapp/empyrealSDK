from typing import Literal, Optional, Union
from uuid import UUID

from eth_typing import ChecksumAddress, HexAddress, HexStr
from httpx import Response

from empyrealSDK.utils import RequestHelpers
from empyrealSDK.exc import handle_response_error


class TokenResource(RequestHelpers):
    async def lookup(self, token_address: HexAddress, chain_id: int = 1) -> Response:
        """Looks up a token's info in the SDK given it's address and chain id.
        This is useful for finding a token's id in the application.
        Using an ID instead of address and chain_id for the SDK simplifies
        the vault logic.

        Args:
            token_address: HexAddress a string in Hex String format
            chain_id: an int for the Chain ID

        Returns:
            Token
        """
        response = await self._get(
            "token/lookup",
            params={
                "address": token_address,
                "chainId": chain_id,
            },
        )
        handle_response_error(response)
        return response

    async def transfer(
        self,
        token_id: UUID,
        from_wallet_id: UUID,
        recipient_address: HexAddress,
        amount: int,
        gas_price: Optional[int] = None,
    ) -> HexStr:
        response = await self._get(
            "token/transfer",
            params={
                "walletId": str(from_wallet_id),
                "tokenId": str(token_id),
                "recipientAddress": recipient_address,
                "amount": amount,
                "gasPrice": gas_price,
            },
        )
        return response.json()

    async def security(
        self,
        token_id: UUID,
        chain_id: int,
    ):
        response = await self._get(
            "security/",
            params={
                "tokenId": str(token_id),
                "chainId": chain_id,
            },
        )
        handle_response_error(response)
        return response.json()["report"]

    async def balance_of(
        self,
        token_address: HexAddress,
        wallet_address: HexAddress,
        chain_id: int = 1,
        block_num: Union[int, Literal["latest"]] = "latest",
    ) -> int:
        response = await self._put(
            "token/balance",
            json={
                "tokenAddress": token_address,
                "ownerAddress": wallet_address,
                "chainId": chain_id,
                "block": block_num,
            },
        )
        handle_response_error(response)
        return response.json()["balance"]

    async def allowance(
        self,
        token_address: ChecksumAddress,
        owner_address: ChecksumAddress,
        spender_address: ChecksumAddress,
        chain_id: int = 1,
        block_num: Optional[Union[int, Literal["latest"]]] = "latest",
    ) -> int:
        response = await self._get(
            "token/allowance",
            params={
                "tokenAddress": token_address,
                "owner": owner_address,
                "spender": spender_address,
                "chainId": chain_id,
                "block": block_num,
            },
        )
        handle_response_error(response)
        return response.json()["allowance"]

    async def approve(
        self,
        token_id: UUID,
        wallet_id: UUID,
        spender_address: ChecksumAddress,
        chain_id: int = 1,
        amount: int = int(2**256 - 1),
        priority_fee: int = 0,
    ):
        response = await self._post(
            "token/approve",
            json={
                "tokenId": token_id,
                "walletId": wallet_id,
                "spender": spender_address,
                "chainId": chain_id,
                "amount": amount,
                "priorityFee": priority_fee,
            },
        )
        handle_response_error(response)
        return response.json()["txHash"]
