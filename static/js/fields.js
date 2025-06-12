let holdInterval;
var table = document.getElementById("table");

var id_max = 0;
var ids = {};

document.getElementById("entry").addEventListener("click", row_selection);

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
      // Element clicked is name input of row that is not entry
      if (invalidName()) sendForbidLaunch();
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

function invalidName() {
  const values = [];
  let hasEmpty = false;
  let hasDuplicate = false;

  Array.from(table.rows).forEach((row) => {
    if (row.id === "entry") return;

    const field = row.querySelector(".field_id");
    if (!field) return;

    const value = field.value.trim();
    if (value == "") {
      hasEmpty = true;
      return;
    } else {
      if (values.includes(value)) {
        hasDuplicate = true;
        return;
      } else {
        values.push(value);
      }
    }
  });
  return hasEmpty || hasDuplicate;
}

function insert() {
  // Insertion control
  var row = document.getElementById("entry");
  if (row.querySelector(".field_id").value == "") return;

  // Clone setup

  const clone = row.cloneNode(true);
  clone.id = "";
  clone.querySelector(".field_id").readOnly = true;
  clone.cells[row.cells.length - 1].innerHTML =
    `<a href="#" onclick="_openPopup(${id_max}); return false;">Click here</a>`;
  ids[id_max++] = clone;

  // Copying selects

  var clone_copy = clone.querySelectorAll("select");
  var row_copy = row.querySelectorAll("select");

  for (var i = 0; i < clone_copy.length; i++) {
    clone_copy[i].value = row_copy[i].value;
  }

  // Cloning listeners

  clone.addEventListener("click", row_selection);
  clone.querySelector(".field_id").addEventListener("blur", () => {
    if (invalidName()) sendForbidLaunch();
    else sendAllowLaunch();
  });

  table.tBodies[0].insertBefore(clone, row);

  // Cleaning input
  clean_input(row);
}

function clean_input(row) {
  row.querySelector(".field_id").value = "";
  row.querySelector(".field_portion").value = "Terrain entier";
}

function _openPopup(id) {
  openPopup("fields", id, ids);
}
