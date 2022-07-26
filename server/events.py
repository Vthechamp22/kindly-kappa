from __future__ import annotations

from enum import Enum
from typing import Literal, Mapping, TypedDict

from pydantic import BaseModel, validator

from .codes import StatusCode

Position = tuple[int, int]
Replacement = TypedDict("Replacement", {"from": int, "to": int, "value": str})


class EventType(str, Enum):
    """The type of a WebSocket event.

    It is declared as a subclass of str to help serialization.
    """

    CONNECT = "connect"
    DISCONNECT = "disconnect"
    SYNC = "sync"
    MOVE = "move"
    REPLACE = "replace"
    ERROR = "error"


class EventData(BaseModel):
    """The data of a WebSocket event.

    This is just a base class that other classes will inherit from.
    """


class ConnectData(EventData):
    """The data of a connection event.

    Fields:
        connection_type: "create" if the user wants to create the room, "join"
            if the user wants to join the room.
        difficulty (optional): The difficulty of the room, only needed if the
            "connection_type" is "create".
        room_code: The unique four-letters code that will represent the room.
        username: The username of the user creating or joining the room.
    """

    connection_type: Literal["create", "join"]
    difficulty: int | None
    room_code: str
    username: str


class DisconnectData(EventData):
    """The data of a disconnection event.

    Fields:
        username: The username of the user disconnecting.
    """

    username: str


class SyncData(EventData):
    """The data of a sync event.

    Fields:
        code: The code that already exists in the room.
        collaborators: The list of users that already collaborate in the room.
    """

    code: str
    collaborators: list[str]


class MoveData(EventData):
    """The data of a move event.

    Fields:
        position: The new position of the cursor.
    """

    position: Position


class ReplaceData(EventData):
    """The data of a replace event.

    Fields:
        code: A list of modifications to the code.
    """

    code: list[Replacement]


class ErrorData(EventData):
    """The data of an error event.

    Fields:
        message: The error message.
    """

    message: str


class Event(BaseModel):
    """A WebSocket event.

    Fields:
        type: The type of the event.
        data: The data of the event.
    """

    type: EventType
    data: EventData
    status_code: StatusCode

    @validator("data", pre=True)
    def valid_data(cls, value: EventData | Mapping, values):
        """Validates the data based on the event type."""
        if isinstance(value, EventData):
            value = value.dict()

        match values["type"]:
            case EventType.CONNECT:
                value = ConnectData(**value)
            case EventType.DISCONNECT:
                value = DisconnectData(**value)
            case EventType.SYNC:
                value = SyncData(**value)
            case EventType.REPLACE:
                value = ReplaceData(**value)
            case EventType.ERROR:
                value = ErrorData(**value)
        return value
