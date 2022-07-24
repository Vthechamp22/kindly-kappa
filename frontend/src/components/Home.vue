<script setup lang="ts">
import { ref, watch } from "vue";

const emit = defineEmits(["join"]);

// When the user clicks anyw0here outside of the modal, close it
const show_modal = ref(false);
const difficulty = ref(0);

window.onclick = function (event) {
  if (event.target == document.getElementById("myModal")) {
    show_modal.value = false;
  }
};

watch(difficulty, (newDiff) => {
  console.log(newDiff);
});
</script>

<template>
  <div id="main">
    <div id="login">
      <div
        class="tooltip"
        data-tip="japan PNG Designed By tsuki from https://pngtree.com/freepng/cute-kappa-in-japanese-mythology-cartoon-style_6544405.html?sol=downref&id=bef"
      >
        <img class="mx-auto" src="kappa-left.png" alt="kappa1" />
      </div>
      <div class="text-center">
        <h2>Kindly Kappas</h2>
        <form>
          <input
            type="text"
            placeholder="Room code"
            class="input input-bordered w-full max-w-xs"
          />
          <button class="btn btn-primary" @click.prevent="emit('join')">
            Join
          </button>
          <label
            for="create-room-modal"
            class="btn modal-button flex w-1/4 mx-auto my-2"
            >Create Room</label
          >
        </form>
      </div>
      <div
        class="tooltip"
        data-tip="cute PNG Designed By Reiko from https://pngtree.com/freepng/japanese-kappa-monster-cartoon_6544406.html?sol=downref&id=bef"
      >
        <img class="mx-auto" src="kappa-right.png" alt="kappa2" />
      </div>
    </div>

    <input type="checkbox" id="create-room-modal" class="modal-toggle" />
    <label for="create-room-modal" class="modal cursor-pointer">
      <label class="modal-box relative" for="">
        <label
          for="create-room-modal"
          class="btn btn-sm btn-circle absolute right-2 top-2"
        >
          <fa-icon icon="fa-solid fa-xmark" />
        </label>
        <h3 class="text-lg font-bold my-4">
          Choose Difficulty: {{ difficulty }}
        </h3>
        <input
          type="range"
          min="0"
          max="5"
          class="range w-full"
          step="1"
          v-model="difficulty"
        />
        <div class="w-full flex justify-between text-xs px-2">
          <span>|</span>
          <span>|</span>
          <span>|</span>
          <span>|</span>
          <span>|</span>
          <span>|</span>
        </div>
        <button class="btn my-4">Create</button>
      </label>
    </label>
  </div>
</template>
<style scoped>
#main {
  height: 100%;
}

#login {
  box-sizing: border-box;
  border: 4px solid white;

  display: grid;
  grid-template-columns: auto 512px auto;
  height: 100%;
  justify-items: center;
  align-items: center;
}

img {
  display: block;
  max-width: 50%;
  max-height: 50%;
  width: auto;
  height: auto;
}

h2 {
  font-size: 64px;
  color: white;
  margin: 12px;
}
</style>
