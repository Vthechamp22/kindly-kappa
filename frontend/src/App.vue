<script setup lang="ts">
import { ref } from "vue";
import Room from "./components/Room.vue";
import Home from "./components/Home.vue";

const joined = ref(false);
</script>
<template>
  <Room
    v-if="joined"
    @join="
      () => {
        joined = false;
      }
    "
  ></Room>
  <Home
    @join="
      () => {
        joined = true;
      }
    "
    v-else
  ></Home>
</template>

<style scoped></style>
