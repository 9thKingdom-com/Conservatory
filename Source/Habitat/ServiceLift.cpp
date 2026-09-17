#include "ServiceLift.h"
#include "Engine/GameViewportClient.h"
#include "Components/SceneComponent.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "Camera/PlayerCameraManager.h"
#include "InputCoreTypes.h"
#include "Engine/Engine.h"
#include "TimerManager.h"
AServiceLift::AServiceLift() {
 PrimaryActorTick.bCanEverTick = true;
 RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Station"));
}
void AServiceLift::Tick(float Dt) {
 Super::Tick(Dt);
 if(GetWorld()->GetGameViewport() && GetWorld()->GetGameViewport()->IgnoreInput()) return;
 auto* PC = UGameplayStatics::GetPlayerController(this,0);
 APawn* Pawn = PC ? PC->GetPawn().Get() : nullptr;
 if(Pawn && Pawn->ActorHasTag(TEXT("RobotEmbodied")))return;
 if (Pawn && GetActorLocation().Z > 5000 && PC->WasInputKeyJustPressed(EKeys::Home)) {
  if (auto* C=Cast<ACharacter>(Pawn)) C->GetCharacterMovement()->StopMovementImmediately();
  Pawn->SetActorLocation(FVector(-10600,0,6350),false,nullptr,ETeleportType::TeleportPhysics);
  PC->SetControlRotation(FRotator(-5,0,0));
 }
 if (!Pawn || FVector::Dist(Pawn->GetActorLocation(),GetActorLocation()) > 230) return;
 if (GEngine) GEngine->AddOnScreenDebugMessage(uint64(GetUniqueID()),0.1f,FColor(190,225,215),FString::Printf(TEXT("[E] Service lift - %s"),*DestinationName));
 if (PC->WasInputKeyJustPressed(EKeys::E)) Travel();
}
bool AServiceLift::Travel() {
 auto* PC = UGameplayStatics::GetPlayerController(this,0);
 APawn* Pawn = PC ? PC->GetPawn().Get() : nullptr;
 if (!Pawn || GetWorld()->GetTimeSeconds()<ReadyAt || FVector::Dist(Pawn->GetActorLocation(),GetActorLocation())>230) return false;
 ReadyAt=GetWorld()->GetTimeSeconds()+2;
 PC->PlayerCameraManager->StartCameraFade(0,1,.3f,FLinearColor::Black,false,true);
 FTimerHandle Handle;
 GetWorldTimerManager().SetTimer(Handle,FTimerDelegate::CreateWeakLambda(this,[this]() {
  auto* Controller=UGameplayStatics::GetPlayerController(this,0);
  if (!Controller || !Controller->GetPawn()) return;
  if (auto* C=Cast<ACharacter>(Controller->GetPawn())) C->GetCharacterMovement()->StopMovementImmediately();
  Controller->GetPawn()->SetActorLocation(Destination,false,nullptr,ETeleportType::TeleportPhysics);
  Controller->SetControlRotation(FRotator(0,DestinationYaw,0));
  Controller->PlayerCameraManager->StartCameraFade(1,0,.4f,FLinearColor::Black,false,false);
 }),.35f,false);
 return true;
}


