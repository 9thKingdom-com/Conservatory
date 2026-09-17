#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "IntercomStation.generated.h"
class UStaticMeshComponent;
class UMaterialInstanceDynamic;
UCLASS()
class CONSERVATORY_API AIntercomStation : public AActor {
 GENERATED_BODY()
public:
 AIntercomStation();
 virtual void BeginPlay() override;
 virtual void Tick(float DeltaSeconds) override;
 UFUNCTION(BlueprintCallable) bool Interact();
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Intercom") FString AreaName;
private:
 bool CanUse(class APawn* Pawn) const;
 UPROPERTY() TObjectPtr<UStaticMeshComponent> Lamp;
 UPROPERTY() TObjectPtr<UMaterialInstanceDynamic> LampMaterial;
};
