"""Opt-in playable kitchen start for reviewing the VR system; normal starts are unchanged."""
import unreal as u
def tick(dt):
 world=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR')
 if not world:return
 player=u.GameplayStatics.get_player_character(world,0)
 if not player:return
 player.set_actor_location(u.Vector(-13470,1350,4090),False,False)
 player.character_movement.stop_movement_immediately()
 u.GameplayStatics.get_player_controller(world,0).set_control_rotation(u.Rotator(pitch=7,yaw=0,roll=0))
 u.log('ROBOT_VR_SHOWCASE_READY - player at kitchen monitor')
 u.unregister_slate_post_tick_callback(handle)
handle=u.register_slate_post_tick_callback(tick)
