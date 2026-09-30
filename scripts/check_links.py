from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parent.parent
errors=[]
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k not in ('href','src') or not v:continue
   u=urlsplit(v)
   if u.scheme or u.netloc or not u.path:continue
   if u.path.startswith('/hlc/'):target=ROOT/u.path[5:]
   elif u.path.startswith('/'):target=ROOT/u.path[1:]
   else:target=p.parent/unquote(u.path)
   if not target.exists():errors.append((str(p.relative_to(ROOT)),v))
for p in ROOT.rglob('*.html'):
 if 'docs' in p.relative_to(ROOT).parts:continue
 parser=Links();parser.feed(p.read_text())
print('\n'.join(f'{a}: {b}' for a,b in errors[:100]))
print(f'{len(errors)} missing links across {len(list(ROOT.rglob("*.html")))} HTML files')
raise SystemExit(bool(errors))
