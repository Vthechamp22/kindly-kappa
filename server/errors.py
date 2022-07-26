from .codes import StatusCode
from .events import ErrorData, Event, EventType


class RoomNotFoundError(Exception):
    """Custom exception raised when joining a room with an invalid code."""

    def __init__(self, message: str) -> None:
        super().__init__(message)

        self.data = Event(type=EventType.ERROR, data=ErrorData(message=message), status_code=StatusCode.ROOM_NOT_FOUND)
