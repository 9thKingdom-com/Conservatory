#include "ControlRoomDrawerCabinet.h"

#include "Components/StaticMeshComponent.h"
#include "Components/SphereComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"

AControlRoomDrawerCabinet::AControlRoomDrawerCabinet()
{
    PrimaryActorTick.bCanEverTick = true;

    Root = CreateDefaultSubobject<USceneComponent>(TEXT("CabinetRoot"));
    SetRootComponent(Root);

    Cabinet = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("CabinetMesh"));
    Cabinet->SetupAttachment(Root);
    Cabinet->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
    Cabinet->SetCollisionResponseToAllChannels(ECR_Block);
    Cabinet->SetGenerateOverlapEvents(false);

    Range = CreateDefaultSubobject<USphereComponent>(TEXT("InteractionRange"));
    Range->SetupAttachment(Root);
    Range->SetSphereRadius(InteractRange);
    Range->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    Range->SetHiddenInGame(true);
}

void AControlRoomDrawerCabinet::OnConstruction(const FTransform& Transform)
{
    Super::OnConstruction(Transform);
    RebuildDrawers();
    if (Range)
    {
        Range->SetSphereRadius(FMath::Max(50.0f, InteractRange));
    }
}

void AControlRoomDrawerCabinet::BeginPlay()
{
    Super::BeginPlay();
    RebuildDrawers();
}

void AControlRoomDrawerCabinet::RebuildDrawers()
{
    for (UStaticMeshComponent* Component : Drawers)
    {
        if (IsValid(Component))
        {
            Component->DestroyComponent();
        }
    }
    Drawers.Reset();
    OpenStates.Reset();
    OpenAmounts.Reset();

    if (!Root)
    {
        return;
    }

    for (int32 Index = 0; Index < DrawerMeshes.Num(); ++Index)
    {
        const FName ComponentName = *FString::Printf(TEXT("Drawer_%02d"), Index);
        UStaticMeshComponent* Component = NewObject<UStaticMeshComponent>(this, ComponentName);
        Component->SetupAttachment(Root);
        Component->RegisterComponent();
        Component->SetStaticMesh(DrawerMeshes[Index]);
        Component->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
        Component->SetCollisionResponseToAllChannels(ECR_Ignore);
        Component->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);
        Component->SetGenerateOverlapEvents(true);
        Component->SetRelativeLocation(FVector::ZeroVector);
        Drawers.Add(Component);
        OpenStates.Add(false);
        OpenAmounts.Add(0.0f);
    }

    if (Cabinet)
    {
        Cabinet->SetStaticMesh(CabinetMesh);
    }
}

void AControlRoomDrawerCabinet::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    UpdateDrawerTransforms(DeltaSeconds);

    if (CanUse() && GEngine)
    {
        GEngine->AddOnScreenDebugMessage(uint64(GetUniqueID()), 0.1f, FColor(225, 215, 180), TEXT("[F] Open / close drawer"));
    }
}

bool AControlRoomDrawerCabinet::CanUse() const
{
    APlayerController* PC = UGameplayStatics::GetPlayerController(this, 0);
    APawn* Pawn = PC ? PC->GetPawn() : nullptr;
    if (!Pawn)
    {
        return false;
    }

    return FVector::Dist(Pawn->GetActorLocation(), GetActorLocation()) <= InteractRange;
}

int32 AControlRoomDrawerCabinet::GetAimedDrawer() const
{
    APlayerController* PC = UGameplayStatics::GetPlayerController(this, 0);
    APawn* Pawn = PC ? PC->GetPawn() : nullptr;
    if (!Pawn)
    {
        return INDEX_NONE;
    }

    FVector Eye;
    FRotator View;
    PC->GetPlayerViewPoint(Eye, View);

    FHitResult Hit;
    FCollisionQueryParams Params;
    Params.AddIgnoredActor(Pawn);
    const FVector TraceEnd = Eye + View.Vector() * 600.0f;
    if (!GetWorld()->LineTraceSingleByChannel(Hit, Eye, TraceEnd, ECC_Visibility, Params))
    {
        return INDEX_NONE;
    }

    const UPrimitiveComponent* HitComponent = Hit.GetComponent();
    for (int32 Index = 0; Index < Drawers.Num(); ++Index)
    {
        if (Drawers[Index] == HitComponent)
        {
            return Index;
        }
    }
    return INDEX_NONE;
}

bool AControlRoomDrawerCabinet::ToggleNearestDrawer()
{
    if (!CanUse())
    {
        return false;
    }

    const int32 Index = GetAimedDrawer();
    if (Index == INDEX_NONE)
    {
        return false;
    }

    OpenStates[Index] = !OpenStates[Index];
    return true;
}

void AControlRoomDrawerCabinet::UpdateDrawerTransforms(float DeltaSeconds)
{
    const FVector OpenOffset = OpenDirection.GetSafeNormal() * OpenDistance;

    for (int32 Index = 0; Index < Drawers.Num(); ++Index)
    {
        if (!Drawers[Index])
        {
            continue;
        }

        const float Target = OpenStates[Index] ? 1.0f : 0.0f;
        const float Speed = 4.0f;
        OpenAmounts[Index] = FMath::FInterpTo(OpenAmounts[Index], Target, DeltaSeconds, Speed);
        Drawers[Index]->SetRelativeLocation(OpenOffset * OpenAmounts[Index]);
    }
}
