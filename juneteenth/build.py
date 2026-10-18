#!/usr/bin/env python3
"""Build the self-contained Juneteenth & the Meaning of Freedom collection.

Generates a landing page and 13 interactive activities as standalone HTML files,
one static edition per language (English at juneteenth/, others at juneteenth/<lang>/).
Each file inlines its CSS and JavaScript; no asset folders, no external scripts.

Content lives in content.py (English, canonical). The English text of every
string doubles as its translation key. Translations load from translations.json
as {lang: {english_text: translated_text}} and fall back to English per string.

Usage:
  python3 juneteenth/build.py            build every language edition
  python3 juneteenth/build.py extract    write strings.en.json (the translation worklist)
"""
import html
import json
import sys
from pathlib import Path

from content import CONTENT, UI

ROOT = Path(__file__).resolve().parent
LANGS = ['en', 'es', 'vi', 'zh', 'hi', 'ur', 'ar']
NAMES = ['English', 'Español', 'Tiếng Việt', '简体中文', 'हिन्दी', 'اردو', 'العربية']
RTL = {'ar', 'ur'}

TRANSLATIONS = {}
tpath = ROOT / 'translations.json'
if tpath.exists():
    TRANSLATIONS = json.loads(tpath.read_text())


def esc(value):
    return html.escape(str(value), quote=True)


def t(key, lang):
    """Translate a UI key or an English content string into `lang`.

    English is canonical: UI uses short keys; content passes English text directly.
    Any string missing a translation falls back to its English form.
    """
    english = UI.get(key, key)
    if lang == 'en':
        return english
    return TRANSLATIONS.get(lang, {}).get(english) or english


# --------------------------------------------------------------------------- #
# Inline stylesheet — HLC design tokens, self-contained.                      #
# --------------------------------------------------------------------------- #
CSS = """
:root{--ink:#183440;--muted:#53666c;--paper:#fbf7ec;--sage:#e5ede4;--gold:#a66a26;--line:#ccd6ce;--accent:#225e60;--good:#1f7a3f;--bad:#9c3327}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:#f4f3ec;color:var(--ink);font:17px/1.55 system-ui,-apple-system,'Segoe UI',sans-serif}
h1,h2,h3,p{margin:0 0 16px}h1,h2{font-family:Georgia,'Noto Serif',serif;line-height:1.12}
h1{font-size:clamp(2.1rem,4.5vw,3.6rem)}h2{font-size:clamp(1.5rem,3vw,2.3rem)}h3{font-size:1.12rem;line-height:1.3}
a{color:#195e66;text-underline-offset:3px}button,input,select,textarea{font:inherit}
button,.button{cursor:pointer;border:1px solid var(--line);border-radius:9px;background:white;color:var(--ink);padding:10px 15px;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:44px}
.button.primary,button.primary{background:var(--ink);border-color:var(--ink);color:white}
button:hover,.button:hover{filter:brightness(.96)}button:disabled{opacity:.45;cursor:default}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible,textarea:focus-visible,[tabindex]:focus-visible{outline:3px solid #bc7a2e;outline-offset:3px}
.wrap{max-width:1120px;padding:0 28px;margin:auto}
.site-head{background:var(--ink);color:white;padding:15px 0}
.head-inner{display:flex;align-items:center;gap:20px;flex-wrap:wrap}
.brand{font-weight:800;letter-spacing:-.03em;color:white;text-decoration:none;font-size:1.05rem}
.site-head nav{display:flex;gap:8px 18px;flex:1;flex-wrap:wrap}
.site-head nav a{color:#ebf0e9;text-decoration:none;font-size:.88rem}
.language{margin-inline-start:auto;display:flex;align-items:center;gap:8px;font-size:.8rem}
.language select{max-width:150px;padding:8px;border-radius:7px;border:1px solid #728a8e;background:white;color:var(--ink)}
.skip{position:absolute;inset-inline-start:-10000px;top:0}.skip:focus{inset-inline-start:8px;z-index:100;background:white;padding:12px}
.hero{background:linear-gradient(120deg,#10272f,#214a4c);color:white;padding:52px 0 44px}
.hero .eyebrow{letter-spacing:.11em;text-transform:uppercase;font-size:.76rem;font-weight:800;margin-bottom:14px;color:#d9b98a}
.hero h1{max-width:900px}.hero p{max-width:720px;font-size:1.12rem;color:#eaf1ec}
.hero .flag{display:flex;gap:6px;margin-bottom:22px}
.hero .flag i{width:26px;height:17px;border-radius:3px;display:block}
.stats{display:flex;gap:22px;flex-wrap:wrap;font-size:.95rem;font-weight:700;padding:20px 0;border-bottom:1px solid var(--line)}
.section{padding:34px 0}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.grid.two{grid-template-columns:repeat(2,minmax(0,1fr))}
.card{padding:23px;border:1px solid var(--line);border-radius:12px;background:white;min-width:0;display:flex;flex-direction:column}
.card .pill{align-self:flex-start}.card .button{margin-top:auto}
.card p{font-size:.97rem}.card h3{font-family:Georgia,serif;font-size:1.3rem;margin-top:8px}
.pill{display:inline-block;background:var(--sage);padding:4px 11px;border-radius:20px;font-size:.77rem;font-weight:700;margin:0 4px 8px 0}
.pill.k2{background:#f3e3cf}.pill.g35{background:#dceadd}.pill.g68{background:#d7e3ef}.pill.g912{background:#e7ddee}
.page-title{padding:34px 0 10px}.page-title p{max-width:820px}
.lesson{max-width:900px;margin:auto}
.actions{display:flex;gap:12px;flex-wrap:wrap;margin:14px 0}
.notice{background:var(--sage);border-inline-start:4px solid var(--accent);padding:16px 20px;border-radius:5px;margin:18px 0}
.objective{font-weight:600}
.source-box{background:white;border:1px solid var(--line);border-inline-start:4px solid var(--gold);border-radius:8px;padding:18px 20px;margin:16px 0}
.source-box .cite{font-size:.8rem;color:var(--muted);margin:10px 0 0}
.source-box blockquote{margin:0;font-size:1.05rem;font-style:italic}
.source-links{font-size:.82rem;margin:10px 0}.source-links a{display:inline-block;margin-inline-end:14px;margin-bottom:6px}
.work-lines{height:150px;background:repeating-linear-gradient(white,white 30px,#bfc9be 31px,white 32px);border:1px solid var(--line);margin:13px 0 20px;border-radius:6px}
details{border-top:1px solid var(--line);padding:15px 0;margin-top:20px}
summary{cursor:pointer;font-weight:700}details h3{margin-top:16px}details p,details ul{margin-top:10px}
.footer{padding:26px 0;border-top:1px solid var(--line);font-size:.8rem;color:var(--muted);margin-top:30px}
.footer p{margin:6px 0}
.small{font-size:.82rem;color:var(--muted)}
.status{font-weight:700;margin:12px 0;min-height:1.4em}
.status.good{color:var(--good)}.status.bad{color:var(--bad)}
.sort-items{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0}
.chip{border:1px solid var(--line);background:white;border-radius:9px;padding:11px 15px;min-height:44px;font-size:.98rem;text-align:start}
.chip[aria-pressed=true]{outline:3px solid var(--gold);outline-offset:2px}
.chip.placed{opacity:.6}
.buckets{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin:14px 0}
.bucket{border:2px dashed var(--line);border-radius:12px;padding:14px;min-height:130px;background:#fff}
.bucket h3{margin:0 0 10px;font-family:Georgia,serif;font-size:1.15rem}
.bucket .drop{display:flex;flex-wrap:wrap;gap:8px;min-height:44px}
.bucket .chip.ok{border-color:var(--good);background:#eef7f0}
.bucket .chip.no{border-color:var(--bad);background:#fbeeec}
.bucket.mapregion{border-style:solid;background:#edf0df}
.seq{list-style:none;padding:0;margin:14px 0}
.seq li{display:flex;gap:12px;align-items:center;background:white;border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-bottom:10px}
.seq li .date{font:700 .95rem Georgia,serif;color:var(--accent);min-width:92px}
.seq li .txt{flex:1;min-width:0}
.seq li .mv{display:flex;flex-direction:column;gap:4px}
.seq li .mv button{min-height:0;padding:4px 10px;font-size:1rem;line-height:1}
.seq li.ok{border-color:var(--good);background:#eef7f0}.seq li.no{border-color:var(--bad);background:#fbeeec}
.reveal{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:14px 0}
.reveal .part{text-align:start;align-items:flex-start;flex-direction:column;gap:6px;padding:15px;height:100%}
.reveal .part b{font-size:1.05rem}
.reveal .part .detail{font-weight:400;font-size:.95rem;color:var(--muted)}
.reveal .part[aria-expanded=false] .detail{display:none}
.tags{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0}
.tags button[aria-pressed=true]{outline:3px solid var(--gold);outline-offset:2px}
.tag-dot{width:14px;height:14px;border-radius:50%;display:inline-block;margin-inline-end:6px;vertical-align:middle}
.passage{background:white;border:1px solid var(--line);border-radius:8px;padding:18px 20px;line-height:2;font-size:1.05rem}
.passage .seg{cursor:pointer;border-radius:4px;padding:2px 3px}
.passage .seg.sel{box-shadow:0 0 0 2px var(--gold)}
.tcol-0{background:#dcecdd}.tcol-1{background:#dbe7f4}.tcol-2{background:#f4ddd6}.tcol-3{background:#e8dcf0}
.tdot-0{background:#1f7a3f}.tdot-1{background:#1f4e79}.tdot-2{background:#9c3327}.tdot-3{background:#6a3d8a}
.passage .seg.wrong{box-shadow:0 0 0 2px var(--bad)}
.lock{border:1px solid var(--line);border-radius:12px;padding:18px;margin:14px 0;background:#fff;position:relative}
.lock[data-open=false] .lock-body{filter:blur(4px);opacity:.45;pointer-events:none;user-select:none}
.lock .badge{position:absolute;inset-inline-end:14px;top:14px;font-size:.72rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.lock[data-open=true] .badge{color:var(--good)}
.lock .clue{font-weight:700;margin-bottom:8px}
.lock .choices{display:flex;flex-direction:column;gap:8px;margin:10px 0}
.lock .choices label{display:flex;gap:9px;align-items:flex-start;background:#fafbf8;border:1px solid var(--line);border-radius:8px;padding:10px 12px;cursor:pointer}
.lock .reveal-text{margin-top:10px;padding:12px 14px;background:var(--sage);border-radius:8px}
@media(max-width:850px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.head-inner{gap:12px}.site-head nav{order:3;flex-basis:100%}}
@media(max-width:560px){.wrap{padding:0 16px}.grid,.grid.two{grid-template-columns:1fr}.stats{gap:10px;flex-direction:column}.language label{display:none}.seq li .date{min-width:0}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation:none!important;transition:none!important}}
@media print{
 @page{margin:14mm}
 body{background:white;color:#000;font-size:11pt}
 .site-head,.footer,.no-print,.language{display:none!important}
 .wrap{max-width:none;padding:0}.section{padding:6px 0}
 .card,.lock,.bucket,.seq li,.source-box{break-inside:avoid}
 .reveal .part[aria-expanded] .detail{display:block!important}
 .lock[data-open=false] .lock-body{filter:none;opacity:1}
 .chip[aria-pressed]{outline:none}
 details{border:0}details>summary{display:none}details[open]{display:block}
 .work-lines{height:120px;print-color-adjust:exact;-webkit-print-color-adjust:exact}
 .tcol-0,.tcol-1,.tcol-2,.tcol-3,.pill,.bucket.mapregion,.hero .flag i{print-color-adjust:exact;-webkit-print-color-adjust:exact}
 h1{font-size:22pt}h2{font-size:15pt}
}
"""

# --------------------------------------------------------------------------- #
# Inline behaviour — one bundle, drives every engine by data attributes.      #
# --------------------------------------------------------------------------- #
JS = r"""
(function(){
 'use strict';
 var L = window.__JT__ || {};
 function say(el, msg, good){ if(!el) return; el.textContent = msg; el.className = 'status ' + (good===true?'good':good===false?'bad':''); }
 document.querySelectorAll('[data-print]').forEach(function(b){ b.addEventListener('click', function(){ window.print(); }); });

 document.querySelectorAll('[data-engine=sort]').forEach(function(root){
  var status = root.querySelector('.status'), picked = null;
  function clearPick(){ if(picked){ picked.setAttribute('aria-pressed','false'); picked=null; } }
  root.querySelectorAll('.chip').forEach(function(chip){
   chip.addEventListener('click', function(){
    if(chip.classList.contains('placed')){ root.querySelector('.sort-items').appendChild(chip); chip.classList.remove('placed','ok','no'); return; }
    if(picked===chip){ clearPick(); return; }
    clearPick(); picked=chip; chip.setAttribute('aria-pressed','true');
   });
  });
  root.querySelectorAll('.bucket').forEach(function(bucket){
   bucket.addEventListener('click', function(e){
    if(e.target.closest('.chip')) return;
    if(!picked) return;
    bucket.querySelector('.drop').appendChild(picked); picked.classList.add('placed'); picked.classList.remove('ok','no'); clearPick();
   });
  });
  var check = root.querySelector('[data-check]');
  if(check) check.addEventListener('click', function(){
   if(root.querySelectorAll('.sort-items .chip').length>0){ say(status, L.pick_item, false); return; }
   var total=0, right=0;
   root.querySelectorAll('.bucket').forEach(function(b){
    b.querySelectorAll('.chip').forEach(function(chip){
     total++; var ok = chip.dataset.cat === b.dataset.cat;
     chip.classList.toggle('ok', ok); chip.classList.toggle('no', !ok); if(ok) right++;
    });
   });
   say(status, right===total? L.all_correct : L.some_wrong, right===total);
  });
  var reset = root.querySelector('[data-reset]');
  if(reset) reset.addEventListener('click', function(){
   var tray = root.querySelector('.sort-items');
   root.querySelectorAll('.bucket .chip').forEach(function(c){ c.classList.remove('placed','ok','no'); tray.appendChild(c); });
   clearPick(); say(status,'');
  });
 });

 document.querySelectorAll('[data-engine=sequence]').forEach(function(root){
  var list = root.querySelector('.seq'), status = root.querySelector('.status');
  list.querySelectorAll('li').forEach(function(li){
   li.querySelector('.up').addEventListener('click', function(){ var p=li.previousElementSibling; if(p) list.insertBefore(li,p); });
   li.querySelector('.down').addEventListener('click', function(){ var n=li.nextElementSibling; if(n) list.insertBefore(n,li); });
  });
  var check = root.querySelector('[data-check]');
  if(check) check.addEventListener('click', function(){
   var ok=true;
   [].slice.call(list.children).forEach(function(li,i){ var good=(+li.dataset.order)===i; li.classList.toggle('ok',good); li.classList.toggle('no',!good); if(!good) ok=false; });
   say(status, ok? L.all_correct : L.some_wrong, ok);
  });
  var reset = root.querySelector('[data-reset]');
  if(reset) reset.addEventListener('click', function(){
   [].slice.call(list.children).sort(function(a,b){ return (+a.dataset.shuffle)-(+b.dataset.shuffle); }).forEach(function(li){ li.classList.remove('ok','no'); list.appendChild(li); });
   say(status,'');
  });
 });

 document.querySelectorAll('[data-engine=reveal] .part').forEach(function(p){
  p.addEventListener('click', function(){ p.setAttribute('aria-expanded', p.getAttribute('aria-expanded')==='true'?'false':'true'); });
 });

 document.querySelectorAll('[data-engine=annotate]').forEach(function(root){
  var status = root.querySelector('.status'), tag = null;
  root.querySelectorAll('.tags button').forEach(function(b){
   b.addEventListener('click', function(){
    root.querySelectorAll('.tags button').forEach(function(x){ x.setAttribute('aria-pressed','false'); });
    b.setAttribute('aria-pressed','true'); tag = b.dataset.tag;
   });
  });
  root.querySelectorAll('.passage .seg').forEach(function(seg){
   seg.addEventListener('click', function(){
    if(tag===null){ say(status, L.pick_tag, false); return; }
    seg.className='seg tcol-'+tag; seg.dataset.pick=tag;
   });
  });
  var check = root.querySelector('[data-check]');
  if(check) check.addEventListener('click', function(){
   var total=0,right=0;
   root.querySelectorAll('.passage .seg[data-answer]').forEach(function(s){ total++; if(s.dataset.pick===s.dataset.answer){right++;} else { s.classList.add('wrong'); } });
   say(status, right===total? L.all_correct : L.some_wrong, right===total);
  });
  var reset = root.querySelector('[data-reset]');
  if(reset) reset.addEventListener('click', function(){
   root.querySelectorAll('.passage .seg').forEach(function(s){ s.className='seg'; delete s.dataset.pick; });
   root.querySelectorAll('.tags button').forEach(function(x){ x.setAttribute('aria-pressed','false'); }); tag=null; say(status,'');
  });
 });

 document.querySelectorAll('[data-engine=breakout]').forEach(function(root){
  var status = root.querySelector('.status'), locks=[].slice.call(root.querySelectorAll('.lock'));
  locks.forEach(function(lock, idx){
   lock.querySelector('[data-submit]').addEventListener('click', function(){
    var chosen = lock.querySelector('input[type=radio]:checked');
    var val = chosen ? chosen.value : '';
    if(val && val === lock.dataset.answer){
     lock.dataset.open='true'; lock.querySelector('.badge').textContent=L.unlocked;
     var rt=lock.querySelector('.reveal-text'); if(rt) rt.hidden=false;
     var next=locks[idx+1];
     if(next){ next.dataset.open='true'; next.querySelector('.badge').textContent='•'; say(status,L.correct,true); }
     else { say(status, L.solved, true); }
    } else { say(status, L.try_again, false); }
   });
  });
 });
})();
"""


# --------------------------------------------------------------------------- #
# Engine renderers.                                                           #
# --------------------------------------------------------------------------- #
def controls(lang):
    return (f'<div class="actions no-print"><button class="primary" data-check>{t("check", lang)}</button>'
            f'<button data-reset>{t("reset", lang)}</button></div>'
            f'<p class="status" aria-live="polite"></p>')


def render_sort(a, lang):
    d = a['engine']
    tray = ''.join(
        f'<button class="chip" data-cat="{esc(it["cat"])}" aria-pressed="false">{t(it["text"], lang)}</button>'
        for it in d['items'])
    cls = ' mapregion' if d.get('map') else ''
    buckets = ''.join(
        f'<div class="bucket{cls}" data-cat="{esc(b["id"])}"><h3>{t(b["text"], lang)}</h3>'
        f'<div class="drop" role="group" aria-label="{t(b["text"], lang)}"></div></div>'
        for b in d['buckets'])
    return (f'<div data-engine="sort"><p class="no-print">{t("Pick a card, then choose where it belongs.", lang)}</p>'
            f'<div class="sort-items">{tray}</div><div class="buckets">{buckets}</div>{controls(lang)}</div>')


def render_sequence(a, lang):
    items = sorted(a['engine']['items'], key=lambda i: i['shuffle'])
    rows = ''
    for it in items:
        date = f'<span class="date">{esc(it["date"])}</span>' if it.get('date') else ''
        rows += (f'<li data-order="{it["order"]}" data-shuffle="{it["shuffle"]}">{date}'
                 f'<span class="txt">{t(it["text"], lang)}</span>'
                 f'<span class="mv no-print"><button class="up" aria-label="{t("Move up", lang)}">▲</button>'
                 f'<button class="down" aria-label="{t("Move down", lang)}">▼</button></span></li>')
    return f'<div data-engine="sequence"><ol class="seq">{rows}</ol>{controls(lang)}</div>'


def render_reveal(a, lang):
    parts = ''.join(
        f'<button class="part button" aria-expanded="false"><b>{t(p["text"], lang)}</b>'
        f'<span class="detail">{t(p["detail"], lang)}</span></button>'
        for p in a['engine']['parts'])
    return (f'<div data-engine="reveal"><p class="no-print">{t("Tap each part to learn what it means.", lang)}</p>'
            f'<div class="reveal">{parts}</div></div>')


def render_annotate(a, lang):
    d = a['engine']
    tags = ''.join(
        f'<button class="button" data-tag="{i}" aria-pressed="false">'
        f'<span class="tag-dot tdot-{i}"></span>{t(tg, lang)}</button>'
        for i, tg in enumerate(d['tags']))
    segs = ''
    for s in d['segments']:
        if s.get('tag') is not None:
            segs += f'<span class="seg" data-answer="{s["tag"]}">{t(s["text"], lang)}</span> '
        else:
            segs += f'{t(s["text"], lang)} '
    return (f'<div data-engine="annotate"><div class="tags no-print">{tags}</div>'
            f'<div class="passage">{segs}</div>{controls(lang)}</div>')


def render_breakout(a, lang):
    locks = ''
    for i, lk in enumerate(a['engine']['locks']):
        openstate = 'true' if i == 0 else 'false'
        badge = '•' if i == 0 else t('Locked', lang)
        body = '<div class="choices">' + ''.join(
            f'<label><input type="radio" name="lk{i}" value="{esc(c["val"])}"> <span>{t(c["text"], lang)}</span></label>'
            for c in lk['choices']) + '</div>'
        rt = f'<div class="reveal-text" hidden>{t(lk["reveal"], lang)}</div>' if lk.get('reveal') else ''
        locks += (f'<div class="lock" data-open="{openstate}" data-answer="{esc(lk["answer"])}">'
                  f'<span class="badge">{badge}</span><p class="clue">{t(lk["clue"], lang)}</p>'
                  f'<div class="lock-body"><p>{t(lk["prompt"], lang)}</p>{body}'
                  f'<button class="button primary no-print" data-submit>{t("Check my work", lang)}</button>{rt}</div></div>')
    return f'<div data-engine="breakout">{locks}<p class="status" aria-live="polite"></p></div>'


ENGINES = {'sort': render_sort, 'sequence': render_sequence, 'reveal': render_reveal,
           'annotate': render_annotate, 'breakout': render_breakout}


# --------------------------------------------------------------------------- #
# Page assembly.                                                              #
# --------------------------------------------------------------------------- #
def base_prefix(lang):
    return '../' if lang == 'en' else '../../'


def header(lang, route):
    base = base_prefix(lang)
    options = ''
    for l, n in zip(LANGS, NAMES):
        if l == 'en':
            url = route if lang == 'en' else '../' + route
        else:
            url = (l + '/' + route) if lang == 'en' else '../' + l + '/' + route
        options += f'<option value="{l}" data-url="{url}" {"selected" if l == lang else ""}>{n}</option>'
    site = base + ('' if lang == 'en' else lang + '/')
    nav = (f'<a href="{site}index.html">{t("History Learning Center", lang)}</a>'
           f'<a href="{site}activities/">{t("All activities", lang)}</a>')
    if route != 'index.html':
        nav = f'<a href="index.html">{t("Back to the collection", lang)}</a>' + nav
    return (f'<a class="skip" href="#main">{t("Start here", lang)}</a>'
            f'<header class="site-head"><div class="wrap head-inner">'
            f'<a class="brand" href="index.html">{t("collection", lang)}</a>'
            f'<nav aria-label="{t("collection", lang)}">{nav}</nav>'
            f'<div class="language"><label for="language">{t("Language", lang)}</label>'
            f'<select id="language" onchange="location.href=this.selectedOptions[0].dataset.url">{options}</select>'
            f'</div></div></header>')


def footer(lang):
    note = f'<p>{t("This translation was authored with AI assistance and awaits review by a fluent speaker.", lang)}</p>' if lang != 'en' else ''
    return (f'<footer class="footer"><div class="wrap">'
            f'<p>{t("No login. No tracking. Responses stay with you.", lang)}</p>'
            f'<p>{t("Works offline. Nothing you type is saved or sent.", lang)}</p>{note}'
            f'<p>{t("footer_credit", lang)}</p></div></footer>')


def page(lang, route, title, body):
    direction = 'rtl' if lang in RTL else 'ltr'
    i18n = {
        'all_correct': t('Every item is placed correctly. Well done.', lang),
        'some_wrong': t('Not yet — the highlighted items need another look.', lang),
        'pick_item': t('Pick a card, then choose where it belongs.', lang),
        'pick_tag': t('Choose a label, then tap a part of the text.', lang),
        'locked': t('Locked', lang), 'unlocked': t('Unlocked', lang),
        'try_again': t('Not the right clue yet. Look again at the evidence.', lang),
        'correct': t('Correct — the next lock opens.', lang),
        'solved': t('All locks are open. You traced the whole chain.', lang),
    }
    data = json.dumps(i18n, ensure_ascii=False).replace('</', '<\\/')
    doc = (f'<!doctype html><html lang="{lang}" dir="{direction}"><head>'
           f'<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
           f'<meta name="referrer" content="no-referrer">'
           f'<meta name="description" content="{esc(t("collection", lang))} · {esc(title)}">'
           f'<title>{esc(title)}{"" if title == t("collection", lang) else " · " + t("collection", lang)}</title>'
           f'<style>{CSS}</style></head><body>'
           f'{header(lang, route)}{body}{footer(lang)}'
           f'<script>window.__JT__={data};</script><script>{JS}</script></body></html>')
    target = ROOT / ('' if lang == 'en' else lang) / route
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(doc)


BAND_CLASS = {'K–2': 'k2', '3–5': 'g35', '6–8': 'g68', '9–12': 'g912'}
BAND_LABEL = {'K–2': 'Grades K–2', '3–5': 'Grades 3–5', '6–8': 'Grades 6–8', '9–12': 'Grades 9–12'}


def teks_block(a, lang):
    cur = a['teks']
    verify = f'<p class="small">{t("Code not yet confirmed — verify against current TEA TEKS before teaching.", lang)}</p>' if cur.get('verify') else ''
    se = f' — {t(cur["se"], lang)}' if cur.get('se') else ''
    return (f'<p><strong>{t("Current TEKS", lang)}:</strong> <bdi>{esc(cur["code"])}</bdi>{se}</p>{verify}'
            f'<p><strong>{t("2026 TEKS (fill once crosswalks publish):", lang)}</strong> <bdi>__________</bdi></p>')


def teacher_panel(a, lang):
    key = ''.join(f'<li>{t(k, lang)}</li>' for k in a['answer_key'])
    disc = ''.join(f'<li>{t(k, lang)}</li>' for k in a['discussion'])
    return (f'<details class="teacher-details" open><summary>{t("Teacher notes & alignment", lang)}</summary>'
            f'<h3>{t("Objective", lang)}</h3><p>{t(a["objective"], lang)}</p>'
            f'<h3>{t("TEKS alignment", lang)}</h3>{teks_block(a, lang)}'
            f'<h3>{t("Answer key", lang)}</h3><ul>{key}</ul>'
            f'<h3>{t("Discussion questions", lang)}</h3><ul>{disc}</ul>'
            f'<h3>{t("Teaching hard history", lang)}</h3><p>{t(a["hard_history"], lang)}</p>'
            f'<p class="small">{t("Standards reviewed October 17, 2026. Selected skill connections, not a full course alignment.", lang)}</p></details>')


def source_block(a, lang):
    s = a.get('source')
    if not s:
        return ''
    links = ''.join(
        f'<a href="{esc(ln["url"])}" target="_blank" rel="noopener">{t(ln["text"], lang)}</a>'
        for ln in s['links'])
    quote = f'<blockquote>{t(s["quote"], lang)}</blockquote>' if s.get('quote') else ''
    return (f'<h2>{t("Primary source", lang)}</h2><div class="source-box">{quote}'
            f'<p class="cite">{t(s["cite"], lang)}</p></div>'
            f'<div class="source-links"><strong>{t("Read the original source:", lang)} </strong>{links}</div>')


def activity_page(lang, a):
    route = a['slug'] + '.html'
    bcls = BAND_CLASS[a['band']]
    engine_html = ENGINES[a['engine']['type']](a, lang)
    body = (f'<main id="main" class="wrap"><div class="lesson">'
            f'<div class="page-title"><p class="small no-print"><a href="index.html">← {t("Back to the collection", lang)}</a></p>'
            f'<span class="pill {bcls}">{t(BAND_LABEL[a["band"]], lang)}</span>'
            f'<span class="pill">{t(a["format"], lang)}</span>'
            f'<h1>{t(a["title"], lang)}</h1><p>{t(a["intro"], lang)}</p>'
            f'<div class="actions no-print"><button class="primary" data-print>{t("Print this activity", lang)}</button></div></div>'
            f'<p class="objective"><strong>{t("I can…", lang)}</strong> {t(a["can"], lang)}</p>'
            f'<h2>{t("Look closely", lang)}</h2>{engine_html}'
            f'{source_block(a, lang)}'
            f'<h2>{t("Show your thinking", lang)}</h2><p>{t(a["response"], lang)}</p>'
            f'<div class="work-lines"></div>'
            f'<p class="notice no-print">{t("See also", lang)}: {t("July 5 & Black Freedom Holidays — Critical Thinking Breakouts in the History Learning Center.", lang)}</p>'
            f'{teacher_panel(a, lang)}</div></main>')
    page(lang, route, t(a['title'], lang), body)


def flag_strip():
    return ('<div class="flag" aria-hidden="true">'
            '<i style="background:#c0392b"></i><i style="background:#1f4e79"></i>'
            '<i style="background:#fff;border:1px solid #cfd8cf"></i>'
            '<i style="background:#1f4e79"></i><i style="background:#c0392b"></i></div>')


def landing_page(lang):
    hero = (f'<section class="hero"><div class="wrap">{flag_strip()}'
            f'<div class="eyebrow">{t("A collection in the History Learning Center", lang)}</div>'
            f'<h1>{t("Juneteenth & the Meaning of Freedom", lang)}</h1>'
            f'<p>{t("land_lede", lang)}</p></div></section>'
            f'<div class="wrap"><div class="stats"><span>{t("13 activities", lang)}</span>'
            f'<span>{t("Grades K–12", lang)}</span><span>{t("Seven languages", lang)}</span></div></div>')
    principles = (f'<section class="section"><div class="wrap"><h2>{t("How this collection works", lang)}</h2><ul>'
                  + ''.join(f'<li>{t(k, lang)}</li>' for k in [
                      'No logins, no data collected, works offline.',
                      'Seven languages, with a printable path for every activity.',
                      'Teacher supports in each activity: TEKS, answer key, and discussion questions.',
                      'Built to teach inside your Civil War and Reconstruction units — not reserved for June.'])
                  + f'</ul><div class="notice"><h3 style="margin-top:0">{t("TEKS alignment and timing", lang)}</h3>'
                  + f'<p style="margin:0">{t("land_teks_body", lang)}</p></div></div></section>')
    bands_html = f'<section class="section"><div class="wrap"><h2>{t("Choose a grade band", lang)}</h2>'
    for band in ['K–2', '3–5', '6–8', '9–12']:
        bcls = BAND_CLASS[band]
        bands_html += (f'<h3 style="font-family:Georgia,serif;font-size:1.5rem;margin-top:26px">'
                       f'{t(BAND_LABEL[band], lang)}</h3><div class="grid">')
        for a in [x for x in CONTENT if x['band'] == band]:
            bands_html += (f'<article class="card"><span class="pill {bcls}">{t(a["format"], lang)}</span>'
                           f'<h3>{t(a["title"], lang)}</h3><p>{t(a["card"], lang)}</p>'
                           f'<a class="button" href="{a["slug"]}.html">{t("Open the activity", lang)}</a></article>')
        bands_html += '</div>'
    bands_html += (f'<p class="small" style="margin-top:26px">{t("land_source_note", lang)}</p>'
                   f'<p class="notice no-print">{t("See also", lang)}: '
                   f'{t("July 5 & Black Freedom Holidays — Critical Thinking Breakouts in the History Learning Center.", lang)}</p>'
                   f'</div></section>')
    page(lang, 'index.html', t('Juneteenth & the Meaning of Freedom', lang),
         f'<main id="main">{hero}{principles}{bands_html}</main>')


# --------------------------------------------------------------------------- #
# String extraction (translation worklist) and build.                        #
# --------------------------------------------------------------------------- #
def all_strings():
    seen = []

    def add(s):
        if s and s not in seen:
            seen.append(s)
    for k in ['collection', 'footer_credit', 'land_lede', 'land_teks_body', 'land_source_note']:
        add(UI[k])
    for k, v in UI.items():
        if k not in ('collection', 'footer_credit', 'land_lede', 'land_teks_body', 'land_source_note'):
            add(v)
    # Static UI phrases used directly in code:
    for s in ['Back to the collection', 'History Learning Center', 'All activities', 'Start here',
              'Language', 'Print this activity', 'I can…', 'Look closely', 'Primary source',
              'Read the original source:', 'Show your thinking', 'Check my work', 'Start over',
              'Move up', 'Move down', 'Locked', 'Unlocked',
              'Pick a card, then choose where it belongs.', 'Tap each part to learn what it means.',
              'Choose a label, then tap a part of the text.',
              'Every item is placed correctly. Well done.',
              'Not yet — the highlighted items need another look.',
              'Not the right clue yet. Look again at the evidence.',
              'Correct — the next lock opens.', 'All locks are open. You traced the whole chain.',
              'Teacher notes & alignment', 'Objective', 'TEKS alignment', 'Current TEKS',
              '2026 TEKS (fill once crosswalks publish):',
              'Code not yet confirmed — verify against current TEA TEKS before teaching.',
              'Answer key', 'Discussion questions', 'Teaching hard history', 'See also',
              'July 5 & Black Freedom Holidays — Critical Thinking Breakouts in the History Learning Center.',
              'Standards reviewed October 17, 2026. Selected skill connections, not a full course alignment.',
              'No login. No tracking. Responses stay with you.',
              'Works offline. Nothing you type is saved or sent.',
              'This translation was authored with AI assistance and awaits review by a fluent speaker.',
              'Grades K–2', 'Grades 3–5', 'Grades 6–8', 'Grades 9–12',
              'A collection in the History Learning Center', 'Juneteenth & the Meaning of Freedom',
              '13 activities', 'Grades K–12', 'Seven languages', 'How this collection works',
              'No logins, no data collected, works offline.',
              'Seven languages, with a printable path for every activity.',
              'Teacher supports in each activity: TEKS, answer key, and discussion questions.',
              'Built to teach inside your Civil War and Reconstruction units — not reserved for June.',
              'TEKS alignment and timing', 'Choose a grade band', 'Open the activity']:
        add(s)

    def walk(obj):
        if isinstance(obj, dict):
            for kk, vv in obj.items():
                if kk in ('text', 'detail', 'quote', 'cite', 'clue', 'prompt', 'reveal', 'se'):
                    add(vv)
                else:
                    walk(vv)
        elif isinstance(obj, list):
            for it in obj:
                walk(it)
    for a in CONTENT:
        for fld in ['title', 'intro', 'card', 'format', 'can', 'objective', 'response', 'hard_history']:
            add(a[fld])
        walk(a['engine'])
        if a.get('source'):
            walk(a['source'])
        for k in a['answer_key']:
            add(k)
        for k in a['discussion']:
            add(k)
    return seen


def build():
    for lang in LANGS:
        landing_page(lang)
        for a in CONTENT:
            activity_page(lang, a)
    print(f'Built {len(LANGS)} language editions · {len(CONTENT)} activities + landing · '
          f'{len(LANGS)*(len(CONTENT)+1)} files.')


if __name__ == '__main__':
    assert len(CONTENT) == 13, f'Expected 13 activities, found {len(CONTENT)}'
    slugs = [a['slug'] for a in CONTENT]
    assert len(slugs) == len(set(slugs)), 'Duplicate activity slug'
    if len(sys.argv) > 1 and sys.argv[1] == 'extract':
        strings = all_strings()
        (ROOT / 'strings.en.json').write_text(json.dumps(strings, ensure_ascii=False, indent=1))
        print(f'Extracted {len(strings)} unique strings to strings.en.json')
    else:
        build()
