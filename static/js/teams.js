let holdInterval;
var table = document.getElementById("table");

onLoad();

async function fetchContent() {
  console.log("UWU");
  return fetch("/teams-content")
    .then((response) => response.text())
    .then((data) => {
      ids = JSON.parse(data);
      console.log("data", data);
    });
}

async function onLoad() {
  id_max = 0;
  ids = {};

  await fetchContent();

  // fetching content from webserver
  console.log("loaded", ids);
  for (const [key, value] of Object.entries(ids)) {
    console.log(value);
    if (id_max <= parseInt(key)) id_max = parseInt(key) + 1;

    var row = document.getElementById("entry");

    const clone = row.cloneNode(true);
    clone.id = "";
    clone.addEventListener("click", row_selection);
    clone.querySelector(".id").readOnly = true;
    clone.querySelector(".id").addEventListener("input", (element) => {
      if (emptyName()) sendForbidLaunch();
      else sendAllowLaunch();
    });

    clone.querySelectorAll(".input").forEach((element) => {
      element.addEventListener("blur", () => {
        element.value = rectified_value(
          Number(element.value.trim()),
          Number(element.parentElement.dataset.min.trim),
          Number(element.parentElement.dataset.max.trim),
        );
      });
    });

    clone.querySelector(".id").value = value[0];
    clone.querySelector(".field_portion").selectedIndex = value[1];
    clone.querySelector(".gametime").querySelector("input").value = value[2];
    clone.querySelector(".priority").querySelector("input").value = value[3];
    clone.querySelector(".field_type").selectedIndex = value[4];

    clone.cells[row.cells.length - 1].innerHTML =
      `<a href="#" onclick="_openPopup(${id_max}); return false;">Click here</a>`;

    ids[key] = clone;
    table.tBodies[0].insertBefore(clone, row);
  }
  console.log(id_max);

  document.querySelectorAll(".input").forEach((element) => {
    element.addEventListener("blur", () => {
      element.value = rectified_value(
        Number(element.value.trim()),
        Number(element.parentElement.dataset.min.trim()),
        Number(element.parentElement.dataset.max.trim()),
      );
    });
  });

  document.addEventListener("keydown", (event) => {
    switch (event.key) {
      case "Enter":
        var activeElement = document.activeElement;

        if (
          activeElement.tagName == "INPUT" &&
          activeElement.parentElement.classList.contains("numbers_entry_div")
        ) {
          activeElement.value = rectified_value(
            Number(activeElement.value.trim()),
            Number(activeElement.parentElement.dataset.min.trim()),
            Number(activeElement.parentElement.dataset.max.trim()),
          );
          return;
        }
        if (!is_row_selected()) insert();
        if (emptyName()) sendForbidLaunch();
        else sendAllowLaunch();

        activeElement.blur();
        return;
      case "Escape":
        if (is_row_selected()) unselect_all();
        document.activeElement.blur();
        return;
      case "Delete":
        if (is_row_selected()) get_selected_row().remove();
      default:
        return;
    }
  });
}

function startHold(button, callback) {
  callback(button);
  holdInterval = setInterval(() => callback(button), 150);
}

function stopHold() {
  clearInterval(holdInterval);
}

function emptyName() {
  const exists = Array.from(table.rows).some((row) => {
    if (row.querySelector(".id") && row.id != "entry")
      return row.querySelector(".id").value.trim() == "";
  });
  return exists;
}

function minus(button) {
  const parent = button.parentElement;
  const input = parent.querySelector("input");
  const min = Number(parent.dataset.min) || 0;
  let value = Number(input.value);
  if (value > min) input.value = --value;
}

function plus(button) {
  const parent = button.parentElement;
  const input = parent.querySelector("input");
  const max = Number(parent.dataset.max);
  let value = Number(input.value);
  if (!max || value < max) input.value = ++value;
}

function rectified_value(value, min, max) {
  var retVal = value;
  if (value < min) retVal = min;
  if (value > max) retVal = max;
  return isNaN(retVal) ? 0 : retVal;
}

function insert() {
  var row = document.getElementById("entry");
  if (row.querySelector(".id").value == "") return;
  const clone = row.cloneNode(true);
  clone.id = "";
  clone.addEventListener("click", row_selection);
  clone.querySelector(".id").readOnly = true;

  var clone_copy = clone.querySelectorAll("select");
  var row_copy = row.querySelectorAll("select");
  clone.querySelector(".id").addEventListener("input", (element) => {
    if (emptyName()) sendForbidLaunch();
    else sendAllowLaunch();
  });

  clone.querySelectorAll(".input").forEach((element) => {
    element.addEventListener("blur", () => {
      console.log("UWU");
      element.value = rectified_value(
        Number(element.value.trim()),
        Number(element.parentElement.dataset.min.trim),
        Number(element.parentElement.dataset.max.trim),
      );
    });
  });

  for (var i = 0; i < clone_copy.length; i++) {
    clone_copy[i].value = row_copy[i].value;
  }

  clone.cells[row.cells.length - 1].innerHTML =
    `<a href="#" onclick="_openPopup(${id_max}); return false;">Click here</a>`;
  ids[id_max++] = clone;
  table.tBodies[0].insertBefore(clone, row);

  // Cleaning input
  clean_input(row);
}

function clean_input(row) {
  row.querySelector(".id").value = "";
  row.querySelector(".field_portion").value = "Terrain entier";
  row.querySelector(".field_type").value = "Terrain en herbe";
  row.querySelector(".gametime").querySelector("input").value = "0";
  row.querySelector(".priority").querySelector("input").value = "0";
}

function _openPopup(id) {
  openPopup("teams", id);
}
