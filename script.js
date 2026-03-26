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
})();