from typing import Optional
from uuid import UUID

from eth_typing import HexAddress, HexStr

from empyrealSDK.types.token import Token
from empyrealSDK.utils import RequestHelpers


class TokenResource(RequestHelpers):
    async def lookup(self, token_address: HexAddress, chain_id: int) -> Token:
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
        return Token(**response.json())

    async def transfer(
        self,
        wallet_id: UUID,
        token_id: UUID,
        recipient_address: HexAddress,
        amount: int,
        gas_price: Optional[int] = None,
    ) -> HexStr:
        response = await self._get(
            "token/lookup",
            params={
                "walletId": str(wallet_id),
                "tokenId": str(token_id),
                "recipientAddress": recipient_address,
                "amount": amount,
                "gasPrice": gas_price,
            },
        )
        return response.json()
