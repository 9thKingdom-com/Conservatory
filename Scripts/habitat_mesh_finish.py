"""Correct inverted closed solids and select restrained moulding accents for export."""
import bmesh

def finish(mesh, brass_index=None):
    bm=bmesh.new();bm.from_mesh(mesh)
    seen=set();fixed=0
    for start in bm.verts:
        if start in seen: continue
        todo=[start];verts=set()
        while todo:
            v=todo.pop()
            if v in verts: continue
            verts.add(v);todo.extend(e.other_vert(v) for e in v.link_edges)
        seen.update(verts)
        faces={f for v in verts for f in v.link_faces}
        edges={e for v in verts for e in v.link_edges}
        if faces and all(e.is_manifold for e in edges):
            volume=sum(f.calc_area()*f.normal.dot(f.calc_center_median())/3 for f in faces)
            if volume < -0.000001:
                bmesh.ops.reverse_faces(bm,faces=list(faces));fixed+=1
        lo=min(v.co.z for v in verts);hi=max(v.co.z for v in verts)
        if brass_index is not None and ((.20<lo and hi<.85 and hi-lo<.13) or (5.0<lo and hi<6.1 and hi-lo<.12)):
            for f in faces:f.material_index=brass_index
    bm.to_mesh(mesh);bm.free();mesh.update()
    return fixed
