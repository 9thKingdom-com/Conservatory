using UnrealBuildTool;
public class Habitat : ModuleRules {
 public Habitat(ReadOnlyTargetRules Target) : base(Target) {
  PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
  PublicDependencyModuleNames.AddRange(new string[]{"Core","CoreUObject","Engine","InputCore"});
 }
}
