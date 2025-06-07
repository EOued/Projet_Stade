// Basic functions

let ignoreClick = false;
let blockBlur = false;

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
  if (ignoreClick) return;
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

function rectified_value(value, min, max) {
  if (value < min) return min;
  if (value > max) return max;
  return value;
}

var table = document.getElementById("table");

document.addEventListener("keydown", (event) => {
  var valid = "true";
  switch (event.key) {
    case "Enter":
      if (document.activeElement.tagName == "INPUT") {
        const element = document.activeElement;
        if (element.parentElement.classList.contains("numbers_entry_div")) {
          const parent = element.parentElement;

          element.value = rectified_value(
            Number(element.value.trim()),
            Number(parent.dataset.min.trim()),
            Number(parent.dataset.max.trim()),
          );
        } else if (
          element.classList.contains("id") &&
          (valid = isValidName(element.value, [
            document.getElementById("entry"),
          ]))
        ) {
          if (
            element.parentElement.parentElement.id == "entry" &&
            element.value != ""
          )
            insert();
          unselect_all();
        }
        if (!valid) _alert(element.value);
        return;
      }
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

function insert() {
  var row = document.getElementById("entry");
  const clone = row.cloneNode(true);
  clone.id = "";
  clone.addEventListener("click", row_selection);
  clone.querySelector(".id").readOnly = true;

  var clone_copy = clone.querySelectorAll("select");
  var row_copy = row.querySelectorAll("select");

  for (var i = 0; i < clone_copy.length; i++) {
    clone_copy[i].value = row_copy[i].value;
  }

  clone.querySelectorAll(".input").forEach((element) => {
    element.addEventListener("blur", () => {
      element.value = rectified_value(
        Number(element.value.trim()),
        Number(element.parentElement.dataset.min.trim),
        Number(element.parentElement.dataset.max.trim),
      );
    });
  });

  // clone.querySelector(".id").addEventListener(
  //   "blur",
  //   (element) => {
  //     console.log(element);
  //     if (blockBlur) return;
  //     if (
  //       isValidName(element.target.value.trim(), [
  //         document.getElementById("entry"),
  //         element.target,
  //       ])
  //     )
  //       return;
  //     ignoreClick = true;
  //     setTimeout(() => {
  //       ignoreClick = false;
  //     }, 3);
  //     blockBlur = true;
  //     _alert(element.target.value.trim());
  //     console.log("uwu");
  //     setTimeout(() => {
  //       blockBlur = false;
  //     }, 2);
  //   },
  //   true,
  // );

  clone.cells[row.cells.length - 1].innerHTML =
    '<a href="#" onclick="openPopup(this); return false;">Click here</a>';

  table.tBodies[0].insertBefore(clone, row);

  // Cleaning input

  clean_output(row);
}

document.addEventListener(
  "mousedown",
  (event) => {
    console.log(document.activeElement);
    if (
      document.activeElement &&
      document.activeElement.className.includes("id") &&
      document.activeElement.parentElement.parentElement.id != "entry" &&
      !isValidName(document.activeElement.value.trim(), [
        document.getElementById("entry"),
        document.activeElement,
      ])
    ) {
      _alert(document.activeElement.value.trim());
      ignoreClick = true;
      setTimeout(() => {
        ignoreClick = false;
      }, 3);

      document.activeElement.focus();
    }
  },
  true,
);

function isValidName(name, ignoreList) {
  if (name == "") {
    return false;
  }

  const exists = Array.from(table.rows).some((row) => {
    if (row.querySelector(".id") && !ignoreList.includes(row))
      return row.querySelector(".id").value.trim() == name;
  });

  if (exists) {
    blockBlur = false;
    return false;
  }
  return true;
}

function _alert(name) {
  if (name == "") {
    alert("Name can't be empty.");
    return;
  }
  alert(`The name ${name} already exist.`);
}

function clean_output(row) {
  row.querySelector(".id").value = "";
  row.querySelector(".field_portion").value = "Terrain entier";
  row.querySelector(".field_type").value = "Terrain en herbe";
  row.querySelector(".gametime").querySelector("input").value = "0";
  row.querySelector(".priority").querySelector("input").value = "0";
}
