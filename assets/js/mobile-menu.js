(() => {
  const button = document.querySelector('.mobile-menu-toggle');
  const nav = document.querySelector('.site-navigation');
  if (!button || !nav) return;
  const setOpen = (open) => {
    button.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('mobile-menu-expanded', open);
  };
  button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
      button.focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (!nav.contains(event.target)) setOpen(false);
  });
  nav.querySelector('#site-main-menu').addEventListener('click', (event) => {
    if (event.target.closest('a, button')) setOpen(false);
  });
  window.matchMedia('(min-width: 768px)').addEventListener('change', () => setOpen(false));
})();
