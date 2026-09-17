#include "VRSuitStation.h"
#include "RobotVRHub.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SphereComponent.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/StaticMesh.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/ConstructorHelpers.h"
#include "Materials/MaterialInterface.h"
AVRSuitStation::AVRSuitStation(){
 PrimaryActorTick.bCanEverTick=true;RootComponent=CreateDefaultSubobject<USceneComponent>(TEXT("SuitRack"));
 Suit=CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("HapticSuit"));Suit->SetupAttachment(RootComponent);
 static ConstructorHelpers::FObjectFinder<USkeletalMesh> Asset(TEXT("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple"));Suit->SetSkeletalMesh(Asset.Object);Suit->SetRelativeRotation(FRotator(0,-90,0));Suit->SetCollisionEnabled(ECollisionEnabled::NoCollision);
 static ConstructorHelpers::FObjectFinder<UStaticMesh> Cube(TEXT("/Engine/BasicShapes/Cube.Cube"));
 auto* Rack=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("RackBack"));Rack->SetupAttachment(RootComponent);Rack->SetStaticMesh(Cube.Object);Rack->SetRelativeLocation(FVector(-30,0,106));Rack->SetRelativeScale3D(FVector(.10,.78,2.12));
 auto* Base=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("RackBase"));Base->SetupAttachment(RootComponent);Base->SetStaticMesh(Cube.Object);Base->SetRelativeLocation(FVector(-8,0,2));Base->SetRelativeScale3D(FVector(.65,.82,.04));
 auto* Headset=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("VRHeadset"));Headset->SetupAttachment(RootComponent);Headset->SetStaticMesh(Cube.Object);Headset->SetRelativeLocation(FVector(13,0,172));Headset->SetRelativeScale3D(FVector(.16,.26,.12));Headset->SetCollisionEnabled(ECollisionEnabled::NoCollision);
 auto* Range=CreateDefaultSubobject<USphereComponent>(TEXT("InteractionRange"));Range->SetupAttachment(RootComponent);Range->SetRelativeLocation(FVector(0,0,90));Range->SetSphereRadius(210.f);Range->SetCollisionEnabled(ECollisionEnabled::NoCollision);Range->SetHiddenInGame(true);
}
float AVRSuitStation::GetUseScore() const{
 auto* PC=UGameplayStatics::GetPlayerController(this,0);APawn* Pawn=PC?PC->GetPawn():nullptr;
 if(!Pawn || !IsValid(Hub) || Hub->IsRemote() || FVector::Dist(Pawn->GetActorLocation(),GetActorTransform().TransformPosition(FVector(0,0,90)))>210)return -1;
 FVector Eye;FRotator View;PC->GetPlayerViewPoint(Eye,View);
 FCollisionQueryParams Params;Params.AddIgnoredActor(Pawn);float Best=-1;
 // Waist, chest and headset targets follow the rack's transform. Looking at
 // the headset at close range must not require aiming down at the chest.
 for(float Height:{80.f,120.f,170.f}){
  const FVector Target=GetActorTransform().TransformPosition(FVector(0,0,Height));
  const float Score=FVector::DotProduct(View.Vector(),(Target-Eye).GetSafeNormal());
  if(Score<.9f || Score<=Best)continue;
  FHitResult Hit;
  if(!GetWorld()->LineTraceSingleByChannel(Hit,Eye,Target,ECC_Visibility,Params) || Hit.GetActor()==this)Best=Score;
 }
 return Best;
}
bool AVRSuitStation::CanUse() const{
 const float Score=GetUseScore();if(Score<0)return false;
 for(TActorIterator<AVRSuitStation> It(GetWorld());It;++It){
  if(*It==this)continue;
  const float Other=It->GetUseScore();
  if(Other>Score+KINDA_SMALL_NUMBER || (Other>=0 && FMath::IsNearlyEqual(Other,Score) && It->GetUniqueID()<GetUniqueID()))return false;
 }
 return true;
}
void AVRSuitStation::BeginPlay(){
 Super::BeginPlay();
 auto* RackMaterial=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Conservatory/Robots/VR/M_RackEnamel.M_RackEnamel"));
 auto* VisorMaterial=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Conservatory/Robots/VR/M_Headset.M_Headset"));
 TInlineComponentArray<UStaticMeshComponent*> Parts(this);
 for(auto* Part:Parts)if(auto* Material=Part->GetFName()==TEXT("VRHeadset")?VisorMaterial:RackMaterial)Part->SetMaterial(0,Material);
}
void AVRSuitStation::Tick(float D){Super::Tick(D);if(!CanUse())return;auto* PC=UGameplayStatics::GetPlayerController(this,0);if(PC->bShowMouseCursor)return;if(GEngine)GEngine->AddOnScreenDebugMessage(uint64(GetUniqueID()),.1f,FColor(185,235,220),FString::Printf(TEXT("[F] Wear VR suit %02d - become robot %02d outside"),RobotId,RobotId));if(PC->WasInputKeyJustPressed(EKeys::F))WearSuit();}
bool AVRSuitStation::WearSuit(){return CanUse() && Hub->EnterRobot(RobotId);}
