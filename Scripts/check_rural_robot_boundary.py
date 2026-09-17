import unreal as u,json
from pathlib import Path
R=Path(u.Paths.project_dir());w=u.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior_RobotVR');bots=[a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if a.get_class().get_name()=='C17Robot'];tests=[]
for b in bots:
 if b.robot_id==11:continue
 assert b.limit_terrain_wander and b.is_inside_wander_bounds(b.get_actor_location())
 # Centre and four permitted inner corners; exact requested perimeter and points outside each edge must be rejected.
 for x,y,expected in [(0,0,True),(-32799,-32799,True),(32799,32799,True),(-32799,32799,True),(32799,-32799,True),(-33000,0,False),(33000,0,False),(0,-33000,False),(0,33000,False),(-34000,0,False),(34000,0,False),(0,-34000,False),(0,34000,False)]:
  actual=b.is_inside_wander_bounds(u.Vector(x,y,0));assert actual==expected;tests.append(dict(robot=b.robot_id,point=[x,y],expected=expected,actual=actual))
(R/'Documentation/RobotRuralBoundaryChecks.json').write_text(json.dumps(dict(passed=True,checks=len(tests),tests=tests),indent=2))
