"""Run with UnrealEditor-Cmd -run=pythonscript -script=<this file>.
Rebuilds the generated exterior map. Back up hand edits before regeneration.
"""
import unreal as u, sys, math, random, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Scripts'))
from layout import height,path_y,clearing,village,SEED
BASE='/Game/Conservatory'; SRC=ROOT/'SourceAssets'/'Environment'
asset_tools=u.AssetToolsHelpers.get_asset_tools(); lib=u.EditorAssetLibrary; mel=u.MaterialEditingLibrary
for folder in ['Maps','Environment/Meshes','Environment/Materials','Player','Documentation']:
 lib.make_directory(BASE+'/'+folder)
def expression(mat,cls,**kwargs):
 e=mel.create_material_expression(mat,cls)
 for k,v in kwargs.items(): e.set_editor_property(k,v)
 return e
def material(name,color,scale=.05,foliage=False,folder='Environment/Materials'):
 path=BASE+'/'+folder
 lib.make_directory(path)
 mat=lib.load_asset(path+'/M_'+name) if lib.does_asset_exist(path+'/M_'+name) else None
 if mat: return mat
 mat=asset_tools.create_asset('M_'+name,path,u.Material,u.MaterialFactoryNew())
 if foliage:
  mat.set_editor_property('two_sided',True)
  mat.set_editor_property('shading_model',u.MaterialShadingModel.MSM_TWO_SIDED_FOLIAGE)
 pos=expression(mat,u.MaterialExpressionWorldPosition)
 noise=expression(mat,u.MaterialExpressionNoise,scale=scale,quality=1,levels=2)
 mel.connect_material_expressions(pos,'',noise,'Position')
 dark=expression(mat,u.MaterialExpressionConstant3Vector,constant=u.LinearColor(*[v*.62 for v in color],1))
 light=expression(mat,u.MaterialExpressionConstant3Vector,constant=u.LinearColor(*color,1))
 lerp=expression(mat,u.MaterialExpressionLinearInterpolate)
 for a,b in [(dark,'A'),(light,'B'),(noise,'Alpha')]: mel.connect_material_expressions(a,'',lerp,b)
 mel.connect_material_property(lerp,'',u.MaterialProperty.MP_BASE_COLOR)
 rough=expression(mat,u.MaterialExpressionConstant,r=.88)
 mel.connect_material_property(rough,'',u.MaterialProperty.MP_ROUGHNESS)
 if foliage: mel.connect_material_property(dark,'',u.MaterialProperty.MP_SUBSURFACE_COLOR)
 mel.layout_material_expressions(mat); mel.recompile_material(mat); lib.save_loaded_asset(mat)
 return mat
colors={'Bark':(.12,.085,.048),'Leaves':(.065,.15,.023),'LeavesLight':(.15,.23,.045),'Stone':(.24,.25,.22),'Plaster':(.49,.45,.35),'Roof':(.15,.12,.105),'Timber':(.11,.085,.058),'Glass':(.017,.027,.025),'Grass':(.19,.24,.07),'Earth':(.24,.20,.12),'Birch':(.64,.63,.55)}
mats={n:material(n,c,foliage=n in ['Leaves','LeavesLight','Grass']) for n,c in colors.items()}
for name,color in {'IvoryFrame':(.62,.57,.43),'Brass':(.42,.255,.085),'FloorLight':(.46,.44,.36),'FloorDark':(.18,.21,.20),'ConservatoryGlass':(.47,.64,.62)}.items():
 mats[name]=material(name,color,scale=.025,folder='Architecture/Materials')
for name in ['IvoryFrame','Brass']:
 mat=mats[name]
 metal=expression(mat,u.MaterialExpressionConstant,r=.7 if name=='Brass' else .45)
 rough=expression(mat,u.MaterialExpressionConstant,r=.26 if name=='Brass' else .34)
 mel.connect_material_property(metal,'',u.MaterialProperty.MP_METALLIC); mel.connect_material_property(rough,'',u.MaterialProperty.MP_ROUGHNESS)
glass=mats['ConservatoryGlass']; mel.delete_all_material_expressions(glass)
glass.set_editor_property('blend_mode',u.BlendMode.BLEND_TRANSLUCENT)
glass.set_editor_property('two_sided',True)
glass.set_editor_property('translucency_lighting_mode',u.TranslucencyLightingMode.TLM_SURFACE_PER_PIXEL_LIGHTING)
gcol=expression(glass,u.MaterialExpressionConstant3Vector,constant=u.LinearColor(.55,.72,.69,1))
mel.connect_material_property(gcol,'',u.MaterialProperty.MP_BASE_COLOR)
fresnel=expression(glass,u.MaterialExpressionFresnel)
mult=expression(glass,u.MaterialExpressionMultiply,const_b=.35); mel.connect_material_expressions(fresnel,'',mult,'A')
opacity=expression(glass,u.MaterialExpressionAdd,const_b=.07); mel.connect_material_expressions(mult,'',opacity,'A')
mel.connect_material_property(opacity,'',u.MaterialProperty.MP_OPACITY)
rough=expression(glass,u.MaterialExpressionConstant,r=.09); mel.connect_material_property(rough,'',u.MaterialProperty.MP_ROUGHNESS)
mel.layout_material_expressions(glass)
for name in ['Roof','Plaster']: mats[name].set_editor_property('two_sided',True)
ridge_mat=material('DistantRidges',(.075,.115,.09),.0002)
mel.delete_all_material_expressions(ridge_mat)
ridge_color=expression(ridge_mat,u.MaterialExpressionConstant3Vector,constant=u.LinearColor(.075,.115,.09,1))
mel.connect_material_property(ridge_color,'',u.MaterialProperty.MP_BASE_COLOR)
ridge_rough=expression(ridge_mat,u.MaterialExpressionConstant,r=1)
mel.connect_material_property(ridge_rough,'',u.MaterialProperty.MP_ROUGHNESS)
mel.recompile_material(ridge_mat); lib.save_loaded_asset(ridge_mat)
ground=material('Ground',(.20,.255,.092),.004)
textures={}
for file in (ROOT/'SourceAssets'/'Textures').glob('*.jpg'):
 path=BASE+'/Environment/Textures/'+file.stem
 if not lib.does_asset_exist(path):
  task=u.AssetImportTask(); task.filename=str(file); task.destination_path=BASE+'/Environment/Textures'
  task.destination_name=file.stem; task.automated=True; task.save=True; asset_tools.import_asset_tasks([task])
 textures[file.stem]=lib.load_asset(path)
if textures:
 normal=textures['T_Forest_Normal']; normal.set_editor_property('compression_settings',u.TextureCompressionSettings.TC_NORMALMAP); normal.set_editor_property('srgb',False); lib.save_loaded_asset(normal)
 mel.delete_all_material_expressions(ground)
 pos=expression(ground,u.MaterialExpressionWorldPosition)
 mask=expression(ground,u.MaterialExpressionComponentMask,r=True,g=True,b=False,a=False)
 assert mel.connect_material_expressions(pos,'',mask,''), 'World position connection failed'
 scale=expression(ground,u.MaterialExpressionMultiply,const_b=.0025)
 mel.connect_material_expressions(mask,'',scale,'A')
 for key,prop in [('T_Forest_Color',u.MaterialProperty.MP_BASE_COLOR),('T_Forest_Normal',u.MaterialProperty.MP_NORMAL)]:
  sample=expression(ground,u.MaterialExpressionTextureSample,texture=textures[key])
  if key.endswith('Normal'): sample.set_editor_property('sampler_type',u.MaterialSamplerType.SAMPLERTYPE_NORMAL)
  mel.connect_material_expressions(scale,'',sample,'UVs'); mel.connect_material_property(sample,'RGB',prop)
 rough=expression(ground,u.MaterialExpressionConstant,r=.92); mel.connect_material_property(rough,'',u.MaterialProperty.MP_ROUGHNESS)
 mel.layout_material_expressions(ground)
for mat in list(mats.values())+[ground]:
 mat.set_editor_property('used_with_instanced_static_meshes',True)
 mel.recompile_material(mat); lib.save_loaded_asset(mat)
meshes={}
for file in sorted(SRC.glob('*.fbx'))+sorted((ROOT/'SourceAssets'/'Conservatory').glob('*.fbx')):
 destination=BASE+('/Architecture/Meshes' if file.parent.name=='Conservatory' else '/Environment/Meshes')
 lib.make_directory(destination)
 path=destination+'/'+file.stem
 mesh=lib.load_asset(path) if lib.does_asset_exist(path) else None
 if not mesh or file.stem=='SM_DistantHills':
  task=u.AssetImportTask(); task.filename=str(file); task.destination_path=destination; task.destination_name=file.stem
  task.automated=True; task.save=True; task.replace_existing=True
  options=u.FbxImportUI(); options.import_mesh=True; options.import_materials=False; options.import_textures=False
  options.import_as_skeletal=False; options.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH
  options.static_mesh_import_data.combine_meshes=True; options.static_mesh_import_data.generate_lightmap_u_vs=False
  options.static_mesh_import_data.auto_generate_collision=False
  task.options=options; asset_tools.import_asset_tasks([task]); mesh=lib.load_asset(path)
 if not mesh: raise RuntimeError('Missing mesh '+path)
 slots=mesh.get_editor_property('static_materials')
 for i,slot in enumerate(slots):
  n=str(slot.material_slot_name)
  if n in mats: mesh.set_material(i,mats[n])
  elif n=='Ground': mesh.set_material(i,ridge_mat)
 if any(k in file.stem for k in ['Rock','Wall','FallenLog','Conservatory']):
  mesh.get_editor_property('body_setup').set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
  mesh.get_editor_property('body_setup').set_editor_property('double_sided_geometry',True)
 lib.save_loaded_asset(mesh); meshes[file.stem]=mesh
 print('READY '+file.stem,flush=True)
editor=u.get_editor_subsystem(u.LevelEditorSubsystem)
world=u.EditorLoadingAndSavingUtils.new_blank_map(False)
land=u.ExteriorTools.create_terrain(str(SRC/'Hill.r16'),ground)
if not land: raise RuntimeError('Landscape import failed')
actors=u.get_editor_subsystem(u.EditorActorSubsystem)
def actor(cls,label,loc=(0,0,0),rot=(0,0,0),folder='04 Atmosphere'):
 a=actors.spawn_actor_from_class(cls,u.Vector(*loc),u.Rotator(pitch=rot[0],yaw=rot[1],roll=rot[2])); a.set_actor_label(label); a.set_folder_path(folder); return a
def mesh_actor(name,label,x,y,z=None,yaw=0,scale=(1,1,1),folder='03 Village'):
 a=actor(u.StaticMeshActor,label,(x*100,y*100,(height(x,y) if z is None else z)*100),(0,yaw,0),folder)
 a.static_mesh_component.set_static_mesh(meshes[name]); a.set_actor_scale3d(u.Vector(*scale))
 assert a.get_actor_up_vector().z>.999, 'Unexpected tilt: '+label
 return a
mesh_actor('SM_OldTrack','Old forestry track — twin worn ruts',0,0,z=0,scale=(1,-1,1),folder='01 Landscape')
if 'SM_DistantHills' in meshes: mesh_actor('SM_DistantHills','Distant wooded ridgelines',0,0,z=0,folder='01 Landscape')
# Three-module initial conservatory, axis north/south, with room to expand on the plateau.
for name,label,y,yaw in [('SM_Conservatory_Dome','01 South dome',-14.744,270),('SM_Conservatory_Corridor','02 Barrel-vaulted corridor',0,90),('SM_Conservatory_Dome','03 North dome',14.744,90)]:
 a=mesh_actor(name,label,-175,y,z=62,yaw=yaw,folder='06 Conservatory / Modules')
 a.tags=['ConservatoryModule','ExpandableKit']
for y in [-14.744,14.744]:
 pot=actor(u.StaticMeshActor,'Dome planter',(-17700,y*100,6230),folder='06 Conservatory / Interior')
 pot.static_mesh_component.set_static_mesh(u.load_asset('/Engine/BasicShapes/Cylinder'))
 pot.static_mesh_component.set_material(0,mats['FloorLight']); pot.set_actor_scale3d(u.Vector(2,2,.6))
 mesh_actor('SM_Oak_2','Young tree under dome',-177,y,z=62.6,scale=(.32,.32,.32),folder='06 Conservatory / Interior')
random.seed(SEED)
houses=[]
for row,y in enumerate([-53,-16,37,76]):
 for col in range(5 if row<3 else 3):
  x=150+col*30+random.uniform(-4,4); yy=y+random.uniform(-5,5)
  yaw=random.uniform(-8,8)+(180 if row%2 else 0)
  houses.append((x,yy)); mesh_actor('SM_Cottage_'+str(1+(row+col)%4),'Cottage_%02d'%(len(houses)),x,yy,z=height(x,yy)-.35,yaw=yaw)
mesh_actor('SM_BellTower','Village bell tower',237,17,z=height(237,17)-.2)
for i in range(43):
 x=136+i*3.5; y=96+2*math.sin(i*.1)
 if i%13 in [6,7]: continue
 mesh_actor('SM_Wall','Old boundary wall_%02d'%i,x,y,yaw=random.uniform(-4,4),scale=(1.55,1,random.uniform(.6,1)))
groups={n:[] for n in meshes if any(s in n for s in ['Oak','Birch','Grass','Fern','Rock','FallenLog'])}
def add(name,x,y,scale=1,yaw=None,z=None):
 t=u.Transform(location=u.Vector(x*100,y*100,(height(x,y) if z is None else z)*100),rotation=u.Rotator(pitch=0,yaw=random.uniform(0,360) if yaw is None else yaw,roll=0),scale=u.Vector(scale,scale,scale))
 groups[name].append(t)
tree_names=[n for n in groups if 'Oak' in n or 'Birch' in n]
for i in range(4400):
 x=random.uniform(-590,590); y=random.uniform(-590,590)
 if clearing(x,y,12) or (x+105)**2+(y+20)**2<18**2: continue
 if -148<x<230 and abs(y-path_y(x))<5: continue
 if village(x,y) and random.random()<.96: continue
 # Protect a wedge of visible meadow between the hill and village.
 if -110<x<320 and abs(y-7)<36 and random.random()<.94: continue
 # Groves leave irregular pockets of meadow.
 if math.sin(x*.019)+math.cos(y*.027)+math.sin((x+y)*.008)<-.55: continue
 add(random.choice(tree_names),x,y,random.uniform(.70,1.28))
for i in range(1400):
 x=random.uniform(-390,-85); y=random.uniform(-240,240)
 if clearing(x,y,12) or (x+105)**2+(y+20)**2<22**2: continue
 if -148<x<230 and abs(y-path_y(x))<6: continue
 add(random.choice(tree_names),x,y,random.uniform(.75,1.25))
for i in range(22000):
 x=random.uniform(-340,350); y=random.uniform(-250,250)
 if abs(x+175)<9 and abs(y)<24: continue
 if any(abs(x-hx)<6 and abs(y-hy)<8 for hx,hy in houses): continue
 if -140<x<220 and .45<abs(y-path_y(x))<1.5: continue
 if random.random()<.08: add('SM_Fern',x,y,random.uniform(.7,1.5))
 else: add('SM_Grass_'+str(random.randint(1,3)),x,y,random.uniform(.6,1.6))
for i in range(280):
 x=random.uniform(-440,420); y=random.uniform(-350,350)
 if clearing(x,y,5) or village(x,y) or (-140<x<220 and abs(y-path_y(x))<4): continue
 add('SM_Rock_'+str(random.randint(1,3)),x,y,random.uniform(.4,2.3))
for i in range(35):
 x=random.uniform(-330,50); y=random.choice([-1,1])*random.uniform(75,250)
 add('SM_FallenLog',x,y,random.uniform(.8,1.6))
for n,transforms in groups.items():
 if transforms: u.ExteriorTools.create_instances(meshes[n],transforms,n.replace('SM_','')+' | '+str(len(transforms)),any(k in n for k in ['Oak','Birch','Rock','FallenLog']))
sun=actor(u.DirectionalLight,'Sun — late afternoon',rot=(-28,-38,0))
sun.light_component.set_editor_property('intensity',5.5)
sun.light_component.set_editor_property('light_color',u.Color(255,239,211,255))
sun.light_component.set_editor_property('atmosphere_sun_light',True)
sun.light_component.set_editor_property('light_source_angle',2.0)
sun.light_component.set_mobility(u.ComponentMobility.MOVABLE)
actor(u.SkyAtmosphere,'Sky atmosphere')
sky=actor(u.SkyLight,'Sky — soft woodland fill')
sky.light_component.set_editor_property('real_time_capture',True)
sky.light_component.set_editor_property('intensity',.8)
sky.light_component.set_mobility(u.ComponentMobility.MOVABLE)
fog=actor(u.ExponentialHeightFog,'Valley fog — low-lying blanket',loc=(0,0,1600))
fc=fog.get_component_by_class(u.ExponentialHeightFogComponent)
fc.set_editor_property('fog_density',.12); fc.set_editor_property('fog_height_falloff',.9)
fc.set_editor_property('start_distance',1500)
fc.set_editor_property('enable_volumetric_fog',True)
start=actor(u.PlayerStart,'Start — hilltop outlook',(-10500,-2000,6100),(-9,4,0),'05 Player')
marker=actor(u.TargetPoint,'SITE — 104 x 80 m, room for expansion',(-17500,0,6200),folder='00 Reserved site')
marker.tags=['ReservedConservatorySite','ExpandableThreeModuleStarter']
editor.set_level_viewport_camera_info(u.Vector(-10500,-2000,5980),u.Rotator(pitch=-9,yaw=4,roll=0),'')
assert u.EditorLoadingAndSavingUtils.save_map(world,BASE+'/Maps/L_Exterior'), 'Map save failed'
lib.save_directory(BASE,only_if_is_dirty=True,recursive=True)
report={'seed':SEED,'landscape_m':1260,'landscape_vertices':505,'clearing_m':[104,80],'conservatory_modules':3,'conservatory_arrangement':'dome-corridor-dome','cottages':len(houses),'instances':{n:len(v) for n,v in groups.items()},'map':'/Game/Conservatory/Maps/L_Exterior'}
(ROOT/'Saved'/'GenerationReport.json').write_text(json.dumps(report,indent=2))
print('EXTERIOR_BUILD_COMPLETE '+json.dumps(report),flush=True)
