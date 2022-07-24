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
    v-else
    @join="
      () => {
        joined = true;
      }
    "
  ></Home>
</template>
