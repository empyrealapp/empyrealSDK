from typing import Optional

from empyrealSDK.utils import RequestHelpers
from empyrealSDK.types.application import Application


class ApplicationResource(RequestHelpers):
    async def info(self):
        """Get basic info about the app given the provided SDK api_key

        Returns:
            Application: a dataclass containing the general information
        Raises:
            ValueError: If api key is invalid
        """
        response = await self._get("app/")
        return Application(**response.json())

    async def update(
        self,
        transfer_fee: Optional[int] = None,
        swap_fee: Optional[int] = 0,
        min_fee: Optional[int] = 0,
        max_fee: Optional[int] = 0,
        fee_collection_amount: Optional[int] = 0,
        owner_wallet_id: Optional[str] = None,
    ) -> bool:
        """update app config.  Any fields left as `None` will be ignored.

        Returns:
            bool: If the update was successful or not
        """

        response = await self._put(
            "app/",
            json={
                "ownerWalletId": owner_wallet_id,
                "transferFee": transfer_fee,
                "swapFee": swap_fee,
                "minFee": min_fee,
                "maxFee": max_fee,
                "feeCollectionAmount": fee_collection_amount,
            },
        )
        return response.status_code == 200
