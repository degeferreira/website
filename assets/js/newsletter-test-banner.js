(() => {
  const banner = document.querySelector('.newsletter-test-banner');
  if (!banner) return;
  banner.querySelector('button').addEventListener('click', () => { banner.hidden = true; });
  // A return through browser history counts as another visit to the home page.
  window.addEventListener('pageshow', () => { banner.hidden = false; });
})();
