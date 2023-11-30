from typing import Optional

from eth_typing import HexAddress
from eth_utils.address import to_checksum_address

from empyrealSDK.exc import handle_response_error
from empyrealSDK.types import DexPair, Network, Token
from empyrealSDK.utils import RequestHelpers


class PriceResource(RequestHelpers):
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
        response_json = response.json()
        token0 = Token(**response_json["token0"])
        token1 = Token(**response_json["token1"])
        return DexPair(
            factory_address=response_json["factoryAddress"],
            token0=token0,
            token1=token1,
            address=response_json["pairAddress"],
            index=response_json["index"],
            fee=response_json["feePercentage"],
            network=Network(response_json["chainId"]),
            block_number=response_json["blockNumber"],
            transaction_hash=response_json["transactionHash"],
        )

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
        return [
            DexPair(
                factory_address=row["factoryAddress"],
                token0=Token(**row["token0"]),
                token1=Token(**row["token1"]),
                address=row["pairAddress"],
                index=row["index"],
                fee=row["feePercentage"],
                network=Network(row["chainId"]),
                block_number=row["blockNumber"],
                transaction_hash=row["transactionHash"],
            )
            for row in response.json()["pairs"]
        ]

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
