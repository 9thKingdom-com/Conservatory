"""Editable road centrelines -> terrain overlay mask; no terrain height edits."""
import math,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];O=R/'SourceAssets/CityRoadDraft';O.mkdir(parents=True,exist_ok=True)
roads=[];origin=(285,-40)
def add(name,points,width=7,curve=False):roads.append(dict(name=name,points=points,width_m=width,curve=curve))
def ring(name,x,y,r,width=8):add(name,[(x+r*math.cos(i*math.tau/128),y+r*math.sin(i*math.tau/128)) for i in range(129)],width)
ring('Civic square loop',0,0,32,9)
add('Civic west avenue',[(-110,0),(-32,0)],10);add('Civic east avenue',[(32,0),(110,0)],10)
add('Civic north avenue',[(0,32),(0,145)],10);add('Civic south avenue',[(0,-32),(0,-350)],10)
add('Town west boulevard',[(-110,-110),(-110,110)],9);add('Town east boulevard',[(110,-110),(110,110)],9)
add('Town north boulevard',[(-110,110),(-65,123),(0,145),(65,123),(110,110)],9,True)
add('Town south boulevard',[(-110,-110),(0,-115),(110,-110)],9,True)
for x in [-55,55]:add('Town grid column '+str(x),[(x,-112),(x,126)],7)
for y in [-55,65]:add('Town grid row '+str(y),[(-110,y),(110,y)],7)
for side,s in [('West',-1),('East',1)]:
 def pts(values):return [(s*x,y) for x,y in values]
 add(side+' estate outer loop',pts([(110,110),(175,130),(238,95),(266,30),(248,-60),(180,-106),(110,-110)]),8,True)
 add(side+' estate middle crescent',pts([(110,77),(162,98),(207,74),(232,23),(215,-43),(166,-76),(110,-78)]),6,True)
 add(side+' estate park crescent',pts([(110,37),(149,63),(181,45),(193,12),(178,-23),(151,-42),(110,-42)]),6,True)
 add(side+' estate north link',pts([(175,130),(162,98),(149,63)]),6,True)
 add(side+' estate south link',pts([(180,-106),(166,-76),(151,-42)]),6,True)
 add(side+' estate cross link',pts([(266,30),(232,23),(193,12)]),6,True)
add('South estate outer crescent',[(-110,-110),(-130,-188),(-100,-255),(0,-290),(100,-255),(130,-188),(110,-110)],8,True)
add('South estate middle crescent',[(-85,-114),(-100,-182),(-70,-235),(0,-263),(70,-235),(100,-182),(85,-114)],6,True)
add('South estate park crescent',[(-55,-115),(-69,-177),(-44,-211),(0,-230),(44,-211),(69,-177),(55,-115)],6,True)
for s in [-1,1]:add('South radial '+str(s),[(s*100,-255),(s*70,-235),(s*44,-211)],6)
add('South neighbourhood cross street',[(-125,-160),(0,-165),(125,-160)],7,True)
add('Hill neighbourhood winding loop',[(0,145),(-72,171),(-123,222),(-90,274),(-20,304),(66,274),(109,219),(60,169),(0,145)],7,True)
add('Hill neighbourhood inner road',[(-72,171),(-60,220),(0,246),(66,274)],6,True)
add('Hill viewpoint spur',[(0,246),(12,282),(-20,304),(-40,338)],5,True)
add('Northwest village approach',[(-238,95),(-266,167),(-273,225),(-262,288)],8,True)
add('Northeast village approach',[(238,95),(272,159),(295,225),(300,305)],8,True)
add('Southwest village approach',[(-248,-60),(-267,-139),(-275,-208),(-275,-310)],8,True)
add('Southeast village approach',[(248,-60),(280,-125),(291,-222),(300,-306)],8,True)
roundabouts=[(-110,0,8),(110,0,8),(-110,-110,9),(110,-110,9),(0,145,9),(0,-115,8),(-238,95,8),(238,95,8)]
def sample(road):
 p=road['points']
 if not road['curve']:return p
 result=[];p=[p[0]]+p+[p[-1]]
 for i in range(1,len(p)-2):
  a,b,c,d=p[i-1:i+3];steps=max(8,int(math.dist(b,c)/2))
  for j in range(steps):
   t=j/steps;result.append(tuple(.5*((2*b[k])+(-a[k]+c[k])*t+(2*a[k]-5*b[k]+4*c[k]-d[k])*t*t+(-a[k]+3*b[k]-3*c[k]+d[k])*t*t*t) for k in range(2)))
 return result+[p[-2]]
N=4096;lo=-630;span=1260;scale=N/span
layers=[Image.new('L',(N,N),0) for _ in range(2)]
def pix(p):return ((p[0]+origin[0]-lo)*scale,(p[1]+origin[1]-lo)*scale)
for image,extra in zip(layers,[0,2]):
 d=ImageDraw.Draw(image)
 for road in roads:
  pts=[pix(p) for p in sample(road)];width=round((road['width_m']+extra)*scale);d.line(pts,fill=255,width=width,joint='curve')
  for x,y in [pts[0],pts[-1]]:d.ellipse((x-width/2,y-width/2,x+width/2,y+width/2),fill=255)
 for x,y,r in roundabouts:
  px,py=pix((x,y));rr=(r+4+extra/2)*scale;d.ellipse((px-rr,py-rr,px+rr,py+rr),fill=255);rr=(r-3-extra/2)*scale;d.ellipse((px-rr,py-rr,px+rr,py+rr),fill=0)
mask=Image.merge('RGB',(layers[0],layers[1],Image.new('L',(N,N),0)));mask.save(O/'CityRoadMask.png')
spec=dict(reference='John supplied CITY-PLAN.png',origin_metres=origin,texture_world_min_metres=[lo,lo],texture_world_span_metres=span,resolution=N,roads=roads,roundabouts=roundabouts,status='Road layout draft only; dimensions fitted to existing valley, not the image scale',terrain_grading=False)
(O/'RoadLayout.json').write_text(json.dumps(spec,indent=2))
# Plan preview with the same mask, flipped so north is up.
preview=Image.new('RGB',(N,N),(111,127,93));preview.paste((176,172,152),mask=layers[1]);preview.paste((73,77,77),mask=layers[0]);preview=preview.crop((int((0-lo)*scale),int((-415-lo)*scale),int((615-lo)*scale),int((320-lo)*scale))).transpose(Image.Transpose.FLIP_TOP_BOTTOM);preview.thumbnail((1100,1300))
canvas=Image.new('RGB',(preview.width+80,preview.height+120),(241,237,225));canvas.paste(preview,(40,85));draw=ImageDraw.Draw(canvas);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24);draw.text((40,22),'CITY ROAD DRAFT — central grid and curved neighbourhoods',font=font,fill=(40,50,43));draw.text((40,canvas.height-27),'Roads only | Terrain and buildings retained | Adjustable layout',fill=(40,50,43));canvas.save(O/'RoadDraft-Plan.png')
print('CITY_ROAD_MASK_CREATED',len(roads))
