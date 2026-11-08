from pathlib import Path
import struct,zlib,json,hashlib
root=Path(__file__).resolve().parents[3];site=root/'outputs/revo-github/site';src=root/'outputs/integracao-fm1/emulator/revo-home-captures';out=site/'assets/homes'
def read(p):return list(struct.unpack('<'+str(p.stat().st_size//2)+'H',p.read_bytes()))
def png(p,w,h,a):
 raw=b''.join(b'\0'+bytes(v for x in a[y*w:y*w+w] for v in (((x>>11)&31)*255//31,((x>>5)&63)*255//63,(x&31)*255//31)) for y in range(h))
 def ch(t,d):return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d))
 p.write_bytes(b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+ch(b'IDAT',zlib.compress(raw))+ch(b'IEND',b''))
def crop(a,y,h):
 a=a[y*240:(y+h)*240];top=(160-h)//2;return [0]*(240*top)+a+[0]*(240*(160-h-top))
for i in range(24):
 a=read(src/f'bioma-{i}.rgb565');png(out/f'bioma-{i:02}.png',240,160,crop(a,45,144));png(out/f'bioma-full-{i:02}.png',240,240,a)
png(out/'bioma-stop.png',240,240,read(src/'bioma-stopped.rgb565'))
for i in range(35):
 a=read(src/f'atolls-a-{i}.rgb565');b=read(src/f'atolls-b-{i}.rgb565')
 # Both layers come from the actual Home renderer, selecting A and B at adjacent
 # capture times. Keep original island/grays and overlay B's exact cyan pixels.
 a=[q if q==0x4e7c else p for p,q in zip(a,b)];png(out/f'atolls-{i:02}.png',240,160,crop(a,58,149))
for k,name in enumerate(['birds','insects','water']):png(site/'assets'/f'{name}-creature.png',64,64,read(Path(f'/tmp/revo-creature-{k}.rgb565')))
r=json.loads((src/'report.json').read_text());(out/'provenance.json').write_text(json.dumps({'source':'Actual Home screens rendered by the ReVo firmware in fm1-emu; no newly drawn animation.','packageSha256':r['packageSha256'],'bioma':'24 native Home captures, 220 ms apart. Native birds, insect pulses and water ripples.','atolls':'35 native Home captures for each selected loop, at about 400 ms per pair. Composite original red A and cyan B Home pixels over the unchanged native island. No paths or sprites added.','creatures':'Original creature() renderer from ilha_ui.c; native Birds, Insects and Water at scale3.'},indent=2))
print('Prepared native Home frames and original creature sprites')
