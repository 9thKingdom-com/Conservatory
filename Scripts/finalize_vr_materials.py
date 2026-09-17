import unreal as u
mat=u.load_asset('/Game/Conservatory/Robots/VR/M_HapticFabric')
u.MaterialEditingLibrary.set_material_usage(mat,u.MaterialUsage.MATUSAGE_SKELETAL_MESH)
u.MaterialEditingLibrary.recompile_material(mat)
assert u.EditorAssetLibrary.save_loaded_asset(mat)
