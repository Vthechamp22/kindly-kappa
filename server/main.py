from uuid import uuid4

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()


class Client:
    """This class represents a client.

    A client is identified by an `id` and contains the corresponding WebSocket that is
    used to send and receive messages.
    """

    def __init__(self, websocket: WebSocket) -> None:
        """The initializer method.

        It initializes a private property `__websocket` and a public property `id`.
        """
        self.__websocket = websocket
        self.id = uuid4()

    async def accept(self) -> None:
        """Accepts a WebSocket connection."""
        await self.__websocket.accept()

    async def send(self, data: dict) -> None:
        """Send JSON data over the WebSocket connection."""
        await self.__websocket.send_json(data)

    async def receive(self) -> dict:
        """Receive JSON data over the WebSocket connection."""
        return await self.__websocket.receive_json()


class ConnectionManager:
    """This class manages the client connections.

    It stores the active connections in the private property `__active_connections`.
    """

    def __init__(self) -> None:
        """The initializer method.

        It initializes the active connections.
        """
        self.__active_connections: set[Client] = set()

    async def connect(self, client: Client) -> None:
        """Handles a client connection and adds it to the active connections."""
        await client.accept()
        self.__active_connections.add(client)

    def disconnect(self, client: Client) -> None:
        """Handles a client connection by removing it from the active connections."""
        self.__active_connections.remove(client)

    async def send(self, data: dict, client: Client) -> None:
        """Sends data to a given client."""
        await client.send(data)

    async def broadcast(self, data: dict) -> None:
        """Broadcasts data to all active connections."""
        for connection in self.__active_connections:
            await connection.send(data)


manager = ConnectionManager()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <input id="input" type="text" autocomplete="off">
        <button onclick="sendMessage(event)">Send</button>
        <ul id="messages"></ul>
        <script>
            let ws = new WebSocket("ws://localhost:8000/ws");

            ws.onmessage = function(event) {
                let data = JSON.parse(event.data);
                switch (data.type) {
                    case "message":
                        let messages = document.getElementById("messages");
                        let message = document.createElement("li");
                        let content = document.createTextNode(data.msg);
                        message.appendChild(content);
                        messages.appendChild(message);
                        break;
                    default:
                        console.log(`Unknown event type '${data.type}'`);
                }
            };

            function sendMessage(event) {
                let input = document.getElementById("input");
                let data = {type: "message", msg: input.value};
                ws.send(JSON.stringify(data));
                input.value = "";
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def chat() -> None:
    """This is the index route for the app.

    It returns the index HTML page.
    """
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """This is the endpoint for the WebSocket connection.

    It creates a client and handles the connection with the ConnectionManager. It continuosly receives, sends and
    broadcasts data accross the active clients.
    """
    client = Client(websocket)
    await manager.connect(client)
    await manager.broadcast({"type": "message", "msg": f"{client.id} joined the chat"})

    try:
        while True:
            data = await client.receive()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(client)
        await manager.broadcast({"type": "message", "msg": f"{client.id} left the chat"})
