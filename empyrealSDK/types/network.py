from enum import Enum


class Network(Enum):
    """
    An enum representing the different Networks supported by the SDK
    """

    Ethereum = 1
    # Arbitrum = 42161

    @property
    def chain_id(self):
        """Returns the Chain ID for a network"""
        return self.value
