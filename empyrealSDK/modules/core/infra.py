from empyrealSDK.utils import RequestHelpers


class PingResource(RequestHelpers):
    async def say_hi(self):
        """ping method to test connection"""
        response = await self._get("ping")
        return response.json()
