import bpy
from pathlib import Path
root=Path('C:/Users/ASUS TUF/Documents/1 conservatory/Asset Chest/01 John Originals/LIFT-MASTER/FabRelease/v1.0')
bpy.ops.wm.open_mainfile(filepath=str(root/'Product/Blender/LIFT-MASTER.blend'))
cache={}
def local_tree(ng):
 if ng in cache:return cache[ng]
 result=ng.copy() if ng.library else ng;cache[ng]=result
 for node in result.nodes:
  if node.type=='GROUP' and node.node_tree:node.node_tree=local_tree(node.node_tree)
 return result
for ob in bpy.data.objects:
 for mod in ob.modifiers:
  if mod.type=='NODES' and mod.node_group:mod.node_group=local_tree(mod.node_group)
for ng in list(bpy.data.node_groups):
 if ng.library:ng.use_fake_user=False
bpy.data.orphans_purge(do_local_ids=True,do_linked_ids=True,do_recursive=True)
assert not [x for x in bpy.data.user_map() if x.library]
while bpy.data.libraries:bpy.data.libraries.remove(bpy.data.libraries[0])
assert not bpy.data.libraries
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(root/'Product/Blender/LIFT-MASTER.blend'))
