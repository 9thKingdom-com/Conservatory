import bpy,json
print('SCENES',[(s.name,len(s.objects)) for s in bpy.data.scenes])
for o in bpy.data.objects:
 if o.type=='EMPTY' or o.modifiers:
  if o.type=='EMPTY' or any(m.type=='NODES' for m in o.modifiers):
   print(o.name,dict(o.items()),[(m.name,m.type) for m in o.modifiers], 'instance',o.instance_type, o.instance_collection.name if o.instance_collection else '', 'parent',o.parent.name if o.parent else '')
print('ACTIVE',bpy.context.scene.name)
print('INSTANCES',sum(1 for i in bpy.context.evaluated_depsgraph_get().object_instances))
