"""Place reusable physical CIDCORE stations; rerunning replaces only our station folder."""
import unreal as u,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Scripts'))

MAP=re.search(r'GameDefaultMap=(.+)',(ROOT/'Config/DefaultEngine.ini').read_text()).group(1).strip()
BASE='/Game/Conservatory/Architecture/Intercom';FOLDER='09 CIDCORE Intercoms'
lib=u.EditorAssetLibrary;lib.make_directory(BASE);at=u.AssetToolsHelpers.get_asset_tools();mel=u.MaterialEditingLibrary

def mat(name,color,metal=0,emissive=False):
 path=BASE+'/M_'+name
 if lib.does_asset_exist(path):return lib.load_asset(path)
 m=at.create_asset('M_'+name,BASE,u.Material,u.MaterialFactoryNew())
 c=mel.create_material_expression(m,u.MaterialExpressionVectorParameter);c.set_editor_property('parameter_name','Color');c.set_editor_property('default_value',u.LinearColor(*color,1));mel.connect_material_property(c,'',u.MaterialProperty.MP_BASE_COLOR)
 if emissive:mel.connect_material_property(c,'',u.MaterialProperty.MP_EMISSIVE_COLOR)
 for value,prop in [(metal,u.MaterialProperty.MP_METALLIC),(.35,u.MaterialProperty.MP_ROUGHNESS)]:
  e=mel.create_material_expression(m,u.MaterialExpressionConstant);e.set_editor_property('r',value);mel.connect_material_property(e,'',prop)
 mel.recompile_material(m);lib.save_loaded_asset(m);return m
brass=mat('Brass',(.48,.30,.10),.8);enamel=mat('Enamel',(.025,.075,.07),.5);dark=mat('Speaker',(.009,.012,.012));lamp=mat('Transmit',(.006,.008,.008),0,True)
w=u.EditorLoadingAndSavingUtils.load_map(MAP);assert w
actors=u.get_editor_subsystem(u.EditorActorSubsystem)
for a in actors.get_all_level_actors():
 if str(a.get_folder_path())==FOLDER:actors.destroy_actor(a)
cls=u.load_class(None,'/Script/Conservatory.IntercomStation');assert cls
cube=lib.load_asset('/Engine/BasicShapes/Cube');stations=[]
def place(name,x,y,floor,yaw,stand=False):
 a=actors.spawn_actor_from_class(cls,u.Vector(x,y,floor+155),u.Rotator(pitch=0,yaw=yaw,roll=0));a.set_actor_label('CIDCORE - '+name);a.set_folder_path(FOLDER);a.set_editor_property('area_name',name)
 for c in a.get_components_by_class(u.StaticMeshComponent):
  n=c.get_name();m=brass if n in ['BrassHousing','ButtonBezel'] else lamp if n=='TransmitLamp' else dark if n.startswith('Speaker') else enamel;c.set_material(0,m)
 if stand:
  for label,z,size in [('Pedestal',floor+65,(12,12,130)),('Foot',floor+3,(38,38,6))]:
   b=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(x,y,z));b.set_actor_label('CIDCORE '+label+' - '+name);b.set_folder_path(FOLDER);c=b.static_mesh_component;c.set_static_mesh(cube);c.set_material(0,brass if label=='Foot' else enamel);b.set_actor_scale3d(u.Vector(*(v/100 for v in size)))
 stations.append(dict(area=name,position_cm=[x,y,floor+155],yaw=yaw,pedestal=stand))
for room in json.loads((ROOT/'Documentation/BunkerLayout.json').read_text())['rooms']:
 x,y,z=(v*100 for v in room['centre']);west=x<-14500
 place(room['name'],x+(582 if west else -582),y-200,z,180 if west else 0)
for name,x,y,z,yaw in [
 ('South dome',-11300,-1411,6243,0),('North dome',-11300,1641,6243,0),('Connecting passage',-10775,0,6243,0),
 ('Habitat corridor',-14770,700,4000,0),('Utilities corridor',-14770,700,3400,0),
 ('Habitat lift lobby',-15365,-2950,4000,0),('Utilities lobby',-15365,-2750,3400,0),
 ('Upper stair landing',-14965,2300,4000,0),('Lower stair landing',-14965,2300,3400,0)]:place(name,x,y,z,yaw,True)
assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
(ROOT/'Documentation/IntercomStations.json').write_text(json.dumps(dict(map=MAP,count=len(stations),stations=stations),indent=2))
print('CIDCORE_STATIONS_PLACED',len(stations),flush=True)

