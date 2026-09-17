import re
# Resume verification after rejecting pointer-bearing struct string comparisons.
def stable(s):return re.sub(r'0x[0-9A-Fa-f]+','PTR',s)
unexpected=[a.get_name() for a in actors if a not in bots and stable(str(a.get_actor_transform()))!=stable(before[a.get_name()])]
assert not unexpected,unexpected
assert all(abs(a.get_actor_location().z-p.z)<0.01 for a,p,row in plans)
assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
report=dict(timestamp=datetime.datetime.now().isoformat(),engine=u.SystemLibrary.get_engine_version(),backup=str(backup),robots=[row for a,p,row in plans],unrelated_changes=unexpected,actor_count=len(actors),saved=True,dirty_maps=[p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
(R/'Documentation/RobotGroundRepair.json').write_text(json.dumps(report,indent=2))
print('ROBOT_GROUND_REPAIR_SAVED')
