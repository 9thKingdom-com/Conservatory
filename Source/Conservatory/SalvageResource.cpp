#include "SalvageResource.h"
#include "SalvageLedger.h"
#include "C17Robot.h"
#include "Components/StaticMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "Engine/StaticMesh.h"
#include "Materials/MaterialInterface.h"
ASalvageResource::ASalvageResource(){
 RootComponent=CreateDefaultSubobject<USceneComponent>(TEXT("Site"));
 for(int I=0;I<3;++I){auto* M=CreateDefaultSubobject<UStaticMeshComponent>(FName(*FString::Printf(TEXT("Piece%d"),I)));M->SetupAttachment(RootComponent);M->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);Pieces.Add(M);}
 Label=CreateDefaultSubobject<UTextRenderComponent>(TEXT("ResourceLabel"));Label->SetupAttachment(RootComponent);Label->SetRelativeLocation(FVector(0,0,88));Label->SetRelativeRotation(FRotator(0,-90,0));Label->SetWorldSize(9);Label->SetHorizontalAlignment(EHTA_Center);Label->SetVerticalAlignment(EVRTA_TextCenter);Label->SetTextRenderColor(FColor(240,222,169));
}
void ASalvageResource::OnConstruction(const FTransform& T){Super::OnConstruction(T);BuildVisuals();}
void ASalvageResource::BuildVisuals(){
 auto* Cylinder=LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));auto* Sphere=LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Sphere.Sphere"));
 auto* Gold=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Conservatory/Robots/C17/M_C17_Ochre.M_C17_Ochre"));auto* Metal=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Conservatory/Robots/C17/M_C17_Steel.M_C17_Steel"));
 for(int I=0;I<Pieces.Num();++I){auto* M=Pieces[I].Get();M->SetRelativeRotation(FRotator::ZeroRotator);
  if(Kind==TEXT("timber")){M->SetStaticMesh(Cylinder);M->SetRelativeRotation(FRotator(90,0,0));M->SetRelativeScale3D(FVector(.28,.28,.85));M->SetRelativeLocation(FVector(0,I==0?-16:I==1?16:0,I<2?14:38));M->SetMaterial(0,Gold);}
  else if(Kind==TEXT("stone")){M->SetStaticMesh(Sphere);M->SetRelativeScale3D(FVector(.40,.36,.32));M->SetRelativeLocation(FVector(I==0?-18:18,I==2?20:-15,16));M->SetMaterial(0,Metal);}
  else {M->SetStaticMesh(Cylinder);M->SetRelativeScale3D(I==0?FVector(.42,.42,.42):FVector(.56,.56,.04));M->SetRelativeLocation(FVector(0,0,I==0?25:I==1?4:46));M->SetMaterial(0,I==0?Gold:Metal);}
 }
 Label->SetText(FText::FromString(FString::Printf(TEXT("%s\n%d available"),*DisplayName,Quantity)));
}
void ASalvageResource::BeginPlay(){Super::BeginPlay();if(auto* L=GetGameInstance()->GetSubsystem<USalvageLedger>())if(L->WasDelivered(SiteId))Consume();}
bool ASalvageResource::IsAvailable() const{return !Consumed && !ReservedBy.IsValid() && !SiteId.IsNone();}
bool ASalvageResource::Reserve(AC17Robot* R){if(!R || !IsAvailable())return false;ReservedBy=R;return true;}
void ASalvageResource::Release(AC17Robot* R){if(ReservedBy.Get()!=R)return;ReservedBy.Reset();if(!Consumed){SetActorHiddenInGame(false);SetActorEnableCollision(true);}}
void ASalvageResource::Lift(AC17Robot* R){if(ReservedBy.Get()==R){SetActorHiddenInGame(true);SetActorEnableCollision(false);}}
void ASalvageResource::Consume(){Consumed=true;ReservedBy.Reset();SetActorHiddenInGame(true);SetActorEnableCollision(false);}
FName ASalvageResource::WorkClip() const{return Kind==TEXT("timber")?FName(TEXT("Chop")):Kind==TEXT("stone")?FName(TEXT("BreakStone")):FName(TEXT("ShelfPick"));}
