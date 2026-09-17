import unreal as u
for name in ['SM_OldTrack','SM_DistantHills','SM_Cottage_1','SM_Oak_1']:
 mesh=u.load_asset('/Game/Conservatory/Environment/Meshes/'+name)
 print('ASSET_BOUNDS '+name+' '+str(mesh.get_bounds()),flush=True)
