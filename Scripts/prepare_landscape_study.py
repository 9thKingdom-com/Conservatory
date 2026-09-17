"""Create an isolated map with a native paintable Landscape material."""
import unreal as u,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];base='/Game/Conservatory/Environment/LandscapePaintStudy';lib=u.EditorAssetLibrary;at=u.AssetToolsHelpers.get_asset_tools();mel=u.MaterialEditingLibrary
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
if not w or w.get_name()!='L_LandscapePaintStudy':
 w=u.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior_RobotVR')
 assert u.EditorLoadingAndSavingUtils.save_map(w,'/Game/Conservatory/Maps/L_LandscapePaintStudy')
mat=at.create_asset('M_PaintedValley',base,u.Material,u.MaterialFactoryNew()) if not lib.does_asset_exist(base+'/M_PaintedValley') else lib.load_asset(base+'/M_PaintedValley');mel.delete_all_material_expressions(mat)
def node(cls,**props):
 e=mel.create_material_expression(mat,cls)
 for k,v in props.items():e.set_editor_property(k,v)
 return e
def connect(a,p,b,q):assert mel.connect_material_expressions(a,p,b,q)
pos=node(u.MaterialExpressionWorldPosition);xy=node(u.MaterialExpressionComponentMask,r=True,g=True,b=False,a=False);connect(pos,'',xy,'')
uv=node(u.MaterialExpressionMultiply,const_b=.0025);connect(xy,'',uv,'A')
ground=node(u.MaterialExpressionTextureSample,texture=lib.load_asset('/Game/Conservatory/Environment/Textures/T_Forest_Color'));connect(uv,'',ground,'UVs')
normal=node(u.MaterialExpressionTextureSample,texture=lib.load_asset('/Game/Conservatory/Environment/Textures/T_Forest_Normal'),sampler_type=u.MaterialSamplerType.SAMPLERTYPE_NORMAL);connect(uv,'',normal,'UVs')
col=ground;norm=normal
for name,color in [('Gravel',(.20,.18,.14)),('Asphalt',(.04,.045,.047)),('Soil',(.075,.043,.021))]:
 noise=node(u.MaterialExpressionNoise,scale=.19 if name!='Soil' else .025,quality=1,levels=2)
 c=node(u.MaterialExpressionConstant3Vector,constant=u.LinearColor(*color,1));dark=node(u.MaterialExpressionConstant3Vector,constant=u.LinearColor(*[x*.62 for x in color],1));mix=node(u.MaterialExpressionLinearInterpolate)
 connect(dark,'',mix,'A');connect(c,'',mix,'B');connect(noise,'',mix,'Alpha')
 weight=node(u.MaterialExpressionLandscapeLayerSample,parameter_name=name,preview_weight=0)
 layer=node(u.MaterialExpressionLinearInterpolate);connect(col,'RGB' if col==ground else '',layer,'A');connect(mix,'',layer,'B');connect(weight,'',layer,'Alpha');col=layer
 flat=node(u.MaterialExpressionConstant3Vector,constant=u.LinearColor(0,0,1,1));nl=node(u.MaterialExpressionLinearInterpolate);connect(norm,'RGB' if norm==normal else '',nl,'A');connect(flat,'',nl,'B');connect(weight,'',nl,'Alpha');norm=nl
mel.connect_material_property(col,'',u.MaterialProperty.MP_BASE_COLOR);mel.connect_material_property(norm,'',u.MaterialProperty.MP_NORMAL)
r=node(u.MaterialExpressionConstant,r=.92);mel.connect_material_property(r,'',u.MaterialProperty.MP_ROUGHNESS);mel.layout_material_expressions(mat);mel.recompile_material(mat);lib.save_loaded_asset(mat)
land=next(a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if isinstance(a,u.Landscape));land.set_editor_property('landscape_material',mat)
assert u.EditorLoadingAndSavingUtils.save_map(w,'/Game/Conservatory/Maps/L_LandscapePaintStudy')
(root/'Documentation/LandscapeStudyPreparation.json').write_text(json.dumps({'map':'/Game/Conservatory/Maps/L_LandscapePaintStudy','material':mat.get_path_name(),'target_layers':str(land.get_editor_property('target_layers'))},indent=2))
