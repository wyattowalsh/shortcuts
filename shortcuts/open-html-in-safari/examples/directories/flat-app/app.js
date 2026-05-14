const button = document.querySelector("#statusButton");
const status = document.querySelector("#status");

button.addEventListener("click", () => {
  status.textContent = `JavaScript ran at ${new Date().toLocaleTimeString()}.`;
});
