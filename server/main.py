"""The main WebSocket server.

This server handles user connection, disconnection and events.
"""
from uuid import uuid4

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class Client:
    """A WebSocket client."""

    def __init__(self, websocket: WebSocket) -> None:
        """Initializes the WebSocket and the ID.

        A client is identified by an ID and contains the corresponding WebSocket
        that is used to send and receive messages.

        Args:
            websocket: A WebSocket instance.
        """
        self._websocket = websocket
        self.id = uuid4()

    async def accept(self) -> None:
        """Accepts the WebSocket connection."""
        await self._websocket.accept()

    async def send(self, data: dict) -> None:
        """Send JSON data over the WebSocket connection.

        Args:
            data: The data to be sent to the client, it should always contain a
                "type" key to indicate the event type.
        """
        await self._websocket.send_json(data)

    async def receive(self) -> dict:
        """Receive JSON data over the WebSocket connection.

        Returns:
            The data received from the client, it should always contain a "type"
            key to indicate the event type.
        """
        return await self._websocket.receive_json()


class ConnectionManager:
    """Manager for the WebSocket clients."""

    def __init__(self) -> None:
        """Initializes the active connections.

        It stores the active connections and is able to broadcast data.
        """
        self._rooms: dict[str, set[Client]] = {}

    async def connect(self, client: Client, room: str) -> None:
        """Accepts the connection and adds it to a room.

        If the room doesn't exist, create it.

        Args:
            client: The Client to which the connection belongs.
            room: The room to which the client will be connected.
        """
        await client.accept()

        if room not in self._rooms:
            self._rooms[room] = set()
        self._rooms[room].add(client)

    def disconnect(self, client: Client, room: str) -> None:
        """Removes the connection from the active connections.

        If, after the disconnection, the room is empty, delete it.

        Args:
            client: The Client to which the connection belongs.
            room: The room from which the client will be disconnected.
        """
        self._rooms[room].remove(client)

        if len(self._rooms[room]) == 0:
            del self._rooms[room]

    async def broadcast(self, data: dict, room: str) -> None:
        """Broadcasts data to all active connections.

        Args:
            data: The data to be sent to the clients, it should always contain a
                "type" key to indicate the event type.
            room: The room to which the data will be sent.
        """
        for connection in self._rooms[room]:
            await connection.send(data)


manager = ConnectionManager()


@app.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str) -> None:
    """This is the endpoint for the WebSocket connection.

    It creates a client and handles connection and disconnection with the
    ConnectionManager. It continuously receives and broadcasts data to the
    active clients.
    """
    client = Client(websocket)
    await manager.connect(client, room)

    try:
        while True:
            data = await client.receive()
            await manager.broadcast(data, room)
    except WebSocketDisconnect:
        manager.disconnect(client, room)
