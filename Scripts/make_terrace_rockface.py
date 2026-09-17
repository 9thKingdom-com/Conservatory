"""Author a fitted bedrock apron and three reusable stones in Blender (metres)."""
import bpy, math, random, sys, json
from pathlib import Path
from mathutils import noise, Vector
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Scripts'))
from layout import height
OUT=ROOT/'SourceAssets/TerraceRockface'; OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
mat=bpy.data.materials.new('WeatheredLimestone'); mat.diffuse_color=(.32,.30,.25,1)
def export(obj):
 bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True); bpy.context.view_layer.objects.active=obj
 obj.data.materials.append(mat)
 uv=obj.data.uv_layers.new(name='RockUV')
 for p in obj.data.polygons:
  axes=sorted(range(3),key=lambda k:abs(p.normal[k]))[:2]
  for li in p.loop_indices:
   co=obj.data.vertices[obj.data.loops[li].vertex_index].co
   uv.data[li].uv=(co[axes[0]]*.5,co[axes[1]]*.5)
 bpy.ops.export_scene.fbx(filepath=str(OUT/(obj.name+'.fbx')),use_selection=True,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',object_types={'MESH'},add_leaf_bones=False,mesh_smooth_type='FACE')

# The back and buried toe overlap existing terrain. The highest rock stays below the deck.
verts=[]; faces=[]; ny=177; nx=49
profile=[(-112,61.28),(-100,61.30),(-93,61.24),(-91.1,61.14),(-90.5,58.6),(-88.1,58.3),(-87.4,55.6),(-84.6,55.0),(-83.7,52.0),(-76,0)]
for j in range(ny):
 y=-45+j*90/(ny-1)
 taper=max(0,min(1,(45-abs(y))/10)); taper=taper*taper*(3-2*taper)
 for i in range(nx):
  x=-112+i*36/(nx-1)
  for k in range(len(profile)-1):
   if profile[k][0]<=x<=profile[k+1][0]:
    t=(x-profile[k][0])/(profile[k+1][0]-profile[k][0]); za=profile[k][1]; zb=profile[k+1][1] or height(-76,-y)-.65
    z=za*(1-t)+zb*t; break
  ground=height(x,-y)-.8
  z=ground+(max(ground,z)-ground)*taper
  strength=max(0,min(1,(x+94)/4))*max(0,min(1,(-76-x)/2))*taper
  n=noise.fractal(Vector((x*.5,y*.24,z*.35)),1.0,2.0,3)
  z=min(61.32,z+strength*(n*.58+.14*math.sin(y*1.7+x*2.8)))
  xx=x+strength*(.32*math.sin(z*4.5)+1.15*math.sin(y*.29)+.42*math.sin(y*.83))
  verts.append((xx+91,y,z))
for j in range(ny-1):
 for i in range(nx-1):
  a=j*nx+i; b=a+1; c=a+nx; d=c+1
  faces.extend([(a,b,d),(a,d,c)] if (i+j)%2 else [(a,b,c),(b,d,c)])
# Close the perimeter underneath the terrain.
edge=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+list(range(ny*nx-2,(ny-1)*nx-1,-1))+[j*nx for j in range(ny-2,0,-1)]
bottom=[]
for a in edge:
 bottom.append(len(verts)); x,y,z=verts[a]; verts.append((x,y,42))
for k,a in enumerate(edge):
 q=(k+1)%len(edge); faces.append((a,bottom[k],bottom[q],edge[q]))
faces.append(tuple(reversed(bottom)))
mesh=bpy.data.meshes.new('Fitted bedrock'); mesh.from_pydata(verts,[],faces); mesh.update()
obj=bpy.data.objects.new('SM_TerraceBedrock',mesh); bpy.context.collection.objects.link(obj); export(obj)
for v in range(3):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3,radius=1)
 obj=bpy.context.object; obj.name='SM_TerraceStone_'+str(v+1)
 for p in obj.data.vertices:
  co=p.co.copy(); n=noise.noise_vector(co*2.1+Vector((v*3,2,1)))
  p.co=Vector((co.x*1.5,co.y*1.15,co.z*.72))*(1+n.x*.18)
  p.co.z+=.06*math.sin(p.co.x*8+v)+.05*math.sin(p.co.y*11)
 export(obj)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Terrace-Rockface.blend'))
print('ROCKFACE_SOURCE_COMPLETE',flush=True)
