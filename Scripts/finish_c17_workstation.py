import unreal as u,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];cfg=ROOT/'Config/DefaultEngine.ini';old=re.search(r'GameDefaultMap=(.+)',cfg.read_text()).group(1).strip();w=u.EditorLoadingAndSavingUtils.load_map(old);actors=u.get_editor_subsystem(u.EditorActorSubsystem)
for a in actors.get_all_level_actors():
 if a.get_actor_label()=='C17 workstation screen':actors.destroy_actor(a)
for body,height,size in [('FIELD OPERATIONS',135,2.5),('C-17',125,4.2),('STANDBY',114,2.5)]:
 a=actors.spawn_actor_from_class(u.TextRenderActor,u.Vector(-13200,1150,4000+height),u.Rotator(pitch=0,yaw=180,roll=0));a.set_actor_label('C17 workstation screen');a.set_folder_path('10 C17 Field Units');c=a.get_component_by_class(u.TextRenderComponent);c.set_text(body);c.set_world_size(size);c.set_horizontal_alignment(u.HorizTextAligment.EHTA_CENTER);c.set_vertical_alignment(u.VerticalTextAligment.EVRTA_TEXT_CENTER);c.set_text_render_color(u.Color(200,225,190,255))
new='/Game/Conservatory/Maps/L_Exterior_C17_Ready';assert u.EditorLoadingAndSavingUtils.save_map(w,new);cfg.write_text(cfg.read_text().replace(old,new))
for file in ['Documentation/C17/Placement.json','Documentation/IntercomStations.json']:
 p=ROOT/file;d=json.loads(p.read_text());d['map']=new;p.write_text(json.dumps(d,indent=2))
