"""The main WebSocket server.

This server handles user connection, disconnection and events.
"""
from __future__ import annotations

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from server.client import Client
from server.connection_manager import ConnectionManager
from server.errors import RoomAlreadyExistsError, RoomNotFoundError
from server.event_handler import EventHandler
from server.events import ConnectData, EventType

app = FastAPI()


manager = ConnectionManager()


@app.websocket("/room")
async def room(websocket: WebSocket) -> None:
    """This is the endpoint for the WebSocket connection.

    It creates a client and handles connection and disconnection with the
    ConnectionManager. It continuously receives and broadcasts data to the
    active clients.
    """
    client = Client(websocket)
    await client.accept()

    handler = EventHandler(client, manager)

    initial_event = await client.receive()
    if initial_event.type != EventType.CONNECT:
        return

    initial_data: ConnectData = initial_event.data
    room_code = initial_data.room_code

    try:
        await handler(initial_event, room_code)
    except (RoomNotFoundError, RoomAlreadyExistsError) as err:
        await client.send(err.response)
        await client.close()
        return

    try:
        while True:
            event = await client.receive()
            await handler(event, room_code)
    except WebSocketDisconnect:
        pass
