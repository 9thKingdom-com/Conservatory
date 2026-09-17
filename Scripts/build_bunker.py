"""Idempotent bunker pass over the library exterior. Dimensions in metres."""
import unreal as u, math, random, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAP='/Game/Conservatory/Maps/L_Exterior_Modular'
world=u.EditorLoadingAndSavingUtils.load_map(MAP); assert world
actors=u.get_editor_subsystem(u.EditorActorSubsystem)
for a in actors.get_all_level_actors():
 if str(a.get_folder_path()).startswith('08 Bunker'): actors.destroy_actor(a)
lib=u.EditorAssetLibrary; mel=u.MaterialEditingLibrary; at=u.AssetToolsHelpers.get_asset_tools()
folder='/Game/Conservatory/Bunker/Materials'; lib.make_directory(folder)
def material(name,color,metal=0,emission=0):
 path=folder+'/M_'+name
 if lib.does_asset_exist(path): return lib.load_asset(path)
 m=at.create_asset('M_'+name,folder,u.Material,u.MaterialFactoryNew())
 c=mel.create_material_expression(m,u.MaterialExpressionConstant3Vector); c.constant=u.LinearColor(*color,1)
 mel.connect_material_property(c,'',u.MaterialProperty.MP_BASE_COLOR)
 for val,prop in [(.48,u.MaterialProperty.MP_ROUGHNESS),(metal,u.MaterialProperty.MP_METALLIC)]:
  e=mel.create_material_expression(m,u.MaterialExpressionConstant); e.r=val; mel.connect_material_property(e,'',prop)
 if emission:
  e=mel.create_material_expression(m,u.MaterialExpressionMultiply); e.set_editor_property('const_b',emission); mel.connect_material_expressions(c,'',e,'A'); mel.connect_material_property(e,'',u.MaterialProperty.MP_EMISSIVE_COLOR)
 mel.recompile_material(m); lib.save_loaded_asset(m); return m
M={n:material(n,c,metal,em) for n,c,metal,em in [
 ('Concrete',(.28,.31,.30),0,0),('Wall',(.64,.66,.59),0,0),('Floor',(.13,.18,.18),.15,0),
 ('Teal',(.035,.22,.22),.3,0),('Steel',(.32,.40,.41),.75,0),('Dark',(.035,.055,.06),.4,0),
 ('Amber',(.75,.35,.055),.25,0),('Wood',(.25,.12,.055),0,0),('Linen',(.48,.52,.40),0,0),
 ('Blue',(.08,.24,.42),.3,0),('Red',(.40,.09,.055),.2,0),('White',(.78,.84,.79),0,0),
 ('Lamp',(.70,.88,.80),0,5),('WarmLamp',(1,.64,.28),0,4),('Green',(.04,.43,.20),0,2)]}
meshes={n:lib.load_asset('/Engine/BasicShapes/'+n) for n in ['Cube','Cylinder','Sphere']}
current='Structure'
def shape(name,pos,size,mat='Wall',mesh='Cube',yaw=0,rot=None,collision=True):
 a=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(*[v*100 for v in pos]),rot or u.Rotator(pitch=0,yaw=yaw,roll=0))
 a.set_actor_label(name); a.set_folder_path('08 Bunker/'+current)
 a.static_mesh_component.set_static_mesh(meshes[mesh]); a.static_mesh_component.set_material(0,M[mat])
 a.static_mesh_component.set_collision_profile_name('BlockAll' if collision else 'NoCollision')
 a.set_actor_scale3d(u.Vector(*size)); return a
def box(n,x,y,z,sx,sy,sz,mat='Wall',**kw): return shape(n,(x,y,z),(sx,sy,sz),mat,**kw)
def cyl(n,x,y,z,r,h,mat='Steel',**kw): return shape(n,(x,y,z),(r*2,r*2,h),mat,'Cylinder',**kw)
def pipe(n,a,b,r=.045,mat='Steel'):
 d=u.Vector(*[(b[i]-a[i])*100 for i in range(3)]); rot=u.MathLibrary.make_rot_from_z(d)
 return shape(n,tuple((a[i]+b[i])/2 for i in range(3)),(r*2,r*2,d.length()/100),mat,'Cylinder',rot=rot,collision=False)
def text(s,x,y,z,yaw=0,size=.18,color=(210,225,210)):
 a=actors.spawn_actor_from_class(u.TextRenderActor,u.Vector(x*100,y*100,z*100),u.Rotator(pitch=0,yaw=yaw,roll=0))
 a.set_actor_label(s.replace('\n',' / ')); a.set_folder_path('08 Bunker/'+current)
 c=a.get_component_by_class(u.TextRenderComponent); c.set_text(s); c.set_world_size(size*100); c.set_text_render_color(u.Color(*color,255)); return a
def light(x,y,z,warm=False,power=1600,radius=10):
 a=actors.spawn_actor_from_class(u.PointLight,u.Vector(x*100,y*100,z*100)); a.set_actor_label('Warm reading light' if warm else 'Ceiling light'); a.set_folder_path('08 Bunker/'+current)
 c=a.point_light_component; c.set_editor_property('intensity_units',u.LightUnits.LUMENS); c.set_intensity(power*.22); c.set_light_color(u.LinearColor(1,.78,.50,1) if warm else u.LinearColor(.78,.91,1,1)); c.set_attenuation_radius(radius*100); c.set_cast_shadows(True); c.set_editor_property('source_radius',18)
 box('Recessed light',x,y,z+.18,1.5,.3,.08,'WarmLamp' if warm else 'Lamp',collision=False)
def table(x,y,z,mat='Steel',length=2):
 box('Work surface',x,y,z+.9,length,.9,.12,mat)
 for dx in [-length/2+.12,length/2-.12]:
  for dy in [-.32,.32]: box('Table leg',x+dx,y+dy,z+.43,.07,.07,.86,'Dark')
def cabinet(x,y,z,seed=False):
 box('Seed archive cabinet' if seed else 'Storage cabinet',x,y,z+1.1,1.1,.55,2.2,'Teal' if seed else 'Steel')
 for k in range(8 if seed else 4):
  dz=.22+k*.25 if seed else .3+k*.5
  box('Archive drawer',x,y-.292,z+dz,.99,.035,.21 if seed else .44,'Wall')
  box('Drawer handle',x,y-.33,z+dz,.24,.065,.025,'Dark',collision=False)
  if seed: box('Seed catalogue label',x+.32,y-.316,z+dz,.17,.01,.07,'Amber',collision=False)
def shelf(x,y,z,books=False):
 for dx in [-1,1]: box('Shelf upright',x+dx,y,z+1.2,.075,.5,2.4,'Wood' if books else 'Steel')
 for h in [.15,.72,1.29,1.86,2.4]:
  box('Shelf',x,y,z+h,2.1,.6,.06,'Wood' if books else 'Steel')
  if h>2: continue
  for k in range(8 if books else 3):
   if books:
    hh=.25+random.random()*.18
    box('Reference volume',x-.88+k*.24,y,z+h+hh/2+.04,.16,.34,hh,random.choice(['Teal','Amber','Linen','Red','Blue']))
   else:
    box('Sealed food crate',x-.68+k*.68,y,z+h+.22,.56,.44,.36,'Linen')
    box('Inventory label',x-.68+k*.68,y-.227,z+h+.23,.25,.015,.12,'White',collision=False)
def tank(x,y,z,r=.8,h=2.7,mat='Blue',name='Water tank'):
 cyl(name,x,y,z+h/2+.18,r,h,mat)
 for dz in [.35,h-.1]: cyl('Tank reinforcing band',x,y,z+dz,r+.035,.07,'Steel')
 cyl('Tank cap',x,y,z+h+.2,r*.8,.09,'Steel')
 for dx in [-r*.6,r*.6]: box('Tank foot',x+dx,y,z+.12,.15,.6,.24,'Dark')
 pipe('Tank outlet',(x,y-r,z+.55),(x,y-r-.5,z+.55),.07)
 cyl('Pressure dial',x,y-r-.08,z+h-.5,.13,.08,'White',rot=u.Rotator(pitch=0,yaw=0,roll=90),collision=False)
 box('Pressure indicator',x,y-r-.14,z+h-.5,.012,.015,.15,'Dark',yaw=25,collision=False)
def monitor(x,y,z):
 box('Monitor stem',x,y,z-.25,.07,.07,.22,'Steel',collision=False)
 box('Monitor base',x,y,z-.35,.4,.23,.025,'Dark',collision=False)
 box('Display chassis',x,y,z, .65,.1,.42,'Dark'); box('Status display',x,y-.06,z,.57,.012,.34,'Teal',collision=False)
 for k in range(3): box('Status bar',x-.1,y-.071,z-.09+k*.08,.29,.005,.015,'Green',collision=False)
def room(x,y,z,title,index):
 global current
 current=('01 Habitat/' if z==40 else '02 Utilities/')+title
 box(title+' floor',x,y,z-.15,12,14,.3,'Floor')
 box('Acoustic ceiling',x,y,z+3.65,12,14,.25,'Concrete')
 for yy in [y-7,y+7]: box('Room partition',x,yy,z+1.8,12,.2,3.6)
 outer=x-6 if x<-145 else x+6; inner=x+6 if x<-145 else x-6
 box('Earth retaining wall',outer,y,z+1.8,.35,14,3.6,'Concrete')
 for dy in [-4.15,4.15]: box('Door wall',inner,y+dy,z+1.8,.2,5.7,3.6)
 box('Door lintel',inner,y,z+3.15,.2,2.6,.9)
 for yy in [y-1.35,y+1.35]: box('Door jamb',inner,yy,z+1.35,.3,.12,2.7,'Teal')
 box('Threshold',inner,y,z+.015,.45,2.6,.03,'Amber')
 # Corridor-facing room names, with colour stripe continuing around rooms.
 facing=0 if x<-145 else 180
 box('Room name plaque',inner+(.13 if x<-145 else -.13),y,z+2.99,.05,2.75,.42,'Dark',collision=False)
 text(f'{index:02d}  {title.upper()}',inner+(.16 if x<-145 else -.16),y+(1.12 if x<-145 else -1.12),z+2.88,facing,.15)
 for yy in [y-6.87,y+6.87]: box('Room colour band',x,yy,z+1.12,11.7,.035,.10,'Teal' if z==40 else 'Amber',collision=False)
 for dx in [-3,3]: light(x+dx,y,z+3.22,title in ['Library & study','Sleeping quarters'],1800)

random.seed(5808)
# Two floors, linked by an open stairwell at the north end.
for z in [40,34]:
 current='Structure'
 box('Central circulation floor',-145,-3,z-.15,6,46,.3,'Floor')
 if z==40: box('Central circulation ceiling',-145,-3,z+3.65,6,46,.25,'Concrete')
 box('Lift lobby floor',-145,-27,z-.15,18,8,.3,'Floor')
 box('Lift lobby ceiling',-145,-27,z+3.65,18,8,.25,'Concrete')
 for x in [-154,-136]: box('Lobby wall',x,-27,z+1.8,.3,8,3.6)
 box('Lobby end wall',-145,-31,z+1.8,18,.3,3.6,'Concrete')
 for y in [-24,-12,0,12,21]:
  light(-145,y,z+3.15,False,1200,9)
  if y<20: box('Floor guidance line',-145,y,z+.018,.07,6,.02,'Amber',collision=False)
 for x in [-147.75,-142.25]:
  pipe('Overhead service main',(x,-25,z+3.18),(x,20,z+3.18),.065,'Teal')
 current='03 Spiral stair'
 if z==34: box('Stairwell foundation',-145,25,z-.2,10,10,.4,'Floor')
 else:
  for x in [-149.25,-140.75]: box('Upper stair gallery',x,25,z-.15,1.5,10,.3,'Floor')
  for y in [20.75,29.25]: box('Upper stair gallery',-145,y,z-.15,7,1.5,.3,'Floor')
for x in [-150,-140]: box('Stairwell retaining wall',x,25,38.8,.35,10,9.8,'Concrete')
box('Stairwell rear wall',-145,30,38.8,10,.35,9.8,'Concrete')
box('Stairwell roof',-145,25,43.65,10,10,.3,'Concrete')
light(-145,25,43.1,True,3200,15); light(-145,25,37.2,False,1900,10)
cyl('Spiral structural core',-145,25,37.3,.35,6.6,'Teal')
# 48 treads, 12.5 cm rise, 540-degree turn: 4 m headroom per revolution.
for i in range(49):
 a=math.radians(i*11.25); z=40-i*.125; x=-145+2.18*math.cos(a); y=25+2.18*math.sin(a)
 box('Spiral tread %02d'%i,x,y,z-.065,2.65,.87,.13,'Steel',yaw=i*11.25)
 box('Anti-slip nosing',x,y,z+.006,2.6,.045,.012,'Amber',yaw=i*11.25,collision=False)
 ox=-145+3.42*math.cos(a); oy=25+3.42*math.sin(a)
 cyl('Spiral guardrail post',ox,oy,z+.52,.024,1.04,'Teal')
 if i:
  pipe('Continuous spiral handrail',previous,(ox,oy,z+1.04),.035,'Teal')
 previous=(ox,oy,z+1.04)
# Flush landing joins the first tread directly to the corridor gallery.
box('Stair to corridor landing',-142.82,23.04,39.85,2.66,3.08,.3,'Floor')
box('Landing guidance line',-142.82,23.0,40.018,.07,3,.02,'Amber',collision=False)
pipe('Landing inner guard',(-144.15,21.5,41.05),(-144.15,24.57,41.05),.035,'Teal')
for y in [21.5,23,24.57]: cyl('Landing guard post',-144.15,y,40.52,.025,1.04,'Teal')
# The south guard ends at the landing entrance instead of blocking the route.
for y in [21.5,28.5]:
 end=-144.15 if y==21.5 else -141.5
 pipe('Stair opening guard',(-148.5,y,41.05),(end,y,41.05),.035,'Teal')
 for x in [-148.5,-146,-143.5,-141.5]:
  if x<=end: cyl('Gallery post',x,y,40.52,.025,1.04,'Teal')
pipe('Stair opening west guard',(-148.5,21.5,41.05),(-148.5,28.5,41.05),.035,'Teal')
text('LOWER DECK\nWATER / AIR / ENERGY',-149.79,26.6,42,0,.22)

names=['Seed laboratory','Library & study','Sleeping quarters','Food reserve','Clinic','Kitchen & washrooms',
       'Water & pumping','Air & oxygen','Power reserve','Workshop','Waste treatment','Equipment stores']
rooms=[]
for index,title in enumerate(names):
 z=40 if index<6 else 34; local=index%6; x=-154 if local%2==0 else -136; y=-15+(local//2)*15
 room(x,y,z,title,index+1); rooms.append(dict(name=title,centre=[x,y,z],size=[12,14,3.6]))
 if title=='Seed laboratory':
  for dx in [-4.5,-3.1,-1.7,-.3,1.1,2.5,3.9]: cabinet(x+dx,y+5.8,z,True)
  text('SEED BANK  /  A - G',x-4.8,y+5.48,z+2.7,-90,.22)
  for dx in [-3,1.2]:
   table(x+dx,y,z,length=2.8)
   for k in range(4):
    box('Seed sample tray',x+dx-.9+k*.58,y,z+1,.45,.5,.08,'Dark')
    for t in range(3): cyl('Sample vial',x+dx-1+k*.58+t*.10,y,z+1.12,.035,.18,'Linen',collision=False)
   monitor(x+dx,y+.27,z+1.28)
  cabinet(x-4.7,y-5,z); cabinet(x-3.3,y-5,z)
 elif title=='Library & study':
  for dx in [-4,-1.5,1,3.5]: shelf(x+dx,y+5.8,z,True)
  for yy in [-2,2]:
   table(x,y+yy,z,'Wood',3.2)
   for dx in [-.9,.9]:
    box('Reading chair',x+dx,y+yy-1,z+.45,.65,.65,.12,'Linen'); box('Chair back',x+dx,y+yy-1.3,z+.85,.65,.1,.8,'Wood')
    for lx in [-.25,.25]:
     for ly in [-.25,.25]: box('Chair leg',x+dx+lx,y+yy-1+ly,z+.21,.05,.05,.42,'Wood')
    box('Open field journal',x+dx,y+yy,z+.985,.45,.34,.03,'Linen',collision=False)
 elif title=='Sleeping quarters':
  for dx in [-3.5,.7]:
   for yy in [-3,2.5]:
    for h in [.45,1.9]:
     box('Bunk frame',x+dx,y+yy,z+h,2.1,1,.12,'Teal'); box('Mattress',x+dx,y+yy,z+h+.15,2,.9,.23,'Linen')
     box('Pillow',x+dx-.72,y+yy,z+h+.29,.42,.72,.14,'White')
    for dd in [-1,1]: box('Bunk upright',x+dx+dd,y+yy+.46,z+1.3,.06,.06,2.6,'Steel')
    cabinet(x+dx+1.4,y+yy,z)
 elif title=='Food reserve' or title=='Equipment stores':
  for dx in [-3.5,0,3.5]:
   for yy in [-3,2.5]: shelf(x+dx,y+yy,z)
  text('SEALED / ROTATE STOCK',x-4.4,y+6.8,z+2.5,-90,.2)
 elif title=='Clinic':
  for yy in [-2.5,2.5]:
   table(x-1,y+yy,z,length=2.2); box('Examination mattress',x-1,y+yy,z+1.04,2.1,.85,.16,'Linen')
   monitor(x-2.7,y+yy,z+1.5); cabinet(x+3.6,y+yy,z)
   box('Bedside monitor pedestal',x-2.7,y+yy,z+.56,.45,.4,1.12,'Steel')
  box('First aid cabinet',x,y+6.6,z+1.6,1.3,.35,1,'White')
  box('Medical cross',x,y+6.40,z+1.6,.18,.02,.6,'Red',collision=False); box('Medical cross',x,y+6.38,z+1.6,.6,.02,.18,'Red',collision=False)
 elif title=='Kitchen & washrooms':
  for dx in [-4,-2,0]: cabinet(x+dx,y+5.8,z); table(x+dx,y+4.8,z,length=1.8)
  for dx in [-2,0]: cyl('Induction hob',x+dx,y+4.8,z+.97,.25,.03,'Dark',collision=False)
  table(x-2,y-2,z,'Wood',3)
  for yy in [-4,0,4]:
   box('Washroom privacy partition',x+3,y+yy-1.5,z+1.3,5,.12,2.6)
   box('Sanitary basin',x+4.4,y+yy,z+.83,.65,.5,.15,'White'); pipe('Tap',(x+4.4,y+yy+.15,z+.95),(x+4.4,y+yy+.15,z+1.18),.025)
   cyl('Sanitation fixture',x+3.1,y+yy,z+.27,.3,.45,'White')
 elif title=='Water & pumping':
  for dx in [-3,0,3]: tank(x+dx,y+3.7,z,1.15,2.7,'Blue','Potable water reservoir')
  pipe('Water header',(x-4,y+2.05,z+.5),(x+4,y+2.05,z+.5),.11,'Blue')
  for dx in [-2,2]:
   box('Pump plinth',x+dx,y-2,z+.15,1.8,1.1,.3,'Concrete')
   cyl('Pump motor',x+dx,y-2,z+.65,.35,1.1,'Teal',rot=u.Rotator(pitch=90,yaw=0,roll=0))
   pipe('Pump riser',(x+dx,y-2,z+.7),(x+dx,y-2,z+2.5),.08,'Blue')
   monitor(x+dx,y-2,z+2.4)
 elif title=='Air & oxygen':
  for dx in [-4,-2.5,-1,.5,2,3.5]: tank(x+dx,y+4.8,z,.38,2.1,'White','Oxygen cylinder')
  for dx in [-3,2]:
   box('Air scrubber cabinet',x+dx,y-1,z+1.35,2.2,1.2,2.7,'Teal')
   for h in range(8): box('Filter grille',x+dx,y-1.62,z+.5+h*.22,1.8,.035,.045,'Dark',collision=False)
   pipe('Filtered air duct',(x+dx,y-1,z+2.7),(x+dx,y-1,z+3.2),.24)
  text('O2  /  PRESSURE INSPECTION',x-4.5,y+4.34,z+2.75,-90,.2)
 elif title=='Power reserve':
  for dx in [-4,-2,0,2,4]:
   cabinet(x+dx,y+4,z)
   for h in [.4,.85,1.3,1.75]: box('Battery module',x+dx,y+3.68,z+h,.85,.09,.32,'Dark'); box('Charge indicator',x+dx+.3,y+3.62,z+h,.05,.025,.07,'Green',collision=False)
  for dx in [-2,2]: box('Inverter cabinet',x+dx,y-2,z+1.2,1.4,1,2.4,'Teal'); monitor(x+dx,y-2.52,z+1.8)
 elif title=='Workshop':
  for yy in [-3,3]:
   table(x,y+yy,z,'Wood',5)
   for k in range(7): box('Tool rack',x-2+k*.6,y+yy+.34,z+1.2,.12,.12,.45,'Steel',yaw=k*10,collision=False)
  for dx in [-4,-2.5,3.5]: cabinet(x+dx,y+5.8,z)
 elif title=='Waste treatment':
  for dx in [-3,1]: tank(x+dx,y+3,z,1,2.5,'Teal','Sealed treatment vessel')
  for dx in [-3,0,3]:
   cyl('Segregated sealed waste bin',x+dx,y-3,z+.65,.55,1.2,'Dark'); cyl('Sealed waste lid',x+dx,y-3,z+1.29,.58,.1,'Amber')
  pipe('Greywater return',(x-4,y+1.5,z+2.6),(x+4,y+1.5,z+2.6),.09,'Teal')
  text('GREYWATER / SEALED WASTE',x-4.4,y+6.75,z+2.6,-90,.2)

current='04 Service lift'
# Compact open-front cabins. Fade transfer avoids an unexcavated landscape shaft.
def cabin(x,y,z,label):
 box('Service lift floor',x,y,z-.06,3,3,.12,'Steel')
 box('Service lift rear',x-1.5,y,z+1.4,.15,3,2.8,'Teal')
 for yy in [y-1.5,y+1.5]: box('Service lift side',x,yy,z+1.4,3,.15,2.8,'Steel')
 box('Service lift roof',x,y,z+2.85,3,3,.15,'Dark')
 text('SERVICE LIFT\n[E]  '+label,x-1.40,y+.95,z+2.05,0,.17)
 box('Lift call panel',x-1.38,y,z+1.15,.08,.35,.55,'Dark'); box('Lift ready indicator',x-1.32,y,z+1.3,.02,.12,.08,'Green',collision=False)
 light(x,y,z+2.55,False,700,4)
 return (x*100,y*100,z*100+90)
top=cabin(-110,-4,62.46,'HABITAT DECK')
bottom=cabin(-150,-27,40,'CONSERVATORY')
liftclass=u.load_class(None,'/Script/Habitat.ServiceLift'); assert liftclass
for origin,dest,label in [(top,bottom,'Habitat deck'),(bottom,top,'Conservatory')]:
 a=actors.spawn_actor_from_class(liftclass,u.Vector(*origin)); a.set_actor_label('Service lift to '+label); a.set_folder_path('08 Bunker/04 Service lift')
 a.set_editor_property('destination',u.Vector(*dest)); a.set_editor_property('destination_yaw',0); a.set_editor_property('destination_name',label)
current='05 Wayfinding'
text('HABITAT  /  DECK 01\nSEED BANK  -  STUDY  -  REST\nNORTH: STAIRS TO UTILITIES',-145,-30.78,42.7,90,.26)
text('UTILITIES  /  DECK 02\nWATER  -  AIR  -  POWER\nKEEP ALL SERVICE AISLES CLEAR',-145,-30.78,36.7,90,.25)
import sys
sys.path.insert(0,str(ROOT/'Scripts'))
from seal_bunker_joints import seal
seal(world)
assert u.EditorLoadingAndSavingUtils.save_map(world,MAP)
(ROOT/'Documentation'/'BunkerLayout.json').write_text(json.dumps({'rooms':rooms,'main_floor_m':40,'utilities_floor_m':34,'spiral':{'treads':49,'rise_cm':12.5,'turn_degrees':540,'headroom_per_turn_m':4},'lift_top_cm':top,'lift_bottom_cm':bottom,'simulation':'Architectural equipment only; no resource consumption or inventory'},indent=2))
print('BUNKER_BUILD_COMPLETE',flush=True)





