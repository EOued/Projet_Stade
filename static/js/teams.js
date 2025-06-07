const channel = new BroadcastChannel("channel");
function openPopup(element) {
  channel.postMessage(element.closest("tr").cells[0].textContent.trim());
}

let holdInterval;

function startHold(button, callback) {
  callback(button);
  holdInterval = setInterval(() => callback(button), 150);
}

function stopHold() {
  clearInterval(holdInterval);
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

