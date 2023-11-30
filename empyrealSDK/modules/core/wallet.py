from typing import Optional
from uuid import UUID

from eth_typing import ChecksumAddress, HexStr
from httpx import Response

from empyrealSDK.utils import RequestHelpers
from empyrealSDK.exc import handle_response_error


class WalletResource(RequestHelpers):
    async def load(self, address: ChecksumAddress):
        response = await self._post(
            "wallets/noncustodial",
            json={
                "address": address,
            },
        )
        return response

    async def get_app_wallets(self, user_id: UUID) -> Response:
        response = await self._get("wallets/app", params={"userId": str(user_id)})
        handle_response_error(response)
        return response

    async def archive(self, wallet_id: UUID):
        response = await self._put(
            "wallets/archive",
            json={
                "walletId": wallet_id,
            },
        )
        handle_response_error(response)
        return response

    async def make_wallet(
        self,
        user_id: UUID,
        name: str,
        private_key: Optional[HexStr] = None,
    ):
        if private_key:
            return await self._make_pk_wallet(user_id, name, private_key)
        return await self._make_mnemonic_wallet(user_id, name)

    async def update_wallet_data(
        self,
        wallet_id: UUID,
        archive: bool = False,
        notes: dict[str, str] = {},
    ):
        return await self._put(
            "wallets/data",
            json={
                "walletId": str(wallet_id),
                "archived": archive,
                "notes": notes,
            },
        )

    async def get_wallet_data(
        self,
        wallet_id: UUID,
    ):
        return await self._get(
            f"wallets/data/{wallet_id}",
        )

    async def _make_mnemonic_wallet(self, user_id: UUID, name: str) -> Response:
        response = await self._post(
            "wallets/mnemonic",
            json={
                "userId": str(user_id),
                "name": name,
            },
        )
        handle_response_error(response)
        return response

    async def _make_pk_wallet(
        self,
        user_id: UUID,
        name: str,
        private_key: HexStr,
    ) -> Response:
        response = await self._post(
            "wallets/pk",
            json={
                "userId": str(user_id),
                "name": name,
                "privateKey": private_key,
            },
        )
        handle_response_error(response)
        return response
