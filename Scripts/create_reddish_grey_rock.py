import unreal as u,json,datetime
from pathlib import Path
R=Path(u.Paths.project_dir()).resolve();MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR';BASE='/Game/Conservatory/Environment/MountainRock'
w=u.EditorLoadingAndSavingUtils.load_map(MAP);sub=u.get_editor_subsystem(u.EditorActorSubsystem);actors=list(sub.get_all_level_actors());land=next(a for a in actors if a.get_class().get_name()=='Landscape');old=land.get_editor_property('landscape_material');lib=u.EditorAssetLibrary;mel=u.MaterialEditingLibrary;at=u.AssetToolsHelpers.get_asset_tools()
assert old.get_path_name()=='/Game/Conservatory/Environment/Materials/M_Ground.M_Ground',old.get_path_name()
def tr(a):
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d();return [p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z]
before={a.get_name():tr(a) for a in actors};lib.make_directory(BASE)
# Resume only the unassigned newly created material after an interrupted build.
landmat=lib.load_asset(BASE+'/M_MountainLandscape') if lib.does_asset_exist(BASE+'/M_MountainLandscape') else lib.duplicate_asset(old.get_path_name(),BASE+'/M_MountainLandscape')
rockmat=at.create_asset('M_ReddishGreyRock',BASE,u.Material,u.MaterialFactoryNew())
code=(R/'SourceAssets/ReddishGreyRock.hlsl').read_text()
for m in [landmat,rockmat]:
 def node(cls,**props):
  n=mel.create_material_expression(m,cls)
  for k,v in props.items():n.set_editor_property(k,v)
  return n
 def link(a,out,b,pin):assert mel.connect_material_expressions(a,out,b,pin)
 def scalar(name,v):return node(u.MaterialExpressionScalarParameter,parameter_name=name,default_value=v)
 def vector(name,c):return node(u.MaterialExpressionVectorParameter,parameter_name=name,default_value=u.LinearColor(*c,1))
 wp=node(u.MaterialExpressionWorldPosition)
 custom=node(u.MaterialExpressionCustom,code=code,output_type=u.CustomMaterialOutputType.CMOT_FLOAT4,description='World-space reddish grey mountain rock')
 ins=[]
 for name in ['P','Scale','Grey','Red','RedAmount']:
  inp=u.CustomInput();inp.set_editor_property('input_name',name);ins.append(inp)
 custom.set_editor_property('inputs',ins)
 link(wp,'',custom,'P');link(scalar('RockScale',1),'',custom,'Scale');link(vector('RockGrey',(.23,.215,.205)),'',custom,'Grey');link(vector('RockOxide',(.31,.15,.115)),'',custom,'Red');link(scalar('RockRedAmount',.65),'',custom,'RedAmount')
 rgb=node(u.MaterialExpressionComponentMask,r=True,g=True,b=True,a=False);link(custom,'',rgb,'')
 height=node(u.MaterialExpressionComponentMask,r=False,g=False,b=False,a=True);link(custom,'',height,'')
 normal=node(u.MaterialExpressionCustom,code='float3 n=normalize(N); float3 px=ddx(P), py=ddy(P); float3 r1=cross(py,n),r2=cross(n,px); float det=dot(px,r1); float3 grad=sign(det)*(ddx(H)*r1+ddy(H)*r2); return normalize(abs(det)*n-Strength*grad);',output_type=u.CustomMaterialOutputType.CMOT_FLOAT3,description='Rock surface relief in world space')
 ins=[]
 for name in ['P','N','H','Strength']:
  inp=u.CustomInput();inp.set_editor_property('input_name',name);ins.append(inp)
 normal.set_editor_property('inputs',ins);link(wp,'',normal,'P');link(node(u.MaterialExpressionVertexNormalWS),'',normal,'N');link(height,'',normal,'H');link(scalar('RockRelief',1.8),'',normal,'Strength')
 tn=node(u.MaterialExpressionTransform,transform_source_type=u.MaterialVectorCoordTransformSource.TRANSFORMSOURCE_WORLD,transform_type=u.MaterialVectorCoordTransform.TRANSFORM_TANGENT);link(normal,'',tn,'')
 rough=scalar('RockRoughness',.88)
 if m==landmat:
  weight=node(u.MaterialExpressionLandscapeLayerSample,parameter_name='ReddishGreyRock',preview_weight=0)
  for prop,src in [(u.MaterialProperty.MP_BASE_COLOR,rgb),(u.MaterialProperty.MP_NORMAL,tn),(u.MaterialProperty.MP_ROUGHNESS,rough)]:
   orig=mel.get_material_property_input_node(m,prop);out=str(mel.get_material_property_input_node_output_name(m,prop))
   if not orig:
    orig=node(u.MaterialExpressionConstant,r=.9) if prop==u.MaterialProperty.MP_ROUGHNESS else node(u.MaterialExpressionConstant3Vector,constant=u.LinearColor(0,0,1,1));out=''
   mix=node(u.MaterialExpressionLinearInterpolate);link(orig,out,mix,'A');link(src,'',mix,'B');link(weight,'',mix,'Alpha');assert mel.connect_material_property(mix,'',prop)
 else:
  for prop,src in [(u.MaterialProperty.MP_BASE_COLOR,rgb),(u.MaterialProperty.MP_NORMAL,tn),(u.MaterialProperty.MP_ROUGHNESS,rough)]:assert mel.connect_material_property(src,'',prop)
 mel.layout_material_expressions(m);mel.recompile_material(m);assert lib.save_loaded_asset(m)
li=lib.duplicate_asset('/Game/Conservatory/Environment/LandscapePaintStudy/LI_Soil',BASE+'/LI_ReddishGreyRock');assert li
land.set_editor_property('landscape_material',landmat);assert u.ExteriorTools.register_reddish_grey_rock_layer();assert lib.save_loaded_asset(li)
assert before=={a.get_name():tr(a) for a in sub.get_all_level_actors()}
assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
(R/'Documentation/ReddishGreyRock.json').write_text(json.dumps(dict(timestamp=datetime.datetime.now().isoformat(),backup=(R/'Documentation/ReddishGreyRockBackup.txt').read_text().strip(),material=landmat.get_path_name(),standalone=rockmat.get_path_name(),layer_info=li.get_path_name(),target_layers=str(land.get_editor_property('target_layers')),actors=len(actors),all_transforms_preserved=True,painting_applied=False),indent=2))

