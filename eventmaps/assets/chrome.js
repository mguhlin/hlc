/* History Event Maps — shared page chrome.
   ---------------------------------------------------------------------------
   Registers one merged dictionary with the hub's shared i18n engine and wires
   the back-to-top button. Loaded by every page in this area.

   Two dictionaries are merged, in this order:
     1. window.HEM_DATA.locales — the map library's own strings (map titles,
        field labels, TEKS focus lines, most UI words). Source of truth for
        anything printed on a sheet.
     2. window.EM_CHROME       — the Activities-hub chrome on top of it.

   Using BreakoutI18n rather than a private language <select> matters: the
   language a teacher picks in CTOBs, PlotPoint, or lab-safety carries into
   this area, because they all share the `hlc.pst.lang` preference.
   ------------------------------------------------------------------------ */
(function () {
  'use strict';

  const I18N = window.BreakoutI18n;
  const base = (window.HEM_DATA && window.HEM_DATA.locales) || {};
  const chrome = window.EM_CHROME || {};

  const merged = {};
  Object.keys(base).forEach(lang => { merged[lang] = Object.assign({}, base[lang]); });
  Object.keys(chrome).forEach(lang => { merged[lang] = Object.assign(merged[lang] || {}, chrome[lang]); });

  I18N.register('eventmaps', merged);

  window.EM = {
    t: (k, vars) => I18N.t(k, vars),
    lang: () => I18N.getLang(),
    onLangChange: (fn) => window.addEventListener('breakout-i18n:changed', fn),
  };

  function wireBackToTop() {
    const btn = document.getElementById('back-to-top');
    if (!btn) return;
    const toggle = () => btn.classList.toggle('visible', window.scrollY > 400);
    window.addEventListener('scroll', toggle, { passive: true });
    btn.addEventListener('click', e => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    toggle();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', wireBackToTop);
  else wireBackToTop();
})();
