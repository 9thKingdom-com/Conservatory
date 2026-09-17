import bpy,math,sys,json
from pathlib import Path
ROOT=Path(r'C:\Users\ASUS TUF\Documents\1 conservatory');sys.path.insert(0,str(ROOT/'Scripts'))
from layout import height
OUT=ROOT/'SourceAssets/CoreHabitat';original=bpy.context.window.scene;scene=bpy.data.scenes.new('TEMP | Habitat ground');bpy.context.window.scene=scene
def distance(x,y):
 d=min(math.hypot(x,y)-20.8,*[math.hypot(x-a,y-b)-15 for a,b in [(46.63755,0),(-46.63755,0),(0,46.63755),(0,-46.63755)]])
 for xx,yy in [(x,y),(y,x)]:
  d=min(d,max(abs(xx)-46.63755,abs(yy)-4.5))
 return d
v=[];f=[];n=171
for j in range(n):
 y=-85+j
 for i in range(n):
  x=-85+i;d=distance(x,y);t=max(0,min(1,d/20));t=t*t*(3-2*t);ground=height(x-110,-y)
  z=(62.17*(1-t)+ground*t) if d<20 else ground-.15
  v.append((x,y,z))
for j in range(n-1):
 for i in range(n-1):
  a=j*n+i;f.extend([(a,a+1,a+n+1),(a,a+n+1,a+n)])
me=bpy.data.meshes.new('Habitat shaped terrain');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new('SM_Core_Terrain',me);scene.collection.objects.link(o);o.select_set(True);bpy.context.view_layer.objects.active=o
mat=bpy.data.materials.new('HabitatGround');me.materials.append(mat)
uv=me.uv_layers.new(name='TerrainUV')
for p in me.polygons:
 p.use_smooth=True
 for li in p.loop_indices:
  co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co.x/5,co.y/5)
bpy.ops.export_scene.fbx(filepath=str(OUT/'SM_Core_Terrain.fbx'),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,mesh_smooth_type='FACE')
bpy.context.window.scene=original;bpy.data.scenes.remove(scene)
p=OUT/'CoreHabitat.json';spec=json.loads(p.read_text());spec['origin_cm'][0]=-11000;spec['meshes']['SM_Core_Terrain']={'kind':'terrain','vertices':len(v),'polygons':len(f)};spec['actors']=[a for a in spec['actors'] if a['mesh']!='SM_Core_Terrain'];spec['actors'].append({'label':'Fitted habitat terrain','mesh':'SM_Core_Terrain','position':[0,0,-62.3095],'yaw':0});p.write_text(json.dumps(spec,indent=2))
print('HABITAT_TERRAIN_EXPORTED')
