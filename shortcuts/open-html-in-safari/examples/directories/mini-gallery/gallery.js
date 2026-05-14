const dawn = document.querySelector("#dawn");
const dusk = document.querySelector("#dusk");
const caption = document.querySelector("#caption");

document.querySelectorAll("button[data-view]").forEach((button) => {
  button.addEventListener("click", () => {
    const showDusk = button.dataset.view === "dusk";
    dawn.hidden = showDusk;
    dusk.hidden = !showDusk;
    caption.textContent = showDusk
      ? "Dusk palette loaded from a sibling SVG file."
      : "Dawn palette loaded from a sibling SVG file.";
  });
});
