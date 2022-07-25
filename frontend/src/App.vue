<script setup lang="ts">
import { ref } from "vue";
import Room from "./components/Room.vue";
import Home from "./components/Home.vue";

const joined = ref(false);

function leaveRoom() {
  joined.value = false;
}

function joinRoom(roomCode) {
  console.log(roomCode);
  joined.value = true;
}
</script>

<template>
  <Room v-if="joined" @leave="leaveRoom"></Room>
  <Home v-else @join="joinRoom"></Home>
</template>
