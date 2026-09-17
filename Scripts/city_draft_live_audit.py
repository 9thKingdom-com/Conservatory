import unreal as u,json
from pathlib import Path
R=Path(u.Paths.project_dir()).resolve();sub=u.get_editor_subsystem(u.EditorActorSubsystem);w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();actors=sub.get_all_level_actors();rows=[]
for a in actors:
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d();row=dict(name=a.get_name(),label=a.get_actor_label(),cls=a.get_class().get_name(),pos=[p.x,p.y,p.z],rot=[r.pitch,r.yaw,r.roll],scale=[s.x,s.y,s.z])
 if isinstance(a,u.StaticMeshActor):
  m=a.static_mesh_component.static_mesh;row['mesh']=m.get_path_name() if m else None
 rows.append(row)
land=next(a for a in actors if a.get_class().get_name()=='Landscape')
out=dict(map=w.get_path_name(),dirty_maps=[p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()],dirty_assets=[p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()],actors=rows,landscape_api=[n for n in dir(land) if 'height' in n or 'spline' in n],actor_component_api=[n for n in dir(land) if 'component' in n])
(R/'Documentation/CityRoadDraftBaseline.json').write_text(json.dumps(out,indent=2));print('CITY_DRAFT_AUDIT_DONE')
m=land.get_editor_property('landscape_material')
extra=dict(material=m.get_path_name(),material_class=m.get_class().get_name(),material_api=[n for n in dir(u.MaterialEditingLibrary) if 'input' in n or 'connection' in n])
(R/'Documentation/CityRoadMaterialAudit.json').write_text(json.dumps(extra,indent=2))
