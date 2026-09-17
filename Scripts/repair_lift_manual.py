import unreal as u,json,math,datetime,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR'
backup=ROOT/'Saved/Backups/LiftManual'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S');backup.mkdir(parents=True)
shutil.copy2(ROOT/'Content/Conservatory/Maps/L_Exterior_RobotVR.umap',backup/'L_Exterior_RobotVR.umap')
shutil.copytree(ROOT/'Content/Conservatory/Maps/_GENERATED/johnmaster',backup/'johnmaster')
w=u.EditorLoadingAndSavingUtils.load_map(MAP);sub=u.get_editor_subsystem(u.EditorActorSubsystem);actors=sub.get_all_level_actors()
by={a.get_name():a for a in actors};baseline=json.loads((ROOT/'Documentation/LiftManualBaseline.json').read_text())
def trans(a):
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d();return [p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z]
before={a.get_name():trans(a) for a in actors}
centre=next(a for a in actors if a.get_actor_label()=='Core habitat | Centre Floor')
theta=math.radians(centre.get_actor_rotation().yaw+135);yaw=math.degrees(theta)-180
p=centre.get_actor_location();pos=u.Vector(p.x+1530*math.cos(theta),p.y+1530*math.sin(theta),6244)
mesh=by['StaticMeshActor_1858'];old=mesh.get_actor_location();oldyaw=mesh.get_actor_rotation().yaw;delta=math.radians(yaw-oldyaw)
changed=['StaticMeshActor_1858','TextRenderActor_18','PointLight_36','ServiceLift_0']
with u.ScopedEditorTransaction('Reposition upper service lift and reconnect endpoints'):
 for name in changed[:3]:
  a=by[name];v=a.get_actor_location()-old;a.modify();a.set_actor_location(pos+u.Vector(v.x*math.cos(delta)-v.y*math.sin(delta),v.x*math.sin(delta)+v.y*math.cos(delta),v.z),False,False);a.set_actor_rotation(u.Rotator(pitch=0,yaw=yaw,roll=0),False)
 upper=by['ServiceLift_0'];lower=by['ServiceLift_1'];upper.modify();lower.modify()
 upper.set_actor_location(pos+u.Vector(0,0,92),False,False);upper.set_actor_rotation(u.Rotator(pitch=0,yaw=yaw,roll=0),False)
 upper.set_editor_property('destination',lower.get_actor_location());lower.set_editor_property('destination',upper.get_actor_location());lower.set_editor_property('destination_yaw',yaw)
unexpected=[a.get_name() for a in actors if a.get_name() not in changed and trans(a)!=before[a.get_name()]]
assert not unexpected,unexpected
assert len(actors)==len(baseline)
assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
(ROOT/'Documentation/LiftManualRepair.json').write_text(json.dumps(dict(engine=u.SystemLibrary.get_engine_version(),timestamp=datetime.datetime.now().isoformat(),backup=str(backup),map=MAP,upper_cm=trans(upper)[:3],yaw=yaw,changed_transforms=changed,changed_properties=['ServiceLift_1.destination','ServiceLift_1.destination_yaw'],unrelated_transform_changes=unexpected,actor_count=len(actors),landscapes=sum(a.get_class().get_name()=='Landscape' for a in actors)),indent=2))
print('LIFT_REPAIR_SAVED')
