"""Check navigation from the terrain beyond every approach into its rear room."""
import unreal as u,json,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'Scripts'))
from layout import height
w=u.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior_RobotVR');u.ExteriorTools.build_terrain_navigation()
checks=[]
for b in json.loads((root/'SourceAssets/ValleySettlements/layout.json').read_text())['buildings']:
 sgn=1 if b['yaw']==0 else -1;x=b['x'];y=b['y']+sgn*(b['d']/2+13.8)
 start=u.Vector(x*100,y*100,(height(x,y)+.35)*100);end=u.Vector(*[v*100 for v in b['rear']])
 path=u.NavigationSystemV1.find_path_to_location_synchronously(w,start,end)
 checks.append({'id':b['id'],'from_terrain_cm':[start.x,start.y,start.z],'passed':bool(path and path.is_valid() and not path.is_partial()),'path_points':[[p.x,p.y,p.z] for p in path.path_points] if path else []})
(root/'Documentation/ValleyApproachNavigation.json').write_text(json.dumps({'checks':checks,'passed':all(c['passed'] for c in checks)},indent=2))
print('VALLEY_APPROACH_NAVIGATION',sum(c['passed'] for c in checks),len(checks))
