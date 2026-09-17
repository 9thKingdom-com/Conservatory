import unreal as u,json,math,datetime
from pathlib import Path
R=Path(u.Paths.project_dir()).resolve();MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR'
w=u.EditorLoadingAndSavingUtils.load_map(MAP);sub=u.get_editor_subsystem(u.EditorActorSubsystem);actors=list(sub.get_all_level_actors());land=next(a for a in actors if a.get_class().get_name()=='Landscape');bots=sorted([a for a in actors if a.get_class().get_name()=='C17Robot'],key=lambda a:a.robot_id)
def xyz(p):return [p.x,p.y,p.z]
def tr(a):return xyz(a.get_actor_location())+[a.get_actor_rotation().pitch,a.get_actor_rotation().yaw,a.get_actor_rotation().roll]+xyz(a.get_actor_scale3d())
before={a.get_name():tr(a) for a in actors}; origin,extent=land.get_actor_bounds(False)
lo=origin-extent;hi=origin+extent; mn=u.Vector(lo.x+30000,lo.y+30000,lo.z);mx=u.Vector(hi.x-30000,hi.y-30000,hi.z)
assert mn.x<mx.x and mn.y<mx.y
ignore=[a for a in actors if a!=land]
def ground(x,y):
 hit=u.SystemLibrary.line_trace_single(w,u.Vector(x,y,hi.z+100000),u.Vector(x,y,lo.z-100000),u.TraceTypeQuery.ECC_VISIBILITY,True,ignore,u.DrawDebugTrace.NONE)
 return hit.to_tuple()[5].z if hit and hit.to_tuple()[0] else None
assert u.ExteriorTools.build_terrain_navigation()
rows=[]
for b in bots:
 if b.robot_id==11:continue
 p=b.get_actor_location();base_x=max(mn.x+500,min(mx.x-500,p.x));base_y=max(mn.y+500,min(mx.y-500,p.y));candidates=[(base_x,base_y)]
 for radius in [500,1000,2000,4000,8000,12000,20000]:
  for i in range(24):candidates.append((base_x+radius*math.cos(i*math.pi/12),base_y+radius*math.sin(i*math.pi/12)))
 chosen=None
 for x,y in candidates:
  if not(mn.x+300<x<mx.x-300 and mn.y+300<y<mx.y-300):continue
  z=ground(x,y)
  if z is None:continue
  q=u.NavigationSystemV1.project_point_to_navigation(w,u.Vector(x,y,z),None,None,query_extent=u.Vector(200,200,300))
  if q is None or abs(q.x-x)>250 or abs(q.y-y)>250 or abs(q.z-z)>300:continue
  if not(mn.x+300<q.x<mx.x-300 and mn.y+300<q.y<mx.y-300):continue
  hs=[ground(q.x+dx,q.y+dy) for dx,dy in [(0,0)]+[(34*math.cos(i*math.pi/4),34*math.sin(i*math.pi/4)) for i in range(8)]]
  if any(h is None for h in hs) or max(hs)-min(hs)>50:continue
  chosen=u.Vector(q.x,q.y,max(hs)+100);break
 assert chosen is not None, 'No walkable placement for robot '+str(b.robot_id)
 b.set_actor_location(chosen,False,True);b.set_editor_property('limit_terrain_wander',True);b.set_editor_property('wander_bounds_min',mn);b.set_editor_property('wander_bounds_max',mx);b.terrain_wander=True;b.wander_enabled=True;b.patrol_enabled=True
 rows.append(dict(id=b.robot_id,before=xyz(p),after=xyz(chosen),ground_z=hs[0],foot_clearance_cm=chosen.z-96-max(hs)))
assert all(tr(a)==before[a.get_name()] for a in actors if a not in bots or a.robot_id==11)
assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
(R/'Documentation/RobotRuralRepair.json').write_text(json.dumps(dict(timestamp=datetime.datetime.now().isoformat(),backup=(R/'Documentation/RobotRuralBackupPath.txt').read_text().strip(),landscape_min=xyz(lo),landscape_max=xyz(hi),wander_min=xyz(mn),wander_max=xyz(mx),robots=rows,actor_count=len(actors),unrelated_transforms_preserved=True,navigation_rebuilt=True,saved=True),indent=2))
