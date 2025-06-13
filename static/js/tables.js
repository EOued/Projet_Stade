// Basic functions

function is_row_selected() {
  return document.querySelectorAll(".row_selected").length > 0;
}

function unselect_all() {
  document
    .querySelectorAll(".row_selected")
    .forEach((element) => element.classList.remove("row_selected"));
}

function get_selected_row() {
  return document.querySelector(".row_selected");
}

function row_selected_interation(row, state) {
  row.querySelectorAll("input").forEach((element) => {
    element.readOnly = state;
  });
}

function row_selection(event) {
  const row = event.currentTarget;

  const old_row = document.querySelector(".row_selected");

  if (
    old_row &&
    !(
      old_row == row &&
      ["SELECT", "BUTTON", "INPUT"].includes(event.target.tagName)
    )
  )
    old_row.classList.remove("row_selected");

  if (row.id == "entry") {
    row_selected_interation(row, false);
    return;
  }

  if (row != old_row) row.classList.add("row_selected");

  row_selected_interation(row, document.querySelector(".row_selected") == null);
}

function sendForbidLaunch() {
  window.top.postMessage("forbid-launch");
}

function sendAllowLaunch() {
  window.top.postMessage("allow-launch");
}

function toArray(row) {
  console.log(row, Array.isArray(row));
  if (Array.isArray(row)) return row;
  return Array.from(row.querySelectorAll("td"), (cell) => cell.children[0])
    .filter((element) => element.classList.length > 0)
    .map((element) => {
      switch (element.tagName) {
        case "DIV":
          return parseInt(element.querySelector("input").value.trim());
        case "SELECT":
          return element.selectedIndex;
        default:
          return element.value.trim();
      }
    });
}

async function sendDivContent() {
  var type = new URL(window.location.href).pathname
    .split("/")
    .filter(Boolean)
    .pop();

  console.log("ids", ids);

  for (const [key, value] of Object.entries(ids)) {
    ids[key] = toArray(value);
  }

  console.log(ids);

  return fetch("/tables-send-data", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    cache: "no-cache",
    body: JSON.stringify({
      type: type,
      data: ids,
    }),
  });
}

async function openPopup(key) {
  await this.sendDivContent(ids);
  window.top.postMessage("open-cal-popup");
}

window.onmessage = async (event) => {
  if (["fields", "teams"].includes(event.data)) {
    if (Object.keys(ids).length != 0) await this.sendDivContent();
    window.top.postMessage(event.data);
  }
};
