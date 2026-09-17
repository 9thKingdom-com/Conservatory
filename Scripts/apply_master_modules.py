"""Apply master-derived modules while preserving the authored exterior and bunker."""
import unreal as u,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BASE='/Game/Conservatory/Architecture/ModularMaster'; TARGET='/Game/Conservatory/Maps/L_Exterior_Modular'; SOURCE='/Game/Conservatory/Maps/L_Exterior_Sealed'
lib=u.EditorAssetLibrary;at=u.AssetToolsHelpers.get_asset_tools();lib.make_directory(BASE)
mel=u.MaterialEditingLibrary
def finish_material(name,color,metal=.3,rough=.4):
 path=BASE+'/M_Master'+name
 if lib.does_asset_exist(path):return lib.load_asset(path)
 mat=at.create_asset('M_Master'+name,BASE,u.Material,u.MaterialFactoryNew())
 c=mel.create_material_expression(mat,u.MaterialExpressionConstant3Vector);c.set_editor_property('constant',u.LinearColor(*color,1));mel.connect_material_property(c,'',u.MaterialProperty.MP_BASE_COLOR)
 for v,prop in [(metal,u.MaterialProperty.MP_METALLIC),(rough,u.MaterialProperty.MP_ROUGHNESS)]:
  e=mel.create_material_expression(mat,u.MaterialExpressionConstant);e.set_editor_property('r',v);mel.connect_material_property(e,'',prop)
 if name=='ConservatoryGlass':
  mat.set_editor_property('blend_mode',u.BlendMode.BLEND_TRANSLUCENT);mat.set_editor_property('two_sided',True);mat.set_editor_property('translucency_lighting_mode',u.TranslucencyLightingMode.TLM_SURFACE_PER_PIXEL_LIGHTING)
  f=mel.create_material_expression(mat,u.MaterialExpressionFresnel);m=mel.create_material_expression(mat,u.MaterialExpressionMultiply);m.set_editor_property('const_b',.15);mel.connect_material_expressions(f,'',m,'A')
  a=mel.create_material_expression(mat,u.MaterialExpressionAdd);a.set_editor_property('const_b',.025);mel.connect_material_expressions(m,'',a,'A');mel.connect_material_property(a,'',u.MaterialProperty.MP_OPACITY)
 mel.recompile_material(mat);lib.save_loaded_asset(mat);return mat
materials={'IvoryFrame':finish_material('IvoryFrame',(.58,.55,.46),.35,.32),'Brass':finish_material('Brass',(.43,.27,.095),.7,.28),'FloorLight':finish_material('FloorLight',(.4,.38,.31),.05,.75),'FloorDark':finish_material('FloorDark',(.16,.20,.19),.05,.75),'ConservatoryGlass':finish_material('ConservatoryGlass',(.68,.8,.78),0,.08)}
spec=json.loads((ROOT/'Documentation/MasterSockets.json').read_text()); L=spec['passage_length']; D=spec['dome_sockets'][0]['position'][0]; S=1.5; Y=(D+L/2)*S*100; Z=6242.75-.61*S*100
meshes={}
for part in ['Dome','Passage']:
 name='SM_Master_'+part;task=u.AssetImportTask();task.filename=str(ROOT/'SourceAssets/ModularMaster'/(name+'.fbx'));task.destination_path=BASE;task.destination_name=name;task.automated=True;task.save=True;task.replace_existing=True
 options=u.FbxImportUI();options.import_mesh=True;options.import_materials=False;options.import_textures=False;options.import_as_skeletal=False;options.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH
 options.static_mesh_import_data.combine_meshes=True;options.static_mesh_import_data.auto_generate_collision=False;options.static_mesh_import_data.generate_lightmap_u_vs=False;task.options=options;at.import_asset_tasks([task])
 mesh=lib.load_asset(BASE+'/'+name);assert mesh
 for i,slot in enumerate(mesh.get_editor_property('static_materials')):
  n=str(slot.material_slot_name).split('.')[0];mat=materials.get(n)
  if mat:mesh.set_material(i,mat)
  else:raise RuntimeError('Unmapped material '+n)
 body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True)
 for i,s in enumerate(spec['dome_sockets' if part=='Dome' else 'passage_sockets']):
  socket_name='Attach_'+('PositiveX' if i==0 else 'NegativeX')
  existing=mesh.find_socket(socket_name)
  if existing:mesh.remove_socket(existing)
  socket=u.StaticMeshSocket(outer=mesh);socket.set_editor_property('socket_name','Attach_'+('PositiveX' if i==0 else 'NegativeX'));socket.set_editor_property('relative_location',u.Vector(*[v*100 for v in s['position']]));socket.set_editor_property('relative_rotation',u.Rotator(pitch=0,yaw=s['yaw'],roll=0));mesh.add_socket(socket)
 lib.save_loaded_asset(mesh);meshes[part]=mesh
world=u.EditorLoadingAndSavingUtils.load_map(TARGET if lib.does_asset_exist(TARGET) else SOURCE);assert world
actors=u.get_editor_subsystem(u.EditorActorSubsystem);allactors=actors.get_all_level_actors()
for a in allactors:
 label=a.get_actor_label()
 if 'ConservatoryModule' in [str(t) for t in a.tags]:
  dome=label.startswith('01') or label.startswith('03');y=(-Y if label.startswith('01') else Y) if dome else 0
  a.static_mesh_component.set_static_mesh(meshes['Dome' if dome else 'Passage']);a.set_actor_location(u.Vector(-10600,y,Z),False,False);a.set_actor_rotation(u.Rotator(pitch=0,yaw=90,roll=0),False);a.set_actor_scale3d(u.Vector(S,S,S))
  a.set_actor_label(('01 South dome' if y<0 else '03 North dome')+' - master frame' if dome else '02 Short passage - master bay')
 if label in ['Dome planter','Young white oak under dome']:
  sign=1 if a.get_actor_location().y>0 else -1
  p=a.get_actor_location();a.set_actor_location(u.Vector(-11100,sign*(Y+400),p.z),False,False)
 if isinstance(a,u.PlayerStart):a.set_actor_location(u.Vector(-10600,0,6350),False,False)
lifts=[a for a in allactors if a.get_class().get_name()=='ServiceLift'];assert len(lifts)==2
upper=max(lifts,key=lambda a:a.get_actor_location().z);lower=min(lifts,key=lambda a:a.get_actor_location().z)
old=upper.get_actor_location();new=u.Vector(-11100,Y-400,6336);delta=new-old
for a in allactors:
 if str(a.get_folder_path()).startswith('08 Bunker/04 Service lift') and a.get_actor_location().z>5000:a.set_actor_location(a.get_actor_location()+delta,False,False)
lower.set_editor_property('destination',new)
assert u.EditorLoadingAndSavingUtils.save_map(world,TARGET)
(ROOT/'Documentation/ModularPlacement.json').write_text(json.dumps({'map':TARGET,'module_scale':S,'dome_y_cm':Y,'origin_z_cm':Z,'floor_z_cm':6242.75,'passage_length_m':L*S,'clear_width_m':(L-.4)*S,'roof_crown_m_above_origin':(4.35+L/2)*S,'upper_lift_cm':[new.x,new.y,new.z],'source_reference':'Reference images/Conservatory-MASTER.blend'},indent=2))
print('MASTER_MODULES_APPLIED',flush=True)
