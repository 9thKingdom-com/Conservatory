import unreal as u,json,shutil,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1];SRC=R/'Asset Chest/01 John Originals/LIFT-MASTER/UnrealExport';BASE='/Game/Conservatory/Architecture/LiftMaster';MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR'
spec=json.loads((SRC/'ExportReport.json').read_text());backup=R/'Saved/Backups/LiftMasterIntegration'/('Unreal-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir(parents=True)
shutil.copy2(R/'Content/Conservatory/Maps/L_Exterior_RobotVR.umap',backup/'L_Exterior_RobotVR.umap')
lib=u.EditorAssetLibrary;at=u.AssetToolsHelpers.get_asset_tools();mel=u.MaterialEditingLibrary;lib.make_directory(BASE)
def scalar(m,v):
 e=mel.create_material_expression(m,u.MaterialExpressionConstant);e.set_editor_property('r',v);return e
def color(m,c):
 e=mel.create_material_expression(m,u.MaterialExpressionConstant3Vector);e.set_editor_property('constant',u.LinearColor(*c,1));return e
def lerp(m,a,b,alpha):
 e=mel.create_material_expression(m,u.MaterialExpressionLinearInterpolate)
 for node,pin in [(a,'A'),(b,'B'),(alpha,'Alpha')]:mel.connect_material_expressions(node,'',e,pin)
 return e
mats={}
for desc in spec['materials'].values():
 name='M_'+desc['slot'];path=BASE+'/'+name
 assert not lib.does_asset_exist(path),'Asset exists; inspect before overwriting '+path
 m=at.create_asset(name,BASE,u.Material,u.MaterialFactoryNew());base=color(m,desc['color']);rough=scalar(m,desc['rough'])
 if desc['ramp']:
  noise=mel.create_material_expression(m,u.MaterialExpressionNoise);noise.set_editor_property('scale',.012 if desc['slot']=='Lift08' else .22);noise.set_editor_property('quality',1);noise.set_editor_property('levels',3);noise.set_editor_property('output_min',0);noise.set_editor_property('output_max',1)
  base=lerp(m,color(m,desc['ramp'][0]),color(m,desc['ramp'][-1]),noise)
  if desc['rough_range']:rough=lerp(m,scalar(m,desc['rough_range'][0]),scalar(m,desc['rough_range'][1]),noise)
 for node,prop in [(base,u.MaterialProperty.MP_BASE_COLOR),(rough,u.MaterialProperty.MP_ROUGHNESS),(scalar(m,desc['metal']),u.MaterialProperty.MP_METALLIC)]:mel.connect_material_property(node,'',prop)
 if desc['emission_strength']:
  mel.connect_material_property(color(m,[x*desc['emission_strength'] for x in desc['emission']]),'',u.MaterialProperty.MP_EMISSIVE_COLOR)
 if desc['glass']:
  m.set_editor_property('blend_mode',u.BlendMode.BLEND_TRANSLUCENT);m.set_editor_property('two_sided',True);m.set_editor_property('translucency_lighting_mode',u.TranslucencyLightingMode.TLM_SURFACE_PER_PIXEL_LIGHTING)
  f=mel.create_material_expression(m,u.MaterialExpressionFresnel);mul=mel.create_material_expression(m,u.MaterialExpressionMultiply);mul.set_editor_property('const_b',.15);mel.connect_material_expressions(f,'',mul,'A');add=mel.create_material_expression(m,u.MaterialExpressionAdd);add.set_editor_property('const_b',.025);mel.connect_material_expressions(mul,'',add,'A');mel.connect_material_property(add,'',u.MaterialProperty.MP_OPACITY)
 else:mel.set_material_usage(m,u.MaterialUsage.MATUSAGE_NANITE)
 mel.recompile_material(m);assert lib.save_loaded_asset(m);mats[desc['slot']]=m
meshes={}
for kind in ['Solid','Glass']:
 name='SM_LiftMaster_'+kind;task=u.AssetImportTask();task.filename=str(SRC/(name+'.fbx'));task.destination_path=BASE;task.destination_name=name;task.automated=True;task.save=True;task.replace_existing=False
 opt=u.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.auto_generate_collision=False;opt.static_mesh_import_data.generate_lightmap_u_vs=False;task.options=opt;at.import_asset_tasks([task]);mesh=lib.load_asset(BASE+'/'+name);assert mesh
 for i,slot in enumerate(mesh.get_editor_property('static_materials')):
  key=str(slot.material_slot_name).split('.')[0];assert key in mats,key;mesh.set_material(i,mats[key])
 body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True)
 if kind=='Solid':
  settings=mesh.get_editor_property('nanite_settings');settings.enabled=True;settings.fallback_relative_error=0.0;mesh.set_editor_property('nanite_settings',settings)
 assert lib.save_loaded_asset(mesh,only_if_is_dirty=False);meshes[kind]=mesh
w=u.EditorLoadingAndSavingUtils.load_map(MAP);sub=u.get_editor_subsystem(u.EditorActorSubsystem);actors=sub.get_all_level_actors();by={a.get_name():a for a in actors}
def trans(a):
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d();return [p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z]
before={a.get_name():trans(a) for a in actors};lift=by['StaticMeshActor_1858'];assert 'SM_OrnateLift_Crowned' in lift.static_mesh_component.static_mesh.get_path_name()
def dest(a):
 v=a.get_editor_property('destination');return [v.x,v.y,v.z]
stations={a.get_name():[trans(a),dest(a),a.get_editor_property('destination_yaw')] for a in actors if a.get_class().get_name()=='ServiceLift'}
lift.static_mesh_component.set_static_mesh(meshes['Solid']);lift.static_mesh_component.set_editor_property('override_materials',[]);lift.set_actor_label('LIFT-MASTER | finished conservatory lift')
glass=sub.spawn_actor_from_class(u.StaticMeshActor,lift.get_actor_location(),lift.get_actor_rotation());glass.set_actor_scale3d(lift.get_actor_scale3d());glass.static_mesh_component.set_static_mesh(meshes['Glass']);glass.set_actor_label('LIFT-MASTER | glazing');glass.set_folder_path(lift.get_folder_path())
sub.destroy_actor(by['TextRenderActor_18'])
light=by['PointLight_36'];light.set_actor_location(lift.get_actor_location()+u.Vector(0,0,280),False,False)
unexpected=[a.get_name() for a in sub.get_all_level_actors() if a.get_name() in before and a.get_name()!='PointLight_36' and trans(a)!=before[a.get_name()]];assert not unexpected,unexpected
for name,value in stations.items():
 a=by[name];assert [trans(a),dest(a),a.get_editor_property('destination_yaw')]==value
assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
report=dict(engine=u.SystemLibrary.get_engine_version(),timestamp=datetime.datetime.now().isoformat(),backup=str(backup),source=spec['source_snapshot'],map=MAP,position=trans(lift),mesh_assets=[m.get_path_name() for m in meshes.values()],removed_old_plaque='TextRenderActor_18',glass_actor=glass.get_name(),unrelated_transform_changes=unexpected,lift_endpoints_preserved=True,actor_count=len(sub.get_all_level_actors()),materials='Source palette/metal/roughness recreated; procedural noise translated to Unreal, glass uses tested Fresnel transparency.')
(R/'Documentation/LiftMasterIntegration.json').write_text(json.dumps(report,indent=2));print('LIFT_MASTER_INTEGRATED')
