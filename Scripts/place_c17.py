"""Add outdoor robot preview and a single future operations workstation."""
import unreal as u,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];cfg=ROOT/'Config/DefaultEngine.ini';old=re.search(r'GameDefaultMap=(.+)',cfg.read_text()).group(1).strip();target='/Game/Conservatory/Maps/L_Exterior_C17'
w=u.EditorLoadingAndSavingUtils.load_map(old);actors=u.get_editor_subsystem(u.EditorActorSubsystem);lib=u.EditorAssetLibrary;folder='10 C17 Field Units'
for a in actors.get_all_level_actors():
 if str(a.get_folder_path())==folder:actors.destroy_actor(a)
cls=u.load_class(None,'/Script/Conservatory.C17Robot');assert cls
robots=[]
for label,x,y,offset in [('C-17 East patrol',-9280,-2100,1100),('C-17 West patrol',-11930,700,700)]:
 a=actors.spawn_actor_from_class(cls,u.Vector(x,y,6320),u.Rotator(pitch=0,yaw=90,roll=0));a.set_actor_label(label);a.set_folder_path(folder);a.set_editor_property('patrol_offset',u.Vector(0,offset,0));robots.append({'label':label,'position_cm':[x,y,6320],'patrol_offset_cm':[0,offset,0]})
# Keep the northern toilet/basin and its privacy partition. Remove only two surplus cubicles.
removed=[]
for a in actors.get_all_level_actors():
 label=a.get_actor_label();p=a.get_actor_location()
 if not str(a.get_folder_path()).startswith('08 Bunker'):continue
 if -13550<p.x<-13000 and 800<p.y<1700 and 3990<p.z<4300 and any(label.startswith(n) for n in ['Washroom privacy partition','Sanitary basin','Sanitation fixture','Tap']):removed.append(label);actors.destroy_actor(a)
mesh=lib.load_asset('/Engine/BasicShapes/Cube');mats={n:lib.load_asset('/Game/Conservatory/Robots/C17/M_C17_'+n) for n in ['Graphite','Steel','Ivory','Amber']}
def box(name,pos,size,mat):
 a=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(*pos));a.set_actor_label('Operations desk - '+name);a.set_folder_path(folder);a.static_mesh_component.set_static_mesh(mesh);a.static_mesh_component.set_material(0,mats[mat]);a.set_actor_scale3d(u.Vector(*(v/100 for v in size)));return a
x=-13210;y=1150;z=4000
box('worktop',(x,y,z+78),(80,155,6),'Steel')
for dx in [-30,30]:
 for dy in [-65,65]:box('leg',(x+dx,y+dy,z+37),(5,5,74),'Graphite')
box('computer tower',(x+12,y+55,z+34),(40,22,65),'Graphite')
for zz in range(20,48,5):box('tower vent',(x-9,y+55,z+zz),(1,16,1),'Steel')
box('monitor foot',(x+10,y,z+83),(27,35,4),'Graphite');box('monitor neck',(x+15,y,z+104),(6,7,40),'Steel')
box('monitor frame',(x+15,y,z+125),(7,73,48),'Graphite');box('monitor screen',(x+10.8,y,z+125),(1,67,42),'Graphite')
box('keyboard',(x-24,y,z+83),(22,49,3),'Graphite')
for row in range(4):
 for col in range(12):box('key',(x-31+row*4.5,y-22+col*3.8,z+85),(3.2,2.8,1),'Ivory')
box('mouse',(x-22,y-36,z+84),(10,6,4),'Graphite')
box('chair seat',(x-105,y,z+46),(46,48,7),'Graphite');box('chair back',(x-126,y,z+73),(6,48,54),'Graphite')
for dx in [-17,17]:
 for dy in [-18,18]:box('chair leg',(x-105+dx,y+dy,z+22),(4,4,44),'Steel')
a=actors.spawn_actor_from_class(u.TextRenderActor,u.Vector(x+10,y,z+127),u.Rotator(pitch=0,yaw=180,roll=0));a.set_actor_label('C17 workstation screen');a.set_folder_path(folder);c=a.get_component_by_class(u.TextRenderComponent);c.set_text('FIELD OPERATIONS\n\nC-17\n\nSTANDBY');c.set_world_size(4.2);c.set_horizontal_alignment(u.HorizTextAligment.EHTA_CENTER);c.set_vertical_alignment(u.VerticalTextAligment.EVRTA_TEXT_CENTER);c.set_text_render_color(u.Color(200,225,190,255))
assert u.EditorLoadingAndSavingUtils.save_map(w,target);cfg.write_text(cfg.read_text().replace(old,target))
# Keep intercom inspection pointed at the live level, without changing its placements.
p=ROOT/'Documentation/IntercomStations.json';d=json.loads(p.read_text());d['map']=target;p.write_text(json.dumps(d,indent=2))
(ROOT/'Documentation/C17/Placement.json').write_text(json.dumps({'map':target,'robots':robots,'workstation_cm':[x,y,z],'removed_surplus_fixtures':removed,'terminal_scope':'Single physical workstation reserved for future remote control; no resource collection gameplay yet'},indent=2))

