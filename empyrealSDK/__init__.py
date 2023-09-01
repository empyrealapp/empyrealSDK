from typing import Literal
from .modules import core


ENVIRONMENTS = {
    "local": "http://localhost:5001",
    "prod": "TBD",
}


class EmpyrealSDK:
    rpc_url: str
    api_key: str

    def __init__(self, api_key: str, env: Literal["local", "prod"] = "local"):
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
