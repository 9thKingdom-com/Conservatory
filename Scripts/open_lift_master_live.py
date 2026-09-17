import bpy
from pathlib import Path
P=Path('C:/Users/ASUS TUF/Documents/1 conservatory/Asset Chest/01 John Originals/LIFT-MASTER');P.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(P/'LIFT-MASTER.blend'))
def connect():
 try:
  if 'blender_mcp' not in bpy.context.preferences.addons:bpy.ops.preferences.addon_enable(module='blender_mcp')
  if not getattr(bpy.context.scene,'blendermcp_server_running',False):bpy.ops.blendermcp.start_server()
 except Exception as e:print('MCP startup:',e)
 return None
bpy.app.timers.register(connect,first_interval=2)
