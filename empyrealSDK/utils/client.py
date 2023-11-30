from contextvars import ContextVar
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from empyrealSDK.sdk import EmpyrealSDK

_current_client: ContextVar[Optional["EmpyrealSDK"]] = ContextVar(
    "_current_client", default=None
)


def _get_global_client() -> Optional["EmpyrealSDK"]:
    return _current_client.get()


def _force_get_global_client():
    if not (client := _get_global_client()):
        raise ValueError("Must initialize EmpyrealSDK client first")
    return client


def _set_global_client(c: Optional["EmpyrealSDK"]) -> None:
    if c is not None:
        _current_client.set(c)


def _del_global_client(c: "EmpyrealSDK") -> None:
    if c == _current_client.get():
        _current_client.set(None)
