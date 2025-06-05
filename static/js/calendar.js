let draggable = false;
let color;

function toggleColor(element) {
  var style = window
    .getComputedStyle(element, null)
    .getPropertyValue("background-color");

  switch (style) {
    case "rgb(159, 159, 159)":
      element.style.backgroundColor = "#52b788";
      break;
    default:
      element.style.backgroundColor = "#9F9F9F";
      break;
  }
}

function escapeClassName(className) {
  return className.replace(/^\d+/, (match) =>
    [...match].map((d) => `\\3${d} `).join(""),
  );
}

function loadData() {
  fetch("/cal-data-call")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      data.forEach(([day, hour]) => {
        const elements = document.getElementsByClassName(
          `filler ${day} ${hour}`,
        );
        elements[0].style.backgroundColor = "#9F9F9F";
      });
    })
    .catch((error) => {
      console.log("Error:", error);
    });
}

function submitData(element) {
  fetch("http://localhost:5000/cal-submit-data", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      day: element.classList[1],
      hour: element.classList[2],
    }),
  });
}

window.onload = loadData;

const elements = document.querySelectorAll(".filler");

elements.forEach((element) => {
  element.addEventListener("mousedown", () => {
    draggable = true;
    const styles = window.getComputedStyle(element);
    switch (styles.getPropertyValue("background-color")) {
      case "rgb(159, 159, 159)":
        color = "#52b788";
        break;
      default:
        color = "#9F9F9F";
        break;
    }

    toggleColor(element);
    submitData(element);
  });

  element.addEventListener("mouseup", () => {
    draggable = false;
  });

  element.addEventListener("mouseover", () => {
    if (draggable) {
      element.style.backgroundColor = color;
      submitData(element);
    }
  });
});
