from typing import Mapping
from uuid import UUID

from empyrealSDK.utils import RequestHelpers
from empyrealSDK.types.vault import VaultType, Vault


class VaultResource(RequestHelpers):
    async def get_all(
        self,
    ):
        """Get all vaults for an app

        This will show the general data for each vault

        :return: a list of `Vault`s
        """
        response = await self._get("vault/")
        return [Vault(**v) for v in response.json()["vaults"]]

    async def get_user_positions(
        self,
        user_id: UUID,
    ):
        """Get all vault positions for a user in your app

        This can be used to inspect a user and show them their current
        balance, or to help a user make determinations about how to
        allocate their escrowed funds across different positions.

        :return: A list of `VaultPosition`'s
        """

        response = await self._get(
            "vault/positions",
            params={"userId": str(user_id)},
        )

        return response.json()

    async def make_new_app_vault(
        self,
        token_id: UUID,
        type: VaultType,
        vault_name: str,
        description: str,
    ) -> Mapping[str, str]:
        """Creates a new app vault.  Currently there are two vault types:
            Bank: This is equivalent to wrapping tokens.  Dividends can be
                  issued to all users based on ownership share, but the user
                  will maintain their deposit regardless of what happens to
                  other accounts.
            Vault: This allows for shared earnings and losses distributed by
                   ownership stake in the vault.  This is designed for
                   applications that want to have a shared stake.

        ```python
        await emp_sdk.vault.make_new_app_vault(
            token.id,
            VaultType.bank,
            "UserFunds",
            "allows users to wrap funds into app",
        )
        await emp_sdk.vault.make_new_app_vault(
            token.id,
            VaultType.vault,
            "VolatileFunds",
            "allows users to buy shares of a volatile asset",
        )
        ```

        Returns:
            UUID: the new vault's UUID
        """
        response = await self._post(
            "vault/",
            json={
                "tokenId": str(token_id),
                "type": type.value,
                "vaultName": vault_name,
                "description": description,
            },
        )

        return response.json()
