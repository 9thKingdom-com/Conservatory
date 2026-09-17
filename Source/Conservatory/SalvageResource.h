#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "SalvageResource.generated.h"
class AC17Robot;
class UStaticMeshComponent;
class UTextRenderComponent;
UCLASS()
class CONSERVATORY_API ASalvageResource : public AActor {
 GENERATED_BODY()
public:
 ASalvageResource();
 virtual void OnConstruction(const FTransform& Transform) override;
 virtual void BeginPlay() override;
 UFUNCTION(BlueprintCallable) void BuildVisuals();
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Salvage") FName SiteId;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Salvage") FName Kind=TEXT("timber");
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Salvage") FString DisplayName=TEXT("Timber bundle");
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Salvage",meta=(ClampMin="1")) int32 Quantity=3;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Salvage") FVector ApproachOffset=FVector(-120,0,76);
 UFUNCTION(BlueprintPure) bool IsAvailable() const;
 bool Reserve(AC17Robot* Robot);
 void Release(AC17Robot* Robot);
 void Lift(AC17Robot* Robot);
 void Consume();
 FVector ApproachPoint() const{return GetActorLocation()+ApproachOffset;}
 FName WorkClip() const;
private:
 UPROPERTY() TArray<TObjectPtr<UStaticMeshComponent>> Pieces;
 UPROPERTY() TObjectPtr<UTextRenderComponent> Label;
 TWeakObjectPtr<AC17Robot> ReservedBy;
 bool Consumed=false;
};
