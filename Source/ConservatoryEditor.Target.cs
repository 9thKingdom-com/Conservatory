using UnrealBuildTool;
public class ConservatoryEditorTarget : TargetRules {
 public ConservatoryEditorTarget(TargetInfo Target) : base(Target) {
  Type = TargetType.Editor; DefaultBuildSettings = BuildSettingsVersion.V7;
  IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_8; ExtraModuleNames.AddRange(new string[]{"Conservatory","ConservatoryEditor"});
 }
}
