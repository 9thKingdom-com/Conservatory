#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ControlRoomDrawerCabinet.generated.h"

UCLASS()
class CONSERVATORY_API AControlRoomDrawerCabinet : public AActor
{
    GENERATED_BODY()

public:
    AControlRoomDrawerCabinet();

protected:
    virtual void OnConstruction(const FTransform& Transform) override;
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;

public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Control Room Drawer Cabinet")
    TObjectPtr<UStaticMesh> CabinetMesh;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Control Room Drawer Cabinet")
    TArray<TObjectPtr<UStaticMesh>> DrawerMeshes;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Control Room Drawer Cabinet")
    float OpenDistance = 45.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Control Room Drawer Cabinet")
    float InteractRange = 320.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Control Room Drawer Cabinet")
    FVector OpenDirection = FVector(0.0f, -1.0f, 0.0f);

    UFUNCTION(BlueprintCallable, Category="Control Room Drawer Cabinet")
    bool ToggleNearestDrawer();

    UFUNCTION(BlueprintPure, Category="Control Room Drawer Cabinet")
    bool CanUse() const;

private:
    void RebuildDrawers();
    int32 GetAimedDrawer() const;
    void UpdateDrawerTransforms(float DeltaSeconds);

    UPROPERTY(VisibleAnywhere, Category="Control Room Drawer Cabinet")
    TObjectPtr<USceneComponent> Root;

    UPROPERTY(VisibleAnywhere, Category="Control Room Drawer Cabinet")
    TObjectPtr<UStaticMeshComponent> Cabinet;

    UPROPERTY(VisibleAnywhere, Category="Control Room Drawer Cabinet")
    TObjectPtr<class USphereComponent> Range;

    UPROPERTY(VisibleAnywhere, Category="Control Room Drawer Cabinet")
    TArray<TObjectPtr<UStaticMeshComponent>> Drawers;

    UPROPERTY(VisibleAnywhere, Category="Control Room Drawer Cabinet")
    TArray<bool> OpenStates;

    UPROPERTY(VisibleAnywhere, Category="Control Room Drawer Cabinet")
    TArray<float> OpenAmounts;
};
