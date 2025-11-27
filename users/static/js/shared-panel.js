// --- hidden shared panel for option card selections ---
document.addEventListener("DOMContentLoaded", () => {
  const sharedPanel = document.getElementById("shared-panel");
  const cards = document.querySelectorAll(".option-card");
  if (!sharedPanel || cards.length === 0) {
    console.warn("Shared panel or cards not found");
    return;
  }
  // --- load template ---
  function loadTemplateIntoPanel(templateId) {
    const template = document.getElementById(templateId);
    if (!template) {
      console.warn("Template not found:", templateId);
      return;
    }

    // clear current sharedpanel content
    sharedPanel.innerHTML = "";

    // clone template and append
    const clone = template.content.cloneNode(true);
    sharedPanel.appendChild(clone);
  }

  cards.forEach((card) => {
    card.addEventListener("click", () => {
      cards.forEach((c) => c.classList.remove("active"));
      card.classList.add("active");

      const tplId = card.dataset.template;
      if (!tplId) {
        console.warn("No data-template on card:", card);
        return;
      }
      loadTemplateIntoPanel(tplId);
    });

    // --- keyboard support ---
    card.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        card.click();
      }
    });
  });
});
