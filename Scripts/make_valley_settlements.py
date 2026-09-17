"""Original editable rural building kit and terrain-fitted settlement infrastructure.
Run in background Blender. No third-party geometry is embedded in this source.
"""
import bpy, math, random, sys, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Scripts'))
from layout import height
# Reuse our original modelling/export helpers, not the old closed buildings.
helpers=(ROOT/'Scripts/make_town_today.py').read_text().split('# All site geometry')[0]
exec(helpers.replace("OUT=ROOT/'SourceAssets/TownToday'","OUT=ROOT/'SourceAssets/ValleySettlements'"))
palette={'Lime':(.63,.59,.49),'Sage':(.22,.29,.23),'Stone':(.29,.27,.23),
 'Oak':(.24,.135,.065),'OakLight':(.38,.25,.13),'Roof':(.065,.077,.079),
 'Metal':(.09,.10,.10),'Glass':(.12,.19,.20),'Floor':(.31,.23,.15),
 'Gravel':(.26,.235,.19),'Asphalt':(.055,.061,.065),'Cream':(.70,.66,.55),
 'Fabric':(.24,.28,.23),'Paper':(.65,.59,.43),'Soil':(.13,.085,.045),
 'Crop':(.26,.31,.10),'Red':(.27,.075,.04)}
mats={}
for n,c in palette.items():
 m=bpy.data.materials.get(n) or bpy.data.materials.new(n);m.diffuse_color=(*c,1);mats[n]=m
parts=[]
random.seed(119)
def window(x,y,z=1.75,w=1.8):
 box((x,y,z),(w,.045,1.45),'Glass',.005)
 for xx in [x-w/2,x,x+w/2]:box((xx,y-.04,z),(.055,.10,1.55),'Metal',.006)
 for zz in [z-.76,z+.76]:box((x,y-.04,zz),(w+.12,.13,.055),'Metal',.005)
 box((x,y-.12,z-.8),(w+.26,.40,.09),'Stone',.015)
def table(x,y):
 box((x,y,.76),(1.8,.86,.08),'OakLight')
 for a in [-.72,.72]:
  for b in [-.30,.30]:box((x+a,y+b,.37),(.07,.07,.74),'Metal',.008)
 box((x+.2,y,.815),(.29,.21,.025),'Paper',.001)
def chair(x,y):
 box((x,y,.46),(.48,.48,.09),'OakLight');box((x,y+.22,.73),(.48,.06,.48),'Oak')
 for a in [-.18,.18]:
  for b in [-.18,.18]:box((x+a,y+b,.23),(.04,.04,.46),'Metal',.004)
def shelf(x,y,w=2):
 for z in [.15,.70,1.25,1.80]:box((x,y,z),(w,.40,.05),'Oak')
 for xx in [x-w/2,x+w/2]:box((xx,y,1),(.06,.40,2),'Metal')
 for i in range(12):
  box((x-w*.4+(i%6)*w*.15,y,.86+(i//6)*.55),(.10,.22,.28),['Sage','Red','Paper'][i%3],.004)
def wall_with_openings(y,w,openings,mat):
 # Each opening: (centre, width, bottom, top). No hidden collision box.
 xs=sorted(set([-w/2,w/2]+[v for x,ww,b,t in openings for v in [x-ww/2,x+ww/2]]))
 for a,b in zip(xs,xs[1:]):
  mid=(a+b)/2;hit=next((q for q in openings if q[0]-q[1]/2<mid<q[0]+q[1]/2),None)
  spans=[(0,3.4)] if hit is None else [(0,hit[2]),(hit[3],3.4)]
  for lo,hi in spans:
   if hi>lo:box((mid,y,(hi+lo)/2),(b-a,.24,hi-lo),mat,.012)
def building(kind,w=10,d=9,finish='Lime'):
 front=-d/2;back=d/2
 box((0,0,-.10),(w+.1,d+.1,.20),'Floor',.005)
 door=2.8 if kind=='Barn' else 1.8
 wall_with_openings(front,w,[(0,door,0,2.7),(-w*.32,1.8,1,2.5),(w*.32,1.8,1,2.5)],finish)
 wall_with_openings(back,w,[(-w*.27,1.8,1,2.5),(w*.27,1.8,1,2.5)],finish)
 for x in [-w*.32,w*.32]:window(x,front-.02)
 for x in [-w*.27,w*.27]:window(x,back+.02)
 for side in [-1,1]:
  box((side*w/2,0,1.7),(.24,d,3.4),finish)
  # Visible board cladding and layered stone plinth, avoiding doorways.
  for j in range(int(d/.22)):
   yy=-d/2+.12+j*.22
   box((side*(w/2+.13),yy,2.25),(.035,.19,2.2),'Oak' if finish!='Sage' else 'Sage',.004)
  for row in range(3):
   for j in range(int(d/.6)):
    yy=-d/2+.3+j*.6
    box((side*(w/2+.14),yy,.12+row*.22),(.06,.575,.20),'Stone',.012)
  face([(side*w/2,-d/2,3.4),(side*w/2,d/2,3.4),(side*w/2,0,5.1)],'Oak')
  face([(-w/2-.45,side*(d/2+.45),3.48),(w/2+.45,side*(d/2+.45),3.48),(w/2+.45,0,5.15),(-w/2-.45,0,5.15)],'Roof')
  # Standing-seam roof, gutters and downpipes.
  for i in range(int((w+1)/.65)):
   xx=-w/2-.4+i*.65;tube((xx,0,5.18),(xx,side*(d/2+.45),3.51),.018,'Metal',6)
  tube((-w/2-.48,side*(d/2+.43),3.47),(w/2+.48,side*(d/2+.43),3.47),.075,'Metal')
  tube((w/2+.3,side*(d/2+.43),3.45),(w/2+.3,side*(d/2+.43),.08),.06,'Metal')
 # Open porch and door leaf folded alongside the entrance, 1.8m clear.
 box((0,front-.9,-.07),(w*.72,1.8,.14),'Stone',.015)
 roof=box((0,front-.9,2.95),(w*.75,2.2,.12),'Metal');roof.rotation_euler.x=.045
 for x in [-w*.33,w*.33]:box((x,front-1.65,1.44),(.13,.13,2.88),'Oak')
 box((door/2+.12,front+.6,1.27),(.065,1.16,2.54),'Oak',.01)
 for x in [-door/2-.035,door/2+.035]:box((x,front-.04,1.35),(.065,.1,2.7),'Metal',.004)
 box((0,front-.04,2.73),(door+.14,.1,.065),'Metal',.004)
 # Roof void is open to the room; exposed rafters, no inaccessible storey.
 for xx in [-w*.34,0,w*.34]:
  tube((xx,-d/2,3.37),(xx,d/2,3.37),.09,'Oak',4)
 if kind in ['Cottage','Farmhouse']:
  # Rear rooms connected through a 1.8m door; front living/kitchen clear centre route.
  wall_with_openings(1.1,w,[(0,1.8,0,2.7)],'Lime')
  box((-w*.3,back-1.5,.25),(1.8,2.1,.5),'Oak');box((-w*.3,back-1.5,.57),(1.75,2.05,.18),'Cream')
  box((-w*.3,back-1.5,.69),(1.78,1.5,.08),'Fabric');box((-w*.3,back-.72,.74),(1.4,.45,.15),'Cream')
  shelf(w*.31,back-.45,2.1)
  box((-w/2+.5,-1.7,.44),(.75,2.8,.88),'Sage');box((-w/2+.5,-1.7,.92),(.86,2.9,.08),'Stone')
  box((-w/2+.5,-2.2,.97),(.55,.7,.025),'Metal',.005)
  for yy in [-2.4,-2.05]:tube((-w/2+.5,yy,.975),(-w/2+.5,yy,.99),.10,'Metal')
  table(w*.28,-1.5);chair(w*.28,-.5);chair(w*.28,-2.5)
  box((w/2-.5,0,.4),(.7,1.45,.8),'Oak');box((w/2-.5,0,1.02),(.08,.95,.6),'Metal')
 elif kind=='Barn':
  for x in [-w*.33,w*.33]:
   for y in [-1,2,4]:
    for z in [.5,1.5]:box((x,y,z),(1.5,1.1,.95),'Crop',.06)
  shelf(-w*.34,-d*.28,2.5);table(w*.30,-d*.27)
 elif kind=='Workshop':
  for x in [-w*.34,w*.34]:shelf(x,back-.45,2.6);table(x,0)
  box((-w*.32,-2,.35),(1.4,.7,.7),'Red');box((w*.30,2,.65),(1,.7,1.3),'Sage')
 else:
  for x in [-w*.30,w*.30]:
   shelf(x,back-.45,2.5);shelf(x,.8,2.5)
  table(-w*.30,-2);box((-w*.30,-2,.98),(.35,.3,.36),'Metal')
  table(w*.30,-2);chair(w*.30,-3.1)
 if kind not in ['Cottage','Farmhouse']:
  text({'Store':'VALLEY PROVISIONS','Workshop':'REPAIR & SUPPLY','Barn':'FIELD STORE'}[kind],(0,front-.14,3.07),.24,'Cream')
 # Modest masonry chimney with a metal cap.
 if kind!='Barn':
  box((-w*.33,d*.22,4.7),(.55,.55,1.55),'Stone');box((-w*.33,d*.22,5.5),(.72,.72,.09),'Metal')
 export('SM_Valley_'+kind+'_'+finish)
for kind,w,d,finish in [('Cottage',10,9,'Lime'),('Cottage',10,9,'Sage'),('Cottage',10,9,'Stone'),('Farmhouse',12,11,'Lime'),('Store',12,10,'Lime'),('Workshop',12,10,'Oak'),('Barn',14,14,'Oak')]:building(kind,w,d,finish)

buildings=[]
def add(group,x,y,kind='Cottage',finish='Lime',yaw=0):
 w,d={'Cottage':(10,9),'Farmhouse':(12,11),'Store':(12,10),'Workshop':(12,10),'Barn':(14,14)}[kind]
 z=max(height(x+dx,y+dy) for dx in [-w/2,0,w/2] for dy in [-d/2,0,d/2])+.20
 buildings.append(dict(id='V%02d'%(len(buildings)+1),group=group,x=x,y=y,z=z,yaw=yaw,w=w,d=d,kind=kind,mesh='SM_Valley_'+kind+'_'+finish))
for row,yy in enumerate([-54,-10,33,77]):
 for col,x in enumerate([153,191,270]):add('Main town',x,yy,finish=['Lime','Sage','Stone'][(row+col)%3],yaw=180 if row>=2 else 0)
add('Main town',235,-12,'Store');add('Main town',305,32,'Workshop','Oak',180)
add('Main town',116,-12,'Workshop','Oak');add('Main town',235,77,finish='Sage',yaw=180)
for group,cx,cy in [('North hamlet',350,165),('South hamlet',340,-155)]:
 add(group,cx-20,cy-14,finish='Stone');add(group,cx+18,cy-14,finish='Lime')
 add(group,cx-20,cy+18,finish='Sage',yaw=180);add(group,cx+18,cy+18,'Workshop','Oak',180)
for group,cx,cy in [('West farm',105,-215),('East farm',450,32)]:
 add(group,cx-15,cy-15,'Farmhouse');add(group,cx+20,cy-18,'Barn','Oak')

# Terrain-following roads and farm tracks. World Y converts to Blender -Y.
site_faces={}
def qworld(v,mat):
 # Navigation discards downward-facing triangles even with double-sided collision.
 area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(v,v[1:]+v[:1]))
 if area<0:v=list(reversed(v))
 site_faces.setdefault(mat,[]).append([(x,-y,z) for x,y,z in reversed(v)])
roads=[]
def road(points,width=5,mat='Gravel'):
 roads.append(dict(points=points,width=width))
 for (x0,y0),(x1,y1) in zip(points,points[1:]):
  dist=math.hypot(x1-x0,y1-y0);nx=-(y1-y0)/dist*width/2;ny=(x1-x0)/dist*width/2
  count=math.ceil(dist/2)
  for i in range(count):
   a=i/count;b=(i+1)/count
   xy=[(x0+(x1-x0)*t+s*nx,y0+(y1-y0)*t+s*ny) for t,s in [(a,-1),(b,-1),(b,1),(a,1)]]
   qworld([(x,y,height(x,y)+.13) for x,y in xy],mat)
road([(65,8),(330,8),(385,35),(470,35)],6,'Asphalt')
road([(225,-70),(225,96)],5,'Asphalt')
for yy in [-35,57]:road([(135,yy),(315,yy)],4.5)
road([(310,57),(325,108),(350,165),(386,165)],4.5)
road([(270,-35),(308,-90),(340,-155),(385,-155)],4.5)
road([(160,-35),(148,-107),(105,-215),(140,-215)],4.5)
for b in buildings:
 x,y,z,w,d=b['x'],b['y'],b['z'],b['w'],b['d'];sgn=1 if b['yaw']==0 else -1
 # Stone retaining foundation with floor flush at z; solid sides only below floor.
 bottom=min(height(x+dx,y+dy) for dx in [-w/2,w/2] for dy in [-d/2,d/2])-.2
 box((x,-y,(z+bottom)/2-.015),(w+.3,d+.3,z-bottom-.03),'Stone',.015)
 # Broad approach tapers gently from porch to terrain over 11m.
 ya=y+sgn*(d/2+1.8);yb=ya+sgn*11
 porch_bottom=min(height(x+dx,yy) for dx in [-w*.36,w*.36] for yy in [y+sgn*d/2,ya])-.15
 box((x,-(y+sgn*(d/2+.9)),(z+porch_bottom)/2-.015),(w*.72,1.8,z-porch_bottom-.03),'Stone',.01)
 for j in range(12):
  a=j/12;c=(j+1)/12
  coords=[]
  for t,side in [(a,-1),(c,-1),(c,1),(a,1)]:
   xx=x+side*2;yy=ya+(yb-ya)*t;zz=max(height(xx,yy)+.13,(z-.005)*(1-t)+(height(xx,yy)+.14)*t)
   coords.append((xx,yy,zz))
  qworld(coords,'Gravel')
  for side,k0,k1 in [(-1,0,1),(1,3,2)]:
   p0,p1=coords[k0],coords[k1];outer=x+side*3.5
   qworld([p0,p1,(outer,p1[1],height(outer,p1[1])-.03),(outer,p0[1],height(outer,p0[1])-.03)],'Gravel')
 # Flat connection beneath porch and threshold, no stair barrier for robots.
 qworld([(x-2,y+sgn*d/2,z-.005),(x+2,y+sgn*d/2,z-.005),(x+2,ya,z-.005),(x-2,ya,z-.005)],'Stone')
 b['approach']=[x,y+sgn*(d/2+1),z+.98];b['inside']=[x,y,z+.98];b['rear']=[x,y-sgn*2.5,z+.98]
 # Discovery anchors are metadata only, future gameplay doesn't auto-trigger.
 b['clue_anchors']=[[x-w*.27,y-sgn*(d/2-.7),z+1.25],[x+w*.27,y,z+.9]]
for cx,cy in [(105,-215),(450,32)]:
 for offset in [35,62]:
  x0=cx-25;x1=cx+35;y0=cy-offset-15;y1=cy-offset
  for j in range(10):
   ya=y0+j*1.5;yb=ya+.8
   for i in range(20):
    xa=x0+i*3;xb=xa+3;qworld([(x,y,height(x,y)+.09) for x,y in [(xa,ya),(xb,ya),(xb,yb),(xa,yb)]],'Soil')
  for xx in range(int(x0),int(x1)+1,4):
   zz=height(xx,y0);tube((xx,-y0,zz),(xx,-y0,zz+1.1),.06,'Oak',6)
   if xx<x1:
    for h in [.5,.95]:tube((xx,-y0,zz+h),(xx+4,-y0,height(xx+4,y0)+h),.025,'Metal',6)
for mat,faces in site_faces.items():
 verts=[];polys=[]
 for f in faces:polys.append(tuple(range(len(verts),len(verts)+len(f))));verts.extend(f)
 me=bpy.data.meshes.new('Terrain fitted '+mat);me.from_pydata(verts,[],polys);me.update();o=bpy.data.objects.new('Terrain fitted '+mat,me);bpy.context.collection.objects.link(o);material(o,mat)
export('SM_Valley_Infrastructure')
for o in bpy.context.scene.objects:o.hide_set(False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Valley-Settlements.blend'))
(OUT/'palette.json').write_text(json.dumps(palette,indent=2))
(OUT/'layout.json').write_text(json.dumps({'buildings':buildings,'roads':roads},indent=2))
print('VALLEY_SOURCE_COMPLETE',len(buildings),flush=True)
