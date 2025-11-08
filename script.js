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
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }

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