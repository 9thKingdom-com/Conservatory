import unreal as u,json
from pathlib import Path
root=Path(u.Paths.project_dir());p=root/'Documentation/IntercomStations.json';data=json.loads(p.read_text())
outside={'West terrace','East terrace','North terrace','South terrace','Woodland approach','Village approach','Village overlook'}
w=u.EditorLoadingAndSavingUtils.load_map(data['map']);actors=u.get_editor_subsystem(u.EditorActorSubsystem);removed=0;moved=0
for a in actors.get_all_level_actors():
 if str(a.get_folder_path())!='09 CIDCORE Intercoms':continue
 area=a.get_actor_label().split(' - ',1)[-1]
 if area in outside:actors.destroy_actor(a);removed+=1
 elif area=='North dome':
  pos=a.get_actor_location();pos.y+=230;a.set_actor_location(pos,False,False);moved+=1
assert removed==21 and moved==3,(removed,moved)
old_map=data['map'];new_map='/Game/Conservatory/Maps/L_Exterior_IndoorIntercoms'
assert u.EditorLoadingAndSavingUtils.save_map(w,new_map)
config=root/'Config/DefaultEngine.ini';config.write_text(config.read_text().replace(old_map,new_map));data['map']=new_map
data['stations']=[s for s in data['stations'] if s['area'] not in outside]
for s in data['stations']:
 if s['area']=='North dome':s['position_cm'][1]=1641
assert len(data['stations'])==21
data['count']=len(data['stations']);p.write_text(json.dumps(data,indent=2))
(root/'Documentation/IntercomAdjustment.json').write_text(json.dumps({'outdoor_stations_removed':7,'remaining_stations':21,'north_dome_shift_cm':230,'lift_entrance_clearance_from_panel_edge_cm':136},indent=2))

