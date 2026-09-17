import unreal as u,json,shutil,datetime
from pathlib import Path
root=Path(__file__).resolve().parents[1];lib=u.EditorAssetLibrary
base='/Game/Conservatory/Architecture/CoreHabitat'
backup=root/'Saved/Backups/HabitatFinish'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S');backup.mkdir(parents=True)
shutil.copy2(root/'Content/Conservatory/Maps/L_Exterior_RobotVR.umap',backup/'L_Exterior_RobotVR.umap')
mats={'HabitatFrame':lib.load_asset('/Game/Conservatory/Architecture/ModularMaster/M_MasterIvoryFrame'),'HabitatBrass':lib.load_asset('/Game/Conservatory/Architecture/ModularMaster/M_MasterBrass')}
for m in mats.values():
    u.MaterialEditingLibrary.set_material_usage(m,u.MaterialUsage.MATUSAGE_NANITE)
    lib.save_loaded_asset(m,only_if_is_dirty=False)
names=['SM_Core_'+s+'_'+k for s in ['Small','Large'] for k in ['Bay','Portal','Cap']]+['SM_Core_WalkwayFrame']
for name in names:
    shutil.copy2(root/'Content/Conservatory/Architecture/CoreHabitat'/(name+'.uasset'),backup/(name+'.uasset'))
    task=u.AssetImportTask();task.filename=str(root/'SourceAssets/CoreHabitat'/(name+'.fbx'));task.destination_path=base;task.destination_name=name;task.automated=True;task.save=True;task.replace_existing=True
    opt=u.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH
    opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.auto_generate_collision=False;opt.static_mesh_import_data.generate_lightmap_u_vs=False;task.options=opt
    u.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);mesh=lib.load_asset(base+'/'+name)
    for i,s in enumerate(mesh.get_editor_property('static_materials')):mesh.set_material(i,mats[str(s.material_slot_name).split('.')[0]])
    settings=mesh.get_editor_property('nanite_settings');settings.enabled=True;mesh.set_editor_property('nanite_settings',settings)
    assert lib.save_loaded_asset(mesh,only_if_is_dirty=False)
actors=u.get_editor_subsystem(u.EditorActorSubsystem);world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
bots=[a for a in actors.get_all_level_actors() if a.get_class().get_name()=='C17Robot']
target=[a for a in bots if a.get_actor_label()=='Outdoor robot 01'];assert len(target)==1
a=target[0];p=a.get_actor_location();before=[p.x,p.y,p.z]
loc=u.NavigationSystemV1.project_point_to_navigation(world,u.Vector(-14000,5000,6300),None,None,query_extent=u.Vector(500,500,10000))
assert loc is not None and loc.y>4000 and loc.x < -13000
a.set_actor_location(loc+u.Vector(0,0,100),False,True)
assert u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Conservatory/Maps/L_Exterior_RobotVR')
(root/'Documentation/HabitatFinish.json').write_text(json.dumps({'meshes':names,'robot_moved':a.get_actor_label(),'before':before,'after':[loc.x,loc.y,loc.z+100],'robot_count':len(bots),'backup':str(backup)},indent=2))
print('HABITAT_FINISH_APPLIED')
