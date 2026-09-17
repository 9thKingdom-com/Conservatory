import unreal as u,json,shutil,datetime,math
from pathlib import Path
R=Path(u.Paths.project_dir()).resolve();MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR';w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();assert w.get_path_name()==MAP+'.L_Exterior_RobotVR'
sub=u.get_editor_subsystem(u.EditorActorSubsystem);actors=sub.get_all_level_actors();assert not any('Town hall | positional' in a.get_actor_label() for a in actors)
def trans(a):
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d();return [p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z]
before={a.get_name():trans(a) for a in actors};land=next(a for a in actors if a.get_class().get_name()=='Landscape');ignore=[a for a in actors if a!=land]
cx,cy=31250,5300;heights=[]
for dx in [-1900,0,1900]:
 for dy in [-1500,0,1500]:
  h=u.SystemLibrary.line_trace_single(w,u.Vector(cx+dx,cy+dy,100000),u.Vector(cx+dx,cy+dy,-100000),u.TraceTypeQuery.ECC_VISIBILITY,True,ignore,u.DrawDebugTrace.NONE);assert h and h.to_tuple()[0];heights.append(h.to_tuple()[5].z)
z=max(heights)+15
backup=R/'Saved/Backups/TownHallPositional'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S');backup.mkdir(parents=True);disk=R/'Content/Conservatory/Maps/L_Exterior_RobotVR.umap';shutil.copy2(disk,backup/'previous-disk.umap');assert u.EditorLoadingAndSavingUtils.save_map(w,MAP);shutil.copy2(disk,backup/'live-user-baseline.umap')
lib=u.EditorAssetLibrary;at=u.AssetToolsHelpers.get_asset_tools();mel=u.MaterialEditingLibrary;BASE='/Game/Conservatory/City/TownHallPositional';lib.make_directory(BASE)
def mat(name,c):
 m=at.create_asset(name,BASE,u.Material,u.MaterialFactoryNew());n=mel.create_material_expression(m,u.MaterialExpressionConstant3Vector);n.set_editor_property('constant',u.LinearColor(*c,1));mel.connect_material_property(n,'',u.MaterialProperty.MP_BASE_COLOR);v=mel.create_material_expression(m,u.MaterialExpressionConstant);v.set_editor_property('r',.8);mel.connect_material_property(v,'',u.MaterialProperty.MP_ROUGHNESS);mel.recompile_material(m);lib.save_loaded_asset(m);return m
stone=mat('M_HallBlockoutStone',(.48,.44,.35));roof=mat('M_HallBlockoutRoof',(.08,.12,.13));trim=mat('M_HallBlockoutTrim',(.65,.60,.48));dark=mat('M_HallBlockoutDoor',(.06,.075,.07));created=[]
def part(label,xyz,size,material,shape='Cube'):
 a=sub.spawn_actor_from_class(u.StaticMeshActor,u.Vector(cx+xyz[0]*100,cy+xyz[1]*100,z+xyz[2]*100));a.set_actor_label('Town hall | positional | '+label);a.set_folder_path('City draft/Town hall positional');a.static_mesh_component.set_static_mesh(lib.load_asset('/Engine/BasicShapes/'+shape));a.static_mesh_component.set_material(0,material);a.set_actor_scale3d(u.Vector(*size));a.tags=['TOWN_HALL_POSITIONAL'];created.append(a);return a
with u.ScopedEditorTransaction('Place town hall scale reference'):
 foundation_height=(z-min(heights))/100+.4
 root=part('foundation',(0,0,-foundation_height/2+.2),(38,30,foundation_height),stone)
 part('central hall',(0,0,6),(16,24,12),stone)
 for side in [-1,1]:
  part('civic wing '+str(side),(side*13,1,4.5),(10,22,9),stone)
  part('wing roof '+str(side),(side*13,1,9.3),(11,23,.6),roof)
 part('main roof',(0,0,12.4),(17,25,.8),roof)
 part('clock tower',(0,4,15.3),(7,7,6),stone)
 part('tower cornice',(0,4,18.5),(8,8,.6),trim)
 part('tower crown',(0,4,19.4),(7.5,7.5,3.0),roof,'Sphere')
 part('entrance portico',(0,-12.7,7.8),(12,4,.8),trim)
 for x in [-4.8,-1.6,1.6,4.8]:part('portico column',(x,-13.6,3.8),(.65,.65,7.6),trim,'Cylinder')
 part('entrance marker',(0,-12.03,2.4),(3,.12,4.8),dark)
 for width,depth,zz in [(13,3,.15),(12,2,.35),(11,1,.55)]:part('entrance step',(0,-13.5,zz),(width,depth,.3),trim)
 # Group the positional assembly under its foundation while retaining world transforms.
 for a in created[1:]:a.attach_to_actor(root,'',u.AttachmentRule.KEEP_WORLD,u.AttachmentRule.KEEP_WORLD,u.AttachmentRule.KEEP_WORLD,False)
assert before=={a.get_name():trans(a) for a in actors};assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
sub.set_selected_level_actors([root]);u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(u.Vector(cx-6200,cy-7600,z+5500),u.Rotator(pitch=-26,yaw=50.8,roll=0))
(R/'Documentation/TownHallPositional.json').write_text(json.dumps(dict(timestamp=datetime.datetime.now().isoformat(),backup=str(backup),position_cm=[cx,cy,z],footprint_m=[38,30],height_m=20.9,placement='North of civic circle, adjacent block east of north avenue; entrance faces civic area',terrain_samples_cm=heights,previous_actor_count=len(actors),new_parts=len(created),all_existing_transforms_preserved=True,terrain_unchanged=True,source_reference='CITY-PLAN.png',status='Positional massing only, no finished facade or explorable interior'),indent=2));print('TOWN_HALL_POSITIONAL_SAVED')
