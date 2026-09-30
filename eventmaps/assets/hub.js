/* History Event Maps — hub (index.html).
   ---------------------------------------------------------------------------
   Renders the 24-map library as filterable cards. Each card carries a live
   thumbnail: the real organizer sheet from sheet.js, scaled to card width.
   Nothing here is a placeholder graphic, so a card always shows the map a
   teacher is about to print, in the language they have selected.
   ------------------------------------------------------------------------ */
(function () {
  'use strict';

  const S = window.HEM_SHEET;
  const t = (k, v) => window.EM.t(k, v);
  const lang = () => window.EM.lang();
  const isRTL = () => window.BreakoutI18n.dirFor(lang()) === 'rtl';

  /* The sheet is authored at 10.5in × 8in = 1008 × 768 CSS px. Thumbnails are
     that same element scaled by (card width / 1008), so the ratio never
     distorts and no part of the sheet is cropped. */
  const SHEET_W = 1008;

  const el = (id) => document.getElementById(id);

  function bandLabel(band) { return t(S.bandKey(band)); }
  function skillLabel(skill) { return t(S.skillKey(skill)); }

  function escapeAttr(s) {
    return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
  }

  /* ---- Filters ------------------------------------------------------- */

  function buildFilters() {
    const L = lang();
    const band = el('f-band'), skill = el('f-skill');
    const keepBand = band.value, keepSkill = skill.value;

    band.innerHTML =
      '<option value="">' + t('all_grade_bands') + '</option>' +
      '<option value="3-5">' + t('band_35') + '</option>' +
      '<option value="6-8">' + t('band_68') + '</option>' +
      '<option value="9-12">' + t('band_912') + '</option>';
    band.value = keepBand;

    /* Sort the skill list in the reader's own language, not by English slug. */
    const skills = [...new Set(S.maps.map(m => m.skill))]
      .map(s => ({ value: s, label: skillLabel(s) }))
      .sort((a, b) => a.label.localeCompare(b.label, L));
    skill.innerHTML = '<option value="">' + t('all_skills') + '</option>' +
      skills.map(s => '<option value="' + escapeAttr(s.value) + '">' + s.label + '</option>').join('');
    skill.value = keepSkill;
  }

  function matches(m, band, skill, q) {
    if (band && m.band !== band) return false;
    if (skill && m.skill !== skill) return false;
    if (!q) return true;
    const hay = [t('map_title_' + m.id), skillLabel(m.skill), bandLabel(m.band), m.band, m.id, m.skill]
      .join(' ').toLowerCase();
    return hay.includes(q);
  }

  /* ---- Cards --------------------------------------------------------- */

  function cardHTML(m) {
    const L = lang();
    const title = t('map_title_' + m.id);
    /* The blurb is the map's own prompts, not a generic band description —
       two maps in the same band would otherwise read identically. */
    const blurb = S.prompts(m, L).join(' · ');
    const id = encodeURIComponent(m.id);
    /* A <div>, not an <a>: the card carries two destinations — preview the map,
       or download its deck — and an anchor cannot legally contain another one.
       The title's `.stretch` link covers the whole card via an absolutely
       positioned ::after, so clicking anywhere still opens the preview, while
       the download sits above it on a higher z-index. */
    return '<div class="card">' +
      '<div class="thumb" aria-hidden="true">' + S.sheetHTML(m, L) + '</div>' +
      '<span class="mnum">' + bandLabel(m.band) + '</span>' +
      '<span class="mtitle"><a class="stretch" href="organizer.html?map=' + id + '">' +
        title + '</a></span>' +
      '<span class="mdesc">' + blurb + '</span>' +
      '<div class="tags"><span class="tag">' + skillLabel(m.skill) + '</span></div>' +
      '<span class="mfoot">' +
        '<span class="tag tag-ok">' + t('view_map') + '</span>' +
        '<a class="tag tag-dl" href="pptx/maps/' + id + '.pptx" download>' +
          t('pptx_short') + '</a>' +
        '<span class="arr">' + (isRTL() ? '←' : '→') + '</span>' +
      '</span>' +
    '</div>';
  }

  /* Scale every thumbnail to its card's current width. Called after render
     and on resize; ResizeObserver catches the grid reflowing at breakpoints
     without a resize event (e.g. the filter bar wrapping). */
  function scaleThumbs() {
    document.querySelectorAll('.thumb').forEach(thumb => {
      const sheet = thumb.firstElementChild;
      if (!sheet) return;
      /* getBoundingClientRect, not clientWidth: the grid gives fractional
         column widths, and rounding down clips the sheet footer. */
      const scale = thumb.getBoundingClientRect().width / SHEET_W;
      sheet.style.transform = 'scale(' + scale + ')';
    });
  }

  /* ---- Downloads ----------------------------------------------------- */

  function renderDownloads() {
    const L = lang();
    const rows = [
      { href: 'pdf-packets/history-event-maps_' + L + '_bw.pdf', title: t('packet_all'), sub: t('grayscale') },
      { href: 'pptx/history-event-maps_' + L + '.pptx', title: t('packet_pptx'), sub: t('editable'), kind: 'PPTX' },
      { href: 'pdf-band-packets/history-event-maps_35_' + L + '_bw.pdf', title: t('packet_band', { band: t('band_35') }), sub: t('grayscale') },
      { href: 'pdf-band-packets/history-event-maps_68_' + L + '_bw.pdf', title: t('packet_band', { band: t('band_68') }), sub: t('grayscale') },
      { href: 'pdf-band-packets/history-event-maps_912_' + L + '_bw.pdf', title: t('packet_band', { band: t('band_912') }), sub: t('grayscale') },
    ];
    el('downloads').innerHTML = rows.map(r =>
      '<a class="dl" href="' + r.href + '" download>' +
      '<span class="dls">' + (r.kind || 'PDF') + ' · ' + r.sub + '</span>' +
      '<span class="dlt">' + r.title + '</span></a>').join('');
  }

  /* ---- Render -------------------------------------------------------- */

  function render() {
    const band = el('f-band').value;
    const skill = el('f-skill').value;
    const q = (el('f-search').value || '').trim().toLowerCase();

    const shown = S.maps.filter(m => matches(m, band, skill, q));
    el('cards').innerHTML = shown.map(cardHTML).join('');
    el('result-count').textContent = shown.length + ' ' + t('maps');
    /* The chip beside the heading counts what is on screen, not the library. */
    el('sec-library').setAttribute('data-band', shown.length);
    el('no-results').style.display = shown.length ? 'none' : 'block';
    scaleThumbs();
  }

  /* The banner artwork carries the title, tagline, and both intro lines — in
     English. Under an English banner the text hero is a verbatim second copy,
     so collapse it to screen-reader-only; every other language needs it
     visible, because the artwork is not translated. Toggling .sr-only rather
     than `hidden` keeps the <h1> and the intro in the accessibility tree and
     available to page translators in all seven languages. */
  function syncHeroText() {
    const host = el('hero-text');
    if (host) host.classList.toggle('sr-only', lang() === 'en');
  }

  function renderAll() {
    syncHeroText();
    buildFilters();
    renderDownloads();
    render();
  }

  function init() {
    ['f-band', 'f-skill'].forEach(id => el(id).addEventListener('change', render));
    el('f-search').addEventListener('input', render);
    el('f-reset').addEventListener('click', () => {
      el('f-band').value = '';
      el('f-skill').value = '';
      el('f-search').value = '';
      render();
    });

    renderAll();
    window.EM.onLangChange(renderAll);

    if (window.ResizeObserver) new ResizeObserver(scaleThumbs).observe(el('cards'));
    else window.addEventListener('resize', scaleThumbs);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
