from pathlib import Path
import json,re,struct,zlib,html
root=Path(__file__).resolve().parents[3];site=root/'outputs/revo-github/site';captures=root/'outputs/integracao-fm1/emulator/revo-inhabitants-captures';out=site/'assets/screens'
def convert(source,dest):
 a=struct.unpack('<57600H',source.read_bytes());raw=b''.join(b'\0'+bytes(v for x in a[y*240:y*240+240] for v in (((x>>11)&31)*255//31,((x>>5)&63)*255//63,(x&31)*255//31)) for y in range(240))
 def c(t,d):return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d))
 dest.write_bytes(b'\x89PNG\r\n\x1a\n'+c(b'IHDR',struct.pack('>IIBBBBB',240,240,8,2,0,0,0))+c(b'IDAT',zlib.compress(raw))+c(b'IEND',b''))
for family in ['birds','insects','water']:
 for mode in ['wild','tame']:
  for i in range(6):convert(captures/f'{family}-{mode}-{i}.rgb565',out/f'inhabitants-{family}-{mode}-{i:02}.png')
convert(root/'outputs/integracao-fm1/emulator/revo-response-clean-capture/response-clean.rgb565',out/'response-clean.png')
p=site/'manual/bioma/data.json';d=json.loads(p.read_text());families={x['id']:x for x in d['chapters'] if x['id'] in ['birds','insects','water']};assert len(families)==3
for key,c in families.items():c['label']=key.title();c['color']={'birds':'var(--red)','insects':'var(--yellow)','water':'var(--cyan)'}[key]
(site/'manual/inhabitants.json').write_text(json.dumps(families,indent=2))
p=site/'manual/bioma/index.html';s=p.read_text();old=re.search(r'<section class="chapter" id="birds".*?</section>',s,re.S)[0]
panel=old[old.index('<div class="chapter-grid">'):old.rindex('</section>')];panel=panel.replace('data-birds-animation','data-inhabitant-screen').replace('../../assets/screens/birds-0.png','../../assets/screens/inhabitants-birds-tame-00.png').replace('alt="ReVo Bioma — Meet Birds."','alt="Birds in Tame mode, with Cycle active"')
panel=panel.replace('<ul class="control-list">','<ul class="control-list inhabitant-controls">').replace('<div class="try"><b>Take a moment.</b>','<div class="try"><b>Take a moment.</b><span data-inhabitant-try>').replace('</div><p class="chapter-extra">','</span></div><p class="chapter-extra" data-inhabitant-extra>')
# Explicitly identify each paragraph for updates, keeping the existing knob help layout.
intro=families['birds']['intro'];tabs='<div class="inhabitant-tabs" role="tablist" aria-label="Island inhabitants">'
for key,c in families.items():tabs+=f'''<button type="button" role="tab" id="inhabitant-tab-{key}" aria-controls="inhabitant-panel" aria-selected="{'true' if key=='birds' else 'false'}" tabindex="{'0' if key=='birds' else '-1'}" data-inhabitant="{key}" style="--family-color:{c['color']}"><img src="../../assets/{key}-creature.png" width="80" height="80" alt=""><span>{c['label']}</span></button>'''
tabs+='</div>'
new='''<section class="chapter inhabitant-chapter" id="inhabitants" style="--accent:var(--red)" data-family="birds" data-timing="tame"><span class="family-anchor" id="birds" aria-hidden="true"></span><span class="family-anchor" id="insects" aria-hidden="true"></span><span class="family-anchor" id="water" aria-hidden="true"></span><div class="chapter-label"><span>02 / BIOMA</span><span>FIELD GUIDE</span></div><h2>Meet our Inhabitants</h2><div class="inhabitant-intro"><p class="chapter-intro" data-inhabitant-description>'''+html.escape(intro)+'''</p>'''+tabs+'''</div><div class="gesture" aria-label="Controls used in this chapter"><kbd>EDIT</kbd> <span aria-hidden="true">→</span> <kbd>ALGO</kbd></div><div class="inhabitant-mode" role="group" aria-label="Compare Wild and Tame"><span>Compare timing</span><button type="button" data-timing="wild" aria-pressed="false">Wild</button><button type="button" data-timing="tame" aria-pressed="true">Tame</button></div><p class="cycle-state" role="status" data-cycle-state>Cycle is active in Tame. It follows the global clock.</p><div id="inhabitant-panel" role="tabpanel" aria-labelledby="inhabitant-tab-birds">'''+panel+'''</div></section>'''
s=s.replace(old,new)
for key in ['insects','water']:s=re.sub(r'<section class="chapter" id="'+key+r'".*?</section>','',s,flags=re.S)
s=re.sub(r'<a href="#birds">.*?</a>','<a href="#inhabitants">02 / Meet our Inhabitants</a>',s)
for key in ['insects','water']:s=re.sub(r'<a href="#'+key+r'">.*?</a>','',s)
count=[0]
def relabel(m):count[0]+=1;return m[1]+f'{count[0]:02} / BIOMA'+m[2]
s=re.sub(r'(<div class="chapter-label"><span>)\d+ / BIOMA(</span>)',relabel,s)
count=[0]
def nav(m):count[0]+=1;return m[1]+f'{count[0]:02} / '+m[2]
s=re.sub(r'(<a href="#[^"]+">)\d+ / ([^<]+</a>)',nav,s)
s=s.replace('assets/screens/dialogues.png','assets/screens/response-clean.png')
p.write_text(s)
# Retain the full family definitions in their separate data file for the submenu.
d['chapters']=[({**c,'id':'inhabitants','title':'Meet our Inhabitants','screen':'inhabitants-birds-tame-00'} if c['id']=='birds' else c) for c in d['chapters'] if c['id'] not in ['insects','water']];p=site/'manual/bioma/data.json';p.write_text(json.dumps(d,indent=2))
print('Prepared three native family screens in both modes; consolidated the inhabitants chapter; Response image cleaned')
