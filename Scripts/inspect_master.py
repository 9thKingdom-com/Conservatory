import bpy,json
from pathlib import Path
p=Path('C:/Users/ASUS TUF/Documents/1 conservatory/Documentation/MasterInspection.json')
r={'units':bpy.context.scene.unit_settings.scale_length,'objects':[{'name':o.name,'type':o.type,'location':list(o.location),'dimensions':list(o.dimensions),'rotation':list(o.rotation_euler),'properties':{k:str(o[k]) for k in o.keys()}} for o in bpy.data.objects]}
p.write_text(json.dumps(r,indent=2))
print(json.dumps(r))
