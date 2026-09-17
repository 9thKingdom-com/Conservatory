using UnrealBuildTool;
public class Conservatory : ModuleRules {
 public Conservatory(ReadOnlyTargetRules Target) : base(Target) {
  PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
  PublicDependencyModuleNames.AddRange(new string[]{"Core","CoreUObject","Engine","InputCore","HTTP","Json","Slate","SlateCore","MediaAssets","AudioMixer","NavigationSystem","AIModule"});
 }
}


