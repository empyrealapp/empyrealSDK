# from typing import Optional
# from uuid import UUID
from httpx import Response

from empyrealSDK.utils import RequestHelpers
from empyrealSDK.exc import handle_response_error


class UserResource(RequestHelpers):
    async def get_from_telegram(self, telegram_id: str) -> Response:
        response = await self._get("users/telegram", params={"id": str(telegram_id)})
        handle_response_error(response)
        return response

    # async def get_grants(
    #     self,
    #     user_id: UUID,
    # ) -> Optional[Grant]:
    #     """Get the wallets and wallet types that have been approved by a user
    #        for the current app.

    #     A grant consists of a Grant object with additional GrantTypes.  The
    #     Grant is for the user, which can be pulled to immediately disable
    #     access to all wallets.  This is in contrast to the GrantType, which
    #     is for more granular control over a specific feature.  Initially,
    #     effort will be concentrated on a broad `GrantAllowType.allow_all`,
    #     which provides full access.

    #     Note:
    #         This naming convention may change, I'm on the fence...

    #     Returns:
    #         Grant: if grant is found for user
    #         None: If no grant has been made yet
    #     """
    #     response = await self._get(
    #         "grant/list",
    #         params={"userId": str(user_id)},
    #     )
    #     if response.json():
    #         return Grant(**response.json())
    #     else:
    #         return None

    # async def request_grant_from_user(
    #     self,
    #     wallet_id: UUID,
    #     grant_types: Optional[list[GrantType]] = None,
    # ):
    #     """Request a user to grant you access to their wallet.
    #     This will create a pending request in the user's telegram to accept
    #     your request for access.

    #     The number of grant request an app can send will be controlled based
    #     on their success rate to prevent spamming.

    #     Returns:
    #         bool: success status of request
    #     """
    #     response = await self._put(
    #         "grant/",
    #         json={
    #             "walletId": str(wallet_id),
    #             "grantType": (
    #                 [dict(gt) for gt in grant_types] if grant_types else None,
    #             ),
    #         },
    #     )
    #     return response.status_code == 200
