#include "IntercomStation.h"
#include "CidcoreIntercom.h"
#include "Components/StaticMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "UObject/ConstructorHelpers.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/Pawn.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Engine/GameViewportClient.h"
AIntercomStation::AIntercomStation() {
 PrimaryActorTick.bCanEverTick=true;
 RootComponent=CreateDefaultSubobject<USceneComponent>(TEXT("Station"));
 static ConstructorHelpers::FObjectFinder<UStaticMesh> Cube(TEXT("/Engine/BasicShapes/Cube.Cube"));
 static ConstructorHelpers::FObjectFinder<UMaterialInterface> Brass(TEXT("/Game/Conservatory/Architecture/Intercom/M_Brass.M_Brass"));
 static ConstructorHelpers::FObjectFinder<UMaterialInterface> Enamel(TEXT("/Game/Conservatory/Architecture/Intercom/M_Enamel.M_Enamel"));
 static ConstructorHelpers::FObjectFinder<UMaterialInterface> Dark(TEXT("/Game/Conservatory/Architecture/Intercom/M_Speaker.M_Speaker"));
 static ConstructorHelpers::FObjectFinder<UMaterialInterface> Transmit(TEXT("/Game/Conservatory/Architecture/Intercom/M_Transmit.M_Transmit"));
 auto Box=[&](FName Name,FVector Position,FVector Size) {
  auto* C=CreateDefaultSubobject<UStaticMeshComponent>(Name);C->SetupAttachment(RootComponent);C->SetStaticMesh(Cube.Object);const FString N=Name.ToString();C->SetMaterial(0,N==TEXT("BrassHousing") || N==TEXT("ButtonBezel")?Brass.Object:N==TEXT("TransmitLamp")?Transmit.Object:N.StartsWith(TEXT("Speaker"))?Dark.Object:Enamel.Object);C->SetRelativeLocation(Position);C->SetRelativeScale3D(Size/100.f);C->SetCollisionEnabled(ECollisionEnabled::QueryOnly);C->SetCollisionResponseToAllChannels(ECR_Block);return C;
 };
 Box(TEXT("BrassHousing"),FVector(0,0,0),FVector(8,40,58));
 Box(TEXT("EnamelFace"),FVector(4.5,0,0),FVector(2,35,53));
 for(int I=0;I<7;++I) Box(FName(*FString::Printf(TEXT("SpeakerSlot%d"),I)),FVector(6,0,5+I*2),FVector(1,25,.65));
 Box(TEXT("ButtonBezel"),FVector(6,0,-15),FVector(3,12,9));
 Box(TEXT("TalkButton"),FVector(8,0,-15),FVector(2,9,6));
 Lamp=Box(TEXT("TransmitLamp"),FVector(6,12,22),FVector(1.5,3,3));
 auto* Text=CreateDefaultSubobject<UTextRenderComponent>(TEXT("Label"));Text->SetupAttachment(RootComponent);Text->SetRelativeLocation(FVector(6,0,-1));Text->SetHorizontalAlignment(EHTA_Center);Text->SetVerticalAlignment(EVRTA_TextCenter);Text->SetWorldSize(3.5);Text->SetText(FText::FromString(TEXT("CIDCORE\n[F] SPEAK")));Text->SetTextRenderColor(FColor(235,212,155));
}
void AIntercomStation::BeginPlay() {Super::BeginPlay();LampMaterial=Lamp->CreateDynamicMaterialInstance(0);}
bool AIntercomStation::CanUse(APawn* Pawn) const {
 if(!Pawn || FVector::Dist(Pawn->GetActorLocation(),GetActorLocation())>220) return false;
 auto* PC=Cast<APlayerController>(Pawn->GetController());if(!PC)return false;
 FVector Eye;FRotator View;PC->GetPlayerViewPoint(Eye,View);
 if(FVector::DotProduct(View.Vector(),(GetActorLocation()-Eye).GetSafeNormal())<.65f) return false;
 FHitResult Hit;FCollisionQueryParams Params;Params.AddIgnoredActor(Pawn);
 return GetWorld()->LineTraceSingleByChannel(Hit,Eye,GetActorLocation(),ECC_Visibility,Params) && Hit.GetActor()==this;
}
bool AIntercomStation::Interact() {
 auto* Pawn=UGameplayStatics::GetPlayerPawn(this,0);
 if(GetWorld()->GetGameViewport() && GetWorld()->GetGameViewport()->IgnoreInput())return false;
 if(!CanUse(Pawn))return false;
 if(auto* Intercom=Pawn->FindComponentByClass<UCidcoreIntercom>()){Intercom->Toggle();return true;}return false;
}
void AIntercomStation::Tick(float D) {
 Super::Tick(D);auto* Pawn=UGameplayStatics::GetPlayerPawn(this,0);if(!Pawn)return;
 auto* Intercom=Pawn->FindComponentByClass<UCidcoreIntercom>();
 if(LampMaterial)LampMaterial->SetVectorParameterValue(TEXT("Color"),Intercom && Intercom->IsTransmitting()?FLinearColor(2.f,.65f,.04f):FLinearColor(.006f,.008f,.008f));
 if(GetWorld()->GetGameViewport() && GetWorld()->GetGameViewport()->IgnoreInput())return;
 if(!CanUse(Pawn))return;
 if(GEngine)GEngine->AddOnScreenDebugMessage(uint64(GetUniqueID()),.1f,FColor(235,212,155),FString::Printf(TEXT("[F] Speak to CIDCORE - %s"),*AreaName));
 if(auto* PC=Cast<APlayerController>(Pawn->GetController()))if(PC->WasInputKeyJustPressed(EKeys::F))Interact();
}


