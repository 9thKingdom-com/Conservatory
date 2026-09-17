"""8-bit native Landscape weightmaps, 505 samples at the existing 2.5m spacing."""
import json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image
root=Path(__file__).resolve().parents[1];out=root/'SourceAssets/LandscapePaintStudy';out.mkdir(parents=True,exist_ok=True)
data=json.loads((root/'SourceAssets/ValleySettlements/layout.json').read_text());Y,X=np.mgrid[0:505,0:505]*2.5-630
masks={n:np.zeros_like(X,dtype=float) for n in ['Gravel','Asphalt','Soil']}
def stroke(points,width):
 d=np.full_like(X,1e9,dtype=float)
 for a,b in zip(points,points[1:]):
  dx=b[0]-a[0];dy=b[1]-a[1];t=np.clip(((X-a[0])*dx+(Y-a[1])*dy)/(dx*dx+dy*dy),0,1)
  d=np.minimum(d,np.hypot(X-a[0]-t*dx,Y-a[1]-t*dy))
 edge=.22*np.sin(X*.43+Y*.17)+.18*np.sin(Y*.62-X*.13)
 return np.clip((width/2+1.4+edge-d)/2.0,0,1)
for i,r in enumerate(data['roads']):
 name='Asphalt' if i<2 else 'Gravel';masks[name]=np.maximum(masks[name],stroke(r['points'],r['width']))
for b in data['buildings']:
 s=1 if b['yaw']==0 else -1
 masks['Gravel']=np.maximum(masks['Gravel'],stroke([(b['x'],b['y']+s*b['d']/2),(b['x'],b['y']+s*(b['d']/2+13))],3.5))
for cx,cy in [(105,-215),(450,32)]:
 for offset in [35,62]:
  # A continuous soil bed replaces the floating individual crop strips.
  d=np.maximum(np.maximum(cx-25-X,X-(cx+35)),np.maximum(cy-offset-15-Y,Y-(cy-offset)))
  masks['Soil']=np.maximum(masks['Soil'],np.clip((1-d)/2,0,1))
for n,a in masks.items():Image.fromarray(np.uint8(a*255)).save(out/(n+'.png'))
(out/'masks.json').write_text(json.dumps({'resolution':[505,505],'sample_spacing_metres':2.5,'world_origin_metres':[-630,-630],'layers':list(masks)},indent=2))
