import gzip
from typing import Optional

from eth_typing import HexAddress, ChecksumAddress
from eth_utils.address import to_checksum_address

from empyrealSDK.exc import handle_response_error
from empyrealSDK.utils import RequestHelpers


class PriceResource(RequestHelpers):
    async def get_taxes(
        self,
        token_address: ChecksumAddress,
        pair_token_address: ChecksumAddress,
        dex: str = "uniswap",
        chain_id: int = 1,
    ):
        response = await self._put(
            "token/taxes",
            json={
                "tokenAddress": token_address,
                "pairToken": pair_token_address,
                "chainId": chain_id,
                "dex": dex,
            },
        )
        handle_response_error(response)
        return response.json()

    async def get_routes(
        self,
        token_address: ChecksumAddress,
    ):
        response = await self._get(
            "dex/routes",
            params={
                "startToken": token_address,
            },
        )
        handle_response_error(response)
        return response.json()

    async def get_pair_info(
        self,
        pair_address: HexAddress,
        force_checksum: bool = True,
        chain_id: int = 1,
    ):
        """
        Get information about a specific pair addresss
        """

        if force_checksum:
            pair_address = to_checksum_address(pair_address)
        response = await self._get(
            "dex/pair",
            params={
                "pairAddress": pair_address,
                "chainId": chain_id,
            },
        )
        return response.json()

    async def get_token_pairs(
        self,
        token_address: HexAddress,
        chain_id: int = 1,
        force_checksum: bool = True,
    ):
        if force_checksum:
            token_address = to_checksum_address(token_address)
        response = await self._get(
            "dex/pairs",
            params={
                "tokenAddress": token_address,
                "chainId": chain_id,
            },
        )
        return response.json()["pairs"]

    async def get_liquidity(
        self,
        token_address: HexAddress,
        chain_id: int = 1,
        force_checksum: bool = True,
        block_number: Optional[int] = None,
    ):
        if force_checksum:
            token_address = to_checksum_address(token_address)
        response = await self._put(
            "dex/liquidity",
            json={
                "pairAddress": token_address,
                "chainId": chain_id,
                "blockNumber": block_number,
            },
        )
        handle_response_error(response)
        return response.json()

    async def load_feed(
        self,
        pair_address: ChecksumAddress,
        use_token0: bool = True,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ):
        response = await self._get(
            "price/",
            params={
                "pairAddress": pair_address,
                "useToken0": use_token0,
            },
        )
        handle_response_error(response)
        return gzip.decompress(response.content).decode("utf-8")
