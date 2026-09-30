/* History Event Maps — organizer sheet renderer.
   ---------------------------------------------------------------------------
   Pure function of (map, lang) -> HTML string for one 10.5in × 8in worksheet.
   No DOM reads, no globals beyond window.HEM_DATA, so the same code renders:

     • organizer.html   — one sheet at full size, for screen / print / PDF
     • index.html       — 24 sheets scaled to card width, as live thumbnails
     • generate_packets.py — 24 sheets per language, printed by Playwright

   That is the point of keeping it a pure renderer: a card thumbnail cannot
   drift away from the sheet it previews, because it *is* the sheet.
   ------------------------------------------------------------------------ */
(function () {
  'use strict';

  const DATA = window.HEM_DATA;

  function t(key, lang) {
    const L = DATA.locales[lang];
    return (L && L[key]) || DATA.locales.en[key] || key;
  }

  function box(key, lang, cls) {
    return '<section class="box ' + (cls || '') + '"><h3>' + t(key, lang) + '</h3><div class="lines"></div></section>';
  }
  function arrow(dir) {
    return dir === 'down'
      ? '<div class="arrow down">↓</div>'
      : '<div class="arrow">→</div>';
  }

  /* The nine-plus layout families. Each returns the grid children for
     `.map-body.layout-<name>`; the grid itself is defined in sheet.css. */
  function layout(m, lang) {
    const b = (k, cls) => box(k, lang, cls);
    const T = (k) => t(k, lang);
    switch (m.layout) {
      case 'snapshot':
        return b('causes','accent') + b('why_important','gold') + b('what_happened_end','purple') + b('how','accent') +
          '<section class="box center-event circle"><h3>' + T('event') + '</h3></section>' +
          b('when') + b('who','purple') + b('where','gold') + b('conclusion','accent');
      case 'causeeffect':
        return '<div class="layout-hybrid" style="grid-column:1/-1;grid-row:1/-1;height:100%">' +
          '<div style="grid-column:2">' + b('why_important','gold') + '</div>' +
          '<section class="box accent circle" style="grid-column:1;grid-row:2"><h3>' + T('causes') + '</h3></section>' +
          '<section class="box event-rect" style="grid-column:2;grid-row:2"><h3>' + T('event') + '</h3><span class="event-line"></span></section>' +
          '<section class="box gold circle" style="grid-column:3;grid-row:2"><h3>' + T('immediate_effects') + '</h3></section>' +
          '<div style="grid-column:1">' + b('who','accent') + '</div>' +
          '<div style="grid-column:3">' + b('later_effects') + '</div>' +
          '<div style="grid-column:2">' + b('conclusion','purple') + '</div></div>';
      case 'sequence':
        return '<div class="stack" style="grid-column:1/-1;grid-row:1/-1;height:100%">' +
          '<div class="sequence-strip"><h3>' + T('sequence_order') + '</h3><div class="seq-lines">' +
          '<span class="num n1">1.</span><span class="num n2">2.</span><span class="num n3">3.</span>' +
          '<span class="num n4">4.</span><span class="num n5">5.</span></div></div>' +
          '<div class="layout-hybrid" style="grid-column:1/-1;grid-row:1/-1;height:100%">' +
          '<div>' + b('where','gold') + '</div>' +
          '<section class="box event-rect" style="grid-column:2;grid-row:1/3"><h3>' + T('event') + '</h3><span class="event-line"></span></section>' +
          '<div>' + b('when','accent') + '</div><div>' + b('beginning') + '</div>' +
          '<div>' + b('who','purple') + '</div><div>' + b('ending') + '</div>' +
          '<div style="grid-column:2">' + b('why_important','accent') + '</div></div></div>';
      case 'peoplegroups':
        return '<div class="layout-peoplegroups" style="grid-column:1/-1;grid-row:1/-1;height:100%">' +
          '<div class="stack"><section class="box event-rect"><h3>' + T('leader') + '</h3><span class="event-line"></span></section>' +
          b('leader_role','purple') + '</div>' +
          '<div class="group-matrix">' +
          '<div class="group-stack"><div class="group-head">' + T('group_1') + '</div>' + b('group_1_goal','accent') + b('conclusion') + '</div>' +
          '<div class="group-stack"><div class="group-head">' + T('group_2') + '</div>' + b('group_2_goal','gold') + b('outcome') + '</div>' +
          '<div class="group-stack"><div class="group-head">' + T('group_3') + '</div>' + b('group_3_goal','purple') + b('result') + '</div>' +
          '</div></div>';
      case 'place':
        return b('physical_features','accent') +
          '<section class="box center-event circle"><h3>' + T('event') + '</h3></section>' +
          b('human_features','gold') + b('why_here') + b('movement','purple') + b('place_effect','accent');
      case 'thennow':
        return '<div class="flow-row">' + b('before','accent') + arrow() + b('event','purple') + arrow() + b('after','gold') + '</div>' +
          '<div class="grid2">' + b('changed','accent') + b('stayed_same') + '</div>';
      case 'evidence3':
        return '<div class="grid3">' +
          '<div class="stack">' + b('source_1','accent') + b('source_1_fact') + '</div>' +
          '<div class="stack">' + b('source_2','gold') + b('source_2_fact') + '</div>' +
          '<div class="stack">' + b('source_3','purple') + b('source_3_fact') + '</div></div>' +
          b('conclusion','accent');
      case 'importance':
        return '<section class="box center-event circle" style="grid-row:1/3"><h3>' + T('event') + '</h3></section>' +
          b('people_effect','accent') + b('government_effect','gold') + b('economy_effect','purple') +
          b('community_effect') + b('most_important_change','accent');
      case 'investigator':
        return '<div class="layout-investigator2" style="grid-column:1/-1;grid-row:1/-1;height:100%">' +
          b('causes','accent') + b('why_important','gold') + b('outcome','purple') + b('how','accent') +
          '<section class="box center-event circle" style="grid-column:2;grid-row:2"><h3>' + T('event') + '</h3></section>' +
          b('when') + b('groups') + b('where','gold') + b('leader','purple') + '</div>';
      case 'pressure':
        return '<div class="flow-row">' + b('long_term_causes','accent') + arrow() + b('short_term_causes') + arrow() +
          b('trigger','gold') + arrow() + b('event','purple') + '</div>' +
          '<div class="grid2">' + b('immediate_effects','accent') + b('later_effects','gold') + '</div>';
      case 'turning':
        return b('before','accent') + arrow() + b('turning_point','purple') + arrow() + b('after','gold') +
          '<div style="grid-column:1/3">' + b('pressures') + '</div>' +
          '<div style="grid-column:3/6" class="grid2">' + b('long_term_change','accent') + b('why_turning_point','gold') + '</div>';
      case 'perspectives':
        return b('group_1','accent') +
          '<section class="box center-event circle" style="grid-row:1/3;grid-column:2"><h3>' + T('event') + '</h3></section>' +
          b('group_2','gold') + b('group_3','purple') + b('group_4') +
          '<div style="grid-column:1/4" class="grid3">' + b('agreement','accent') + b('conflict','gold') + b('missing_voice','purple') + '</div>';
      case 'leader':
        return '<div class="layout-peoplegroups" style="grid-column:1/-1;grid-row:1/-1;height:100%">' +
          '<div class="stack"><section class="box event-rect"><h3>' + T('leader') + '</h3><span class="event-line"></span></section>' +
          b('impact','gold') + b('evidence') + '</div>' +
          '<div class="stack"><section class="box event-rect"><h3>' + T('event') + '</h3><span class="event-line"></span></section>' +
          '<div class="grid2">' + b('goals','accent') + b('decisions','gold') + '</div>' +
          '<div class="grid2">' + b('allies') + b('opponents','purple') + '</div></div></div>';
      case 'conflict':
        return '<div class="stack">' + b('side_a','accent') + b('side_a_goal') + b('side_a_action') + '</div>' +
          '<section class="box center-event circle"><h3>' + T('conflict_event') + '</h3></section>' +
          '<div class="stack">' + b('side_b','gold') + b('side_b_goal') + b('side_b_action') + '</div>' +
          '<div style="grid-column:1/4" class="grid2">' + b('resolution','purple') + b('result','accent') + '</div>';
      case 'chain':
        return '<div class="flow-row">' + b('action_1','accent') + arrow() + b('reaction_1') + arrow() +
          b('action_2','gold') + arrow() + b('reaction_2') + arrow() + b('crisis','purple') + arrow() + b('result') + '</div>' +
          '<div class="grid2">' + b('most_important_link','accent') + b('evidence','gold') + '</div>';
      case 'geo':
        return b('physical_geography','accent') +
          '<section class="box center-event circle" style="grid-row:1/3;grid-column:2"><h3>' + T('event') + '</h3></section>' +
          b('human_geography','gold') + b('resources') + b('movement','purple') +
          '<div style="grid-column:1/4" class="grid2">' + b('why_location_mattered','accent') + b('geographic_effect','gold') + '</div>';
      case 'context':
        return '<div class="layout-investigator2" style="grid-column:1/-1;grid-row:1/-1;height:100%">' +
          b('historical_context','accent') + b('long_term_causes','gold') + b('immediate_cause','purple') +
          b('people_groups') + b('what_happened','accent') +
          '<section class="box event-rect" style="grid-column:2;grid-row:2"><h3>' + T('event') + '</h3><span class="event-line"></span></section>' +
          b('immediate_outcome','gold') + b('long_term_outcome') + b('significance','purple') + '</div>';
      case 'ranking':
        return b('cause_1','accent') + b('cause_2','gold') + b('cause_3','purple') + b('cause_4') +
          '<div class="grid2" style="grid-column:1/3">' + b('rank_causes','accent') + b('most_important_cause','gold') + '</div>';
      case 'turning2':
        return b('before','accent') + b('event','purple') + b('immediate_change','gold') +
          b('long_term_change','accent') + b('continuities') + b('turning_point_judgment','purple') +
          '<div style="grid-column:1/4">' + b('evidence','gold') + '</div>';
      case 'perspevidence':
        return b('perspective_1','accent') +
          '<section class="box center-event circle" style="grid-row:1/3;grid-column:2"><h3>' + T('event') + '</h3></section>' +
          b('perspective_2','gold') + b('perspective_3','purple') + b('perspective_4') +
          '<div style="grid-column:1/4" class="grid4">' + b('evidence','accent') + b('agreement') + b('conflict','gold') + b('missing_voice','purple') + '</div>';
      case 'impact4':
        return b('political','accent') +
          '<section class="box center-event circle" style="grid-row:1/3;grid-column:2"><h3>' + T('event') + '</h3></section>' +
          b('economic','gold') + b('social_cultural','purple') + b('geographic_environmental') +
          '<div style="grid-column:1/4" class="grid3">' + b('immediate','accent') + b('long_term','gold') + b('greatest_significance','purple') + '</div>';
      case 'continuity':
        return b('before','accent') + b('during','purple') + b('after','gold') +
          b('changed_significantly','accent') + b('changed_gradually') + b('stayed_same','gold') +
          '<div style="grid-column:1/4" class="grid2">' + b('why') + b('judgment','purple') + '</div>';
      case 'dossier':
        return '<div style="grid-column:1/4">' + b('historical_question','purple') + '</div>' +
          '<div class="stack">' + b('source_1','accent') + b('source_1_evidence') + b('source_1_limit') + '</div>' +
          '<div class="stack">' + b('source_2','gold') + b('source_2_evidence') + b('source_2_limit') + '</div>' +
          '<div class="stack">' + b('source_3','purple') + b('source_3_evidence') + b('source_3_limit') + '</div>' +
          '<div style="grid-column:1/2">' + b('conflicting_evidence') + '</div>' +
          '<div style="grid-column:2/4">' + b('working_conclusion','accent') + '</div>';
      case 'compare':
        return b('event_a','accent') + '<div></div>' + b('event_b','gold') +
          '<div class="stack">' + b('causes') + b('people_groups') + '</div>' +
          '<div class="stack">' + b('similarities','purple') + b('differences') + '</div>' +
          '<div class="stack">' + b('causes') + b('people_groups') + '</div>' +
          '<div class="stack">' + b('outcomes') + b('significance') + '</div>' +
          b('comparison_judgment','accent') +
          '<div class="stack">' + b('outcomes') + b('significance') + '</div>' +
          '<div style="grid-column:1/4">' + b('evidence','gold') + '</div>';
      default:
        return m.fields.map(f => box(f, lang)).join('');
    }
  }

  /* Full sheet: header (student meta + title + topic line), body, footer. */
  function sheetInner(m, lang) {
    const T = (k) => t(k, lang);
    const skills = m.band === '3-5' ? T('teks_35') : m.band === '6-8' ? T('teks_68') : T('teks_912');
    const compact = (m.layout === 'dossier' || m.layout === 'compare') ? ' compact' : '';
    return '<header class="sheet-header">' +
        '<div class="student-meta">' + T('name') + ': <span class="blankline"></span><br>' +
          T('date') + ': <span class="blankline" style="min-width:.8in"></span> &nbsp; ' +
          T('class_period') + ': <span class="blankline" style="min-width:.75in"></span></div>' +
        '<div class="sheet-title"><h1>' + T('map_title_' + m.id) + '</h1>' +
          '<div class="band">' + T('grade_band') + ': ' + m.band + '</div></div>' +
        '<div class="topic-line">' + T('topic_event') + ': <span class="blankline"></span></div>' +
      '</header>' +
      '<main class="map-body layout-' + m.layout + compact + '">' + layout(m, lang) + '</main>' +
      '<footer class="sheet-footer">' +
        '<div class="source-lines"><strong>' + T('sources_used') + ':</strong> 1.<span></span> 2.<span></span> 3.<span></span></div>' +
        '<div class="skill-note"><strong>' + T('teks_focus') + ':</strong> ' + skills + '</div>' +
        '<div class="credit-note">CC BY-NC 4.0 · Miguel Guhlin 2026</div>' +
      '</footer>';
  }

  /* Complete <article class="sheet">…</article>, ready to inject anywhere. */
  function sheetHTML(m, lang) {
    const rtl = (lang === 'ar' || lang === 'ur') ? ' rtl' : '';
    return '<article class="sheet bw' + rtl + '">' + sheetInner(m, lang) + '</article>';
  }

  /* The prompts actually printed on a map, in order, deduped.
     Read back out of the rendered layout rather than from `m.fields`, because
     several layouts add boxes the data file does not list — this way a card
     blurb can never advertise a prompt the sheet does not carry. */
  function prompts(m, lang) {
    const seen = new Set();
    const html = layout(m, lang);
    let match;
    const re = /<h3>([\s\S]*?)<\/h3>/g;
    while ((match = re.exec(html)) !== null) seen.add(match[1]);
    return [...seen];
  }

  window.HEM_SHEET = {
    maps: DATA.maps,
    byId: (id) => DATA.maps.find(m => m.id === id),
    prompts: prompts,
    t: t,
    layout: layout,
    sheetInner: sheetInner,
    sheetHTML: sheetHTML,
    /* Grade-band label key, so chrome and sheets agree on wording. */
    bandKey: (band) => band === '3-5' ? 'band_35' : band === '6-8' ? 'band_68' : 'band_912',
    /* A map's thinking-skill label is stored as a slug in the locales. */
    skillKey: (skill) => 'skill_' + String(skill).toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, ''),
    pdfHref: (id, lang) => 'pdf/' + id + '/' + lang + '/bw.pdf',
  };
})();
