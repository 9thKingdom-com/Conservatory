import unreal as u,sys
sys.path.insert(0,'C:/Users/ASUS TUF/Documents/1 conservatory/Scripts')
from seal_bunker_joints import seal
w=u.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior_Library')
assert w
seal(w)
assert u.EditorLoadingAndSavingUtils.save_map(w,'/Game/Conservatory/Maps/L_Exterior_Sealed')
