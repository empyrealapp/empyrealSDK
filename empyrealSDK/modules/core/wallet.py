from typing import Optional
from uuid import UUID

from eth_typing import ChecksumAddress, HexStr
from httpx import Response

from empyrealSDK.utils import RequestHelpers


class WalletResource(RequestHelpers):
    async def info(
        self,
        wallet_id: UUID,
        with_private_key: bool = False,
    ):
        response = await self._get(
            "wallets/",
            params={
                "walletId": str(wallet_id),
                "withPrivateKey": with_private_key,
            },
        )
        return response.json()

    async def load(self, address: ChecksumAddress):
        response = await self._post(
            "wallets/noncustodial",
            json={
                "address": address,
            },
        )
        return response.json()

    async def get_app_wallets(self) -> Response:
        response = await self._get("wallets/app")
        return response.json()

    async def get_user_wallets(self, user_id: UUID) -> Response:
        response = await self._get("wallets/user", params={"userId": str(user_id)})
        return response.json()

    async def archive(self, wallet_id: UUID):
        response = await self._put(
            "wallets/archive",
            json={
                "walletId": wallet_id,
            },
        )
        return response

    async def make_app_wallet(
        self,
        name,
        private_key: Optional[HexStr] = None,
    ):
        """
        Make an app wallet
        """
        return await self._make_pk_wallet(name, private_key)

    async def make_user_wallet(
        self,
        user_id: UUID,
        name: str,
        private_key: Optional[HexStr] = None,
    ):
        """
        Make a wallet for a user.
        """
        if private_key:
            return await self._make_pk_wallet(name, private_key, user_id=user_id)
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
        return response

    async def _make_pk_wallet(
        self,
        name: str,
        private_key: Optional[HexStr] = None,
        user_id: Optional[UUID] = None,
    ) -> Response:
        response = await self._post(
            "wallets/pk",
            json={
                "name": name,
                "privateKey": private_key,
                "userId": user_id,
            },
        )
        return response
