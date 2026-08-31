(() => {
  const YM_COUNTER_ID = 103969668;
  const GA_MEASUREMENT_ID = 'G-FL8MNDG3M8';
  const CONSENT_KEY = 'digitrack_cookie_consent';
  let metrikaLoaded = false;
  let gaLoaded = false;

  const getCounterId = () => {
    const fromScript = Number(document.currentScript?.dataset?.counter);
    if (fromScript > 0) return fromScript;
    const meta = document.querySelector('meta[name="yandex-metrika-counter"]');
    const fromMeta = Number(meta?.getAttribute('content'));
    if (fromMeta > 0) return fromMeta;
    return YM_COUNTER_ID;
  };

  const getGaId = () => {
    const fromScript = document.currentScript?.dataset?.ga;
    if (fromScript) return fromScript;
    const meta = document.querySelector('meta[name="google-analytics-id"]');
    const fromMeta = meta?.getAttribute('content');
    if (fromMeta) return fromMeta;
    return GA_MEASUREMENT_ID;
  };

  const counterId = getCounterId();
  const gaId = getGaId();

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

  const loadGoogleAnalytics = () => {
    if (gaLoaded || !gaId) return;
    gaLoaded = true;

    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function gtag() { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', gaId);

    if (document.getElementById('ga-gtag-loader')) return;

    const script = document.createElement('script');
    script.id = 'ga-gtag-loader';
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(gaId)}`;
    document.head.appendChild(script);
  };

  const loadAnalytics = () => {
    loadMetrika();
    loadGoogleAnalytics();
  };

  const hideBanner = () => {
    document.getElementById('cookieConsentBanner')?.remove();
  };

  const openPolicyModal = (event) => {
    event.preventDefault();
    const modalEl = document.getElementById('privacyModal') || document.getElementById('consentModal');
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
    loadAnalytics();
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
          Мы используем cookie и сервисы
          <a class="cookie-consent-banner__link" href="https://yandex.ru/legal/confidential/" target="_blank" rel="noopener noreferrer">Яндекс.Метрика</a>
          и
          <a class="cookie-consent-banner__link" href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer">Google Analytics</a>
          для анализа посещаемости сайта.
          <a class="cookie-consent-banner__link" href="#" data-cookie-details>Подробнее</a>
        </p>
        <button type="button" class="btn btn-primary-gy cookie-consent-banner__btn" data-cookie-accept>Принять</button>
      </div>
    `;

    document.body.appendChild(banner);
    banner.querySelector('[data-cookie-accept]')?.addEventListener('click', acceptCookies);
    banner.querySelector('[data-cookie-details]')?.addEventListener('click', openPolicyModal);
  };

  const init = () => {
    if (!counterId && !gaId) return;

    let consented = false;
    try {
      consented = localStorage.getItem(CONSENT_KEY) === '1';
    } catch {
      consented = false;
    }

    if (consented) {
      loadAnalytics();
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
