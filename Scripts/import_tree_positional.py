import unreal as u,json,shutil,datetime,math
from pathlib import Path
R=Path(u.Paths.project_dir());SRC=R/'Asset Chest/01 John Originals/TREE-MASTER/UnrealExport';BASE='/Game/Conservatory/Botanical/TreeMaster';MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR'
spec=json.loads((SRC/'ExportReport.json').read_text());lib=u.EditorAssetLibrary;at=u.AssetToolsHelpers.get_asset_tools();mel=u.MaterialEditingLibrary
w=u.EditorLoadingAndSavingUtils.load_map(MAP);sub=u.get_editor_subsystem(u.EditorActorSubsystem)
def state(a):
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d();return [p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z]
actors=sub.get_all_level_actors();before={a.get_name():state(a) for a in actors};baseline=json.loads((R/'Documentation/TreePositionBaseline.json').read_text())['actors'];expected={a['name']:a['pos']+a['rot']+a['scale'] for a in baseline};assert before==expected,'Map changed after audit'
assert not any('TREE-MASTER' in a.get_actor_label() for a in actors)
floor=next(a for a in actors if a.get_actor_label()=='Core habitat | Centre Floor');center=floor.get_actor_location();c,e=floor.get_actor_bounds(False);z=c.z+e.z;pos=u.Vector(center.x,center.y,z)
backup=R/'Saved/Backups/TreePositional'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S');backup.mkdir(parents=True);shutil.copy2(R/'Content/Conservatory/Maps/L_Exterior_RobotVR.umap',backup/'L_Exterior_RobotVR.umap')
lib.make_directory(BASE);mats={}
def scalar(m,v):
 e=mel.create_material_expression(m,u.MaterialExpressionConstant);e.set_editor_property('r',v);return e
def color(m,c):
 e=mel.create_material_expression(m,u.MaterialExpressionConstant3Vector);e.set_editor_property('constant',u.LinearColor(*c,1));return e
for source,desc in spec['materials'].items():
 name='M_'+desc['slot'];assert not lib.does_asset_exist(BASE+'/'+name)
 m=at.create_asset(name,BASE,u.Material,u.MaterialFactoryNew());base=color(m,desc['color'])
 if desc['back_color']:
  sign=mel.create_material_expression(m,u.MaterialExpressionTwoSidedSign);alpha=mel.create_material_expression(m,u.MaterialExpressionMultiply);alpha.set_editor_property('const_b',.5);mel.connect_material_expressions(sign,'',alpha,'A');add=mel.create_material_expression(m,u.MaterialExpressionAdd);add.set_editor_property('const_b',.5);mel.connect_material_expressions(alpha,'',add,'A');mix=mel.create_material_expression(m,u.MaterialExpressionLinearInterpolate);mel.connect_material_expressions(color(m,desc['back_color']),'',mix,'A');mel.connect_material_expressions(base,'',mix,'B');mel.connect_material_expressions(add,'',mix,'Alpha');base=mix
 if 'limestone' in source.lower() or 'Bark' in source:
  noise=mel.create_material_expression(m,u.MaterialExpressionNoise);noise.set_editor_property('scale',.07);noise.set_editor_property('levels',2);noise.set_editor_property('quality',1);noise.set_editor_property('output_min',0);noise.set_editor_property('output_max',1);mix=mel.create_material_expression(m,u.MaterialExpressionLinearInterpolate);mel.connect_material_expressions(color(m,[v*.75 for v in desc['color']]),'',mix,'A');mel.connect_material_expressions(base,'',mix,'B');mel.connect_material_expressions(noise,'',mix,'Alpha');base=mix
 for node,prop in [(base,u.MaterialProperty.MP_BASE_COLOR),(scalar(m,desc['rough']),u.MaterialProperty.MP_ROUGHNESS),(scalar(m,desc['metal']),u.MaterialProperty.MP_METALLIC)]:mel.connect_material_property(node,'',prop)
 if desc['foliage']:m.set_editor_property('two_sided',True)
 mel.recompile_material(m);assert lib.save_loaded_asset(m);mats[desc['slot']]=m
u.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0');placed=[]
for kind in ['Structure','Foliage']:
 name='SM_TreeMaster_'+kind;task=u.AssetImportTask();task.filename=str(SRC/(name+'.fbx'));task.destination_path=BASE;task.destination_name=name;task.automated=True;task.save=True;task.replace_existing=False
 opt=u.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;d=opt.static_mesh_import_data;d.combine_meshes=True;d.auto_generate_collision=False;d.generate_lightmap_u_vs=False;d.normal_import_method=u.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS;task.options=opt;at.import_asset_tasks([task]);mesh=lib.load_asset(BASE+'/'+name);assert mesh
 for i,slot in enumerate(mesh.get_editor_property('static_materials')):mesh.set_material(i,mats[str(slot.material_slot_name).split('.')[0]])
 settings=mesh.get_editor_property('nanite_settings');settings.enabled=False;mesh.set_editor_property('nanite_settings',settings)
 if kind=='Structure':
  body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True)
 assert lib.save_loaded_asset(mesh,only_if_is_dirty=False)
 a=next(a for a in actors if a.get_actor_label()==('Dome planter' if kind=='Structure' else 'Young white oak under dome'));a.set_actor_location(pos,False,False);a.set_actor_rotation(u.Rotator(0,0,0),False);a.set_actor_scale3d(u.Vector(1,1,1));a.set_actor_label('TREE-MASTER | positional olive '+kind.lower());a.set_folder_path('Core habitat/Tree centrepiece');a.static_mesh_component.set_static_mesh(mesh);a.static_mesh_component.set_editor_property('override_materials',[])
 if kind=='Foliage':a.static_mesh_component.set_collision_enabled(u.CollisionEnabled.NO_COLLISION)
 a.tags=['TREE_MASTER_POSITIONAL'];placed.append(a)
changed={a.get_name() for a in placed};after={a.get_name():state(a) for a in sub.get_all_level_actors() if a.get_name() in before and a.get_name() not in changed};assert after=={k:v for k,v in before.items() if k not in changed}
assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
report=dict(engine=u.SystemLibrary.get_engine_version(),timestamp=datetime.datetime.now().isoformat(),backup=str(backup),map=MAP,position=[pos.x,pos.y,pos.z],actors=[a.get_name() for a in placed],existing_actors_preserved=len(before),actor_count=len(sub.get_all_level_actors()),unrelated_transform_changes=[],source=spec['source'],triangles=spec['triangles'],purpose='Positional assembly; original Blender remains editable',materials='Palette and procedural colour variation, two-sided silver olive foliage; not final production shaders')
(R/'Documentation/TreePositionalImport.json').write_text(json.dumps(report,indent=2));print('TREE_POSITIONAL_IMPORTED')
