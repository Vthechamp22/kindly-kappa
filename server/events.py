from __future__ import annotations

from enum import Enum
from typing import Literal, TypedDict

from pydantic import BaseModel

Position = tuple[int, int]
Replacement = TypedDict("Replacement", {"from": int, "to": int, "value": str})


class EventType(Enum):
    """The type of a WebSocket event."""

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


class ConnectionData(EventData):
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
    room_code: str
    difficulty: int | None
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
