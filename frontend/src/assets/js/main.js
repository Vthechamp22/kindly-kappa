function generateRoomCode(length = 4) {
  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  let roomCode = "";

  for (let i = 0; i < length; i++) {
    roomCode += alphabet.charAt(Math.floor(Math.random() * alphabet.length));
  }

  return roomCode;
}

let collaborators = [];
let code = "";
let connected = false;
let websocket;

let editor;
function setEditor(e) {
  editor = e.getModel();
  editor.setValue(code);

  const list = document.getElementById("collabul");
  collaborators.forEach((c) => {
    const elem = document.createElement("li");
    elem.id = `collaborator-${c.data.username}`;
    elem.appendChild(document.createTextNode(c.data.username));
    list.appendChild(elem);
  });
}

function positionToIndex(line, col) {
  let index = 0;

  for (let i = 1; i < line; i++) {
    index += editor.getLineLength(i) + 2;
  }

  return index + col - 1;
}

function connect(username, roomCode, difficulty, hackyObject) {
  const websocket = new WebSocket("ws://localhost:8000/room");

  websocket.onopen = function (ev) {
    connected = true;

    if (roomCode) {
      websocket.send(
        JSON.stringify({
          type: "connect",
          data: {
            username,
            room_code: roomCode,
            connection_type: "join",
            message: "you shouldn't be seeing this",
          },
        })
      );
    } else {
      websocket.send(
        JSON.stringify({
          type: "connect",
          data: {
            username,
            room_code: generateRoomCode(),
            connection_type: "create",
            difficulty: difficulty._value,
            message: "how are you seeing this?",
          },
        })
      );
    }
  };

  websocket.onmessage = function (ev) {
    const message = JSON.parse(ev.data);

    switch (message.type) {
      case "connect":
        collaborators.push(message.data);
        var list = document.getElementById("collabul");
        var elem = document.createElement("li");
        elem.id = `collaborator-${message.data.username}`;
        elem.appendChild(document.createTextNode(message.data.username));
        list.appendChild(elem);
        break;

      case "disconnect":
        collaborators = collaborators.filter((collaborator) => {
          return collaborator.id !== message.data.id;
        });
        var list = document.getElementById("collabul");
        var elem = document.getElementById(
          `collaborator-${message.data.username}`
        );
        list.removeChild(elem);
        break;

      case "sync":
        collaborators = message.data.collaborators;
        code = message.data.code;
        editor.setValue(code);

        hackyObject.switchToRoom();
        break;

      case "replace":
        for (let index = 0; index < message.data.code.length; index++) {
          const element = message.data.code[index];
          code =
            code.substring(0, element.from) +
            element.value +
            code.substring(element.to);
        }
        editor.setValue(code);
        break;

      case "error":
        if (message.status_code === 4001) {
          hackyObject.reportMissingRoom();
        }
        break;

      default:
        alert(`Invalid event type '${message.type}'`);
    }
  };

  websocket.onclose = function (ev) {
    connected = false;
    hackyObject.reportWSClose();
  };

  websocket.onerror = function (ev) {
    connected = false;
    hackyObject.reportConnectionError();
  };
}

window.handleContentChange = function (ev) {
  const changes = [];

  for (let i = 0; i < ev.changes.length; i++) {
    const element = ev.changes[i];

    changes.push({
      from: positionToIndex(
        element.range.startLineNumber,
        element.range.startColumn
      ),
      to: positionToIndex(element.range.endLineNumber, element.range.endColumn),
      value: element.text,
    });
  }

  if (connected) {
    websocket.send(
      JSON.stringify({
        type: "replace",
        data: {
          code: changes,
        },
      })
    );
  }
};
