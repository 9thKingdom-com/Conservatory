"""Replace only the active connector mesh; import a separate reusable joint frame."""
import unreal as u,re,json,shutil,datetime,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];MAP=re.search(r'GameDefaultMap=(.+)',(ROOT/'Config/DefaultEngine.ini').read_text()).group(1).strip();BASE='/Game/Conservatory/Architecture/PassageDetail'
spec=json.loads((ROOT/'SourceAssets/PassageDetail/PassageKit.json').read_text());ref=ROOT/'Reference images/Conservatory-MASTER.blend';assert hashlib.sha256(ref.read_bytes()).hexdigest()==spec['source_sha256']
backup=ROOT/'Saved/Backups/PassageDetail'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S');backup.mkdir(parents=True,exist_ok=True);mapfile=ROOT/'Content'/Path(MAP.removeprefix('/Game/')+'.umap');shutil.copy2(mapfile,backup/mapfile.name)
world=u.EditorLoadingAndSavingUtils.load_map(MAP);assert world
actors=u.get_editor_subsystem(u.EditorActorSubsystem);at=u.AssetToolsHelpers.get_asset_tools();lib=u.EditorAssetLibrary;mel=u.MaterialEditingLibrary;lib.make_directory(BASE)
materials={n:lib.load_asset('/Game/Conservatory/Architecture/ModularMaster/M_Master'+n) for n in ['IvoryFrame','Brass','FloorLight','FloorDark']}
def node(mat,cls,**props):
 e=mel.create_material_expression(mat,cls)
 for k,v in props.items():e.set_editor_property(k,v)
 return e
for name in ['Gasket','ConservatoryGlass']:
 path=BASE+'/M_Passage'+name;mat=lib.load_asset(path) if lib.does_asset_exist(path) else at.create_asset('M_Passage'+name,BASE,u.Material,u.MaterialFactoryNew());mel.delete_all_material_expressions(mat)
 c=node(mat,u.MaterialExpressionConstant3Vector,constant=u.LinearColor(*((.018,.024,.022,1) if name=='Gasket' else (.75,.85,.84,1))));mel.connect_material_property(c,'',u.MaterialProperty.MP_BASE_COLOR)
 r=node(mat,u.MaterialExpressionConstant,r=.86 if name=='Gasket' else .14);mel.connect_material_property(r,'',u.MaterialProperty.MP_ROUGHNESS)
 if name=='ConservatoryGlass':
  mat.set_editor_property('blend_mode',u.BlendMode.BLEND_TRANSLUCENT);mat.set_editor_property('two_sided',True);mat.set_editor_property('translucency_lighting_mode',u.TranslucencyLightingMode.TLM_SURFACE_PER_PIXEL_LIGHTING)
  f=node(mat,u.MaterialExpressionFresnel);mul=node(mat,u.MaterialExpressionMultiply,const_b=.11);mel.connect_material_expressions(f,'',mul,'A');add=node(mat,u.MaterialExpressionAdd,const_b=.02);mel.connect_material_expressions(mul,'',add,'A');mel.connect_material_property(add,'',u.MaterialProperty.MP_OPACITY)
  sp=node(mat,u.MaterialExpressionConstant,r=.28);mel.connect_material_property(sp,'',u.MaterialProperty.MP_SPECULAR)
 mel.recompile_material(mat);lib.save_loaded_asset(mat);materials[name]=mat
meshes={}
for name in ['SM_Passage_Detailed','SM_Passage_JoinFrame']:
 task=u.AssetImportTask();task.filename=str(ROOT/'SourceAssets/PassageDetail'/(name+'.fbx'));task.destination_path=BASE;task.destination_name=name;task.automated=True;task.save=True;task.replace_existing=True
 opt=u.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.auto_generate_collision=False;opt.static_mesh_import_data.generate_lightmap_u_vs=False;task.options=opt;at.import_asset_tasks([task]);mesh=lib.load_asset(BASE+'/'+name);assert mesh
 for i,s in enumerate(mesh.get_editor_property('static_materials')):
  key=re.sub(r'_\d{3}$','',str(s.material_slot_name).split('.')[0]);assert key in materials,key;mesh.set_material(i,materials[key])
 mesh.get_editor_property('body_setup').set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);mesh.get_editor_property('body_setup').set_editor_property('double_sided_geometry',True)
 if name.endswith('Detailed'):
  for s in spec['sockets']:
   old=mesh.find_socket(s['name'])
   if old:mesh.remove_socket(old)
   socket=u.StaticMeshSocket(outer=mesh);socket.set_editor_property('socket_name',s['name']);socket.set_editor_property('relative_location',u.Vector(*[x*100 for x in s['position_m']]));socket.set_editor_property('relative_rotation',u.Rotator(pitch=0,yaw=s['yaw'],roll=0));mesh.add_socket(socket)
 lib.save_loaded_asset(mesh);meshes[name]=mesh
def state(a):
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d();return [p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z]
allactors=actors.get_all_level_actors();before={a.get_path_name():state(a) for a in allactors}
passages=[a for a in allactors if a.get_actor_label().startswith('02 Short passage')];assert len(passages)==1
a=passages[0];c=a.get_component_by_class(u.StaticMeshComponent);oldmesh=c.get_editor_property('static_mesh').get_path_name();c.set_static_mesh(meshes['SM_Passage_Detailed'])
domes=[a for a in allactors if 'ConservatoryModule' in [str(t) for t in a.tags] and a not in passages];errors=[]
for sn in ['Attach_PositiveX','Attach_NegativeX']:
 p=c.get_socket_location(sn);options=[]
 for dome in domes:
  dc=dome.get_component_by_class(u.StaticMeshComponent)
  for dn in ['Attach_PositiveX','Attach_NegativeX']:options.append((dc.get_socket_location(dn)-p).length())
 errors.append(min(options))
assert max(errors)<.1,'Existing dome sockets no longer align'
assert {a.get_path_name():state(a) for a in actors.get_all_level_actors()}==before
assert u.EditorLoadingAndSavingUtils.save_map(world,MAP)
report={'map':MAP,'old_mesh':oldmesh,'new_mesh':meshes['SM_Passage_Detailed'].get_path_name(),'all_actor_transforms_preserved':True,'socket_errors_cm':errors,'reference_sha256':spec['source_sha256'],'backup':str(backup/mapfile.name),'body_triangles':spec['meshes']['Body']['triangles'],'standalone_joint_triangles':spec['meshes']['JoinFrame']['triangles'],'construction_gameplay_implemented':False}
(ROOT/'Documentation/PassageDetail.json').write_text(json.dumps(report,indent=2));print('PASSAGE_APPLIED '+json.dumps(report),flush=True)
