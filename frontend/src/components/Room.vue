<script setup lang="ts">
import * as monaco from "monaco-editor"; // skipcq: JS-C1003
import Timer from "./Timer.vue";
import { onMounted, ref, toRaw } from "vue";
import { themes } from "../assets/js/theme";

const props = defineProps({
  state: Object,
  sync: Object,
});
const emit = defineEmits(["leaveRoom"]);

let collaborators = ref(toRaw(props.sync?.collaborators));
let code = props.sync?.code; // skipcq: JS-V005
let editor: monaco.editor.IStandaloneCodeEditor;

onMounted(() => {
  for (let theme of themes) {
    monaco.editor.defineTheme(theme.name, theme.theme);
  }
  const theme = document.querySelector("body").getAttribute("data-theme");

  let e = monaco.editor.create(document.getElementById("content"), {
    value: "",
    language: "python",
    insertSpaces: true,
    theme,
  });

  editor.getModel()?.onDidChangeContent(contentHandler);
  editor.getModel()?.setValue(code);
  editor.getModel()?.setEOL(0);
});

/**
 * Function to conver the editor lines to index positions.
 */
function positionToIndex(line, col) {
  let index = 0;
  for (let i = 1; i < line; i++) {
    index += code.split("\n")[i - 1].length + 1;
  }
  return index + col - 1;
}

/**
 * Function to transform content into JSOn serializable content.
 */
function contentHandler(ev) {
  if (code === editor.getModel()?.getValue()) return;

  const changes = ev.changes.map((change) => {
    return {
      from: positionToIndex(
        change.range.startLineNumber,
        change.range.startColumn
      ),
      to: positionToIndex(change.range.endLineNumber, change.range.endColumn),
      value: change.text,
    };
  });

  props.state?.websocket.send(
    JSON.stringify({
      type: "replace",
      data: {
        code: changes,
      },
    })
  );

  code = editor.getModel()?.getValue();
}

/**
 * Function to receive events from the server.
 */
// skipcq: JS-0611
props.state.websocket.onmessage = function (ev) {
  const message = JSON.parse(ev.data);

  switch (message.type) {
    case "connect":
      collaborators.value.push(message.data);
      break;

    case "disconnect":
      collaborators.value = collaborators.value.filter((c) => {
        return c.id !== message.data.id;
      });
      break;

    case "replace":
      message.data.code.forEach((change) => {
        code =
          code.substring(0, change.from) +
          change.value +
          code.substring(change.to);
      });
      editor.setValue(code);
  }
};

if (!collaborators.value.length) {
  setInterval(() => {
    props.state?.websocket.send(
      JSON.stringify({
        type: "sync",
        data: {
          code: code,
        },
      })
    );
  }, 30000);
}

/**
 * Function for a client to leave a room.
 */
function leaveRoom() {
  props.state?.websocket.send(
    JSON.stringify({
      type: "disconnect",
      data: {},
    })
  );
  emit("leaveRoom");
}
</script>

<template>
  <div id="room">
    <div id="sidebar">
      <h2 class="text-6xl text-white m-3">Collaborators</h2>
      <ul style="margin-left: 20px">
        <li v-for="collaborator in collaborators" :key="collaborator.id">
          {{ collaborator.username }}
        </li>
      </ul>
      <div id="info">
        <Timer :time="props.sync?.time"></Timer>
        <p>Username: {{ props.state?.username }}</p>
        <p>Room: {{ props.state?.roomCode }}</p>
        <p>Owner: undefined</p>
      </div>
      <ul id="collabul"></ul>
      <button class="btn btn-primary mt-auto" @click="leaveRoom">
        <i class="gg-log-out mr-4"></i>
        Leave Room {{ props.state?.roomCode }}
      </button>
    </div>

    <div id="content">
      <div id="container"></div>
    </div>
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
  padding: 4px;
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

#container {
  text-align: left;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

#info {
  position: absolute;
  left: 20px;
  bottom: 68px;
  font-size: 24px;
  text-align: left;
  line-height: 24px;
}
</style>
