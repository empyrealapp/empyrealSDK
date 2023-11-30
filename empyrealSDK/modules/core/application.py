from typing import Optional
from uuid import UUID

from empyrealSDK.utils import RequestHelpers
from empyrealSDK.types import Application
from empyrealSDK.exc import handle_response_error


class ApplicationResource(RequestHelpers):
    async def info(self):
        """Get basic info about the app given the provided SDK api_key

        Returns:
            Application: a dataclass containing the general information
        Raises:
            ValueError: If api key is invalid
        """
        response = await self._get("app/")
        if not response.status_code == 200:
            raise ValueError(response.json()["detail"])
        return Application(**response.json())

    async def update(
        self,
        swap_fee: Optional[int] = None,
        fee_collection_amount: Optional[int] = None,
        app_wallet_id: Optional[UUID] = None,
    ):
        """update app config.  Any fields left as `None` will be ignored.

        :returns: bool: If the update was successful or not
        """

        response = await self._put(
            "app/",
            json={
                "swapFee": swap_fee,
                "feeCollectionAmount": fee_collection_amount,
                "appWalletId": app_wallet_id,
            },
        )
        return response

    async def update_api_key(
        self,
    ):
        response = await self._put(
            "app/apikey",
        )
        handle_response_error(response)
        new_api_key = response.json()["apiKey"]
        self.sdk.api_key = new_api_key

        return new_api_key
