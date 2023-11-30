from httpx import Response


class RateLimitError(Exception):
    """Raised when hitting rate limit"""


class NotFoundError(Exception):
    """Information was not found during execution"""


class UnknownError(Exception):
    """Unknown Error.  Please contact Empyreal Team"""


def handle_response_error(response: Response):
    if response.status_code == 429:
        raise RateLimitError(response.json()["detail"])
    elif response.status_code == 400:
        raise NotFoundError(response.json()["detail"])
    elif response.status_code == 500:
        raise UnknownError()


__all__ = [
    "RateLimitError",
    "UnknownError",
]
