from typing import cast

from server.client import Client
from server.codes import StatusCode
from server.connection_manager import ConnectionManager
from server.events import (
    ConnectData,
    ErrorData,
    EventRequest,
    EventResponse,
    EventType,
    MoveData,
    ReplaceData,
    SyncData,
)
from server.room import Room


class EventHandler:
    """An request event handler."""

    def __init__(self, client: Client, manager: ConnectionManager):
        """Initializes the event handler for each client.

        Args:
            client: The client sending the requests.
            connection: The connection to the room.
        """
        self.client = client
        self.manager = manager

        self.room: Room

    async def __call__(self, request: EventRequest, room_code: str) -> None:
        """Handle a request received.

        Args:
            request: The data received from the client.
            room_code: The room to which the data will be sent.

        Raises:
            WebSocketDisconnect: If the event type is a disconnect.
            NotImplementedError: In any other case.
        """
        event_data = request.data

        match request.type:
            case EventType.CONNECT:
                connect_data = cast(ConnectData, event_data)
                self.client.username = connect_data.username

                match connect_data.connection_type:
                    case "create":
                        if connect_data.difficulty is None:
                            response = (
                                EventResponse(
                                    type=EventType.ERROR,
                                    data=ErrorData(message="Data not found."),
                                    status_code=StatusCode.DATA_NOT_FOUND,
                                ),
                            )
                            await self.client.send(response)
                            return

                        self.manager.create_room(self.client, connect_data.room_code, connect_data.difficulty)
                        self.room = self.manager._rooms[room_code]
                    case "join":
                        self.manager.join_room(self.client, room_code)
                        self.room = self.manager._rooms[room_code]

                        collaborators = [{"id": c.id.hex, "username": c.username} for c in self.room.clients]

                        # Send a sync event to the client to update the code and
                        # the collaborators' list
                        response = EventResponse(
                            type=EventType.SYNC,
                            data=SyncData(code=self.room.code, collaborators=collaborators),
                            status_code=StatusCode.SUCCESS,
                        )
                        await self.client.send(response)

                        # Broadcast to other clients a connect event to update
                        # the collaborators' list
                        response = EventResponse(
                            type=EventType.CONNECT,
                            data=connect_data,
                            status_code=StatusCode.SUCCESS,
                        )
                        await self.manager.broadcast(response, room_code, sender=self.client)
            case EventType.DISCONNECT:
                collaborators = [{"id": c.id.hex, "username": c.username} for c in self.room.clients]

                # Broadcast to other clients a sync event to update the
                # collaborators' list
                response = EventResponse(
                    type=EventType.SYNC,
                    data=SyncData(code=self.room.code, collaborators=collaborators),
                    status_code=StatusCode.SUCCESS,
                )
                await self.manager.broadcast(response, room_code, sender=self.client)

                self.manager.disconnect(self.client, room_code)
            case EventType.MOVE:
                move_data = cast(MoveData, event_data)
                self.room.cursors[self.client.id] = move_data.position

                # Broadcast to every client a move event to update the cursors'
                # positions
                response = EventResponse(type=EventType.MOVE, data=move_data, status_code=StatusCode.SUCCESS)
                await self.manager.broadcast(response, room_code, sender=self.client)
            case EventType.REPLACE:
                replace_data = cast(ReplaceData, event_data)
                self.room.update_code(replace_data)

                # Broadcast to every client a replace event to update the code
                response = EventResponse(type=EventType.REPLACE, data=replace_data, status_code=StatusCode.SUCCESS)
                await self.manager.broadcast(response, room_code, sender=self.client)
            case EventType.SEND_BUGS:
                self.room.introduce_bugs()

                collaborators = [{"id": c.id.hex, "username": c.username} for c in self.room.clients]

                # Broadcast to other clients a sync event to update the code
                response = EventResponse(
                    type=EventType.SYNC,
                    data=SyncData(code=self.room.code, collaborators=collaborators),
                    status_code=StatusCode.SUCCESS,
                )
                await self.manager.broadcast(response, room_code, sender=self.client)
            case _:
                # Anything that doesn't match the request.type
                response = EventResponse(
                    type=EventType.ERROR,
                    data=ErrorData(message="This has not been implemented yet."),
                    status_code=StatusCode.DATA_NOT_FOUND,
                )
                await self.client.send(response)
