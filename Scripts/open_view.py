"""Optional editor startup view; does not rebuild or alter scene assets."""
import unreal
editor=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
editor.set_level_viewport_camera_info(unreal.Vector(-13300,-3200,6450),unreal.Rotator(pitch=4,yaw=145,roll=0),'')
