from html.parser import HTMLParser
from pathlib import Path
import re
class LinkCreator(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=False);self.parts=[];self.anchors=0;self.script=0
 def handle_starttag(self,t,a):self.parts.append(self.get_starttag_text());self.anchors+=t=='a';self.script+=t in ['script','style']
 def handle_startendtag(self,t,a):self.parts.append(self.get_starttag_text())
 def handle_endtag(self,t):self.parts.append('</'+t+'>');self.anchors-=t=='a';self.script-=t in ['script','style']
 def handle_data(self,s):
  if not self.anchors and not self.script:s=re.sub(r'(?<![\w.])gggguto(?!\w|\.com)','<a href="https://gggguto.com" target="_blank" rel="noopener noreferrer">gggguto</a>',s)
  self.parts.append(s)
 def handle_entityref(self,s):self.parts.append('&'+s+';')
 def handle_charref(self,s):self.parts.append('&#'+s+';')
 def handle_decl(self,s):self.parts.append('<!'+s+'>')
 def handle_comment(self,s):self.parts.append('<!--'+s+'-->')
site=Path(__file__).resolve().parents[1]/'site'
for p in site.rglob('*.html'):
 a=LinkCreator();a.feed(p.read_text());s=''.join(a.parts);assert 'href="https://gggguto.com"' in s,p;p.write_text(s)
print('Linked creator mentions on every page, opening a new tab')
