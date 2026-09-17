"""Add optional IK authoring controls to a separate Blender workbench copy.
Baked exported actions remain unchanged; default influence is zero.
"""
import bpy
from mathutils import Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];arm=bpy.data.objects['C17_Rig'];arm.animation_data_clear()
for p in arm.pose.bones:p.matrix_basis.identity()
bpy.context.view_layer.objects.active=arm;bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
for side,s in [('l',1),('r',-1)]:
 for limb,tip,pole in [('arm','hand_'+side,(s*.6,.22,1.0)),('leg','foot_'+side,(s*.15,-.55,.46))]:
  src=arm.data.edit_bones[tip];c=arm.data.edit_bones.new('CTRL_'+limb+'_'+side);c.head=src.head;c.tail=src.tail;c.roll=src.roll;c.use_deform=False
  p=arm.data.edit_bones.new('POLE_'+limb+'_'+side);p.head=pole;p.tail=Vector(pole)+Vector((0,0,.08));p.use_deform=False
bpy.ops.object.mode_set(mode='POSE');arm['IK Authoring']=0.0;arm.id_properties_ui('IK Authoring').update(min=0,max=1,description='0: play baked clips. 1: pose using CTRL / POLE bones for a new action.')
collection=arm.data.collections.new('IK authoring controls')
for side in ['l','r']:
 for limb,lower in [('arm','lowerarm_'+side),('leg','calf_'+side)]:
  c=arm.pose.bones[lower].constraints.new('IK');c.name='Optional authoring IK';c.target=arm;c.subtarget='CTRL_'+limb+'_'+side;c.pole_target=arm;c.pole_subtarget='POLE_'+limb+'_'+side;c.chain_count=2;c.use_stretch=False
  f=c.driver_add('influence');d=f.driver;d.type='AVERAGE';v=d.variables.new();v.name='ik';v.type='SINGLE_PROP';v.targets[0].id=arm;v.targets[0].data_path='["IK Authoring"]'
  for prefix in ['CTRL_','POLE_']:collection.assign(arm.data.bones[prefix+limb+'_'+side]);arm.pose.bones[prefix+limb+'_'+side].color.palette='THEME04'
bpy.ops.object.mode_set(mode='OBJECT');bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'SourceAssets/C17/C17-AnimationRig.blend'))
