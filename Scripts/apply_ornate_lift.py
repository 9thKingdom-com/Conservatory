import unreal as u,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];cfg=ROOT/'Config/DefaultEngine.ini';config=cfg.read_text();MAP=re.search(r'GameDefaultMap=(.+)',config).group(1).strip()
BASE='/Game/Conservatory/Architecture/OrnateLift';lib=u.EditorAssetLibrary;at=u.AssetToolsHelpers.get_asset_tools();mel=u.MaterialEditingLibrary;lib.make_directory(BASE)
def material(name,col,metal,rough,emit=0):
 path=BASE+'/M_'+name
 if lib.does_asset_exist(path):return lib.load_asset(path)
 m=at.create_asset('M_'+name,BASE,u.Material,u.MaterialFactoryNew());c=mel.create_material_expression(m,u.MaterialExpressionConstant3Vector);c.set_editor_property('constant',u.LinearColor(*col,1));mel.connect_material_property(c,'',u.MaterialProperty.MP_BASE_COLOR)
 for v,p in [(metal,u.MaterialProperty.MP_METALLIC),(rough,u.MaterialProperty.MP_ROUGHNESS)]:
  e=mel.create_material_expression(m,u.MaterialExpressionConstant);e.set_editor_property('r',v);mel.connect_material_property(e,'',p)
 if emit:
  e=mel.create_material_expression(m,u.MaterialExpressionMultiply);e.set_editor_property('const_b',emit);mel.connect_material_expressions(c,'',e,'A');mel.connect_material_property(e,'',u.MaterialProperty.MP_EMISSIVE_COLOR)
 mel.recompile_material(m);lib.save_loaded_asset(m);return m
mats={'LiftEnamel':material('LiftEnamel',(.025,.075,.07),.6,.28),'Brass':material('AgedBrass',(.48,.30,.10),.8,.27),'FloorLight':material('IvoryPanel',(.52,.47,.34),.15,.5),'FloorDark':material('DarkFloor',(.11,.16,.14),.1,.65),'Lamp':material('WarmLamp',(1,.65,.23),0,.3,3),'ConservatoryGlass':lib.load_asset('/Game/Conservatory/Architecture/ModularMaster/M_MasterConservatoryGlass')}
meshes={}
for part in ['Crowned','Bunker']:
 n='SM_OrnateLift_'+part;t=u.AssetImportTask();t.filename=str(ROOT/'SourceAssets/OrnateLift'/(n+'.fbx'));t.destination_path=BASE;t.destination_name=n;t.automated=True;t.replace_existing=True;t.save=True
 opt=u.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.auto_generate_collision=False;t.options=opt;at.import_asset_tasks([t]);m=lib.load_asset(BASE+'/'+n);assert m
 for i,s in enumerate(m.get_editor_property('static_materials')):
  name=str(s.material_slot_name);mat=mats.get(name)
  if mat:m.set_material(i,mat)
 body=m.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True);lib.save_loaded_asset(m);meshes[part]=m
w=u.EditorLoadingAndSavingUtils.load_map(MAP);assert w;actors=u.get_editor_subsystem(u.EditorActorSubsystem)
allactors=actors.get_all_level_actors();lifts=[a for a in allactors if a.get_class().get_name()=='ServiceLift'];assert len(lifts)==2
for a in allactors:
 if str(a.get_folder_path()).startswith('08 Bunker/04 Service lift') and a not in lifts:actors.destroy_actor(a)
y=json.loads((ROOT/'Documentation/ModularPlacement.json').read_text())['dome_y_cm']
upper=max(lifts,key=lambda a:a.get_actor_location().z);lower=min(lifts,key=lambda a:a.get_actor_location().z)
positions=[(-11600,y,6244),(-15000,-2700,3998)]
for station,part,pos,destname in [(upper,'Crowned',positions[0],'HABITAT DECK'),(lower,'Bunker',positions[1],'CONSERVATORY')]:
 x,y,z=pos;station.set_actor_location(u.Vector(x,y,z+92),False,False)
 a=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(x,y,z));a.set_actor_label('Ornate service lift - '+part);a.set_folder_path('08 Bunker/04 Service lift');a.static_mesh_component.set_static_mesh(meshes[part])
 text=actors.spawn_actor_from_class(u.TextRenderActor,u.Vector(x-99,y,z+232));text.set_actor_label('Lift destination plaque');text.set_folder_path('08 Bunker/04 Service lift');c=text.get_component_by_class(u.TextRenderComponent);c.set_text('SERVICE LIFT\n'+destname+'\n\n[E] TRAVEL');c.set_world_size(9);c.set_horizontal_alignment(u.HorizTextAligment.EHTA_CENTER);c.set_vertical_alignment(u.VerticalTextAligment.EVRTA_TEXT_CENTER);c.set_text_render_color(u.Color(25,18,8,255))
 light=actors.spawn_actor_from_class(u.PointLight,u.Vector(x,y,z+265));light.set_actor_label('Lift warm ceiling lamp');light.set_folder_path('08 Bunker/04 Service lift');c=light.point_light_component;c.set_editor_property('intensity_units',u.LightUnits.LUMENS);c.set_intensity(130);c.set_light_color(u.LinearColor(1,.72,.4,1));c.set_attenuation_radius(350);c.set_editor_property('source_radius',12)
upper.set_editor_property('destination',lower.get_actor_location());lower.set_editor_property('destination',upper.get_actor_location())
upper.set_editor_property('destination_yaw',0);lower.set_editor_property('destination_yaw',0)
if not u.EditorLoadingAndSavingUtils.save_map(w,MAP):
 target='/Game/Conservatory/Maps/L_Exterior_Ornate';assert u.EditorLoadingAndSavingUtils.save_map(w,target)
 cfg.write_text(config.replace(MAP,target));MAP=target
report={'map':MAP,'upper_cm':list(positions[0]),'lower_cm':list(positions[1]),'width_m':2.5,'depth_m':2.35,'upper_height_m':4.32,'clear_entrance_m':1.48,'upper_station_cm':list(upper.get_actor_location().to_tuple()) if hasattr(upper.get_actor_location(),'to_tuple') else [upper.get_actor_location().x,upper.get_actor_location().y,upper.get_actor_location().z]}
(ROOT/'Documentation/OrnateLift.json').write_text(json.dumps(report,indent=2))
for f in ['ModularPlacement.json','BunkerLayout.json']:
 p=ROOT/'Documentation'/f;r=json.loads(p.read_text());r['upper_lift_cm' if f.startswith('Modular') else 'lift_top_cm']=report['upper_station_cm'];p.write_text(json.dumps(r,indent=2))
print('ORNATE_LIFT_APPLIED',flush=True)

