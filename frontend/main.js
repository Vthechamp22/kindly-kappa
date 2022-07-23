// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == document.getElementById("myModal")) {
    document.getElementById("myModal").style.display = "none";
  }
};

function showCRDialog() {
  event.preventDefault();
  document.getElementById("myModal").style.display = "block";
  document.getElementsByClassName("close")[0].onclick = function () {
    document.getElementById("myModal").style.display = "none";
  };
}

function connect() {
  event.preventDefault();
  document.getElementById("login").style.display = "none";
  document.getElementById("room").style.display = "block";

  require.config({ paths: { vs: "node_modules/monaco-editor/min/vs" } });

  require(["vs/editor/editor.main"], function () {
    monaco.editor.defineTheme("Dracula", dracula);
    monaco.editor.setTheme("Dracula");

    editor = monaco.editor.create(document.getElementById("content"), {
      value: "",
      language: "python",
      insertSpaces: true,
      theme: "Dracula",
    });
  });
}

function updateDifficulty(value) {
  console.log(value);
}

function leaveRoom() {
  monaco.editor.getModels().forEach((model) => model.dispose());
  document.getElementById("room").style.display = "none";
  document.getElementById("login").style.display = "block";
}
