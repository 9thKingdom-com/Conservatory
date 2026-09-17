"""Original decorative lift kit based on the user's lift1 reference."""
import bpy,math,sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Scripts'))
# Reuse only the geometry helper definitions, without regenerating environment meshes.
source=(ROOT/'Scripts/make_assets.py').read_text();exec(source[:source.index('for variant in range(6):')])
OUT=ROOT/'SourceAssets/OrnateLift';OUT.mkdir(parents=True,exist_ok=True)
for n in ['LiftEnamel','Brass','FloorLight','FloorDark','ConservatoryGlass','Lamp']:
 MATS.append(n);materials[n]=bpy.data.materials.new(n)
def tube(m,a,b,r=.025,mat='Brass'):
 # Stable axis basis, including a tube parallel to world Y.
 a,b=Vector(a),Vector(b);d=(b-a).normalized();v=d.cross(Vector((0,0,1)) if abs(d.z)<.9 else Vector((0,1,0))).normalized();w=d.cross(v)
 rings=[[p+r*(math.cos(i*math.tau/10)*v+math.sin(i*math.tau/10)*w) for i in range(10)] for p in [a,b]]
 for i in range(10):m.face([rings[0][i],rings[0][(i+1)%10],rings[1][(i+1)%10],rings[1][i]],mat)
 m.face(list(reversed(rings[0])),mat);m.face(rings[1],mat)
def line(m,pts,r=.02,mat='Brass'):
 for a,b in zip(pts,pts[1:]):tube(m,a,b,r,mat)
def ring(m,x,y,z,r,plane='front',thick=.018):
 line(m,[(x,y+r*math.cos(a),z+r*math.sin(a)) if plane=='front' else (x+r*math.cos(a),y+r*math.sin(a),z) for a in [i*math.tau/48 for i in range(49)]],thick)
def scroll(m,x,y,z,size,flip=1):
 line(m,[(x,y+flip*size*(1-t)*math.cos(t*math.tau*1.55),z+size*(1-t)*math.sin(t*math.tau*1.55)) for t in [i/64 for i in range(65)]],.015)
def build(crown):
 m=Mesh();m.box((0,0,-.04),(2.35,2.5,.08),'LiftEnamel');m.box((0,0,.005),(2.2,2.3,.03),'FloorLight')
 for y in [-1.12,1.12]:m.box((0,y,.025),(2.15,.025,.012),'Brass')
 for x in [-1.04,1.04]:m.box((x,0,.025),(.025,2.25,.012),'Brass')
 ring(m,0,0,.027,.52,'floor');ring(m,0,0,.027,.44,'floor',.009)
 # Solid decorative back, translucent side panels, open entrance.
 m.box((-1.1,0,1.45),(.12,2.3,2.9),'LiftEnamel')
 m.box((-1.027,0,1.85),(.025,1.75,1.65),'FloorLight')
 for y in [-1.13,1.13]:
  m.face([(-1.04,y,.45),(1.05,y,.45),(1.05,y,2.9),(-1.04,y,2.9)],'ConservatoryGlass')
  m.box((0,y,.22),(2.15,.065,.44),'LiftEnamel')
  for z in [.48,2.85]:tube(m,(-1.04,y,z),(1.04,y,z),.025)
  for x in [-.4,.4]:tube(m,(x,y,.48),(x,y,2.85),.018)
  tube(m,(-1.02,y*.92,1.05),(.94,y*.92,1.05),.032)
 for x in [-1.08,1.08]:
  for y in [-1.14,1.14]:
   m.box((x,y,.14),(.22,.24,.28),'Brass');tube(m,(x,y,.3),(x,y,2.92),.073,'LiftEnamel')
   for z in [.33,.43,2.55,2.66,2.89]:tube(m,(x,y,z),(x,y,z+.065),.10)
   for a in [i*math.tau/8 for i in range(8)]:tube(m,(x+.075*math.cos(a),y+.075*math.sin(a),.48),(x+.075*math.cos(a),y+.075*math.sin(a),2.53),.007)
 # Entrance surround leaves 1.58 m clear; keystone and arched transom.
 for y in [-.88,.88]:
  m.box((1.07,y,1.43),(.12,.12,2.86),'LiftEnamel');tube(m,(1.145,y,.10),(1.145,y,2.52),.018)
  for z in [.30,.72,2.63]:scroll(m,1.15,y,z,.14,1 if y<0 else -1)
 for z in [2.92,3.03,3.12]:m.box((0,0,z),(2.42,2.5,.075),'LiftEnamel' if z==3.03 else 'Brass')
 # Cornice boxes above are hollowed visually with a separate interior ceiling below.
 m.box((0,0,2.90),(2.12,2.2,.06),'LiftEnamel')
 line(m,[(1.15,.79*math.cos(t),2.43+.46*math.sin(t)) for t in [i*math.pi/40 for i in range(41)]],.027)
 ring(m,1.17,0,2.71,.16);ring(m,1.18,0,2.71,.135,thick=.007)
 for y in [-.52,.52]:scroll(m,1.16,y,2.73,.14,1 if y<0 else -1)
 for y in [-.89,.89]:tube(m,(-1.00,y,.28),(-1.00,y,2.7),.015)
 for z in [.28,.85,2.7]:tube(m,(-1.00,-.89,z),(-1.00,.89,z),.015)
 m.box((-.98,0,1.30),(.06,.25,.52),'Brass');m.box((-.94,0,1.30),(.035,.21,.48),'LiftEnamel')
 for z in [1.22,1.45]:ring(m,-.915,0,z,.045,thick=.008)
 m.box((-.902,0,1.45),(.008,.045,.045),'Lamp')
 m.tube((0,0,2.76),(0,0,2.85),.18,.18,'Brass',24);m.tube((0,0,2.71),(0,0,2.77),.14,.18,'Lamp',24)
 if crown:
  for j in range(8):
   a=j*math.tau/8
   line(m,[(1.10*math.cos(t)*math.cos(a),1.16*math.cos(t)*math.sin(a),3.17+.85*math.sin(t)) for t in [i*math.pi/40 for i in range(21)]],.026)
  for i in range(48):
   a=i*math.tau/48;b=(i+1)*math.tau/48
   for j in range(10):
    t=j*math.pi/20;v=(j+1)*math.pi/20
    m.face([(1.10*math.cos(p)*math.cos(q),1.16*math.cos(p)*math.sin(q),3.17+.85*math.sin(p)) for q,p in [(a,t),(b,t),(b,v),(a,v)]],'ConservatoryGlass')
  ring(m,1.00,0,3.43,.23)
  for y in [-.76,.76]:scroll(m,1.06,y,3.26,.18,1 if y<0 else -1)
  for x,y,h in [(0,0,4.02)]+[(x,y,3.15) for x in [-1.08,1.08] for y in [-1.14,1.14]]:
   m.tube((x,y,h),(x,y,h+.12),.11,.07,'Brass',16);m.tube((x,y,h+.12),(x,y,h+.3),.085,.004,'Brass',16)
 m.export('SM_OrnateLift_'+('Crowned' if crown else 'Bunker'))
build(True);build(False)
print('ORNATE_LIFT_EXPORTED',flush=True)
