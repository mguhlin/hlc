"""History Event Maps — build the editable PowerPoint version of the library.

    python3 generate_pptx.py

Produces two families of deck, both US Letter landscape and both cut from the
same measurements, so they can never disagree with each other or with the PDFs:

    pptx/history-event-maps_<lang>.pptx   7 decks x 24 slides — one language,
                                          every map; mirrors the printed packet
    pptx/maps/<map-id>.pptx              24 decks x 7 slides — one map, every
                                          language, for a teacher who wants a
                                          single organizer their whole class
                                          can read

WHY IT IS BUILT THIS WAY
------------------------
Converting the PDF would give a deck of pictures, or — via a PDF importer — a
tangle of absolutely-placed glyph runs and paths. Neither is editable in any
sense a teacher cares about.

So the slides are built from the same source the site and the PDFs are built
from, and the browser is used as the layout engine exactly as generate_packets.py
uses it: headless Chrome renders the real sheets, then every box, label, and
rule is measured with getBoundingClientRect() and re-emitted as a native
PowerPoint autoshape at the same position. The result is genuinely editable —
each prompt is real text in a real text frame, each box is a real shape that can
be moved, restyled, or deleted, and a student can click inside one and type.

The one deliberate difference from the print version: the ruled writing lines
are omitted. On paper they guide handwriting; in PowerPoint they only get in the
way of the cursor, so each box is left as open typing space below its prompt.

Requires Chrome/Chromium on PATH. No third-party Python packages —
pptx_ooxml.py writes the OOXML package directly.
"""
import argparse
import base64
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pptx_ooxml as ox

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
OUT_DIR = ROOT / 'pptx'

DATA = json.loads((ROOT / 'data.json').read_text(encoding='utf-8'))
SHEET_CSS = (ASSETS / 'sheet.css').read_text(encoding='utf-8')
DATA_JS = (ASSETS / 'data.js').read_text(encoding='utf-8')
SHEET_JS = (ASSETS / 'sheet.js').read_text(encoding='utf-8')

BROWSERS = ['google-chrome', 'chromium', 'chromium-browser', 'google-chrome-stable']

# The sheet is 10.5in x 8in centred on an 11in x 8.5in slide.
PAGE_W, PAGE_H = 11.0, 8.5
MARGIN = 0.25

RTL_LANGS = {'ar', 'ur'}


def find_browser():
    for name in BROWSERS:
        path = shutil.which(name)
        if path:
            return path
    raise SystemExit('No Chrome/Chromium on PATH (tried: %s)' % ', '.join(BROWSERS))


# --------------------------------------------------------------------------
# 1. Measure the real sheets in a browser
# --------------------------------------------------------------------------

# Runs inside the page. Walks each rendered sheet and returns a flat list of
# positioned elements, in inches relative to the sheet's own top-left corner.
PROBE_JS = r"""
var S = window.HEM_SHEET, LANG = __LANG__;
var host = document.getElementById('host');
var out = [];

function px(v) { return v / 96; }

/* Text of an element with the empty <span class="blankline"> write-on rules
   turned into underscores, so the blank survives as editable text. */
function textOf(el) {
  var s = '';
  el.childNodes.forEach(function (n) {
    if (n.nodeType === 3) { s += n.textContent; return; }
    if (n.nodeType !== 1) return;
    if (n.tagName === 'BR') { s += '\n'; return; }
    if (!n.textContent.trim() && n.getBoundingClientRect().width > 4) {
      var w = n.getBoundingClientRect().width / 96;
      s += '_'.repeat(Math.max(6, Math.round(w * 13)));
      return;
    }
    s += textOf(n);
  });
  return s.replace(/ /g, ' ').replace(/[ \t]+/g, ' ').trim();
}

S.maps.forEach(function (m) {
  host.innerHTML = S.sheetHTML(m, LANG);
  var sheet = host.querySelector('.sheet');
  var sb = sheet.getBoundingClientRect();
  var els = [];
  function rect(el) {
    var r = el.getBoundingClientRect();
    return { x: px(r.left - sb.left), y: px(r.top - sb.top),
             w: px(r.width), h: px(r.height) };
  }
  function push(kind, el, extra) {
    var o = rect(el); o.kind = kind;
    for (var k in extra) o[k] = extra[k];
    els.push(o);
  }
  function fontPt(el) { return parseFloat(getComputedStyle(el).fontSize) * 0.75; }

  /* --- header --- */
  var meta = sheet.querySelector('.student-meta');
  if (meta) push('text', meta, { text: textOf(meta), pt: fontPt(meta), align: 'l' });
  var h1 = sheet.querySelector('.sheet-title h1');
  if (h1) push('text', h1, { text: h1.textContent, pt: fontPt(h1), bold: true, align: 'ctr' });
  var band = sheet.querySelector('.sheet-title .band');
  if (band) push('text', band, { text: band.textContent, pt: fontPt(band), align: 'ctr' });
  var topic = sheet.querySelector('.topic-line');
  if (topic) push('text', topic, { text: textOf(topic), pt: fontPt(topic),
                                   align: LANG_RTL ? 'l' : 'r' });
  var hdr = sheet.querySelector('.sheet-header');
  if (hdr) {
    var r = rect(hdr);
    els.push({ kind: 'rule', x: r.x, y: r.y + r.h, w: r.w, h: 0, weight: 2.25 });
  }

  /* --- body: every bordered element becomes a shape --- */
  sheet.querySelectorAll('.box, .group-head, .sequence-strip').forEach(function (el) {
    var cs = getComputedStyle(el);
    var h3 = el.querySelector('h3');
    var label = h3 ? h3.textContent : textOf(el);
    var isCircle = el.classList.contains('circle');
    var style = cs.borderTopStyle, bw = parseFloat(cs.borderTopWidth) || 2;
    /* CSS 'double' has no PowerPoint equivalent; carry the emphasis as weight. */
    var weight = style === 'double' ? Math.max(2.25, bw * 0.9) : bw * 0.75;
    var extraLine = !!el.querySelector('.event-line');
    push('shape', el, {
      text: label,
      pt: h3 ? fontPt(h3) : fontPt(el),
      bold: true,
      geom: isCircle ? 'ellipse' : 'roundRect',
      adj: el.classList.contains('event-rect') || el.classList.contains('group-head')
        || el.classList.contains('sequence-strip') ? 6000 : 14000,
      dash: style === 'dashed' ? 'dash' : null,
      weight: Math.min(3, Math.max(1, weight)),
      align: (isCircle || el.classList.contains('event-rect')
        || el.classList.contains('group-head')
        || el.classList.contains('sequence-strip')) ? 'ctr' : 'l',
      anchor: isCircle ? 'ctr' : 't',
      blank: extraLine
    });
  });

  /* Flow arrows between boxes — at their real size, not a guess. Flagged so
     the writer can widen the frame: the CSS column is only .28in, which is
     narrower than a 22pt glyph, and PowerPoint would shrink it to fit. */
  sheet.querySelectorAll('.arrow').forEach(function (el) {
    push('text', el, { text: el.textContent.trim(), pt: fontPt(el), bold: true,
                       align: 'ctr', anchor: 'ctr', arrow: true });
  });

  /* The numbered sequence strip's 1..5 markers. */
  sheet.querySelectorAll('.seq-lines .num').forEach(function (el) {
    push('text', el, { text: el.textContent.trim(), pt: fontPt(el), bold: true,
                       align: LANG_RTL ? 'r' : 'l' });
  });

  /* --- footer --- */
  var foot = sheet.querySelector('.sheet-footer');
  if (foot) {
    var fr = rect(foot);
    els.push({ kind: 'rule', x: fr.x, y: fr.y, w: fr.w, h: 0, weight: 0.75 });
    ['.source-lines', '.skill-note', '.credit-note'].forEach(function (sel, i) {
      var el = foot.querySelector(sel);
      if (el) push('text', el, { text: textOf(el), pt: fontPt(el),
                                 align: i === 0 ? (LANG_RTL ? 'r' : 'l')
                                                : (LANG_RTL ? 'l' : 'r') });
    });
  }

  out.push({ id: m.id, band: m.band, title: S.t('map_title_' + m.id, LANG), els: els });
});

document.getElementById('result').textContent =
  btoa(unescape(encodeURIComponent(JSON.stringify(out))));
"""


def probe_html(lang):
    js = PROBE_JS.replace('__LANG__', json.dumps(lang))
    js = js.replace('LANG_RTL', 'true' if lang in RTL_LANGS else 'false')
    rtl = ' dir="rtl"' if lang in RTL_LANGS else ''
    return (
        f'<!doctype html><html lang="{lang}"{rtl}><head><meta charset="utf-8">'
        f'<style>*{{box-sizing:border-box}}body{{margin:0}}{SHEET_CSS}</style></head>'
        '<body><div id="host"></div><div id="result"></div>'
        f'<script>{DATA_JS}</script><script>{SHEET_JS}</script>'
        f'<script>{js}</script></body></html>')


def measure(browser, lang):
    tmp = ROOT / f'_probe_{lang}.html'
    tmp.write_text(probe_html(lang), encoding='utf-8')
    try:
        dom = subprocess.run([
            browser, '--headless=new', '--disable-gpu', '--no-sandbox',
            '--run-all-compositor-stages-before-draw', '--virtual-time-budget=30000',
            '--dump-dom', tmp.as_uri(),
        ], check=True, capture_output=True, text=True).stdout
    finally:
        tmp.unlink(missing_ok=True)
    m = re.search(r'<div id="result">([A-Za-z0-9+/=]*)</div>', dom)
    if not m or not m.group(1):
        raise RuntimeError(f'{lang}: probe produced no geometry — did sheet.js throw?')
    return json.loads(base64.b64decode(m.group(1)).decode('utf-8'))


# --------------------------------------------------------------------------
# 2. Turn measurements into slides
# --------------------------------------------------------------------------

def build_slide(sheet, rtl):
    """One measured sheet -> the shape XML for one slide."""
    parts = []
    sid = 2  # shape id 1 is the slide's own group

    for el in sheet['els']:
        x = el['x'] + MARGIN
        y = el['y'] + MARGIN
        w, h = el['w'], el['h']

        if el['kind'] == 'rule':
            parts.append(ox.line(sid, 'rule', x, y, w, line_w_pt=el.get('weight', 1)))
        elif el['kind'] == 'shape':
            paras = [(el['text'], el['pt'], True)]
            if el.get('blank'):
                # The event-name slot: a write-on rule under the label.
                paras.append(('________________', el['pt'], False))
            elif el.get('geom') != 'ellipse':
                # An empty unbolded paragraph, so clicking into the box puts the
                # cursor on a fresh line below the prompt instead of inside it.
                # Ellipses are centred labels with no room to answer in.
                paras.append(('', el['pt'], False))
            parts.append(ox.shape(
                sid, el['text'][:60] or 'box', x, y, w, h,
                geom=el.get('geom', 'roundRect'), adj=el.get('adj'),
                line_w_pt=el.get('weight', 1.5), dash=el.get('dash'),
                paragraphs=paras, align=el.get('align', 'l'),
                anchor=el.get('anchor', 't'), rtl=rtl))
        elif el.get('arrow'):
            # Widen about the same centre so the glyph is never squeezed.
            grow = max(0.0, 0.55 - w) / 2
            parts.append(ox.textbox(
                sid, 'arrow', x - grow, y, w + 2 * grow, h,
                paragraphs=[(el['text'], el['pt'], True)],
                align='ctr', anchor='ctr', rtl=rtl, wrap=False))
        else:
            # Text is measured tight; give it a little slack so PowerPoint's
            # metrics (which differ slightly from the browser's) do not clip it.
            parts.append(ox.textbox(
                sid, 'label', x, y, w + 0.04, h + 0.06,
                paragraphs=[(el['text'], el['pt'], el.get('bold', False))],
                align=el.get('align', 'l'), anchor=el.get('anchor', 't'), rtl=rtl))
        sid += 1

    return ''.join(parts)


def _write(out, slides, title):
    out.parent.mkdir(parents=True, exist_ok=True)
    ox.write_pptx(out, slides, width_in=PAGE_W, height_in=PAGE_H, title=title)
    return out


def build_language_deck(lang, sheets):
    """One language, all 24 maps — the deck that mirrors the printed packet."""
    slides = [build_slide(s, lang in RTL_LANGS) for s in sheets]
    title = DATA['locales'].get(lang, {}).get('title', 'History Event Maps')
    return _write(OUT_DIR / f'history-event-maps_{lang}.pptx', slides, title)


def build_map_deck(index, measurements, langs):
    """One map, all seven languages — so a teacher who wants a single organizer
    gets every language their classroom needs in one file, in one download."""
    map_id = DATA['maps'][index]['id']
    slides = [build_slide(measurements[lang][index], lang in RTL_LANGS)
              for lang in langs]
    title = DATA['locales']['en'].get('map_title_' + map_id, map_id)
    return _write(OUT_DIR / 'maps' / f'{map_id}.pptx', slides,
                  f'{title} — 7 languages')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lang', help='build only this language\'s full-library deck')
    args = ap.parse_args()

    browser = find_browser()
    langs = list(DATA['locales'])          # en first, then the other six
    n_maps = len(DATA['maps'])

    # Measure every language once; both deck families are cut from the same
    # measurements, so a per-map deck can never disagree with the packet.
    measurements = {}
    for lang in langs:
        sheets = measure(browser, lang)
        if len(sheets) != n_maps:
            raise RuntimeError(f'{lang}: measured {len(sheets)} sheets, expected {n_maps}')
        measurements[lang] = sheets
        print(f'  measured {lang}')

    if args.lang and args.lang not in langs:
        sys.exit(f'unknown language: {args.lang}')

    total = 0
    for lang in ([args.lang] if args.lang else langs):
        out = build_language_deck(lang, measurements[lang])
        total += out.stat().st_size
        print(f'{lang}: {n_maps} slides -> {out.relative_to(ROOT)} '
              f'({out.stat().st_size // 1024} KB)')

    for i in range(n_maps):
        out = build_map_deck(i, measurements, langs)
        total += out.stat().st_size
        print(f'{DATA["maps"][i]["id"]}: {len(langs)} slides -> '
              f'{out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)')

    print(f'\n{total // 1024} KB total')


if __name__ == '__main__':
    main()
