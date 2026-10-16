'use strict';
// Staging only: crawlers must not index Cloudflare preview subdomains.
if (location.hostname.endsWith('.pages.dev') || location.hostname === 'localhost' || location.hostname === '127.0.0.1') {
  const robots = document.createElement('meta');
  robots.name = 'robots';
  robots.content = 'noindex,nofollow';
  document.head.appendChild(robots);
}
const langButton = document.querySelector('.language-toggle');
const langMenu = document.getElementById('language-menu');
const mobileButton = document.querySelector('.mobile-toggle');
const mobileNav = document.getElementById('mobile-nav');
if (langButton && langMenu) {
  langButton.addEventListener('click', () => {
    const open = langButton.getAttribute('aria-expanded') !== 'true';
    langButton.setAttribute('aria-expanded', String(open));
    langMenu.hidden = !open;
  });
  document.addEventListener('click', e => {
    if (!e.target.closest('.language-picker')) {
      langButton.setAttribute('aria-expanded', 'false');
      langMenu.hidden = true;
    }
  });
}
if (mobileButton && mobileNav) {
  mobileButton.addEventListener('click', () => {
    const open = mobileButton.getAttribute('aria-expanded') !== 'true';
    mobileButton.setAttribute('aria-expanded', String(open));
    mobileNav.hidden = !open;
  });
}
document.addEventListener('keydown', e => {
  if (e.key !== 'Escape') return;
  if (langMenu && langButton) { langMenu.hidden = true; langButton.setAttribute('aria-expanded', 'false'); }
  if (mobileNav && mobileButton) { mobileNav.hidden = true; mobileButton.setAttribute('aria-expanded', 'false'); }
});
