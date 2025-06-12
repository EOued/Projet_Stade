const teams_div = document.getElementById("teams_div");
const fields_div = document.getElementById("fields_div");
//const settings_div = document.getElementById("settings_div");
const fit_div = document.getElementById("fit_div");

const load_file = document.getElementById("load_file");
const save_file = document.getElementById("save_file");

const box = document.getElementById("preview");

teams_div.addEventListener("click", () => {
  box.innerHTML =
    '<object width="100%" height="100%" type="text/html" data="/teams"</object>';
});

fields_div.addEventListener("click", () => {
  box.innerHTML =
    '<object width="100%" height="100%" type="text/html" data="/fields"</object>';
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
        const rawString = event.target.result; // This is your string
        fetch("http://localhost:5000/content_decoding", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            content: rawString,
          }),
        });

        console.log("Raw string:", rawString);
        // You can now save or send this string as-is
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

const channel = new BroadcastChannel("channel");
channel.onmessage = (event) => {
    console.log("Received", event.data);
  switch (event.data) {
    case "forbid-launch":
      document.getElementById("fit_div").classList.add("disabled");
      return;
    case "allow-launch":
      document.getElementById("fit_div").classList.remove("disabled");
      return;
    default:
      // Sending content of div to webserver`
      var content = box.innerHTML;
     console.log(box.contentWindow);
      console.log(content.querySelector(".entry"));
      box.innerHTML =
        '<object width="100%" height="100%" type="text/html" data="/toggable_calendar"</object>';
      return;
  }
};
