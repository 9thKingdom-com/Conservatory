"""Original dome/corridor kit inspired by Reference images/conservatory-design1.png.
Run with Blender --background --python Scripts/make_conservatory.py.
"""
import sys, math
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Scripts'))
import make_assets as env
env.OUT=ROOT/'SourceAssets'/'Conservatory'; env.OUT.mkdir(parents=True,exist_ok=True)
for n in ['IvoryFrame','Brass','ConservatoryGlass','FloorLight','FloorDark']:
 env.MATS.append(n); env.materials[n]=bpy.data.materials.new(n)
Mesh=env.Mesh
def pipe(m,a,b,r=.055,mat='IvoryFrame',n=8): m.tube(a,b,r,r,mat,n)
def arc(m,pts,r=.045,mat='IvoryFrame'):
 for a,b in zip(pts,pts[1:]): pipe(m,a,b,r,mat)
def column(m,x,y,h=5.2):
 m.box((x,y,.22),(.40,.40,.44),'FloorLight')
 m.tube((x,y,.42),(x,y,h-.3),.095,.078,'IvoryFrame',12)
 for z,r in [(.5,.15),(.64,.12),(h-.34,.13),(h-.2,.19)]: m.tube((x,y,z),(x,y,z+.12),r,r,'Brass',12)
def sphere(m,c,r,mat):
 x,y,z=c
 for j in range(8):
  p0=-math.pi/2+j*math.pi/8; p1=p0+math.pi/8
  for k in range(12):
   a=k*math.tau/12; b=a+math.tau/12
   m.face([(x+r*math.cos(p)*math.cos(t),y+r*math.cos(p)*math.sin(t),z+r*math.sin(p)) for p,t in [(p0,a),(p0,b),(p1,b),(p1,a)]],mat)
def tiled_floor(m,inside):
 for x in range(-8,9):
  for y in range(-8,9):
   if inside(x+.5,y+.5): m.box((x+.5,y+.5,.26),(.985,.985,.05),'FloorLight' if (x+y)%2 else 'FloorDark')

m=Mesh(); R=7; H=5.2; D=6.2; N=40
# Continuous stone disk with tile inset. Corridor portal faces local -X.
m.tube((0,0,-.12),(0,0,.22),7.2,7.2,'FloorLight',80)
tiled_floor(m,lambda x,y:x*x+y*y<6.9**2)
angles=[(i+.5)*math.tau/N for i in range(N+1)]
for i,a in enumerate(angles[:-1]):
 x,y=R*math.cos(a),R*math.sin(a)
 portal=math.cos(a)<-.82
 door=math.cos(a)>.975
 if not portal and not door: column(m,x,y,H)
 b=angles[i+1]; mid=(a+b)/2
 corridor=math.cos(mid)<-.82; entrance=math.cos(mid)>.965
 if not corridor:
  lo=3.0 if entrance else .52
  m.face([(R*math.cos(a),R*math.sin(a),lo),(R*math.cos(b),R*math.sin(b),lo),(R*math.cos(b),R*math.sin(b),H),(R*math.cos(a),R*math.sin(a),H)],'ConservatoryGlass')
  if not entrance:
   m.face([(R*math.cos(a),R*math.sin(a),.24),(R*math.cos(b),R*math.sin(b),.24),(R*math.cos(b),R*math.sin(b),.5),(R*math.cos(a),R*math.sin(a),.5)],'FloorLight')
   pipe(m,(x,y,2.8),(R*math.cos(b),R*math.sin(b),2.8),.032)
 for j in range(12):
  t0=j*math.pi/24; t1=(j+1)*math.pi/24
  def v(ang,t): return (R*math.cos(t)*math.cos(ang),R*math.cos(t)*math.sin(ang),H+D*math.sin(t))
  m.face([v(a,t0),v(b,t0),v(b,t1),v(a,t1)],'ConservatoryGlass')
 arc(m,[(R*math.cos(t)*math.cos(a),R*math.cos(t)*math.sin(a),H+D*math.sin(t)) for t in [j*math.pi/40 for j in range(21)]],.043)
for z,r in [(H-.15,R+.10),(H+.06,R+.06)]:
 arc(m,[(r*math.cos(a),r*math.sin(a),z) for a in [j*math.tau/120 for j in range(121)]],.095)
for j in [2,4,6,8,10]:
 t=j*math.pi/24; r=R*math.cos(t); z=H+D*math.sin(t)
 arc(m,[(r*math.cos(a),r*math.sin(a),z) for a in [j*math.tau/100 for j in range(101)]],.03,'Brass')
# Lantern crown and finial.
m.tube((0,0,H+D-.12),(0,0,H+D+.20),.65,.55,'IvoryFrame',24)
m.tube((0,0,H+D+.2),(0,0,H+D+.9),.25,.08,'Brass',16)
sphere(m,(0,0,H+D+1),.18,'Brass'); pipe(m,(0,0,H+D+1),(0,0,H+D+1.6),.032,'Brass')
# Portal jambs, threshold and entrance arch; doors intentionally open for inspection.
for s in [-1,1]:
 column(m,-5.744,s*4,H)
 column(m,6.84,s*1.42,3.1)
arc(m,[(6.84,1.42*math.cos(t),3.05+1.15*math.sin(t)) for t in [i*math.pi/20 for i in range(21)]],.075,'Brass')
m.box((7.65,0,.065),(1.25,3.4,.13),'FloorLight')
m.box((7.15,0,.16),(.50,3.1,.2),'FloorLight')
# Narrow perimeter benches leave the centre and both portals unobstructed.
for sign in [-1,1]:
 m.box((0,sign*5.75,.75),(3.7,.6,.16),'Timber')
 for x in [-1.45,1.45]: m.box((x,sign*5.75,.46),(.13,.48,.48),'IvoryFrame')
m.export('SM_Conservatory_Dome')

m=Mesh(); L=18; W=8; H=5.2
m.box((0,0,.06),(L,W+.4,.32),'FloorLight')
for x in range(-9,9):
 for y in range(-4,4): m.box((x+.5,y+.5,.26),(.985,.985,.05),'FloorLight' if (x+y)%2 else 'FloorDark')
for x in range(-9,10,2):
 for side in [-1,1]: column(m,x,side*4,H)
 arc(m,[(x,4*math.cos(t),H+4*math.sin(t)) for t in [j*math.pi/32 for j in range(33)]],.065)
for j in range(17):
 t=j*math.pi/16; y,z=4*math.cos(t),H+4*math.sin(t)
 pipe(m,(-9,y,z),(9,y,z),.032,'Brass')
for x in range(-9,9,2):
 for side in [-1,1]:
  y=side*4
  m.face([(x,y,.5),(x+2,y,.5),(x+2,y,H),(x,y,H)],'ConservatoryGlass')
  m.box((x+1,y,.36),(2,.15,.22),'FloorLight')
  pipe(m,(x,y,2.8),(x+2,y,2.8),.035)
  # Gothic-inspired small decorative arch within each bay.
  arc(m,[(x+1+math.cos(t)*.88,y,3.9+math.sin(t)*1.05) for t in [i*math.pi/20 for i in range(21)]],.028,'Brass')
 for j in range(16):
  a=j*math.pi/16; b=a+math.pi/16
  m.face([(x,4*math.cos(a),H+4*math.sin(a)),(x+2,4*math.cos(a),H+4*math.sin(a)),(x+2,4*math.cos(b),H+4*math.sin(b)),(x,4*math.cos(b),H+4*math.sin(b))],'ConservatoryGlass')
for y in [-4,4]:
 pipe(m,(-9,y,H),(9,y,H),.1)
 pipe(m,(-9,y,H+.14),(9,y,H+.14),.05,'Brass')
m.export('SM_Conservatory_Corridor')
print('CONSERVATORY_KIT_COMPLETE',flush=True)
