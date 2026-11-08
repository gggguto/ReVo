from pathlib import Path
import re,json,hashlib
site=Path(__file__).resolve().parents[1]/'site'
p=site/'index.html';old=p.read_text();bottom=re.search(r'(<section class="section section-row">.*?</section>)',old,re.S)[1]
def cards(pre):
 result='<div class="islands native-islands">'
 for name,index,label,desc,color in [('bioma','01','A LIVING ISLAND','A synthesized ecosystem. Natural voices listen, answer and find their own way.','red'),('atolls','02','TWO MOVING CURRENTS','Guide two sea currents. Shape their movement, their force and the ways they meet.','cyan')]:
  result+=f'''<a class="island-card native-island" style="--accent:var(--{color})" href="{pre}manual/{name}/"><span class="card-index">{index} / {label}</span><h2>{name.title()}</h2><span class="island-arrow" aria-hidden="true">↗</span><img class="native-home" data-island-machine="{name}" src="{pre}assets/homes/{name}-00.png" width="240" height="160" alt="{name.title()} island, with the original Home animation from ReVo"><p>{desc}</p></a>'''
 return result+'</div>'
def welcome(pre,eyebrow):return f'''<div class="island-welcome"><p class="eyebrow">{eyebrow}</p><div class="welcome-grid"><h1>Hello,<br>traveller.</h1><div><p>Welcome to ReVo. An experimental soundscape generator, and a fertile ground for sonic exploration.</p><p>There are two paths waiting for you. Choose an island. Take your time. Let it surprise you.</p></div></div></div>'''+cards(pre)
head=old[:old.index('<main id="main">')];foot=old[old.index('<footer>'):]
p.write_text(head+'<main id="main"><div class="container">'+welcome('','AN EXPERIMENTAL FIRMWARE FOR M-VAVE FM-1')+bottom+'</div></main>'+foot)
p=site/'manual/index.html';s=p.read_text();start=s.index('<main id="main"');end=s.index('<footer>');p.write_text(s[:start]+'<main id="main" class="container">'+welcome('../','THE REVO FIELD GUIDE / TWO ISLANDS')+'</main>'+s[end:])
# Global header is shared across every page, including tools and both manuals.
for p in site.rglob('*.html'):
 s=p.read_text();s=s.replace('href="style.css"','href="style.css?v=20261106-islands"').replace('href="../style.css"','href="../style.css?v=20261106-islands"').replace('href="../../style.css"','href="../../style.css?v=20261106-islands"')
 depth=len(p.relative_to(site).parts)-1;pre='../'*depth
 if 'home-islands.js' not in s:s=s.replace('</body>',f'<script type="module" src="{pre}home-islands.js"></script></body>')
 p.write_text(s)
p=site/'manual/bioma/index.html';s=p.read_text();s=re.sub(r'<section class="chapter" id="seeds".*?</section>','',s,flags=re.S);s=re.sub(r'<a href="#seeds">.*?</a>','',s)
s=s.replace('<kbd>PLAY/STOP</kbd> <span aria-hidden="true">→</span> <kbd>HOME</kbd>','<kbd>HOME</kbd> <span aria-hidden="true">→</span> <kbd>PLAY/STOP</kbd>',1)
s=s.replace('src="../../assets/screens/home.png" alt="ReVo Bioma — Wake the island."','src="../../assets/homes/bioma-stop.png" data-home-player="bioma" data-home-mode="stop" alt="Bioma Home — STOP status, grey shortcuts and the island"',1)
# Explain the display conventions here, rather than presenting GLO / Seed early.
controls='''<div class="home-view-buttons" role="group" aria-label="View Home transport states"><button type="button" data-home-status="stop" aria-pressed="true">View STOP</button><button type="button" data-home-status="play" aria-pressed="false">View PLAY</button></div>'''
s=s.replace('<figcaption>Native ReVo display / 240 × 240</figcaption></figure>','<figcaption>Native ReVo display / 240 × 240</figcaption></figure>'+controls,1)
for n,name in enumerate(['Birds','Insects','Water'],1):
 target=f'<strong><span class="number">{n}</span>{name}</strong>'
 s=s.replace(target,f'<img class="family-icon" src="../../assets/{name.lower()}-creature.png" width="64" height="64" alt="Original ReVo {name} drawing">'+target,1)
notes='''<div class="screen-reading"><h3>Find your way around the display.</h3><div class="screen-reading-grid"><div><b>01 / The top line</b><p>The machine’s name is on the left. PLAY or STOP appears at the top right, so you can always see whether the island’s inhabitants are awake.</p></div><div><b>02 / The grey shortcuts</b><p>The hints along the bottom tell you what is available on this page. They change as you travel. On Home, EDIT opens the inhabitants, FX opens the effects, and SELECT takes you through pages.</p></div><div><b>03 / HOME</b><p>A short press brings you back to this island view. Hold HOME to open the menu, choose a machine or visit Settings.</p></div><div><b>04 / SEL: Random Seed</b><p>Press SEL on Home to choose a new Seed: a different starting point for the island’s generative choices. Your levels stay where you left them. For now, just listen to the change; we will visit the Seed control later, in GLO.</p></div></div></div>'''
pattern=r'(<section class="chapter" id="welcome".*?)(</section>)';s=re.sub(pattern,lambda m:m[1]+notes+m[2],s,count=1,flags=re.S)
# Renumber only chapter labels / index entries; knob numbers remain unchanged.
count=[0]
def label(m):count[0]+=1;return m[1]+f'{count[0]:02} / BIOMA'+m[2]
s=re.sub(r'(<div class="chapter-label"><span>)\d+ / BIOMA(</span>)',label,s)
count=[0]
def nav(m):count[0]+=1;return m[1]+f'{count[0]:02} / '+m[2]
s=re.sub(r'(<a href="#[^"]+">)\d+ / ([^<]+</a>)',nav,s)
p.write_text(s)
p=site/'manual/bioma/data.json';d=json.loads(p.read_text());d['chapters']=[c for c in d['chapters'] if c['id']!='seeds'];d['chapters'][0]['gesture']=['HOME','PLAY/STOP'];d['chapters'][0]['extra']+=' Press SEL on Home for another Seed; its GLO control is introduced later.';p.write_text(json.dumps(d,indent=2))
new=(site/'index.html').read_text();assert re.search(r'(<section class="section section-row">.*?</section>)',new,re.S)[1]==bottom
(site/'assets/homes/layout-validation.json').write_text(json.dumps({'discoverySectionUnchanged':True,'discoverySectionSha256':hashlib.sha256(bottom.encode()).hexdigest(),'header':'Global shared header, non-sticky on every page','homeIntroGesture':'HOME → PLAY/STOP','seedIntroduction':'Home SEL only; no separate early Seed page'},indent=2))
print('Applied island welcome on Home/manual; shared header; native family icons; Home screen conventions; discovery section unchanged')
