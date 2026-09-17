using UnrealBuildTool;
public class ConservatoryTarget : TargetRules {
 public ConservatoryTarget(TargetInfo Target) : base(Target) {
  Type = TargetType.Game; DefaultBuildSettings = BuildSettingsVersion.V7;
  IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_8; ExtraModuleNames.Add("Conservatory");
 }
}
