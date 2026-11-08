from pathlib import Path
import json,re,html
site=Path(__file__).resolve().parents[1]/'site';keys=json.loads((site/'manual/fragment-map.json').read_text());names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];white=0
board='<div class="fragment-keyboard-scroll" tabindex="0" aria-label="Fragment keyboard, scroll horizontally on a small screen"><div class="fragment-keyboard"><div class="bank-label bank-a">LOOP A / LEFT BANK</div><div class="bank-label bank-b">LOOP B / RIGHT BANK</div>'
for k in keys:
 pitch=k['pitch'];name=names[pitch%12]+str(pitch//12-1);is_black=pitch%12 in [1,3,6,8,10];k['note']=name;k['black']=is_black;label={'Reverse':'REV','Half':'½ SPEED','Double':'2× SPEED','Divider':'SPLIT'}.get(k['label'],k['label']);left=white*6.25-(2.1 if is_black else 0)
 if not is_black:white+=1
 cls=('black' if is_black else 'white')+(' reverse' if k['action']==8 else '')+(' divider' if k['bank']=='divider' else '')
 bank=k['bank'];color='var(--red)' if bank=='A' else 'var(--cyan)' if bank=='B' else 'var(--ink)';aria=f"{'Loop '+bank if bank!='divider' else 'Silent divider'} {name}: {k['label']}";style=f'left:{left:.4f}%;width:calc({4.2 if is_black else 6.25}% - 2px);--key-color:{color}'
 board+=f'<button type="button" class="note-key {cls}" data-fragment-key="{k["key"]}" style="{style}" aria-label="{html.escape(aria)}" aria-pressed="false"><small>{name}</small><strong>{html.escape(label)}</strong></button>'
board+='</div></div>'
block='''<div class="fragment-keyboard-guide" id="fragments-keyboard"><h3>Find the gesture under your fingers.</h3><p class="note">The left bank controls A; the right bank controls B. Select a key below to read its gesture. The first black key in each bank is Reverse.</p>'''+board+'''<div class="fragment-key-detail" role="status"><h3 data-fragment-title>Loop A / F#3 — Reverse</h3><p data-fragment-description>Temporarily reverse the current direction. Hold this key with another Fragment to keep its division while reversing it. If the loop is stopped, Reverse alone prepares the direction; press a Fragment to start the sound.</p></div><p class="note">The centre F#4 is an illuminated, silent divider. White keys move from longer to shorter repeats. The other black keys offer Half speed, Double speed, 1/8T and 1/16T triplets. The two banks have different black-key spacing, just like the FM-1 keyboard.</p></div>'''
p=site/'manual/atolls/index.html';s=p.read_text();s=re.sub(r'(<section class="chapter" id="fragments".*?)(</section>)',lambda m:m[1]+block+m[2],s,count=1,flags=re.S)
# Put Fragment AR immediately after Fragments, before loop-edge shaping.
sections=re.findall(r'<section class="chapter" id="[^"]+".*?</section>',s,re.S);byid={re.search(r'id="([^"]+)"',x)[1]:x for x in sections};order=list(byid);order.remove('fragment-envelope');order.insert(order.index('fragments')+1,'fragment-envelope')
env=byid['fragment-envelope'].replace('Press ENV again to set the Attack and Release of Fragment gestures.','Turn PRESET again from the Fragments page to set the Attack and Release of Fragment gestures.').replace('<kbd>ENV</kbd> <span aria-hidden="true">→</span> <kbd>ENV</kbd>','<kbd>PRESET</kbd>');byid['fragment-envelope']=env
start=s.index('<article id="chapters">');end=s.index('</article>',start);new=''
for i,id in enumerate(order):
 x=re.sub(r'(<div class="chapter-label"><span>)\d+ / ATOLLS',lambda m:m[1]+f'{i+1:02} / ATOLLS',byid[id]);new+=x
s=s[:start]+'<article id="chapters">'+new+s[end:]
nav=''.join(f'<a href="#{id}">{i+1:02} / '+re.search(r'<h2>(.*?)</h2>',byid[id])[1]+'</a>' for i,id in enumerate(order));s=re.sub(r'<div id="chapters-nav">.*?</div>','<div id="chapters-nav">'+nav+'</div>',s,count=1,flags=re.S);p.write_text(s)
p=site/'manual/atolls/data.json';d=json.loads(p.read_text());data={x['id']:x for x in d['chapters']};d['chapters']=[data[id] for id in order];data['fragment-envelope']['gesture']=['PRESET'];data['fragment-envelope']['intro']=data['fragment-envelope']['intro'].replace('Press ENV again','Turn PRESET again from Fragments');p.write_text(json.dumps(d,indent=2));(site/'manual/fragment-map.json').write_text(json.dumps(keys,indent=2))
print('Added exact 27-key map from revo_fragment.h; Fragment AR follows Fragments, then Fades')
