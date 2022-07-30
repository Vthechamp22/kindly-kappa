<script setup lang="ts">
import { ref } from "vue";

const min = ref(0);
const sec = ref(0);
const mil = ref(0);

setInterval(() => {
  mil.value = mil.value + 1;

  if (mil.value == 100) {
    sec.value = sec.value + 1;
    mil.value = 0;
  }

  if (sec.value == 60) {
    min.value = min.value + 1;
    sec.value = 0;
  }
}, 10);
</script>

<template>
  <div id="timer">
    {{ min.toString().padStart(2, "0") }} :
    {{ sec.toString().padStart(2, "0") }} :
    {{ mil.toString().padStart(2, "0") }}
  </div>
</template>

<style>
#timer {
  font-size: 70px;
  margin-bottom: 26px;
}
</style>
