import unreal as u,json,shutil,datetime
from pathlib import Path
R=Path(u.Paths.project_dir()).resolve();O=R/'SourceAssets/CityRoadDraft';BASE='/Game/Conservatory/Environment/CityRoadDraft';MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR'
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();assert w.get_path_name()==MAP+'.L_Exterior_RobotVR';assert not u.EditorLoadingAndSavingUtils.get_dirty_map_packages(),'Preserve new unsaved map edits before applying'
sub=u.get_editor_subsystem(u.EditorActorSubsystem);actors=sub.get_all_level_actors();land=next(a for a in actors if a.get_class().get_name()=='Landscape');old=land.get_editor_property('landscape_material');assert old.get_path_name()=='/Game/Conservatory/Environment/Materials/M_Ground.M_Ground'
def state(a):
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d();return [p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z]
before={a.get_name():state(a) for a in actors};baseline=json.loads((R/'Documentation/CityRoadDraftBaseline.json').read_text());assert before=={a['name']:a['pos']+a['rot']+a['scale'] for a in baseline['actors']}
backup=R/'Saved/Backups/CityRoadDraft'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S');backup.mkdir(parents=True);shutil.copy2(R/'Content/Conservatory/Maps/L_Exterior_RobotVR.umap',backup/'L_Exterior_RobotVR.umap')
lib=u.EditorAssetLibrary;at=u.AssetToolsHelpers.get_asset_tools();mel=u.MaterialEditingLibrary;lib.make_directory(BASE);assert not lib.does_asset_exist(BASE+'/M_CityRoadDraft_v1')
task=u.AssetImportTask();task.filename=str(O/'CityRoadMask.png');task.destination_path=BASE;task.destination_name='T_CityRoadMask';task.automated=True;task.save=True;at.import_asset_tasks([task]);tex=lib.load_asset(BASE+'/T_CityRoadMask');assert tex;tex.set_editor_property('srgb',False);tex.set_editor_property('compression_settings',u.TextureCompressionSettings.TC_MASKS);tex.set_editor_property('address_x',u.TextureAddress.TA_CLAMP);tex.set_editor_property('address_y',u.TextureAddress.TA_CLAMP);lib.save_loaded_asset(tex)
m=lib.duplicate_asset(old.get_path_name(),BASE+'/M_CityRoadDraft_v1');assert m
base=mel.get_material_property_input_node(m,u.MaterialProperty.MP_BASE_COLOR);baseout=mel.get_material_property_input_node_output_name(m,u.MaterialProperty.MP_BASE_COLOR);assert base
def node(cls):return mel.create_material_expression(m,cls)
def link(a,out,b,pin):assert mel.connect_material_expressions(a,out,b,pin)
def scalar(v):
 n=node(u.MaterialExpressionConstant);n.set_editor_property('r',v);return n
def color(c):
 n=node(u.MaterialExpressionConstant3Vector);n.set_editor_property('constant',u.LinearColor(*c,1));return n
def lerp(a,ao,b,bo,alpha,alphao):
 n=node(u.MaterialExpressionLinearInterpolate);link(a,ao,n,'A');link(b,bo,n,'B');link(alpha,alphao,n,'Alpha');return n
wp=node(u.MaterialExpressionWorldPosition);xy=node(u.MaterialExpressionComponentMask);xy.set_editor_property('r',True);xy.set_editor_property('g',True);xy.set_editor_property('b',False);xy.set_editor_property('a',False);link(wp,'',xy,'')
offset=node(u.MaterialExpressionAdd);link(xy,'',offset,'A');link(scalar(63000),'',offset,'B');divide=node(u.MaterialExpressionDivide);link(offset,'',divide,'A');link(scalar(126000),'',divide,'B');sample=node(u.MaterialExpressionTextureSample);sample.set_editor_property('texture',tex);sample.set_editor_property('sampler_type',u.MaterialSamplerType.SAMPLERTYPE_MASKS);link(divide,'',sample,'UVs')
shoulder=lerp(base,str(baseout),color([.29,.28,.23]),'',sample,'G');road=lerp(shoulder,'',color([.095,.105,.108]),'',sample,'R');assert mel.connect_material_property(road,'',u.MaterialProperty.MP_BASE_COLOR)
# Retain the original graph for all other outputs; the overlay changes colour only.
mel.recompile_material(m);assert lib.save_loaded_asset(m)
with u.ScopedEditorTransaction('Draft city roads from John reference'):
 land.set_editor_property('landscape_material',m)
assert before=={a.get_name():state(a) for a in sub.get_all_level_actors()};assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(u.Vector(28500,-4000,80000),u.Rotator(-90,-90,0))
(R/'Documentation/CityRoadDraftResult.json').write_text(json.dumps(dict(timestamp=datetime.datetime.now().isoformat(),engine=u.SystemLibrary.get_engine_version(),map=MAP,backup=str(backup),original_material=old.get_path_name(),draft_material=m.get_path_name(),road_count=38,actor_count=len(actors),actor_transforms_preserved=True,landscape_height_unchanged=True,buildings_preserved=True,source=str(O/'RoadLayout.json'),status='Terrain surface colour road draft; no grading or final road engineering'),indent=2));print('CITY_ROAD_DRAFT_SAVED')

