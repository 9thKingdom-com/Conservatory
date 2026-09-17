using UnrealBuildTool;
public class ConservatoryEditor : ModuleRules {
 public ConservatoryEditor(ReadOnlyTargetRules Target) : base(Target) {
  PCHUsage=PCHUsageMode.UseExplicitOrSharedPCHs;
  PublicDependencyModuleNames.AddRange(new string[]{"Core","CoreUObject","Engine","UnrealEd","Landscape","Conservatory","NavigationSystem","Foliage"});
 }
}
