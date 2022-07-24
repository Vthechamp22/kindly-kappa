<script setup lang="ts">
import * as monaco from "monaco-editor";
import { onMounted } from "vue";
import { dracula } from "../assets/js/theme";

const emit = defineEmits(["join"]);

onMounted(() => {
  monaco.editor.defineTheme("Dracula", dracula);
  monaco.editor.setTheme("Dracula");

  monaco.editor.create(document.getElementById("content"), {
    value: "",
    language: "python",
    insertSpaces: true,
    theme: "Dracula",
  });
});

function leaveRoom() {
  monaco.editor.getModels().forEach((model) => model.dispose());
  emit("join", "leave");
}
</script>

<template>
  <div id="room">
    <div id="sidebar">
      <h2 class="text-6xl text-white m-3">Collaborators</h2>
      <ul>
        <li>You</li>
      </ul>
      <button class="btn btn-primary mt-auto" @click="leaveRoom()">
        <fa-icon icon="fa-solid fa-arrow-right-from-bracket" />
        Leave Room
      </button>
    </div>

    <div id="content"></div>
  </div>
</template>

<style scoped>
#room {
  height: 100%;
  display: grid;
  grid-template-columns: 1fr 3fr;
}

#content {
  text-align: left;
}

#sidebar,
#content {
  border: solid white;
}

#sidebar {
  border-width: 4px 2px 4px 4px;
}
#content {
  border-width: 4px 4px 4px 2px;
}

#sidebar h1 {
  text-align: center;
}

ul {
  text-align: center;
  font-size: 2em;
}

li {
  margin: 30px;
}

#sidebar,
#content {
  border: solid white;
  display: flex;
  flex-direction: column;
}

li {
  text-align: left;
  color: white;
  font-size: 24px;
  margin-left: 48px;
  list-style: disc;
}

.fa-arrow-right-from-bracket {
  -webkit-transform: scale(-1, 1);
  -moz-transform: scale(-1, 1);
  -ms-transform: scale(-1, 1);
  -o-transform: scale(-1, 1);
  transform: scale(-1, 1);
  margin-right: 1em;
}
</style>
