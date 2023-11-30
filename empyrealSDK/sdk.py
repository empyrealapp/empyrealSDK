from typing import Literal

from .modules.dex import price

from .modules import core
from .utils.client import _set_global_client

ENVIRONMENTS = {
    "local": "http://localhost:8080",
    "prod": "https://api.empyrealsdk.com",
}


class EmpyrealSDK:
    """
    The EmpyrealSDK instance.  This is currently a global, singleton instance.
    So when a user initializes the empyrealSDK instance, this will be used automatically
    in all Empyreal types.

    Examples
    --------
    Initially in any codebase using the SDK, be sure to declare

    >>> from empyrealSDK import *
    >>> api_key = "<api_key>"
    >>> EmpyrealSDK(api_key)
    >>> app = Application.load()

    This will declare your SDK instance and inject it in all method invocations.
    Then when you call 5 :meth:`empyrealSDK.types.Application.load`, you are able to get the instance attached
    to your ``API_KEY``.
    """

    rpc_url: str
    api_key: str

    def __init__(self, api_key: str, env: Literal["local", "prod"] = "prod"):
        if env not in ENVIRONMENTS:
            raise ValueError(
                "Invalid Environment.  Must provide one of ['local', 'prod']"
            )
        self.rpc_url = ENVIRONMENTS[env]
        self.api_key = api_key

        self.app = core.ApplicationResource(self)
        self.infra = core.PingResource(self)
        self.token = core.TokenResource(self)
        self.user = core.UserResource(self)
        self.vault = core.VaultResource(self)
        self.wallet = core.WalletResource(self)
        self.prices = price.PriceResource(self)
        _set_global_client(self)
