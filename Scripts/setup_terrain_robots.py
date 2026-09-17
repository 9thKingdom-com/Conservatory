"""Save terrain navigation and spread the ten exterior units across the landscape."""
import unreal as u,json,sys
from pathlib import Path
ROOT=Path(u.Paths.project_dir());OLD='/Game/Conservatory/Maps/L_Exterior_WanderingBots';NEW='/Game/Conservatory/Maps/L_Exterior_TerrainRobots'
sys.path.insert(0,str(ROOT/'Scripts'))
from layout import height
w=u.EditorLoadingAndSavingUtils.load_map(OLD)
lib=u.EditorAssetLibrary
dest='/Game/Conservatory/Robots/Manny/A_MannyTerrainWalk'
walk=lib.load_asset(dest) if lib.does_asset_exist(dest) else lib.duplicate_asset('/Game/Characters/Mannequins/Animations/Manny/MM_Walk_Fwd',dest)
assert walk
walk.set_editor_property('enable_root_motion',False)
walk.set_editor_property('force_root_lock',True)
walk.set_editor_property('root_motion_root_lock',u.RootMotionRootLock.ANIM_FIRST_FRAME)
assert lib.save_loaded_asset(walk)
assert u.ExteriorTools.build_terrain_navigation()
actors=u.get_editor_subsystem(u.EditorActorSubsystem)
bots=sorted([a for a in actors.get_all_level_actors() if a.get_class().get_name()=='C17Robot'],key=lambda a:a.get_actor_label())
outdoors=[a for a in bots if a.get_actor_label().startswith('Outdoor')]
assert len(outdoors)==10
# Broad coverage: conservatory approach, valley route, town and woodland quadrants.
points=[(-13200,0),(-5000,-5000),(14000,830),(24000,-4000),(-33000,-22000),(-35000,27000),(0,30000),(36000,38000),(42000,-27000),(5000,-40000)]
report=[]
for i,(a,(x,y)) in enumerate(zip(outdoors,points),1):
 loc=u.NavigationSystemV1.project_point_to_navigation(w,u.Vector(x,y,height(x/100,y/100)*100+10),None,None,query_extent=u.Vector(1200,1200,600))
 assert loc is not None, (x,y,'no walkable navmesh')
 # Python returns a Vector for successful projection.
 a.set_actor_location(loc+u.Vector(0,0,100),False,True)
 a.set_editor_property('terrain_wander',True);a.set_editor_property('robot_id',i)
 a.set_editor_property('wander_speed',180)
 a.set_actor_label(f'Outdoor robot {i:02d}')
 report.append({'id':i,'position':[loc.x,loc.y,loc.z+100]})
for a in bots:
 if a not in outdoors:a.set_editor_property('robot_id',11)
assert u.EditorLoadingAndSavingUtils.save_map(w,NEW)
(ROOT/'Documentation/TerrainRobotsPlacement.json').write_text(json.dumps({'map':NEW,'previous_map':OLD,'outdoor':report,'indoor_count':1,'walk':dest,'native_walk_speed_cm_s':240,'terrain_size_m':1260},indent=2))
u.log('TERRAIN_ROBOTS_SETUP_SUCCESS')


