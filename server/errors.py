from enum import IntEnum


class StatusCode(IntEnum):
    """Custom status codes for a WebSocket event."""

    SUCCESS = 200
    INVALID_ERROR = 4000
    ROOM_NOT_FOUND = 4001


class RoomNotFoundError(Exception):
    """Custom exception raised when joining a room with an invalid code."""

    def __init__(self, message: str) -> None:
        super().__init__(message)

        self.code = StatusCode.ROOM_NOT_FOUND
        self.message = message
