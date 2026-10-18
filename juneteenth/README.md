# Juneteenth & the Meaning of Freedom

A self-contained collection in the History Learning Center: a landing page and 13 interactive,
browser-based activities across four grade bands (K–2, 3–5, 6–8, 9–12), each in seven languages.
Students trace June 19, 1865, from Galveston to a federal holiday — reading General Order No. 3,
weighing what freedom meant in practice, and connecting the past to how Texans mark the day today.

Source list: NEA, [Teaching Juneteenth and the Meaning of Freedom](https://www.nea.org/professional-excellence/student-engagement/tools-tips/teaching-juneteenth-and-meaning-freedom).

## Design

- Every activity is one self-contained HTML file: inline CSS and JavaScript, no asset folders, no external scripts. Works offline.
- No logins, no storage, no data collected. Student responses are completed on paper or orally.
- Seven language editions: English at `juneteenth/`, others at `juneteenth/<lang>/`. Arabic and Urdu use right-to-left layouts.
- Each activity ships with a teacher panel: objective, TEKS (current code plus a blank 2026 field), answer key, discussion questions, and hard-history guidance. A grayscale print path is built in.
- Five reusable interaction engines cover all 13 activities: sort (tap-to-assign, with a map variant), sequence (accessible up/down ordering), reveal (tap-to-explore), annotate (tag passage segments), and breakout (clue locks).

## Build

Content lives in `content.py` (English, canonical); the English text of each string is also its
translation key. Translations load from `translations.json` (`{lang: {english: translated}}`) with
English fallback per string.

```
python3 juneteenth/build.py            # build all seven language editions (98 files)
python3 juneteenth/build.py extract    # write strings.en.json, the translation worklist
```

`t_<lang>.json` are the per-language translation drafts merged into `translations.json`.
Translations were authored with AI assistance and await review by fluent speakers.

## Standards and timing

Activities align to the TEKS in force now. The State Board of Education completed its K–12 social
studies revision in September 2026; districts begin implementing the new standards in 2030–31 for the
early grades, with high-school courses following in 2033–34. Grade 2 culture-strand and §113.41
(U.S. History Since 1877) codes are marked for verification in the activities that use them.

Content: **CC BY-NC 4.0 · © 2026 TCEA** · code **MIT**. Historical sources retain their own terms.
