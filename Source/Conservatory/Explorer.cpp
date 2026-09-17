#include "Explorer.h"
#include "CidcoreIntercom.h"
#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Engine/World.h"
#include "Engine/GameViewportClient.h"
#include "Framework/Application/IInputProcessor.h"
#include "Framework/Application/SlateApplication.h"
#include "Input/Events.h"

// Runs before UI widgets, so text fields and robot panels cannot swallow Escape.
class FDesktopExitInput final : public IInputProcessor {
public:
 virtual void Tick(float, FSlateApplication&, TSharedRef<ICursor>) override {}
 virtual bool HandleKeyDownEvent(FSlateApplication&, const FKeyEvent& Event) override {
  if(Event.GetKey()!=EKeys::Escape) return false;
  UE_LOG(LogTemp,Display,TEXT("Escape pressed: closing standalone game."));
  FPlatformMisc::RequestExit(false);
  return true;
 }
};
AExplorer::AExplorer() {
 Intercom=CreateDefaultSubobject<UCidcoreIntercom>(TEXT("CIDCORE"));
 PrimaryActorTick.bCanEverTick=true;
 GetCapsuleComponent()->InitCapsuleSize(34,88);
 auto* Camera=CreateDefaultSubobject<UCameraComponent>(TEXT("Eyes"));
 Camera->SetupAttachment(GetCapsuleComponent()); Camera->SetRelativeLocation(FVector(0,0,66)); Camera->bUsePawnControlRotation=true;
 Camera->FieldOfView=85;
 GetCharacterMovement()->MaxWalkSpeed=380; GetCharacterMovement()->MaxStepHeight=48;
 GetCharacterMovement()->SetWalkableFloorAngle(48); GetCharacterMovement()->JumpZVelocity=420;
}
void AExplorer::SetupPlayerInputComponent(UInputComponent* I) {
 Super::SetupPlayerInputComponent(I);
 I->BindKey(EKeys::C,IE_Pressed,this,&AExplorer::OpenIntercom);
 I->BindAxis("Forward",this,&AExplorer::Forward); I->BindAxis("Right",this,&AExplorer::Right);
 I->BindAxis("Look",this,&AExplorer::Look); I->BindAxis("Turn",this,&AExplorer::Turn);
 I->BindAction("Jump",IE_Pressed,this,&ACharacter::Jump); I->BindAction("Jump",IE_Released,this,&ACharacter::StopJumping);
 I->BindAction("Run",IE_Pressed,this,&AExplorer::Run); I->BindAction("Run",IE_Released,this,&AExplorer::Walk);
 I->BindAction("Return",IE_Pressed,this,&AExplorer::ResetView);
}
void AExplorer::OpenIntercom() { Intercom->Toggle(); }
void AExplorer::Forward(float V) { if(Controller) AddMovementInput(FRotationMatrix(FRotator(0,Controller->GetControlRotation().Yaw,0)).GetUnitAxis(EAxis::X),V); }
void AExplorer::Right(float V) { if(Controller) AddMovementInput(FRotationMatrix(FRotator(0,Controller->GetControlRotation().Yaw,0)).GetUnitAxis(EAxis::Y),V); }
void AExplorer::Look(float V) { AddControllerPitchInput(V); }
void AExplorer::Turn(float V) { AddControllerYawInput(V); }
void AExplorer::Run() { GetCharacterMovement()->MaxWalkSpeed=700; }
void AExplorer::Walk() { GetCharacterMovement()->MaxWalkSpeed=380; }
void AExplorer::ResetView() { SetActorLocation(FVector(-10500,-2000,6100),false); GetCharacterMovement()->StopMovementImmediately(); if(Controller) Controller->SetControlRotation(FRotator(-9,4,0)); }
void AExplorer::Tick(float D) {
 Super::Tick(D); if(GetActorLocation().Z < -7000) ResetView();
 if(!FParse::Param(FCommandLine::Get(),TEXT("ExteriorSmokeTest"))) return;
 if(InspectionTime==0) { if(Controller) Controller->SetIgnoreLookInput(true); }
 InspectionTime+=D;
 if(InspectionTime>5 && InspectionStage==0) {
  InspectionStart=GetActorLocation(); InspectionStage=1;
  UE_LOG(LogTemp,Display,TEXT("EXTERIOR_TEST start=%s grounded=%d"),*InspectionStart.ToString(),GetCharacterMovement()->IsMovingOnGround());
 }
 if(InspectionTime>5 && InspectionTime<9) Forward(1);
 if(InspectionTime>10 && InspectionStage==1) {
  const float Distance=FVector::Dist2D(GetActorLocation(),InspectionStart);
  const bool Passed=GetCharacterMovement()->IsMovingOnGround() && Distance>1000 && FMath::Abs(InspectionStart.Z-5906)<100;
  FString Result=FString::Printf(TEXT("{\"passed\":%s,\"walk_distance_cm\":%.1f,\"start_z_cm\":%.1f,\"grounded\":%s}"),Passed?TEXT("true"):TEXT("false"),Distance,InspectionStart.Z,GetCharacterMovement()->IsMovingOnGround()?TEXT("true"):TEXT("false"));
  FFileHelper::SaveStringToFile(Result,*(FPaths::ProjectSavedDir()/TEXT("WalkTest.json")));
  UE_LOG(LogTemp,Display,TEXT("EXTERIOR_TEST %s"),*Result);
  ResetView(); InspectionStage=2;
 }
 if(InspectionTime>14 && InspectionStage==2) { UE_LOG(LogTemp,Display,TEXT("EXTERIOR_CAMERA %s location=%s"),*GetControlRotation().ToString(),*GetActorLocation().ToString()); FScreenshotRequest::RequestScreenshot(FPaths::ProjectSavedDir()/TEXT("Screenshots/Hilltop.png"),false,false); InspectionStage=3; }
 if(InspectionTime>17 && InspectionStage==3) {
  FHitResult Hit; FCollisionQueryParams Params; Params.AddIgnoredActor(this);
  const FVector Above(12000,-10500,15000), Below(12000,-10500,-5000);
  if(GetWorld()->LineTraceSingleByChannel(Hit,Above,Below,ECC_Visibility,Params)) SetActorLocation(Hit.Location+FVector(0,0,100));
  GetCharacterMovement()->StopMovementImmediately(); if(Controller) Controller->SetControlRotation(FRotator(-2,40,0)); InspectionStage=4;
 }
 if(InspectionTime>22 && InspectionStage==4) {
  UE_LOG(LogTemp,Display,TEXT("EXTERIOR_VILLAGE grounded=%d location=%s"),GetCharacterMovement()->IsMovingOnGround(),*GetActorLocation().ToString());
  FScreenshotRequest::RequestScreenshot(FPaths::ProjectSavedDir()/TEXT("Screenshots/Village.png"),false,false); InspectionStage=5;
 }
 if(InspectionTime>25 && InspectionStage==5) {
  SetActorLocation(FVector(-13300,-3200,6400)); GetCharacterMovement()->StopMovementImmediately();
  if(Controller) Controller->SetControlRotation(FRotator(4,145,0)); InspectionStage=6;
 }
 if(InspectionTime>29 && InspectionStage==6) {
  FScreenshotRequest::RequestScreenshot(FPaths::ProjectSavedDir()/TEXT("Screenshots/Conservatory.png"),false,false); InspectionStage=7;
 }
 if(InspectionTime>32 && InspectionStage==7) {
  SetActorLocation(FVector(-17500,0,6400)); GetCharacterMovement()->StopMovementImmediately();
  if(Controller) Controller->SetControlRotation(FRotator(0,90,0)); InspectionStart=GetActorLocation(); InspectionStage=8;
 }
 if(InspectionStage==8 && InspectionTime>32.5 && InspectionTime<35.5) Forward(1);
 if(InspectionTime>36 && InspectionStage==8) {
  const float Distance=FVector::Dist2D(GetActorLocation(),InspectionStart);
  const bool Passed=GetCharacterMovement()->IsMovingOnGround() && Distance>700 && FMath::Abs(GetActorLocation().Z-6318)<20;
  const FString Result=FString::Printf(TEXT("{\"passed\":%s,\"walk_distance_cm\":%.1f,\"capsule_z_cm\":%.1f,\"grounded\":%s}"),Passed?TEXT("true"):TEXT("false"),Distance,GetActorLocation().Z,GetCharacterMovement()->IsMovingOnGround()?TEXT("true"):TEXT("false"));
  FFileHelper::SaveStringToFile(Result,*(FPaths::ProjectSavedDir()/TEXT("InteriorTest.json")));
  UE_LOG(LogTemp,Display,TEXT("CONSERVATORY_INTERIOR %s"),*Result);
  FScreenshotRequest::RequestScreenshot(FPaths::ProjectSavedDir()/TEXT("Screenshots/Interior.png"),false,false); InspectionStage=9;
 }
 if(InspectionTime>39 && InspectionStage==9) { FPlatformMisc::RequestExit(false); InspectionStage=10; }
}
AConservatoryGameMode::AConservatoryGameMode() { DefaultPawnClass=AExplorer::StaticClass(); }
void AConservatoryGameMode::BeginPlay() {
 Super::BeginPlay();
 // Never quit the editor process: PIE keeps its normal Stop Play shortcut.
 if(!GIsEditor && GetWorld()->WorldType==EWorldType::Game && FSlateApplication::IsInitialized()) {
  DesktopExitInput=MakeShared<FDesktopExitInput>();
  FSlateApplication::Get().RegisterInputPreProcessor(DesktopExitInput,0);
 }
}
void AConservatoryGameMode::EndPlay(const EEndPlayReason::Type Reason) {
 if(DesktopExitInput && FSlateApplication::IsInitialized())
  FSlateApplication::Get().UnregisterInputPreProcessor(DesktopExitInput);
 DesktopExitInput.Reset();
 Super::EndPlay(Reason);
}

