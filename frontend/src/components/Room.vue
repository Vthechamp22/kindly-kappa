<script setup lang="ts">
import * as monaco from "monaco-editor";
import { onMounted } from "vue";
import { themes } from "../assets/js/theme";

const emit = defineEmits(["join"]);

onMounted(() => {
  for (let theme of themes) {
    monaco.editor.defineTheme(theme.name, theme.theme);
  }
  const theme = document
    .querySelector('body')
    .getAttribute('data-theme')

  let e = monaco.editor.create(document.getElementById("content"), {
    value: "",
    language: "python",
    insertSpaces: true,
    theme,
  });

  e.getModel()?.onDidChangeContent(window.handleContentChange);
});

function leaveRoom() {
  monaco.editor.getModels().forEach((model) => model.dispose());
  emit("join", "leave");
}
</script>

<template>
  <div id="room">
    <div id="sidebar">
      <h2 class="text-6xl m-3">Collaborators</h2>
      <ul id="collabul"></ul>
      <button class="btn btn-primary mt-auto" @click="leaveRoom()">
        <i class="gg-log-out mr-4"></i>
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
  border: solid hsl(var(--bc));
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
  display: flex;
  flex-direction: column;
}

li {
  text-align: left;
  color: hsl(var(--bc));
  font-size: 24px;
  margin-left: 48px;
  list-style: disc;
}
</style>
