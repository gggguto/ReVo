from pathlib import Path
import struct,zlib,json,hashlib,re
root=Path(__file__).resolve().parents[3];site=root/'outputs/revo-github/site';base=root/'outputs/integracao-fm1/emulator';records={}
for name,ms in [('distance',400),('drift',300),('beam',150),('resonance',180)]:
 src=base/f'revo-{name}-captures';report=json.loads((src/'report.json').read_text());assert not report['halted'] and not report['jitFailures'];hashes=set();kept=[];skipped=[]
 for i in range(48):
  a=struct.unpack('<57600H',(src/f'{name}-{i}.rgb565').read_bytes());color=0xd650 if name=='resonance' else 0x4e7c if name=='distance' else 65535
  popup=all(sum(a[y*240+x]==color for x in range(40,200))>=155 for y in [96,127])
  (skipped if popup else kept).append(i)
 for p in (site/'assets/screens').glob('motion-'+name+'-*.png'):p.unlink()
 for output_index,i in enumerate(kept):
  blob=(src/f'{name}-{i}.rgb565').read_bytes();a=struct.unpack('<57600H',blob);raw=b''.join(b'\0'+bytes(v for x in a[y*240:y*240+240] for v in (((x>>11)&31)*255//31,((x>>5)&63)*255//63,(x&31)*255//31)) for y in range(240))
  def c(t,d):return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d))
  (site/f'assets/screens/motion-{name}-{output_index:02}.png').write_bytes(b'\x89PNG\r\n\x1a\n'+c(b'IHDR',struct.pack('>IIBBBBB',240,240,8,2,0,0,0))+c(b'IDAT',zlib.compress(raw))+c(b'IEND',b''))
  graph=b''.join(blob[(y*240+8)*2:(y*240+232)*2] for y in range(60,160));hashes.add(hashlib.sha256(graph).hexdigest())
 assert len(hashes)>1,(name,'The graph does not move')
 records[name]={'frames':len(kept),'omittedPopupFrames':skipped,'intervalMs':ms,'distinctGraphStates':len(hashes),'packageSha256':report['packageSha256'],'source':'Real firmware LCD captures, after temporary value popup expired.'}
 p=site/'manual/bioma/index.html';s=p.read_text();pattern=r'(<section class="chapter" id="'+name+r'".*?)(</section>)'
 def update(m):
  old=m[1];old=re.sub(r'<img src="../../assets/screens/[^\"]+" alt=',f'<img src="../../assets/screens/motion-{name}-00.png" data-native-sequence="{name}" alt=',old,count=1);return old+m[2]
 s,count=re.subn(pattern,update,s,count=1,flags=re.S);assert count==1,name;p.write_text(s)
(site/'assets/screens/native-sequences.json').write_text(json.dumps(records,indent=2))
print('Prepared and verified moving graph regions:',{k:v['distinctGraphStates'] for k,v in records.items()})
