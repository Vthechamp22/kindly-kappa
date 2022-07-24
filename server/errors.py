class InvalidCodeError(Exception):
    """Custom exception raised when joining a room with an invalid code."""

    def __init__(self, message: str, code: str) -> None:
        super().__init__(message)

        self.code = code
        self.message = message
