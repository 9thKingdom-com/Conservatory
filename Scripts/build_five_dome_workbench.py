"""Run in the live Blender file; preserve its existing scenes and create editable layout."""
import bpy, bmesh, math, json, os
import numpy as np
from mathutils import Matrix, Vector, Quaternion

ROOT = r'C:\Users\ASUS TUF\Documents\1 conservatory'
SOURCE = 'Cornice | profiled ring course.474'
SCENE = 'ASSEMBLY | Five domes - editable'

def components(mesh):
    parent = list(range(len(mesh.vertices)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for e in mesh.edges:
        a, b = map(find, e.vertices)
        parent[b] = a
    groups = {}
    for v in mesh.vertices:
        groups.setdefault(find(v.index), []).append(v.index)
    return list(groups.values())

def subset(source, omit, name):
    mesh = source.copy()
    bm = bmesh.new(); bm.from_mesh(mesh); bm.verts.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[bm.verts[i] for i in omit], context='VERTS')
    bm.to_mesh(mesh); bm.free(); mesh.name = name; mesh.update()
    return mesh

def prepare():
    assert bpy.context.mode == 'OBJECT'
    assert SCENE not in bpy.data.scenes, 'Layout scene already exists; inspect before rebuilding.'
    source_scene = bpy.context.scene
    src = bpy.data.objects[SOURCE]
    groups = components(src.data)
    assert len(groups) == 265, 'Source topology changed; re-inspect component identities.'
    # Each shared column/rib belongs to one bay, avoiding coincident duplicate assemblies.
    redundant = [26,27,28,29,30,76,77,78] + list(range(79,84)) + list(range(93,109)) + list(range(151,162)) + list(range(218,265))
    remove = {i for k in redundant for i in groups[k]}
    normal = subset(src.data, remove, 'Template | dome bay')
    # Retain the entrance arch and side pillars; remove infill, mullions and raised sill.
    opening = list(range(2,26)) + list(range(34,52)) + [148,149,150]
    portal = subset(src.data, remove | {i for k in opening for i in groups[k]}, 'Template | open arch bay')
    deps = bpy.context.evaluated_depsgraph_get()
    walkway = []
    for o in source_scene.objects:
        if o.name == 'WINDOWS_SMALL' or o.name == 'Torus.383' or o.name.startswith('Corridor | arch crown'):
            mesh = bpy.data.meshes.new_from_object(o.evaluated_get(deps), depsgraph=deps)
            mesh.transform(o.matrix_world)
            walkway.append((o.name, mesh))
    floors = [(o.name, o.data.copy(), o.matrix_world.copy()) for o in source_scene.objects if o.name.startswith('Corridor | foundation') or o.name.startswith('Corridor | side plinth') or o.name.startswith('PASSAGE-FLOOR')]
    for _, mesh, transform in floors:
        mesh.transform(transform)
    caps = []
    for o in source_scene.objects:
        if o.name.startswith('Cupola |'):
            mesh = o.data.copy(); mesh.transform(o.matrix_world); caps.append((o.name, mesh))
    state = dict(normal=normal, portal=portal, walkway=walkway, floors=floors, caps=caps, source_scene=source_scene.name)
    bpy.app.driver_namespace['five_dome_build'] = state
    print('Prepared editable source meshes:',len(normal.vertices),'vertices per bay;',len(portal.vertices),'per portal.')

def build():
    st = bpy.app.driver_namespace['five_dome_build']
    scene = bpy.data.scenes.new(SCENE)
    scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1
    bpy.context.window.scene = scene
    def collection(name):
        c=bpy.data.collections.new(name);scene.collection.children.link(c);return c
    def obj(name,mesh,c,transform=None):
        o=bpy.data.objects.new(name,mesh);c.objects.link(o)
        if transform is not None:o.matrix_world=transform
        return o
    def root(name,c,position,angle=0):
        o=obj(name,None,c);o.empty_display_type='PLAIN_AXES';o.empty_display_size=2
        o.location=position;o.rotation_euler.z=angle;return o
    def child(name,mesh,c,parent):
        o=obj(name,mesh,c);o.parent=parent;return o
    # End-frame centres define the complete walkway module, retaining its original cross-section.
    x0=19.4544;x1=28.5638;length=x1-x0
    small_socket=11.3675;large_socket=small_socket*1.5
    distance=large_socket+2*length+small_socket
    domes=[('Centre',24,1.5,(0,0,0),{0,6,12,18})]
    for label,angle in [('East',0),('North',math.pi/2),('West',math.pi),('South',3*math.pi/2)]:
        domes.append((label,16,1,(distance*math.cos(angle),distance*math.sin(angle),0),{(round(angle/(2*math.pi)*16)+8)%16}))
    for label,count,scale,position,portals in domes:
        c=collection('DOME | '+label);p=root(label+' | move whole dome',c,position)
        p['diameter_factor']=scale;p['bay_count']=count
        for i in range(count):
            mesh=(st['portal'] if i in portals else st['normal']).copy()
            mesh.name=f'{label} | bay {i+1:02d} editable mesh'
            if scale!=1:
                a=np.empty(len(mesh.vertices)*3);mesh.vertices.foreach_get('co',a);a=a.reshape((-1,3))
                r=np.linalg.norm(a[:,:2],axis=1)*scale;t=np.arctan2(a[:,1],a[:,0])/scale
                a[:,0]=r*np.cos(t);a[:,1]=r*np.sin(t)
                a[:,2]=np.where(a[:,2]>8.5,8.5+(a[:,2]-8.5)*scale,a[:,2])
                mesh.vertices.foreach_set('co',a.ravel());mesh.update()
            o=child(f'{label} | Bay {i+1:02d}'+(' | OPEN CONNECTION' if i in portals else ''),mesh,c,p)
            o.rotation_euler.z=i*math.tau/count
            o['editable']='Independent mesh; Tab enters Edit Mode.'
        for i,(_,source) in enumerate(st['caps']):
            mesh=source.copy()
            if scale!=1:
                mesh.transform(Matrix.Translation((0,0,8.5*(1-scale)))@Matrix.Diagonal((scale,scale,scale,1)))
            child(f'{label} | Cap {i+1:02d}',mesh,c,p)
        # Simple editable floor datum to make each mapped connection continuous.
        n=128;radius=11.3675*scale;verts=[(radius*math.cos(i*math.tau/n),radius*math.sin(i*math.tau/n),z) for z in [0.0037,0.118] for i in range(n)]
        faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
        mesh=bpy.data.meshes.new(label+' | floor mesh');mesh.from_pydata(verts,[],faces);mesh.update();child(label+' | Floor datum',mesh,c,p)
    for label,angle in [('East',0),('North',math.pi/2),('West',math.pi),('South',3*math.pi/2)]:
        c=collection('WALKWAY | '+label+' - two sections');p=root(label+' | move whole walkway',c,(0,0,0),angle)
        for section in range(2):
            start=large_socket+section*length
            for name,source in st['walkway']:
                mesh=source.copy();mesh.transform(Matrix.Translation((start-x0,0,0)))
                child(f'{label} | Section {section+1} | {name}',mesh,c,p)
            for name,source,_ in st['floors']:
                mesh=source.copy();a=np.empty(len(mesh.vertices)*3);mesh.vertices.foreach_get('co',a);a=a.reshape((-1,3));lo=a[:,0].min();hi=a[:,0].max()
                a[:,0]=start+(a[:,0]-lo)/(hi-lo)*length
                if 'foundation slab' in name:
                    if section==0:a[abs(a[:,0]-start)<.02,0]-=.30
                    else:a[abs(a[:,0]-(start+length))<.02,0]+=.30
                mesh.vertices.foreach_set('co',a.ravel());mesh.update();child(f'{label} | Section {section+1} | {name}',mesh,c,p)
    scene['layout_note']='One larger central dome; four original-size outer domes; two complete source walkway assemblies per connection. Editable Blender planning assembly.'
    scene['walkway_section_length']=length;scene['centre_diameter_factor']=1.5
    bpy.context.view_layer.update()
    for a in bpy.context.screen.areas:
        if a.type=='VIEW_3D':
            r=a.spaces.active.region_3d;r.view_location=(0,0,5);r.view_distance=155
            r.view_rotation=Quaternion((1,0,0),math.radians(32));r.view_perspective='ORTHO'
            a.spaces.active.clip_end=1000
    report={'scene':scene.name,'source_scene_preserved':st['source_scene'],'centre_factor':1.5,'centre_bays':24,'outer_domes':4,'outer_bays_each':16,'walkway_sections_each':2,'section_length_m':length,'outer_centre_distance_m':distance,'objects':len(scene.objects),'meshes':sum(o.type=='MESH' for o in scene.objects),'backup':bpy.app.driver_namespace.get('layout_backup'),'status':'Editable Blender assembly; visual and connection checks pending.'}
    bpy.app.driver_namespace['five_dome_report']=report
    print(json.dumps(report))

if __name__=='__main__':
    prepare()
