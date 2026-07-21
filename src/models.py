from json import dumps


class NetboxError(Exception):
    """Base exception for Netbox errors.

    Args:
        message (str): Description of the error.
        error (str): Content from the error itself.
        status_code (int): HTTP status code.
    """
    def __init__(self, message: str, error: str, status_code: int, *args) -> None:
        self.message = message
        self.error: str = error
        self.status_code = status_code
        super().__init__(*args)

    def __str__(self) -> str:
        return dumps({
            "message": self.message,
            "error": self.error,
            "status_code": self.status_code,
        })

