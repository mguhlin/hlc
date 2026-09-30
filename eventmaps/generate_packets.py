"""History Event Maps — build the printable PDF library.

Renders every organizer with headless Chrome (the same engine that renders the
site, from the same assets/ files, so the PDFs and the on-screen sheets cannot
diverge), then splits the result three ways:

    pdf/<map-id>/<lang>/bw.pdf                     24 x 7 = 168 single sheets
    pdf-packets/history-event-maps_<lang>_bw.pdf   7 x 24-page full library
    pdf-band-packets/..._<band>_<lang>_bw.pdf      21 x 8-page grade-band packets

Grayscale only: the sheets carry role by border style, not colour, so one
monochrome print works on any classroom copier.

    python3 generate_packets.py

Requires: pypdf, and Chrome or Chromium on PATH. Re-run after editing
assets/data.js, assets/sheet.js, assets/sheet.css, or assets/sheet-print.css —
otherwise the downloads drift away from what the site shows.
"""
from pathlib import Path
import json
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
DATA = json.loads((ROOT / 'data.json').read_text(encoding='utf-8'))

# The packet document is assembled from the very same files the browser loads.
SHEET_CSS = (ASSETS / 'sheet.css').read_text(encoding='utf-8')
PRINT_CSS = (ASSETS / 'sheet-print.css').read_text(encoding='utf-8')
DATA_JS = (ASSETS / 'data.js').read_text(encoding='utf-8')
SHEET_JS = (ASSETS / 'sheet.js').read_text(encoding='utf-8')

PDF_DIR = ROOT / 'pdf'
PACKETS = ROOT / 'pdf-packets'
BAND_PACKETS = ROOT / 'pdf-band-packets'

BANDS = ['3-5', '6-8', '9-12']

BROWSERS = ['google-chrome', 'chromium', 'chromium-browser', 'google-chrome-stable']


def find_browser():
    for name in BROWSERS:
        path = shutil.which(name)
        if path:
            return path
    raise SystemExit('No Chrome/Chromium found on PATH (tried: %s)' % ', '.join(BROWSERS))


def packet_html(lang):
    """One document holding all 24 sheets for a language, one per page."""
    build = """
var S = window.HEM_SHEET, lang = %s;
document.documentElement.lang = (lang === 'zh') ? 'zh-CN' : lang;
if (lang === 'ar' || lang === 'ur') document.documentElement.dir = 'rtl';
document.getElementById('packet').innerHTML = S.maps.map(function (m) {
  return '<section class="packet-page">' + S.sheetHTML(m, lang) + '</section>';
}).join('');
""" % json.dumps(lang)
    return (
        '<!doctype html><html class="packet-html"><head><meta charset="utf-8">'
        f'<style>{SHEET_CSS}\n{PRINT_CSS}</style></head>'
        '<body class="packet-doc"><main id="packet" class="packet-shell"></main>'
        f'<script>{DATA_JS}</script><script>{SHEET_JS}</script><script>{build}</script>'
        '</body></html>'
    )


def render_packet(browser, lang, out_path):
    """Print one language's 24-page packet. A temp file next to the assets keeps
    fonts and relative resolution identical to the served site."""
    tmp = ROOT / f'_packet_{lang}.html'
    tmp.write_text(packet_html(lang), encoding='utf-8')
    try:
        subprocess.run([
            browser, '--headless=new', '--disable-gpu', '--no-sandbox',
            '--no-pdf-header-footer', '--run-all-compositor-stages-before-draw',
            '--virtual-time-budget=30000',
            f'--print-to-pdf={out_path}', tmp.as_uri(),
        ], check=True, capture_output=True)
    finally:
        tmp.unlink(missing_ok=True)


def split_packet(packet_path, lang):
    from pypdf import PdfReader, PdfWriter
    reader = PdfReader(str(packet_path))
    if len(reader.pages) != len(DATA['maps']):
        raise RuntimeError(
            f'{packet_path}: expected {len(DATA["maps"])} pages, got {len(reader.pages)}. '
            'A sheet is overflowing its page — check sheet.css before shipping.')
    by_band = {band: [] for band in BANDS}
    for idx, m in enumerate(DATA['maps']):
        out = PDF_DIR / m['id'] / lang / 'bw.pdf'
        out.parent.mkdir(parents=True, exist_ok=True)
        writer = PdfWriter()
        writer.add_page(reader.pages[idx])
        with out.open('wb') as f:
            writer.write(f)
        by_band[m['band']].append(reader.pages[idx])
    for band, pages in by_band.items():
        writer = PdfWriter()
        for page in pages:
            writer.add_page(page)
        out = BAND_PACKETS / f'history-event-maps_{band.replace("-", "")}_{lang}_bw.pdf'
        with out.open('wb') as f:
            writer.write(f)


def main():
    browser = find_browser()
    for path in (PDF_DIR, PACKETS, BAND_PACKETS):
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)

    for lang in DATA['locales']:
        out = PACKETS / f'history-event-maps_{lang}_bw.pdf'
        render_packet(browser, lang, out)
        split_packet(out, lang)
        print(lang, 'bw done')


if __name__ == '__main__':
    main()
