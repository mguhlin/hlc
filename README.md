# History Learning Center

Live: https://mguhlin.github.io/hlc/ · Repository: https://github.com/mguhlin/hlc

This is the classroom resource itself. The earlier illustrated build plan is retained in `docs/` for project history.

## Classroom resources

- Student-facing daily flipbook: 185 school-day slots, organized as 37 five-day investigations. Each stimulus supports notice, compare, connect, question, and transfer practice.
- Four grade-band scaffolds; 49 inquiry activities and teaching routines; 16 printable tools.
- Seven language editions: English, Spanish, Vietnamese, Chinese, Hindi, Urdu, Arabic. Arabic and Urdu use right-to-left layouts. Translations have not been independently reviewed by fluent speakers.
- PST: complete imported problem-solving collection, including grade-specific units, assessment packs, teacher guidance, image inquiry, and games.
- Event Maps: 24 reusable organizers, seven-language print-ready PDF sheets and packets, and editable PowerPoint downloads.
- Juneteenth & the Meaning of Freedom: a seven-language collection of 13 self-contained interactive activities (K–12) tracing June 19, 1865, from Galveston to a federal holiday. Built from `juneteenth/build.py`; see `juneteenth/README.md`.
- Teacher guidance connects TEKS skills, current ELPS, UDL, ACE/SOLO progression, evidence-based instructional strategies, and official assessment resources.

The calendar supplements grade-specific history instruction; it is not a complete course curriculum. Invented practice scenarios are labeled. Historical statements link to original records. Selected TEKS examples are explicitly representative, not blanket alignment for every grade. Effect sizes describe research syntheses, not promised gains from these activities.

## Build and preview

`python3 scripts/build.py` generates the seven static language editions from `data/`.

`python3 scripts/check_links.py` checks local HTML links and dependencies.

`python3 -m http.server 4178` serves a local preview.

The flipbook embeds its data and needs no runtime content service. School start date and excluded dates stay in browser local storage. Student responses are completed on paper or orally; no accounts or response collection.

## Imported collections

`pst/` and `eventmaps/` are independently runnable, with their shared language scripts bundled locally. Content attribution: **CC BY-NC 4.0 · Miguel Guhlin 2026**. Original third-party historical sources retain their own terms. Generated classroom images are illustrative, not authentic evidence. Image provenance is recorded in `credits.json`.

To refresh Event Maps downloads after source edits, run `python3 eventmaps/generate_packets.py` and `python3 eventmaps/generate_pptx.py` (Chrome and pypdf required). The starter-kit ZIP mirrors the adapted `pst/pst-starter-kit/` directory.

GitHub Pages serves the root of `main`. Commit, push, monitor the Pages workflow, and verify the live site after publication.
