from typing import Any, Mapping, Optional, TYPE_CHECKING

import httpx
from httpx import Response
from httpx._types import PrimitiveData

if TYPE_CHECKING:
    from .. import EmpyrealSDK


class RequestHelpers:
    def __init__(self, sdk: "EmpyrealSDK", version="v1"):
        self.sdk = sdk
        self.version = version

    @property
    def rpc_url(self):
        return self.sdk.rpc_url

    @property
    def api_key(self):
        return self.sdk.api_key

    async def _get(
        self, path: str, params: Optional[Mapping[str, PrimitiveData]] = None
    ) -> Response:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.rpc_url}/{self.version}/{path}",
                headers={
                    "API-KEY": self.api_key,
                },
                params=params,
            )
        return response

    async def _post(self, path: str, json: Any) -> Response:
        async with httpx.AsyncClient() as client:
            return await client.post(
                f"{self.rpc_url}/{self.version}/{path}",
                json=json,
                headers={
                    "API-KEY": self.api_key,
                },
            )

    async def _put(self, path: str, json: Any = {}) -> Response:
        async with httpx.AsyncClient() as client:
            return await client.put(
                f"{self.rpc_url}/{self.version}/{path}",
                json=json,
                headers={
                    "API-KEY": self.api_key,
                },
            )

    async def _delete(self, path: str) -> Response:
        async with httpx.AsyncClient() as client:
            return await client.delete(
                f"{self.rpc_url}/{self.version}/{path}",
                headers={
                    "API-KEY": self.api_key,
                },
            )
