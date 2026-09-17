"""Opt-in editor/game validation only. Normal project launches do nothing here."""
import unreal,sys
from pathlib import Path
if '-RobotAccessInspection' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import inspect_robot_access
if '-RobotVRShowcase' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import show_robot_vr
if '-RobotVRPhotos' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import photo_robot_vr
if '-RobotVRInspection' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import inspect_robot_vr
if '-IndoorDockInspection' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import inspect_indoor_dock
if '-TerrainRobotsInspection' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import inspect_terrain_robots
if '-WanderingBotsInspection' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import inspect_wandering_bots
if '-PassageDetailInspection' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import inspect_passage_detail
if '-TownTodayInspection' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import inspect_town_today
if '-RockfaceInspection' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import inspect_terrace_rockface
if '-LibraryInspection' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import inspect_hill_edge_play
if '-BunkerInspection' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import inspect_bunker_play
if '-HabitatPhotos' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import capture_habitat
if '-LandingInspection' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import inspect_landing
if '-ModularInspection' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import inspect_modular
if '-OrnateLiftInspection' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import inspect_ornate_lift

if '-IntercomInspection' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import inspect_intercoms


if '-C17Inspection' in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/'Scripts'))
    import inspect_c17


if "-R11Inspection" in unreal.SystemLibrary.get_command_line():
    sys.path.insert(0,str(Path(unreal.Paths.project_dir())/"Scripts"))
    import inspect_r11
