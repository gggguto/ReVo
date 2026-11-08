from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import re,json,hashlib
root=Path(__file__).resolve().parents[1];site=root/'site';errors=[];checked=0
class Parse(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=set()
 def handle_starttag(self,t,a):
  a=dict(a)
  if 'id'in a:self.ids.add(a['id'])
  for k in ['href','src']:
   if a.get(k):self.refs.append(a[k])
parsed={}
for p in site.rglob('*.html'):
 d=Parse();d.feed(p.read_text());parsed[p.resolve()]=d
for p,d in parsed.items():
 for raw in d.refs:
  u=urlsplit(raw)
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  if target.is_dir():target=target/'index.html'
  checked+=1
  if not target.is_file():errors.append(f'{p.relative_to(site)}: missing {raw}');continue
  if u.fragment and target.suffix=='.html' and u.fragment not in parsed[target].ids:errors.append(f'{p.relative_to(site)}: missing anchor {raw}')
for p in site.rglob('*'):
 if p.suffix in ['.js','.mjs']:
  for rel in re.findall(r"(?:from|import)\s*['\"]([^'\"]+)['\"]",p.read_text()):
   if rel.startswith('.') and not (p.parent/rel).resolve().is_file():errors.append(f'{p}: missing import {rel}')
m=json.loads((site/'install/release.json').read_text())
for name,key in [('ReVo-development.fwsc','sha256'),('ReVo-development-source.zip','source_sha256')]:assert hashlib.sha256((site/'install'/name).read_bytes()).hexdigest()==m[key]
assert (site/'install/ReVo-development.fwsc').stat().st_size==m['bytes']
assert not errors,'\n'.join(errors)
assert '#seeds' not in (site/'manual/bioma/index.html').read_text()
assert len(list((site/'assets/homes').glob('bioma-[0-9][0-9].png')))==24
assert len(list((site/'assets/homes').glob('atolls-[0-9][0-9].png')))==35
print(f'PASS {len(parsed)} static pages, {checked} local links/assets/anchors, module imports, native Home frames and matching firmware/source SHA-256')
