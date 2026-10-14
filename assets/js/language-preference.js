(() => {
  const key = "site-language";
  const homes = { en: "/", pt: "/pt-br/" };
  const languageOf = (path) => path.startsWith(homes.pt) ? "pt" : "en";
  let saved;
  try { saved = localStorage.getItem(key); } catch (_) {}

  if (location.pathname === homes.en) {
    const preferred = (navigator.languages || [navigator.language])[0] || "en";
    const language = saved === "pt" || saved === "en"
      ? saved : preferred.toLowerCase().startsWith("pt") ? "pt" : "en";
    if (language === "pt") {
      location.replace(homes.pt + location.search + location.hash);
    }
  }

  document.addEventListener("click", (event) => {
    const link = event.target.closest("a");
    if (!link || !link.closest("header")) return;
    const url = new URL(link.href, location.href);
    if (url.origin !== location.origin) return;
    // Only language-switch links match a translated version of this page.
    const alternates = [...document.querySelectorAll('link[rel="alternate"][hreflang]:not([hreflang="x-default"])')];
    if (!alternates.some((alternate) => alternate.href === url.href)) return;
    try { localStorage.setItem(key, languageOf(url.pathname)); } catch (_) {}
  });
})();
