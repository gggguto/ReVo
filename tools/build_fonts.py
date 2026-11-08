"""Convert the firmware's OFL Terminus bitmap glyphs into outlined web TTFs.
Development-only: fonttools is required to regenerate; not to serve the site.
"""
from pathlib import Path
import sys,re
sys.path.insert(0,'/tmp/revo-font-tools')
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
base=Path(__file__).resolve().parents[1];assets=base/'site/assets'
for variant,suffix in [('n','Text'),('b','Display')]:
 src=assets/'font-source'/('ter-u16'+variant+'.bdf');text=src.read_text();glyphs={};cmap={};metrics={};pen=TTGlyphPen(None);glyphs['.notdef']=pen.glyph();metrics['.notdef']=(512,0)
 for block in text.split('STARTCHAR ')[1:]:
  cp=int(re.search(r'\nENCODING (\d+)',block)[1]);
  if not (32<=cp<=255 or cp in [0x2013,0x2014,0x2018,0x2019,0x201c,0x201d,0x2026] or 0x2190<=cp<=0x21ff):continue
  width,height,xoff,yoff=map(int,re.search(r'\nBBX (\d+) (\d+) (-?\d+) (-?\d+)',block).groups());rows=re.search(r'\nBITMAP\n(.*?)\nENDCHAR',block,re.S)[1].splitlines();pen=TTGlyphPen(None)
  for y,row in enumerate(rows):
   bits=bin(int(row,16))[2:].zfill(((width+7)//8)*8)[:width];x=0
   while x<width:
    if bits[x]=='0':x+=1;continue
    end=x+1
    while end<width and bits[end]=='1':end+=1
    left=(x+xoff)*64;right=(end+xoff)*64;bottom=(height-1-y+yoff)*64;top=bottom+64
    pen.moveTo((left,bottom));pen.lineTo((left,top));pen.lineTo((right,top));pen.lineTo((right,bottom));pen.closePath();x=end
  name=f'uni{cp:04X}';glyphs[name]=pen.glyph();cmap[cp]=name;metrics[name]=(512,0)
 fb=FontBuilder(1024,isTTF=True);fb.setupGlyphOrder(list(glyphs));fb.setupCharacterMap(cmap);fb.setupGlyf(glyphs);fb.setupHorizontalMetrics(metrics);fb.setupHorizontalHeader(ascent=768,descent=-256);fb.setupNameTable({'familyName':'ReVo Field '+suffix,'styleName':'Regular','uniqueFontIdentifier':'ReVoField'+suffix+'2026','fullName':'ReVo Field '+suffix,'psName':'ReVoField-'+suffix,'version':'Version 1.0','copyright':'Derived from Terminus. Copyright 2020 Dimitar Toshkov Zhekov. SIL Open Font License 1.1. ReVo outline conversion 2026.'});fb.setupOS2(sTypoAscender=768,sTypoDescender=-256,usWinAscent=768,usWinDescent=256);fb.setupPost();fb.setupMaxp();fb.save(str(assets/('revo-'+suffix.lower()+'.ttf')))
 print('Built',suffix,len(glyphs),'glyphs')
