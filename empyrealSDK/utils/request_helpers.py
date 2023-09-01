from typing import Any, Mapping, Optional, TYPE_CHECKING

import httpx
from httpx import Response
from httpx._types import PrimitiveData

if TYPE_CHECKING:
    from .. import EmpyrealSDK


class RequestHelpers:
    rpc_url: str
    api_key: str

    def __init__(self, sdk: "EmpyrealSDK"):
        self.rpc_url = sdk.rpc_url
        self.api_key = sdk.api_key

    async def _get(
        self, path: str, params: Optional[Mapping[str, PrimitiveData]] = None
    ) -> Response:
        async with httpx.AsyncClient() as client:
            return await client.get(
                f"{self.rpc_url}/{path}",
                headers={
                    "API-KEY": self.api_key,
                },
                params=params,
            )

    async def _post(self, path: str, json: Any) -> Response:
        async with httpx.AsyncClient() as client:
            return await client.post(
                f"{self.rpc_url}/{path}",
                json=json,
                headers={
                    "API-KEY": self.api_key,
                },
            )

    async def _put(self, path: str, json: Any) -> Response:
        async with httpx.AsyncClient() as client:
            return await client.put(
                f"{self.rpc_url}/{path}",
                json=json,
                headers={
                    "API-KEY": self.api_key,
                },
            )

    async def _delete(self, path: str) -> Response:
        async with httpx.AsyncClient() as client:
            return await client.delete(
                f"{self.rpc_url}/{path}",
                headers={
                    "API-KEY": self.api_key,
                },
            )
