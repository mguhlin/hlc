# History Event Maps

24 reusable, one-page social studies graphic organizers for grades 3–5, 6–8,
and 9–12. Published at **https://mguhlin.github.io/hlc/eventmaps/**.

## What this is

- Printable event maps — organizers, not lessons or units
- Eight maps per grade band, each built around one thinking skill
- Seven languages: English, Spanish, Vietnamese, Arabic, Simplified Chinese, Urdu, Hindi
- Grayscale, US Letter landscape; box roles are carried by border *style*, not
  colour, so one monochrome print works on any classroom copier
- TEKS-aligned by reusable Social Studies Skills focus
- Static HTML/CSS/JS, no login, no data collection

## Layout

```
index.html          the 24-map library, filterable by grade band / skill / search
organizer.html?map= one sheet, full size, for screen and print
about.html          about / how to use / standards / privacy / accessibility
assets/
  data.js           24 maps + 7 locales (the map library's own dictionary)
  i18n-chrome.js    the Activities-hub chrome strings layered on top
  i18n.js           the shared hub i18n engine (canonical copy: ctobs/assets/i18n.js)
  chrome.js         merges the two dictionaries, registers them, wires back-to-top
  sheet.js          pure (map, lang) -> sheet HTML renderer
  sheet.css         the printable sheet
  sheet-print.css   @page rules — organizer.html only, never the hub
  eventmaps.css     hub chrome (activities design system)
  hub.js            the library page
  hero.png          the index banner (also the og:image)
pdf/<map>/<lang>/bw.pdf   168 single sheets
pdf-packets/              7 full-library packets (24 pages)
pdf-band-packets/         21 grade-band packets (8 pages)
pptx/                     7 editable decks, one per language (24 slides)
pptx/maps/                24 editable decks, one per map (7 slides)
generate_packets.py       the PDFs
generate_pptx.py          the decks
pptx_ooxml.py             dependency-free .pptx writer
```

## Thumbnails are the real sheet

The library cards do not use preview images. Each card renders the *actual*
organizer via `sheet.js` and scales it to card width with a CSS transform, so a
thumbnail cannot drift out of sync with the map it previews, and it re-renders
in whatever language the reader picked. The card blurb is likewise read back
out of the rendered layout — it lists the prompts genuinely printed on that
sheet.

This is also why `sheet.css` states `box-sizing`, margins, and `text-align`
explicitly, and why the hub's footer rules are scoped to `.wrap > footer`: the
sheet carries its own `<header>` and `<footer>`, and a bare element selector in
the page chrome silently reaches into all 24 thumbnails and the printout.

## The banner and the text under it

`assets/hero.png` states the title, tagline, and both intro lines — in English,
baked into the artwork. So `hub.js` collapses the `#hero-text` block to
`.sr-only` when English is selected (it would otherwise be a verbatim second
copy) and shows it for the other six languages, where the banner is not a
translation. It toggles `.sr-only` rather than `hidden` so the `<h1>` and the
intro stay in the accessibility tree and reachable by page translators in all
seven languages. With JS off the block simply stays visible.

## Language

The picker uses the hub's shared engine, so the language a teacher chose in
CTOBs, PlotPoint, or lab-safety carries into this area (`hlc.pst.lang`),
and `?lang=es` share links work. Arabic and Urdu render right-to-left, sheets
included.

## Regenerating the PDFs

```bash
python3 generate_packets.py
```

Renders each language's 24-page packet with headless Chrome from the same
`assets/` files the site loads, then splits it into single sheets and grade-band
packets. Requires `pypdf` and Chrome/Chromium on PATH.

**Re-run it after editing `data.js`, `sheet.js`, `sheet.css`, or
`sheet-print.css`** — otherwise the downloads drift away from what the site
shows. The splitter fails loudly if a sheet overflows onto a second page.

## Regenerating the PowerPoint

```bash
python3 generate_pptx.py
```

Builds two families of deck from one set of measurements, so they cannot
disagree with each other or with the PDFs:

| Output | Shape | For |
|---|---|---|
| `pptx/history-event-maps_<lang>.pptx` | 7 decks × 24 slides | one language, every map — mirrors the printed packet |
| `pptx/maps/<map-id>.pptx` | 24 decks × 7 slides | one map, every language — a single organizer a whole mixed-language class can read |

Same inputs, same re-run rule. Converting the PDF would give either a deck of
pictures or, through a PDF importer, a tangle of loose glyph runs and paths —
editable in name only. So the deck is built from the measurements instead:
headless Chrome renders the real sheets, `getBoundingClientRect()` reports where
every box, label, and rule ended up, and each one is re-emitted as a native
PowerPoint autoshape at the same coordinates. Every prompt is real text in a
real text frame; every box is a real shape that can be moved, restyled, or
deleted; a student can click into one and type.

Two deliberate differences from the print version:

- **No ruled writing lines.** On paper they guide handwriting; on a slide they
  just obstruct the cursor. Each box is open typing space under its prompt,
  with an empty second paragraph so the caret lands below the prompt rather
  than inside it.
- **CSS `double` borders become heavier solid ones**, because PowerPoint has no
  double-stroke preset. Dashed and solid carry over exactly, so the roles the
  boxes encode still read without relying on colour.

`pptx_ooxml.py` writes the OOXML package directly — python-pptx is not
installable here (no pip) and vendoring it for one script is not worth it.

### Why the library cards are `<div>`s

Each card offers two destinations — preview the map, or download its deck — and
an `<a>` cannot legally contain another `<a>`. So the card is a `<div>`, the
title link carries `.stretch` (an absolutely positioned `::after` covering the
card at `z-index:1`) to keep the whole card clickable, and the download link
sits above it at `z-index:2` so it wins its own clicks. Keep `.card`
`position:relative` or the stretched link escapes to the nearest positioned
ancestor and swallows the page.

## Current TEKS basis

Aligned to the 2022-adopted Texas Social Studies TEKS implemented beginning in
2024–2025. The Texas Education Agency is revising the Social Studies TEKS, so
exact codes should be reviewed when new standards take effect. Alignment here
emphasizes the recurring Social Studies Skills strand: source use, chronology,
sequencing, cause/effect, comparison, historical context, point of view,
geographic interpretation, claims/evidence, and written/visual communication.

See `TEKS_ALIGNMENT.md` for the reference table.

## Privacy

No accounts, cookies, forms, analytics, or student data. The only thing stored
in the browser is the language preference.
