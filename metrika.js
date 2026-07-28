(() => {
  const YM_COUNTER_ID = 103969668;
  const CONSENT_KEY = 'digitrack_cookie_consent';
  let metrikaLoaded = false;

  const getCounterId = () => {
    const fromScript = Number(document.currentScript?.dataset?.counter);
    if (fromScript > 0) return fromScript;
    const meta = document.querySelector('meta[name="yandex-metrika-counter"]');
    const fromMeta = Number(meta?.getAttribute('content'));
    if (fromMeta > 0) return fromMeta;
    return YM_COUNTER_ID;
  };

  const counterId = getCounterId();

  const loadMetrika = () => {
    if (metrikaLoaded || !counterId) return;
    metrikaLoaded = true;

    (function (m, e, t, r, i, k, a) {
      m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); };
      m[i].l = 1 * new Date();
      for (let j = 0; j < document.scripts.length; j++) {
        if (document.scripts[j].src === r) return;
      }
      k = e.createElement(t);
      a = e.getElementsByTagName(t)[0];
      k.async = 1;
      k.src = r;
      k.id = 'ym-tag-loader';
      a.parentNode.insertBefore(k, a);
    })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js', 'ym');

    window.ym(counterId, 'init', {
      clickmap: true,
      trackLinks: true,
      accurateTrackBounce: true,
      webvisor: true,
    });

    if (!document.getElementById('ym-noscript-pixel')) {
      const noscript = document.createElement('noscript');
      noscript.id = 'ym-noscript-pixel';
      noscript.innerHTML = `<div><img src="https://mc.yandex.ru/watch/${counterId}" style="position:absolute; left:-9999px;" alt="" /></div>`;
      document.body.appendChild(noscript);
    }
  };

  const hideBanner = () => {
    document.getElementById('cookieConsentBanner')?.remove();
  };

  const openConsentModal = (event) => {
    event.preventDefault();
    const modalEl = document.getElementById('consentModal');
    if (modalEl && window.bootstrap?.Modal) {
      window.bootstrap.Modal.getOrCreateInstance(modalEl).show();
    }
  };

  const acceptCookies = () => {
    try {
      localStorage.setItem(CONSENT_KEY, '1');
    } catch {
      // ignore storage errors
    }
    hideBanner();
    loadMetrika();
  };

  const showBanner = () => {
    if (document.getElementById('cookieConsentBanner')) return;

    const banner = document.createElement('div');
    banner.id = 'cookieConsentBanner';
    banner.className = 'cookie-consent-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-live', 'polite');
    banner.setAttribute('aria-label', 'Уведомление об использовании cookie');
    banner.innerHTML = `
      <div class="cookie-consent-banner__inner">
        <p class="cookie-consent-banner__text mb-0">
          Мы используем файлы cookie и сервис
          <a class="cookie-consent-banner__link" href="https://yandex.ru/legal/confidential/" target="_blank" rel="noopener noreferrer">Яндекс.Метрика</a>
          для анализа посещаемости сайта.
          <a class="cookie-consent-banner__link" href="#" data-cookie-details>Подробнее</a>
        </p>
        <button type="button" class="btn btn-primary-gy cookie-consent-banner__btn" data-cookie-accept>Принять</button>
      </div>
    `;

    document.body.appendChild(banner);
    banner.querySelector('[data-cookie-accept]')?.addEventListener('click', acceptCookies);
    banner.querySelector('[data-cookie-details]')?.addEventListener('click', openConsentModal);
  };

  const init = () => {
    if (!counterId) return;

    let consented = false;
    try {
      consented = localStorage.getItem(CONSENT_KEY) === '1';
    } catch {
      consented = false;
    }

    if (consented) {
      loadMetrika();
    } else {
      showBanner();
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
