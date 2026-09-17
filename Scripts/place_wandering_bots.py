"""Replace preview units in a new map; retain workstation references and source map."""
import unreal as u, json, re
from pathlib import Path
ROOT=Path(u.Paths.project_dir())
cfg=ROOT/'Config/DefaultEngine.ini'
old=re.search(r'GameDefaultMap=(.+)',cfg.read_text()).group(1).strip()
target='/Game/Conservatory/Maps/L_Exterior_WanderingBots'
w=u.EditorLoadingAndSavingUtils.load_map(old)
actors=u.get_editor_subsystem(u.EditorActorSubsystem)
cls=u.load_class(None,'/Script/Conservatory.C17Robot')
mesh=u.load_asset('/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple')
idle=u.load_asset('/Game/Characters/Mannequins/Animations/Manny/MM_Idle')
walk=u.load_asset('/Game/Characters/Mannequins/Animations/Manny/MM_Walk_InPlace')
assert mesh and idle and walk
units=[a for a in actors.get_all_level_actors() if a.get_class()==cls]
positions=[(-9280,-2500),(-9280,-1500),(-9280,-500),(-9280,500),(-9280,1500),(-11930,-2700),(-11930,-1700),(-11930,-700),(-11930,300),(-11930,2100),(-10600,0)]
report=[]
for i,(x,y) in enumerate(positions):
 a=units[i] if i<len(units) else actors.spawn_actor_from_class(cls,u.Vector(x,y,6355))
 assert a
 a.set_actor_location(u.Vector(x,y,6355),False,True)
 a.set_actor_label(('Indoor bot' if i==10 else 'Outdoor bot')+f' {i+1:02d}')
 a.set_folder_path('10 Wandering Mannequins')
 a.set_editor_property('use_mannequin',True)
 a.set_editor_property('wander_enabled',True)
 a.set_editor_property('patrol_enabled',True)
 a.set_editor_property('wander_extent',u.Vector(100,350 if i<10 else 180,110))
 a.set_editor_property('wander_speed',115+i*2 if i<10 else 100)
 a.mesh.set_skeletal_mesh_asset(mesh)
 a.mesh.set_relative_location(u.Vector(0,0,-96),False,False)
 a.mesh.set_relative_rotation(u.Rotator(0,-90,0),False,False)
 a.capsule_component.set_capsule_size(34,96)
 a.mesh.set_animation_mode(u.AnimationMode.ANIMATION_SINGLE_NODE)
 a.mesh.override_animation_data(idle,True,True,0,1)
 report.append({'name':a.get_actor_label(),'position':[x,y,6355],'inside':i==10})
for a in units[11:]:actors.destroy_actor(a)
assert u.EditorLoadingAndSavingUtils.save_map(w,target)
(ROOT/'Documentation/WanderingBots.json').write_text(json.dumps({'map':target,'previous_map':old,'bots':report,'mesh':mesh.get_path_name(),'walk':walk.get_path_name(),'idle':idle.get_path_name()},indent=2))
u.log('WANDER_PLACEMENT_SUCCESS '+target)

