import unreal as u,json
from pathlib import Path
ROOT=Path(u.Paths.project_dir());OLD='/Game/Conservatory/Maps/L_Exterior_TerrainRobots';NEW='/Game/Conservatory/Maps/L_Exterior_RobotVR'
lib=u.EditorAssetLibrary;at=u.AssetToolsHelpers.get_asset_tools();mel=u.MaterialEditingLibrary;BASE='/Game/Conservatory/Robots/VR';lib.make_directory(BASE)
task=u.AssetImportTask();task.filename=str(ROOT/'SourceAssets/VR/T_TerrainMap.png');task.destination_path=BASE;task.automated=True;task.replace_existing=True;task.save=True;at.import_asset_tasks([task])
def mat(name,color,rough=.65,metal=0):
 path=BASE+'/'+name
 m=lib.load_asset(path) if lib.does_asset_exist(path) else at.create_asset(name,BASE,u.Material,u.MaterialFactoryNew())
 mel.delete_all_material_expressions(m)
 c=mel.create_material_expression(m,u.MaterialExpressionConstant3Vector);c.set_editor_property('constant',u.LinearColor(*color,1));mel.connect_material_property(c,'',u.MaterialProperty.MP_BASE_COLOR)
 for val,prop in [(rough,u.MaterialProperty.MP_ROUGHNESS),(metal,u.MaterialProperty.MP_METALLIC)]:
  e=mel.create_material_expression(m,u.MaterialExpressionConstant);e.set_editor_property('r',val);mel.connect_material_property(e,'',prop)
 mel.recompile_material(m);lib.save_loaded_asset(m);return m
cloth=mat('M_HapticFabric',(.035,.065,.055),.86);visor=mat('M_Headset',(.015,.022,.028),.24);enamel=mat('M_RackEnamel',(.025,.075,.07),.38,.4)
mel.set_material_usage(cloth,u.MaterialUsage.MATUSAGE_SKELETAL_MESH);mel.recompile_material(cloth);lib.save_loaded_asset(cloth)
screen=mat('M_SecurityScreen',(0,0,0));mel.delete_all_material_expressions(screen);screen.set_editor_property('shading_model',u.MaterialShadingModel.MSM_UNLIT)
e=mel.create_material_expression(screen,u.MaterialExpressionTextureSampleParameter2D);e.set_editor_property('parameter_name','ScreenImage');e.set_editor_property('texture',lib.load_asset(BASE+'/T_TerrainMap'));mel.connect_material_property(e,'RGB',u.MaterialProperty.MP_EMISSIVE_COLOR);mel.recompile_material(screen);lib.save_loaded_asset(screen)
w=u.EditorLoadingAndSavingUtils.load_map(OLD);actors=u.get_editor_subsystem(u.EditorActorSubsystem)
removed=[]
for a in actors.get_all_level_actors():
 label=a.get_actor_label()
 if a.get_class().get_name() in ['RobotTerminal','RobotVRHub','VRSuitStation'] or label.startswith('Operations desk - ') or label=='C17 workstation screen' or str(a.get_folder_path()).startswith('11 Kitchen VR'):
  removed.append(label);actors.destroy_actor(a)
hub=actors.spawn_actor_from_class(u.load_class(None,'/Script/Conservatory.RobotVRHub'),u.Vector(-13020,1350,4210),u.Rotator(pitch=0,yaw=180,roll=0));hub.set_actor_label('Kitchen wall security monitor - all ten robots');hub.set_folder_path('11 Kitchen VR/Wall security monitor');hub.get_editor_property('screen').set_material(0,screen)
brass=lib.load_asset('/Game/Conservatory/Architecture/OrnateLift/M_AgedBrass');cube=lib.load_asset('/Engine/BasicShapes/Cube')
def text(label,value,pos,yaw,size=7):
 a=actors.spawn_actor_from_class(u.TextRenderActor,u.Vector(*pos),u.Rotator(pitch=0,yaw=yaw,roll=0));a.set_actor_label(label);a.set_folder_path('11 Kitchen VR/Labels');c=a.get_component_by_class(u.TextRenderComponent);c.set_text(value);c.set_world_size(size);c.set_horizontal_alignment(u.HorizTextAligment.EHTA_CENTER);c.set_vertical_alignment(u.VerticalTextAligment.EVRTA_TEXT_CENTER);c.set_text_render_color(u.Color(190,210,190,255));return a
text('Security monitor controls','FIELD SECURITY  /  [F] VIEW CAMERAS',(-13028,1350,4100),180,6)
stations=[];idle=lib.load_asset('/Game/Characters/Mannequins/Animations/Manny/MM_Idle')
for i in range(10):
 x=-14090+i*105;y=850;z=4003
 a=actors.spawn_actor_from_class(u.load_class(None,'/Script/Conservatory.VRSuitStation'),u.Vector(x,y,z),u.Rotator(pitch=0,yaw=90,roll=0));a.set_actor_label(f'VR suit {i+1:02d} - robot {i+1:02d}');a.set_folder_path('11 Kitchen VR/Numbered suits');a.set_editor_property('robot_id',i+1);a.set_editor_property('hub',hub)
 a.get_editor_property('suit').set_animation_mode(u.AnimationMode.ANIMATION_SINGLE_NODE);a.get_editor_property('suit').override_animation_data(idle,True,False,0,1)
 for slot in range(a.get_editor_property('suit').get_num_materials()):a.get_editor_property('suit').set_material(slot,cloth)
 for c in a.get_components_by_class(u.StaticMeshComponent):c.set_material(0,visor if c.get_name()=='VRHeadset' else enamel)
 text(f'VR suit {i+1:02d} label',f'SUIT {i+1:02d}\nROBOT {i+1:02d}\n[F] WEAR',(x,y-22,z+197),90,6)
 stations.append({'id':i+1,'position':[x,y,z],'approach':[x,y+145,4090]})
assert u.ExteriorTools.build_terrain_navigation()
assert u.EditorLoadingAndSavingUtils.save_map(w,NEW)
(ROOT/'Documentation/RobotVRPlacement.json').write_text(json.dumps({'map':NEW,'previous_map':OLD,'monitor':[-13020,1350,4210],'suits':stations,'removed_old_connection':removed},indent=2))
u.log('ROBOT_VR_ROOM_SAVED')


