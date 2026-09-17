"""Generate a terrain-derived north-up map for the in-world security display."""
from pathlib import Path
from PIL import Image,ImageDraw
from layout import height,path_y
ROOT=Path(__file__).resolve().parents[1];N=768
im=Image.new('RGB',(N,N));pixels=im.load()
for row in range(N):
 for col in range(N):
  x=-630+1260*col/(N-1);y=630-1260*row/(N-1);h=height(x,y)
  shade=max(.6,min(1.3,1+(height(x-2,y+2)-h)*.11))
  contour=.7 if h%10<.4 else 1
  pixels[col,row]=tuple(int(v*shade*contour) for v in (28+h*.42,46+h*.48,44+h*.37))
d=ImageDraw.Draw(im)
def p(x,y):return ((x+630)/1260*N,(630-y)/1260*N)
for v in range(-600,601,200):
 d.line([p(v,-630),p(v,630)],fill=(65,83,78),width=1);d.line([p(-630,v),p(630,v)],fill=(65,83,78),width=1)
d.rectangle([p(130,110),p(310,-100)],fill=(60,64,59),outline=(121,129,113),width=2)
d.line([p(x,path_y(x)) for x in range(-170,260)],fill=(148,134,108),width=3)
for y in [-50,0,50]:d.line([p(130,y),p(310,y)],fill=(126,130,119),width=2)
for x in [160,220,280]:d.line([p(x,-100),p(x,110)],fill=(126,130,119),width=2)
d.text(p(175,125),'TOWN',fill=(205,219,201));d.text(p(-460,380),'WOODLAND',fill=(163,190,173));d.text(p(-260,-340),'VALLEY',fill=(163,190,173))
out=ROOT/'SourceAssets/VR';out.mkdir(parents=True,exist_ok=True);im.save(out/'T_TerrainMap.png')
