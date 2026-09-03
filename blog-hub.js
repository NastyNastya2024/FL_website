(() => {
  const HUB_LABELS = {
    fl: 'Федеративное обучение',
    bdp: 'Платформа данных',
  };

  const MONTHS_RU = [
    'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
    'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря',
  ];

  let articles = [];
  let searchTerm = '';

  const listEl = document.getElementById('blog-articles-list');
  const loadingEl = document.getElementById('blog-cards-loading');
  const searchInput = document.getElementById('searchArticles');

  function formatDate(iso) {
    if (!iso) return '';
    const [y, m, d] = iso.split('-').map(Number);
    if (!y || !m || !d) return iso;
    return `${d} ${MONTHS_RU[m - 1]} ${y}`;
  }

  function articleUrl(article) {
    if (article.href) return article.href;
    return `blog/articles/${article.slug}.html`;
  }

  function normalizeImage(src, slug) {
    if (src && src.startsWith('img/blog/')) return src;
    if (slug) return `img/blog/${slug}.png`;
    return (src || 'img/blog/fl-guide.png').replace(/^\.\.\/\.\.\/img\//, 'img/');
  }

  function matchesFilter(article) {
    if (!searchTerm) return true;
    const hay = `${article.title} ${article.excerpt} ${article.search || ''} ${article.category || ''}`.toLowerCase();
    return hay.includes(searchTerm);
  }

  function renderList(items) {
    if (!listEl) return;
    if (!items.length) {
      listEl.innerHTML = '<div class="col-12"><p class="blog-empty-state">Ничего не найдено. Попробуйте другой запрос.</p></div>';
      return;
    }
    listEl.innerHTML = items.map((article) => `
      <div class="col-12 col-md-6 col-lg-4">
        <a href="${articleUrl(article)}" class="blog-grid-card d-block h-100 text-decoration-none" data-hub="${article.hub}" data-search="${(article.search || '').replace(/"/g, '&quot;')}">
          <div class="blog-grid-card-media">
            <img src="${normalizeImage(article.image, article.slug)}" alt="" loading="lazy" width="640" height="360"/>
          </div>
          <div class="blog-grid-card-body">
            <span class="blog-article-tag">${article.category || HUB_LABELS[article.hub] || 'DigiTrack'}</span>
            <h2 class="blog-grid-card-title">${article.title}</h2>
            <time class="blog-article-date" datetime="${article.date || ''}">${formatDate(article.date)}</time>
          </div>
        </a>
      </div>`).join('');
  }

  function render() {
    renderList(articles.filter(matchesFilter));
  }

  function bindSearch() {
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        searchTerm = e.target.value.toLowerCase().trim();
        render();
      });
      const params = new URLSearchParams(window.location.search);
      const q = params.get('q');
      if (q) {
        searchInput.value = q;
        searchTerm = q.toLowerCase().trim();
      }
    }
  }

  async function init() {
    if (!listEl) return;
    try {
      const res = await fetch('blog/articles-manifest.json', { cache: 'no-cache' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      articles = await res.json();
      if (loadingEl) loadingEl.remove();
      bindSearch();
      render();
    } catch (err) {
      if (loadingEl) {
        loadingEl.textContent = 'Не удалось загрузить статьи. Обновите страницу.';
      }
      console.error('blog-hub:', err);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
