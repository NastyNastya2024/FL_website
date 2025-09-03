// Прогресс анимации для «книжного» наложения HFL → VFL
(function () {
  const section = document.querySelector('.flip-section');
  const stack   = document.querySelector('.flip-stack');

  if (!section || !stack) return;

  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

  function update() {
    const vh = window.innerHeight;
    const start = section.offsetTop;                  // верх секции
    const end   = start + section.offsetHeight - vh;  // когда sticky «отлипает»
    const y     = window.scrollY;

    const p = clamp((y - start) / (end - start), 0, 1); // 0..1
    stack.style.setProperty('--p', p.toFixed(4));
  }

  update();
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
})();
