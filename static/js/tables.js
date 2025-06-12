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

const channel = new BroadcastChannel("channel");

function sendForbidLaunch() {
  channel.postMessage("forbid-launch");
}

function sendAllowLaunch() {
  channel.postMessage("allow-launch");
}

function toArray(row) {
  return Array.from(row.querySelectorAll("td"), (cell) => cell.children[0])
    .filter((element) => element.classList.length > 0)
    .map((element) =>
      element.tagName == "DIV"
        ? element.querySelector("input").value.trim()
        : element.value.trim(),
    );
}

function openPopup(type, key, ids) {
  for (const [key, value] of Object.entries(ids)) {
    ids[key] = toArray(value);
  }

  console.log(ids);
  fetch("/tables-send-data", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      type: type,
      data: ids,
    }),
  });

  channel.postMessage(`${type} ${key}`);
}
