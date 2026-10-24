(() => {
  const tabs = [...document.querySelectorAll('.explorer-tab')];
  const views = {
    magnitude: document.getElementById('view-magnitude'),
    direction: document.getElementById('view-direction'),
    controls: document.getElementById('view-controls')
  };

  tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.view;
      tabs.forEach((t) => t.classList.toggle('is-active', t === tab));
      Object.entries(views).forEach(([name, el]) => {
        if (el) el.classList.toggle('is-hidden', name !== target);
      });
    });
  });

  const slider = document.getElementById('dose-slider');
  const output = document.getElementById('dose-value');
  const rows = [...document.querySelectorAll('.receiver-row')];

  function updateDose() {
    if (!slider || !output) return;
    const lambda = Number(slider.value) / 100;
    output.textContent = `${lambda.toFixed(2)}×`;
    rows.forEach((row) => {
      const sensitivity = Number(row.dataset.sensitivity || 0.5);
      // Pedagogical animation only: preserve receiver ordering while letting dose grow smoothly.
      const normalized = Math.min(1, sensitivity * (0.22 + 0.78 * Math.pow(lambda, 0.72)));
      const fill = row.querySelector('.effect-fill');
      if (fill) fill.style.width = `${Math.max(7, normalized * 100)}%`;
      row.style.setProperty('--pulse', String(0.35 + 0.65 * lambda));
    });
  }

  if (slider) {
    slider.addEventListener('input', updateDose);
    updateDose();
  }
})();
