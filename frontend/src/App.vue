<script setup>
import { ref } from "vue";
import Room from "./components/Room.vue";
import Home from "./components/Home.vue";

/**
 * Function to generate a room code.
 * @param length The number of characters.
 * @returns A randomly generated, uppercase, code.
 */
function generateCode(length = 4) {
  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  let code = "";
  for (let i = 0; i < length; i++) {
    code += alphabet.charAt(Math.floor(Math.random() * alphabet.length));
  }
  return code;
}

const websocket = new WebSocket("ws://localhost:8000/room");
websocket.onerror = function () {
  alert(`Oh no! Something has gone very wrong
This genuinely is a bug, not a feature :(`);
};
websocket.onclose = function () {
  alert(`The websocket closed... why?`);
};

const joined = ref(false);
const state = ref({
  roomCode: "",
  username: "",
  websocket,
});

const sync = ref({
  collaborators: [],
  code: "",
  difficulty: 0,
  time: undefined,
});
let joining = false;

/**
 * Function to join a room.
 */
function joinRoom({ username, roomCode }) {
  if (joining) return;
  joining = true;

  roomCode = roomCode.toUpperCase();

  websocket.send(
    JSON.stringify({
      type: "connect",
      data: {
        connection_type: "join",
        room_code,
        username,
      },
    })
  );

  state.value = {
    roomCode,
    username,
    websocket,
  };
}

/**
 * Function to create a room.
 */
function createRoom({ username, difficulty }) {
  if (joining) return;
  joining = true;

  const roomCode = generateCode();

  websocket.send(
    JSON.stringify({
      type: "connect",
      data: {
        connection_type: "create",
        difficulty,
        room_code: roomCode,
        username,
      },
    })
  );

  state.value = {
    roomCode,
    username,
    websocket,
  };
}

websocket.onmessage = function (ev) {
  const message = JSON.parse(ev.data);

  if (message.type === "sync") {
    sync.value = {
      collaborators: message.data.collaborators,
      code: message.data.code,
      difficulty: message.data.difficulty,
      time: message.data.time,
    };
    joined.value = true;
  }

  if (message.type === "error") {
    joining = false;
  }
};

/**
 * Function to leave a room.
 */
function leaveRoom() {
  console.log(websocket);
  joined.value = false;
  console.log(websocket);
  joining = false;
}
</script>

<template>
  <Room v-if="joined" :state="state" :sync="sync" @leaveRoom="leaveRoom"></Room>
  <Home v-else @joinRoom="joinRoom" @createRoom="createRoom"></Home>
</template>
