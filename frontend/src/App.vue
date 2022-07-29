<script setup lang="ts">
import { ref } from "vue";
import Room from "./components/Room.vue";
import Home from "./components/Home.vue";

const roomStatus = ref({
  code: "",
  username: "",
  joined: false,
});

/**
 * Function to leave a room.
 */
function leaveRoom() {
  roomStatus.value = { ...roomStatus.value, joined: false };
}

/**
 * Function to join a room.
 */
function joinRoom({ code, username }) {
  roomStatus.value = {
    code,
    username,
    joined: true,
  };
}
</script>

<template>
  <Room v-if="roomStatus.joined" @leave="leaveRoom" :data="roomStatus"></Room>
  <Home v-else @join="joinRoom"></Home>
</template>
