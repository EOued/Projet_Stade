const teams_div = document.getElementById("teams_div");
const fields_div = document.getElementById("fields_div");
//const settings_div = document.getElementById("settings_div");
const fit_div = document.getElementById("fit_div");

const load_file = document.getElementById("load_file");
const save_file = document.getElementById("save_file");

const iframe = document.getElementById("iframe");

var isIFrameLoaded = false;

teams_div.addEventListener("click", () => {
  if (isIFrameLoaded) iframe.contentWindow.postMessage("teams");
  else iframe.src = "/teams";
  isIFrameLoaded = false;
});

fields_div.addEventListener("click", () => {
  if (isIFrameLoaded) iframe.contentWindow.postMessage("fields");
  iframe.src = "/fields";
  isIFrameLoaded = false;
});

iframe.addEventListener("load", () => {
  isIFrameLoaded = true;
  var innerDoc = iframe.contentDocument
    ? iframe.contentDocument
    : iframe.contentWindow.document;
  console.log(innerDoc.getElementById("table"));
});

load_file.addEventListener("click", () => {
  const fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.style.display = "none";
  fileInput.accept = ".get";

  fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (event) {
        const rawString = event.target.result;
        fetch("http://localhost:5000/content_decoding", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            content: rawString,
          }),
        });

        console.log("Raw string:", rawString);
      };

      reader.readAsText(file);
    }
  });

  document.body.appendChild(fileInput);
  fileInput.click();
  document.body.removeChild(fileInput);
});

save_file.addEventListener("click", () => {
  // Ask webserver for content
  var content;
  fetch("/content_encoding")
    .then((response) => response.text())
    .then((data) => {
      content = data;
      console.log(data);

      const blob = new Blob([content], { type: "text/plain" });
      const url = URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "example.get"; // User can rename in the browser's save dialog
      a.click();

      URL.revokeObjectURL(url); // Clean up
    })
    .catch((error) => {
      console.log("Error:", error);
    });
});

window.onmessage = (event) => {
  console.log("Received", event.data);
  switch (event.data) {
    case "forbid-launch":
      document.getElementById("fit_div").classList.add("disabled");
      return;
    case "allow-launch":
      document.getElementById("fit_div").classList.remove("disabled");
      return;
    case "teams":
      iframe.src = "/teams";
      return;
    case "fields":
      iframe.src = "/fields";
    default:
      return;
  }
};
