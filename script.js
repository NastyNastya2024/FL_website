(() => {
  const year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());

  // Smooth scroll for same-page links
  const links = document.querySelectorAll('a[href^="#"]');
  for (const link of links) {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href') || '';
      const id = href.startsWith('#') ? href.slice(1) : '';
      const target = id ? document.getElementById(id) : null;
      // Do not hijack Bootstrap modals via hash links
      if (target && !target.classList.contains('modal')) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }

  // Deep-linkable Bootstrap modals via hash (e.g. /page.html#pricingModal)
  const modalIds = ['pricingModal', 'legalModal', 'consentModal', 'privacyModal', 'contactModal'];
  const modalById = new Map();
  const ensureModal = (id) => {
    if (!window.bootstrap || !window.bootstrap.Modal) return null;
    if (modalById.has(id)) return modalById.get(id);
    const el = document.getElementById(id);
    if (!el) return null;
    const instance = window.bootstrap.Modal.getOrCreateInstance(el);
    modalById.set(id, instance);
    return instance;
  };

  let lastNonModalHash = window.location.hash && !modalIds.includes(window.location.hash.slice(1))
    ? window.location.hash
    : '';

  const openFromHash = () => {
    const hash = window.location.hash || '';
    const id = hash.startsWith('#') ? hash.slice(1) : '';
    if (!id || !modalIds.includes(id)) return;
    const instance = ensureModal(id);
    if (instance) instance.show();
  };

  window.addEventListener('hashchange', () => {
    const id = (window.location.hash || '').replace('#', '');
    if (!modalIds.includes(id)) {
      lastNonModalHash = window.location.hash || '';
      return;
    }
    openFromHash();
  });

  // Keep URL hash in sync when modals open/close
  for (const id of modalIds) {
    const el = document.getElementById(id);
    if (!el) continue;

    el.addEventListener('show.bs.modal', () => {
      const current = window.location.hash || '';
      const currentId = current.startsWith('#') ? current.slice(1) : '';
      if (currentId && !modalIds.includes(currentId)) lastNonModalHash = current;
      if (current !== `#${id}`) history.pushState(null, '', `#${id}`);
    });

    el.addEventListener('hidden.bs.modal', () => {
      const current = window.location.hash || '';
      if (current === `#${id}`) {
        history.pushState(null, '', lastNonModalHash || window.location.pathname + window.location.search);
      }
    });
  }

  // Open modal if page loaded with hash
  openFromHash();

  // Инверсия цвета навигации при скролле
  const nav = document.querySelector('.nav-glass');
  const hero = document.querySelector('.hero-hero');
  
  if (nav) {
    function updateNavColor() {
      if (hero) {
        const heroBottom = hero.offsetTop + hero.offsetHeight;
        const scrollY = window.scrollY || window.pageYOffset;
        const navHeight = nav.offsetHeight;
        
        // Если прокрутили ниже hero-блока, переключаем на темный текст
        if (scrollY + navHeight + 50 > heroBottom) {
          nav.classList.add('nav-light');
        } else {
          nav.classList.remove('nav-light');
        }
      } else {
        // Если нет hero-блока, сразу применяем темный текст
        nav.classList.add('nav-light');
      }
    }
    
    // Проверяем при загрузке
    updateNavColor();
    
    // Проверяем при скролле
    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          updateNavColor();
          ticking = false;
        });
        ticking = true;
      }
    });
    
    // Также проверяем при изменении размера окна
    window.addEventListener('resize', () => {
      updateNavColor();
    });
  }

  // "Ping-pong" loop for all videos: forward -> backward -> forward...
  // HTML5 video has no native reverse-loop, so we step currentTime back manually.
  const prefersReducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!prefersReducedMotion) {
    const videos = Array.from(document.querySelectorAll('video'));
    for (const video of videos) {
      // allow opting out per-element if needed
      if (video.hasAttribute('data-no-pingpong')) continue;

      // We control the looping ourselves
      video.loop = false;

      let rafId = 0;
      let reversing = false;

      const cancelReverse = () => {
        if (rafId) cancelAnimationFrame(rafId);
        rafId = 0;
        reversing = false;
      };

      const playForward = async () => {
        cancelReverse();
        try {
          await video.play();
        } catch {
          // autoplay may be blocked; ignore
        }
      };

      const playReverse = () => {
        cancelReverse();
        reversing = true;

        // ensure we start from the end
        if (!Number.isFinite(video.currentTime) || video.currentTime <= 0) {
          const d = video.duration;
          if (Number.isFinite(d) && d > 0) video.currentTime = d;
        }

        let lastT = 0;
        const step = (t) => {
          if (!reversing) return;
          if (!lastT) lastT = t;
          const dt = (t - lastT) / 1000;
          lastT = t;

          const next = Math.max(0, video.currentTime - dt);
          video.currentTime = next;

          if (next <= 0.02) {
            cancelReverse();
            playForward();
            return;
          }

          rafId = requestAnimationFrame(step);
        };

        // pause normal playback while reversing
        video.pause();
        rafId = requestAnimationFrame(step);
      };

      video.addEventListener('ended', () => {
        // finished forward playback -> reverse
        playReverse();
      });

      // If user pauses/plays manually, stop reverse stepping
      video.addEventListener('play', cancelReverse);
      video.addEventListener('pause', () => {
        // if paused during reverse, stop stepping
        if (reversing) cancelReverse();
      });
    }
  }

  // Horizontal scroll arrows for feature carousels
  const arrowButtons = Array.from(document.querySelectorAll('button[data-scroll-target]'));
  const setArrowState = (scroller, leftBtn, rightBtn) => {
    if (!scroller) return;
    const max = scroller.scrollWidth - scroller.clientWidth;
    const x = scroller.scrollLeft;
    if (leftBtn) leftBtn.disabled = x <= 1;
    if (rightBtn) rightBtn.disabled = x >= max - 1;
  };

  for (const btn of arrowButtons) {
    const sel = btn.getAttribute('data-scroll-target');
    if (!sel) continue;
    const scroller = document.querySelector(sel);
    if (!scroller) continue;

    const wrap = btn.closest('.dp-features-wrap') || document;
    const leftBtn = wrap.querySelector('.dp-scroll-arrow--left');
    const rightBtn = wrap.querySelector('.dp-scroll-arrow--right');

    const dir = btn.classList.contains('dp-scroll-arrow--left') ? -1 : 1;
    btn.addEventListener('click', () => {
      const delta = Math.max(220, Math.floor(scroller.clientWidth * 0.8)) * dir;
      scroller.scrollBy({ left: delta, behavior: 'smooth' });
    });

    const update = () => setArrowState(scroller, leftBtn, rightBtn);
    scroller.addEventListener('scroll', () => window.requestAnimationFrame(update), { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  // Lead modal: subject from trigger button, mailto with phone + email
  const leadModalEl = document.getElementById('leadModal');
  const leadForm = document.getElementById('leadForm');
  const leadModalTitle = document.getElementById('leadModalLabel');
  let leadSubject = 'Заявка с сайта DigiTrack';

  document.querySelectorAll('[data-bs-target="#leadModal"][data-lead-subject]').forEach((btn) => {
    btn.addEventListener('click', () => {
      leadSubject = btn.getAttribute('data-lead-subject') || leadSubject;
      if (leadModalTitle) leadModalTitle.textContent = leadSubject;
    });
  });

  if (leadModalEl) {
    leadModalEl.addEventListener('hidden.bs.modal', () => {
      if (leadForm) leadForm.reset();
      if (leadModalTitle) leadModalTitle.textContent = 'Оставьте контакты';
      leadSubject = 'Заявка с сайта DigiTrack';
    });
  }

  if (leadForm) {
    leadForm.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!leadForm.checkValidity()) {
        leadForm.reportValidity();
        return;
      }
      const fd = new FormData(leadForm);
      const body = [
        `Тема: ${leadSubject}`,
        `Email: ${fd.get('email')}`,
        `Телефон: ${fd.get('phone')}`,
      ].join('\n');
      const modal = leadModalEl && window.bootstrap?.Modal?.getInstance(leadModalEl);
      if (modal) modal.hide();
      window.location.href = `mailto:info@digi-track.ru?subject=${encodeURIComponent(leadSubject)}&body=${encodeURIComponent(body)}`;
    });
  }
})();