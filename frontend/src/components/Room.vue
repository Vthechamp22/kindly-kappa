<script setup lang="ts">
import * as monaco from "monaco-editor";
import { onMounted, toRefs } from "vue";
import { onedark } from "../assets/js/theme";

const emit = defineEmits(["leave"]);
const props = defineProps({
  data: Object,
});

onMounted(() => {
  monaco.editor.defineTheme("OneDarkPro", onedark);
  monaco.editor.setTheme("OneDarkPro");

  monaco.editor.create(document.getElementById("content"), {
    value: "",
    language: "python",
    insertSpaces: true,
    theme: "OneDarkPro",
  });
});

function leaveRoom() {
  emit("leave");
}
</script>

<template>
  <div id="room">
    <div id="sidebar">
      <h2 class="text-6xl m-3">Collaborators</h2>
      <ul>
        <li>You ({{ data.username }})</li>
      </ul>
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

#sidebar {
  display: flex;
  flex-direction: column;
}

#sidebar,
#content {
  border: 3px solid hsl(var(--bc));
}

ul {
  text-align: center;
  align-self: center;
  font-size: 2em;
}

li {
  margin: 30px;
  text-align: left;
  font-size: 24px;
  margin-left: 48px;
  list-style: disc;
}
</style>
