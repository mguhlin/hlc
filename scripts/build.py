#!/usr/bin/env python3
"""Build the static, localized classroom center from reviewed content records."""
import html
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ['en', 'es', 'vi', 'zh', 'hi', 'ur', 'ar']
NAMES = ['English', 'Español', 'Tiếng Việt', '简体中文', 'हिन्दी', 'اردو', 'العربية']
WORDS = {lang: {} for lang in LANGS}
for source in sorted((ROOT / 'data').glob('*.tsv')):
    for number, line in enumerate(source.read_text().splitlines(), 1):
        if not line.strip() or line.startswith('#'):
            continue
        cells = line.split('|')
        assert len(cells) == 8, (source.name, number, len(cells))
        key, *translations = cells
        assert key not in WORDS['en'], f'Duplicate translation key: {key}'
        for lang, value in zip(LANGS, translations):
            assert value.strip(), (source.name, key, lang)
            WORDS[lang][key] = value

MODULES = json.loads((ROOT / 'data/modules.json').read_text())
SOURCES = json.loads((ROOT / 'data/sources.json').read_text())
SOURCES['veterans'] = {'name': 'Veterans Day history', 'url': 'https://department.va.gov/veterans-day/history-of-veterans-day/'}
ROUTINES = json.loads((ROOT / 'data/routines.json').read_text())
assert len(MODULES) == 37
assert len({m['id'] for m in MODULES}) == 37
TOPICS = {'map': 'maps', 'timeline': 'time', 'pair': 'evidence', 'budget': 'choices', 'data': 'patterns'}
PHASES = ['first', 'second', 'third', 'fourth', 'fifth']
BANDS = ['k2', 'g35', 'g68', 'g912']
TEA = 'https://tea.texas.gov/laws-and-rules/sboe-rules-tac/sboe-tac-currently-effect/'
TEKS = {
 'map':['§113.13(c)(3)(A)–(B)','§113.15(c)(20)(A)','§113.20(c)(29)(H)','§113.41(d)(30)(B)'],
 'timeline':['§113.13(c)(16)(A)–(C)','§113.15(c)(19)(C)–(D)','§113.20(c)(29)(B)–(C)','§113.41(d)(28)(B)'],
 'pair':['§113.13(c)(15)(A), (D)','§113.15(c)(19)(B), (G)','§113.20(c)(29)(E)–(F)','§113.41(d)(28)(A), (F)'],
 'budget':['§113.13(c)(17)(B)','§113.15(c)(22)(B)','§113.20(c)(31)(B)','§113.41(d)(31)(B)'],
 'data':['§113.13(c)(15)(D)','§113.15(c)(19)(D)','§113.20(c)(29)(C)','§113.41(d)(30)(B)']}
TOOLS = [
 ('observe','observeTool',['noticeBox','inferBox','wonderBox']),
 ('compare','compareTool',['recordA','recordB','agreementBox','claimBox']),
 ('timeline','timelineTool',['timelineBox']*3+['timelineLimit']),
 ('map','mapTool',['legendBox','routeBox']),
 ('decision','decisionTool',['optionsBox']*3+['recommendBox']),
 ('ace','aceTool',['articulateBox','connectBox','extendBox']),
 ('solo','soloTool',['unrelated','oneIdea','severalIdeas','relatedIdeas','transferIdea']),
 ('jigsaw','jigsawTool',['expertBox','groupBox','claimBox'])]
TOOLS += [(r['tool'],r['title'],r['fields']) for r in ROUTINES if r.get('tool')]

def esc(value):
    return html.escape(str(value), quote=True)

def prefix(lang):
    return '' if lang == 'en' else lang + '/'

class Page:
    def __init__(self, lang, route):
        self.lang, self.route = lang, route
        self.path = prefix(lang) + route
        self.base = '../' * self.path.count('/')
        self.w = WORDS[lang]
    def t(self, key):
        value=self.w[key]
        if key=='weeksCount':
            value=value.replace('37',str(len(MODULES)+len(ROUTINES))).replace('٣٧','٤٩').replace('۳۷','۴۹')
        if key=='templatesCount':
            value=value.replace('8',str(len(TOOLS))).replace('٨','١٦').replace('۸','۱۶')
        return esc(value)
    def url(self, route='', lang=None):
        return self.base + prefix(lang or self.lang) + route
    def asset(self, file):
        return self.base + 'assets/' + file
    def link(self, route, key, cls=''):
        return f'<a class="{cls}" href="{self.url(route)}">{self.t(key)}</a>'
    def header(self):
        options = ''.join(f'<option value="{l}" data-url="{self.url(self.route, l)}" {"selected" if l == self.lang else ""}>{n}</option>' for l,n in zip(LANGS,NAMES))
        nav = ''.join(self.link(r,k) for r,k in [('calendar/','calendar'),('activities/','activities'),('printables/','printables'),('teacher/','teacher')])
        nav += f'<a href="{self.base}pst/?lang={self.lang}">PST</a><a href="{self.base}eventmaps/?lang={self.lang}">{self.t("eventMaps")}</a>'
        return f'<a class="skip" href="#main">{self.t("startHere")}</a><header class="site-head"><div class="wrap head-inner">{self.link("", "site", "brand")}<nav aria-label="{self.t("site")}">{nav}</nav><div class="language"><label for="language">{self.t("language")}</label><select id="language">{options}</select></div></div></header>'
    def write(self, title, body, calendar=False, tail=''):
        direction = 'rtl' if self.lang in ['ar','ur'] else 'ltr'
        footer = f'<footer class="footer"><div class="wrap"><p>{self.t("privacy")}</p>'
        if self.lang != 'en':
            footer += f'<p>{self.t("translationNote")}</p>'
        footer += '</div></footer>'
        output = f'''<!doctype html><html lang="{self.lang}" dir="{direction}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="referrer" content="no-referrer"><meta name="description" content="{self.t('heroText')}"><title>{esc(title)} · {self.t('site')}</title><link rel="stylesheet" href="{self.asset('site.css')}"></head><body class="{'calendar-body' if calendar else ''}">{self.header()}{body}{footer}<script src="{self.asset('site.js')}" defer></script>{tail}</body></html>'''
        target = ROOT / self.path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output)

def sources_for(m):
    keys = list(m.get('sources', [])) + [r[2] for r in m.get('rows',[]) if len(r)>2]
    return list(dict.fromkeys(keys))

def stimulus(p, m):
    kind=m['kind']; out=''
    if kind == 'map':
        symbols={'school':'▣','library':'▤','river':'≈','bridge':'═','park':'♧','homes':'⌂','farm':'◇','market':'▥','museum':'▦','mountain':'▲','forest':'♧','station':'▧'}
        out=f'<div class="map-location"><b>{p.t("north")} ↑</b></div><div class="map" dir="ltr" role="group" aria-label="{p.t(m["title"])}">'
        for key in m['cells']:
            out+=f'<div class="cell {key}"><span class="symbol" aria-hidden="true">{symbols[key]}</span><span dir="auto">{p.t(key)}</span></div>'
        out+=f'</div><p class="small">{p.t("mapHelp")}</p>'
    elif kind in ['timeline','pair']:
        out='<div class="source-cards">'
        for row in m['rows']:
            head = str(row[0]) if isinstance(row[0],int) else p.w[row[0]]
            out+=f'<div class="evidence-card"><b dir="auto">{esc(head)}</b><p>{p.t(row[1])}</p></div>'
        out+='</div>'
    else:
        if kind == 'budget':
            out=f'<p class="total">{p.t("available")}: <bdi>{m["total"]}</bdi></p>'
        label = 'cost' if kind=='budget' else m['unit']
        out+=f'<table class="metric-table"><thead><tr><th>{p.t(m["title"])}</th><th>{p.t(label)}</th>'
        if m.get('sample'): out+=f'<th>{p.t("sample")}</th>'
        out+='</tr></thead><tbody>'
        for i,row in enumerate(m['rows']):
            out+=f'<tr><td>{p.t(row[0])}</td><td class="num"><bdi>{row[1]}</bdi></td>'
            if m.get('sample'): out+=f'<td><bdi>{m["sample"][i]}</bdi></td>'
            out+='</tr>'
        out+='</tbody></table>'
    out+=f'<p class="evidence-note">{p.t("historical" if m.get("historical") else "practice")}</p>'
    sourcekeys=sources_for(m)
    if sourcekeys:
        out+=f'<div class="source-links"><strong>{p.t("sources")}: </strong>'
        for key in sourcekeys:
            s=SOURCES[key]
            out+=f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["name"])}</a>'
        out+='</div>'
    return out

def alignment(p,m):
    out=f'<p>{p.t("alignmentExamples")}</p><ul>'
    for i,code in enumerate(TEKS[m['kind']]):
        pdf=['ch113a.pdf','ch113a.pdf','ch113b.pdf','ch113c.pdf'][i]
        out+=f'<li>{p.t(BANDS[i])} · <a href="{TEA+pdf}" target="_blank" rel="noopener"><bdi>{esc(code)}</bdi></a></li>'
    out+=f'</ul><p>{p.t("elpsNote")}</p><p><a href="{TEA}ch120b.pdf" target="_blank" rel="noopener">ELPS <bdi>§120.20(d)(2)(E), (4)(F) · §120.21(d)(2)(E), (4)(F)</bdi></a></p><p>{p.t("languageGoal")}</p><p>{p.t("alignmentCaution")}</p><p class="small">{p.t("reviewed")}</p>'
    return out

def check(p,m):
    out=f'<p>{p.t(m["kind"]+"Key")}</p>'
    if m['kind']=='timeline':
        ordered=sorted(m['rows'],key=lambda r:r[0])
        out+='<p>'+' → '.join(f'<bdi>{r[0]}</bdi>: {p.t(r[1])}' for r in ordered)+'</p>'
    if m['kind']=='budget':
        out+='<p>'+ ' · '.join(f'{p.t(r[0])}: <bdi>{r[1]} ≤ {m["total"]}</bdi>' for r in m['rows'] if r[1]<=m['total'])+'</p>'
        pairs=[(a,b) for a,b in itertools.combinations(m['rows'],2) if a[1]+b[1]<=m['total']]
        if pairs: out+='<p>'+ ' · '.join(f'{p.t(a[0])} + {p.t(b[0])}: <bdi>{a[1]} + {b[1]} = {a[1]+b[1]}</bdi>' for a,b in pairs)+'</p>'
    if m.get('sample'):
        out+='<p>'+ ' · '.join(f'{p.t(r[0])}: <bdi>{r[1]}/{m["sample"][i]} = {r[1]/m["sample"][i]*100:g}%</bdi>' for i,r in enumerate(m['rows']))+'</p>'
    return out

def card(p,m,i):
    text=' '.join([p.w[m['title']],p.w[TOPICS[m['kind']]]]+[p.w[r[1]] if isinstance(r[0],int) else p.w[r[0]] for r in m.get('rows',[])])
    return f'<article class="card" data-search="{esc(text)}" data-topic="{m["kind"]}"><div class="number">{p.t("week")} {i+1:02d}</div><span class="pill">{p.t(TOPICS[m["kind"]])}</span><h2 style="font-size:1.55rem;margin-top:12px">{p.t(m["title"])}</h2><p>{p.t("activityLength")}</p>{p.link("activities/"+m["id"]+".html", "browse", "button")}</article>'

def home(p):
    hero=f'<main id="main"><section class="hero"><img class="hero-image" src="{p.asset("investigation-workspace.webp")}" alt=""><div class="wrap"><div class="hero-copy"><div class="eyebrow">{p.t("site")}</div><h1>{p.t("heroTitle")}</h1><p>{p.t("heroText")}</p><div class="actions">{p.link("calendar/","openToday","button")}{p.link("activities/","browse","button secondary")}</div><p class="small" style="color:#e5eee4;margin-top:18px">{p.t("fiveMinutes")} · {p.t("noPrep")}</p></div></div></section><div class="wrap"><div class="stats"><span>{p.t("daysCount")}</span><span>{p.t("weeksCount")}</span><span>{p.t("templatesCount")}</span></div></div><section class="section"><div class="wrap"><h2>{p.t("startHere")}</h2><div class="grid">'
    for i,(route,key,description,action) in enumerate([('calendar/','calendar','dailyText','calendarStart'),('activities/','activities','activityText','browse'),('printables/','printables','printText','printables')]):
        hero+=f'<article class="card"><div class="number">0{i+1}</div><h2 style="font-size:1.9rem">{p.t(key)}</h2><p>{p.t(description)}</p>{p.link(route,action,"button primary")}</article>'
    hero+=f'<article class="card"><div class="number">04</div><h2>PST</h2><p>{p.t("pstIntro")}</p><a class="button primary" href="{p.base}pst/?lang={p.lang}">{p.t("browse")}</a></article><article class="card"><div class="number">05</div><h2>{p.t("eventMaps")}</h2><p>{p.t("eventIntro")}</p><a class="button primary" href="{p.base}eventmaps/?lang={p.lang}">{p.t("browse")}</a></article></div><p class="small" style="margin-top:22px">{p.t("practiceScope")}</p></div></section><section class="section"><div class="wrap grid two"><div><img class="mini-photo" src="{p.asset("students-comparing-evidence.webp")}" alt=""><p class="caption">{p.t("illustration")}</p></div><div><h2>{p.t("studentGoal")}</h2><p>{p.t("contentGoal")}</p><p>{p.t("activityText")}</p>{p.link("activities/founding-documents.html","founding","button")}</div></div></section><section class="section"><div class="wrap"><h2>{p.t("activities")}</h2><div class="grid">'+''.join(card(p,MODULES[i],i) for i in [0,4,13])+f'</div><p style="margin-top:22px">{p.link("activities/","browse")}</p></div></section></main>'
    p.write(p.w['site'],hero)

def library(p):
    filters=f'<div class="filters"><label>{p.t("search")}<input id="search" type="search" autocomplete="off"></label><label>{p.t("all")}<select id="topic"><option value="">{p.t("all")}</option>' + ''.join(f'<option value="{k}">{p.t(v)}</option>' for k,v in TOPICS.items())+'</select></label></div>'
    routinecards=''
    for r in ROUTINES:
        topic='pair' if r['id'] not in ['storyboard-a-change','holidays-have-histories'] else 'timeline'
        routinecards+=f'<article class="card" data-search="{p.t(r["title"])}" data-topic="{topic}"><span class="pill">{p.t("teacher" if r.get("teacherOnly") else "activities")}</span><h2 style="font-size:1.55rem;margin-top:12px">{p.t(r["title"])}</h2><p>{p.t("routineIntro")}</p>{p.link("activities/"+r["id"]+".html",r["title"],"button")}</article>'
    body=f'<main id="main" class="wrap"><div class="page-title"><h1>{p.t("activities")}</h1><p>{p.t("activityText")}</p></div>{filters}<p class="filter-count"><span id="resultCount" aria-live="polite">49</span> · {p.t("activities")}</p><p id="noResults" hidden>{p.t("noResults")} <button id="clearFilters">{p.t("clear")}</button></p><div class="grid">'+routinecards+''.join(card(p,m,i) for i,m in enumerate(MODULES))+f'</div><div class="notice">{p.t("practiceScope")}</div></main>'
    p.write(p.w['activities'],body)

def lesson(p,m,i):
    body=f'<main id="main" class="wrap"><div class="lesson"><div class="page-title"><p class="small">{p.link("activities/","backActivities")}</p><h1>{p.t(m["title"])}</h1><p>{p.t("activityLength")}</p><div class="actions"><button data-print>{p.t("lessonPrint")}</button>{p.link("calendar/#day-"+str(i*5+1),"calendar","button")}{p.link("printables/ace.html","aceTool","button")}</div></div><div class="student-fields"><span>{p.t("name")}: __________________</span><span>{p.t("date")}: __________</span></div><p><strong>{p.t("studentGoal")}</strong></p><p>{p.t("materials")}</p><h2>{p.t("look")}</h2>{stimulus(p,m)}<h2 style="margin-top:25px">{p.t("task")}</h2><ol class="lesson-steps">'
    for key in ['recallStep','modelStep','investigateStep','connectStep','independentStep','reviseStep']:
        body+=f'<li>{p.t(key)}</li>'
    body+='</ol>'+band_controls(p)+'<div class="card"><h3>'+p.t('task')+'</h3><ol>'
    for d in range(5): body+=f'<li>{p.t(m["kind"]+str(d))}</li>'
    body+=f'</ol></div><div class="notice"><strong>{p.t("independent")}</strong><p>{p.t("stem")}</p></div><p>{p.t("writeSpace")}</p><div class="work-lines"></div><details class="teacher-details"><summary>{p.t("teacherNotes")}</summary><p>{p.t("lookFor")}</p>{check(p,m)}<p>{p.t("support")}</p>{alignment(p,m)}</details></div></main>'
    p.write(p.w[m['title']],body)

def tools_index(p):
    body=f'<main id="main" class="wrap"><div class="page-title"><h1>{p.t("printables")}</h1><p>{p.t("templateIntro")}</p></div><div class="grid">'
    for slug,title,fields in TOOLS:
        body+=f'<article class="card"><h2 style="font-size:1.7rem">{p.t(title)}</h2><p>{p.t("writeSpace") if slug!="solo" else p.t("soloNote")}</p>{p.link("printables/"+slug+".html",title,"button")}</article>'
    body+='</div></main>';p.write(p.w['printables'],body)

def worksheet(p,slug,title,fields):
    body=f'<main id="main" class="wrap"><div class="page-title no-print"><p>{p.link("printables/","backPrintables")}</p><button data-print>{p.t("print")}</button></div><article class="worksheet"><h1>{p.t(title)}</h1><div class="student-fields"><span>{p.t("name")}: ________________</span><span>{p.t("date")}: __________</span></div>'
    if slug=='map': body+='<div class="blank-map">'+('<div></div>'*9)+'</div>'
    if slug=='hexagons':
        body+='<div class="hex-grid">'+''.join(f'<div class="hex-card">{p.t(k)}</div>' for k in fields)+f'</div><p>{p.t("hex2")}</p><div class="work-lines"></div>'
    elif slug=='solo': body+='<ol class="rubric">'+''.join(f'<li>{p.t(k)}</li>' for k in fields)+f'</ol><p>{p.t("soloNote")}</p>'
    else:
        for k in fields:
            body+=f'<h3>{p.t(k)}</h3><div class="work-lines"></div>'
    body+='</article></main>';p.write(p.w[title],body)

def band_controls(p):
    return f'<label class="no-print">{p.t("grade")} <select id="activityGrade">'+''.join(f'<option value="{b}">{p.t(b)}</option>' for b in BANDS)+ '</select></label>'+''.join(f'<div class="notice band-content" data-band="{b}" {"hidden" if b!="g35" else ""}><strong>{p.t(b)}</strong><p>{p.t(b+"Task")}</p></div>' for b in BANDS)

def routine(p,r):
    m=r.get('custom') or next(m for m in MODULES if m['id']==r['module'])
    body=f'<main id="main" class="wrap"><div class="lesson"><div class="page-title"><p>{p.link("activities/","backActivities")}</p><h1>{p.t(r["title"])}</h1><p>{p.t("routineIntro")}</p><div class="actions"><button data-print>{p.t("print")}</button>'
    if r.get('tool'): body+=p.link('printables/'+r['tool']+'.html',r['title'],'button')
    body+='</div></div>'
    if not r.get('teacherOnly'):body+=f'<p><strong>{p.t("studentGoal")}</strong></p>'+band_controls(p)
    if r.get('approvedSources'):
        body+='<div class="notice"><p>'+p.t('remembrance1')+'</p></div><div class="source-links">'
        for grade,slug in [('collectionK5','holocaust-k-5-resources'),('collection68','holocaust-6-8-resources'),('collection912','holocaust-9-12-resources')]:
            body+=f'<a href="https://thgaac.texas.gov/learning/hrw/{slug}" target="_blank" rel="noopener">{p.t(grade)}</a>'
        body+='</div>'
    else:body+=f'<h2>{p.t("look")}</h2>'+stimulus(p,m)
    body+=f'<h2 style="margin-top:22px">{p.t("task")}</h2><ol class="lesson-steps">'+''.join(f'<li>{p.t(k)}</li>' for k in r['steps'])+'</ol>'
    if r.get('official'):body+=f'<p class="source-links"><a href="{r["official"]}" target="_blank" rel="noopener">TEA · {p.t(r["title"])}</a></p>'
    for field in r['fields'][:3]:body+=f'<h3>{p.t(field)}</h3><div class="work-lines"></div>'
    body+=f'<details class="teacher-details"><summary>{p.t("teacherNotes")}</summary><p>{p.t("lookFor")}</p><p>{p.t("support")}</p>{alignment(p,m)}</details></div></main>'
    p.write(p.w[r['title']],body)

def teacher(p):
    body=f'<main id="main" class="wrap"><div class="teacher-tools"><div class="page-title"><h1>{p.t("guide")}</h1><p>{p.t("practiceScope")}</p></div><div class="card"><h2>TEKS + ELPS</h2><p>{p.t("alignmentExamples")}</p><p>{p.t("alignmentCaution")}</p><p>{p.t("elpsNote")}</p><p>{p.t("languageGoal")}</p><p class="source-links"><a href="https://tea.texas.gov/educators/subject-areas/social-studies/social-studies">TEA · Social Studies TEKS, skills matrices & crosswalks</a><a href="https://tea.texas.gov/curriculum-and-instruction/english-language-proficiency-standards">TEA · ELPS</a></p></div><div class="card" style="margin-top:22px"><h2>UDL</h2><p>{p.t("support")}</p><img class="reference-img" src="{p.asset("udl-quick-reference.jpg")}" alt="UDL"><p>{p.t("contentGoal")}</p></div><div class="card" style="margin-top:22px"><h2>{p.t("research")}</h2><p>{p.t("researchNote")}</p><ul><li><a href="https://www.visiblelearningmetax.com/influences/view/jigsaw_method">Jigsaw · d = 0.92</a></li><li><a href="https://www.visiblelearningmetax.com/influences/view/reciprocal_teaching">Reciprocal teaching · d = 0.74</a></li><li><a href="https://www.visiblelearningmetax.com/influences/view/concept_mapping">Concept mapping · d = 0.66</a></li><li><a href="https://www.visiblelearningmetax.com/influences/view/feedback">Feedback · d = 0.50</a></li></ul><p>{p.t("lookFor")}</p><p>{p.link("printables/solo.html","soloTool")}</p><img class="reference-img" src="{p.asset("ace-solo-guide.png")}" alt="ACE + SOLO"></div><div class="card" style="margin-top:22px"><h2>SST · STAAR</h2><p>{p.t("sstNote")}</p><p>{p.t("scorePractice")}</p><p>{p.link("printables/ace.html","aceTool")}</p><div class="source-links"><a href="https://tea.texas.gov/data-reports/student-assessment-overview/house-bill-8-student-assessment">TEA · SST</a><a href="https://tea.texas.gov/data-reports/staar/staar-social-studies-resources">TEA · STAAR Social Studies & scoring guides</a><a href="https://tea.texas.gov/data-reports/staar/staar-released-test-questions">TEA · Released questions</a><a href="https://tea.texas.gov/data-reports/staar/released-test-questions/2026-staar-8-social-studies-scoring-guide.pdf">TEA · Grade 8 · 2026 scoring guide</a><a href="https://tea.texas.gov/data-reports/staar/released-test-questions/2026-staar-us-history-scoring-guide.pdf">TEA · U.S. History · 2026 scoring guide</a><a href="https://tea.texas.gov/educators/subject-areas/celebrate-freedom-week">TEA · Celebrate Freedom Week</a></div></div><p class="small" style="margin:22px 0">{p.t("reviewed")}</p></div></main>'
    p.write(p.w['teacher'],body)

def calendar(p):
    records=[]
    for i,m in enumerate(MODULES):
        records.append({'id':m['id'],'title':p.w[m['title']],'kind':m['kind'],'stimulus':stimulus(p,m),'check':check(p,m),'alignment':alignment(p,m),'activityUrl':p.url('activities/'+m['id']+'.html')})
    first=records[0]
    hero=f'<section class="opener-hero no-print" aria-labelledby="openerHeroTitle"><div class="opener-hero-copy"><p class="eyebrow">{p.t("calendar")} · {p.t("fiveMinutes")}</p><h1 id="openerHeroTitle">{p.t("openerHeroTitle")}</h1><p>{p.t("openerHeroText")}</p><p>{p.t("openerHeroHelp")}</p><div class="actions"><button class="primary" id="heroTodayBtn">{p.t("openToday")}</button><button id="heroStartBtn">{p.t("openerStart")}</button></div><div class="opener-badges"><span>{p.t("daysCount")}</span><span>{p.t("fiveMinutes")}</span><span>{p.t("grade")} · K–12</span><span>{p.t("printOrProject")}</span></div></div><figure><img src="{p.asset("history-daily-openers-hero.webp")}" width="1448" height="1086" alt="" fetchpriority="high"><figcaption>{p.t("illustration")}</figcaption></figure></section>'
    body=f'<main id="main" class="wrap">{hero}<div class="cal-tools no-print"><div class="group"><button id="todayBtn">{p.t("today")}</button><button id="monthBtn">{p.t("month")}</button><button id="settingsBtn">{p.t("settings")}</button></div><label>{p.t("grade")} <select id="gradeSelect">'+''.join(f'<option value="{b}">{p.t(b)}</option>' for b in BANDS)+f'</select></label><div class="group"><button id="printBtn">{p.t("printDay")}</button><button id="projectBtn">{p.t("project")}</button><button id="copyBtn">{p.t("copyLink")}</button></div></div><p id="dateNotice" class="cal-banner" hidden></p><div class="calendar-shell"><div class="rings" aria-hidden="true">'+('<i></i>'*10)+f'</div><article class="calendar-page" id="calendarPage"><header class="cal-head"><div><p class="eyebrow">{p.t("calendar")} · {p.t("fiveMinutes")}</p><h1 id="dateHeading">{p.t("day")} 1</h1><p class="cal-month" id="subDate">{p.t("week")} 1</p></div><div class="cal-day-number" id="dateNumber" aria-hidden="true">01</div></header><span class="pill" id="phaseLabel">{p.t("first")}</span><h2 id="activityTitle" class="cal-title">{esc(first["title"])}</h2><section id="stimulus">{first["stimulus"]}</section><section class="challenge"><h3>{p.t("task")}</h3><p id="taskText">{p.t("map0")}</p></section><div class="cal-response"><section><h3>{p.t("talk")}</h3><p id="bandTask">{p.t("k2Task")}</p></section><section><h3>{p.t("respond")}</h3><p>{p.t("stem")}</p></section></div><details class="check-details" id="checkDetails"><summary>{p.t("check")}</summary><div id="answerText">{first["check"]}</div></details><details class="teacher-details" id="teacherDetails"><summary>{p.t("teacherNotes")}</summary><p>{p.t("lookFor")}</p><p>{p.t("support")}</p><div id="alignmentText">{first["alignment"]}</div></details><a class="deeper" id="activityLink" href="{first["activityUrl"]}">{p.t("goDeeper")}</a></article><div class="cal-base"><button class="flip-btn" id="prevBtn" aria-label="{p.t("previous")}">‹</button><div class="counter"><span id="counter">{p.t("day")} 1 / 185</span><a href="{p.url("calendar/all.html")}">{p.t("daysCount")}</a></div><button class="flip-btn" id="nextBtn" aria-label="{p.t("next")}">›</button></div></div><div class="cal-tools no-print"><div class="group"><button id="timerBtn">{p.t("timerStart")}</button><output class="timer" id="timer">5:00</output></div><label>{p.t("day")} <input id="dayJump" type="number" min="1" max="185" value="1" style="width:75px;padding:8px;border-radius:7px;border:0"></label></div><noscript><div class="calendar-noscript">{p.link("calendar/all.html","daysCount")}</div></noscript></main><button class="exit-projector" id="exitProjectBtn">{p.t("exitProject")}</button>'
    body+=f'<dialog id="monthDialog" aria-labelledby="monthTitle"><div class="dialog-head"><h2 id="monthTitle">{p.t("month")}</h2><button data-close="monthDialog">{p.t("close")}</button></div><div class="month-head"><button id="prevMonth">‹</button><h3 id="monthLabel"></h3><button id="nextMonth">›</button></div><div class="weekday-grid" id="weekdays"></div><div class="month-grid" id="monthGrid"></div><div class="actions no-print" style="margin-top:18px"><button id="printMonthBtn">{p.t("print")}</button></div></dialog><dialog id="settingsDialog" aria-labelledby="settingsTitle"><div class="dialog-head"><h2 id="settingsTitle">{p.t("settings")}</h2><button data-close="settingsDialog">{p.t("close")}</button></div><p>{p.t("calendarHelp")}</p><form id="settingsForm" class="settings-form"><label>{p.t("startDate")}<input id="startDate" type="date" required></label><label>{p.t("excluded")}<textarea id="excludedDates"></textarea></label><p id="settingsError" class="error" hidden>{p.t("invalidDates")}</p><div class="actions"><button class="primary" type="submit">{p.t("apply")}</button><button id="resetCalendar" type="button">{p.t("reset")}</button></div></form></dialog><div class="sr-only" id="live" aria-live="polite"></div>'
    data={'lang':p.lang,'labels':p.w,'modules':records,'bands':BANDS,'phases':PHASES,'tasks':{kind:[p.w[kind+str(d)] for d in range(5)] for kind in TOPICS}}
    encoded=json.dumps(data,ensure_ascii=False).replace('</','<\\/')
    tail=f'<script type="application/json" id="calendarData">{encoded}</script><script src="{p.asset("calendar.js")}" defer></script>'
    p.write(p.w['calendar'],body,True,tail)

def archive(p):
    body=f'<main id="main" class="wrap"><div class="page-title"><h1>{p.t("daysCount")}</h1>{p.link("calendar/","calendarStart","button")}</div>'
    for i,m in enumerate(MODULES):
        for d in range(5):
            n=i*5+d+1
            body+=f'<article class="archive-day" id="day-{n}"><p class="eyebrow">{p.t("day")} {n} · {p.t(PHASES[d])}</p><h2>{p.t(m["title"])}</h2>{stimulus(p,m)}<div class="challenge"><p>{p.t(m["kind"]+str(d))}</p></div><p>{p.t("stem")}</p>{p.link("calendar/#day-"+str(n),"calendarStart")}</article>'
    body+='</main>';p.write(p.w['daysCount'],body)

for lang in LANGS:
    home(Page(lang,'index.html'))
    library(Page(lang,'activities/index.html'))
    for i,m in enumerate(MODULES):
        assert m['kind'] in TOPICS
        for source in sources_for(m): assert source in SOURCES
        lesson(Page(lang,'activities/'+m['id']+'.html'),m,i)
    for r in ROUTINES: routine(Page(lang,'activities/'+r['id']+'.html'),r)
    tools_index(Page(lang,'printables/index.html'))
    for slug,title,fields in TOOLS: worksheet(Page(lang,'printables/'+slug+'.html'),slug,title,fields)
    teacher(Page(lang,'teacher/index.html'))
    calendar(Page(lang,'calendar/index.html'))
    archive(Page(lang,'calendar/all.html'))
print(f'Built {len(LANGS)} locales, 185 daily slots, {len(MODULES)+len(ROUTINES)} activities, {len(TOOLS)} printable tools.')
