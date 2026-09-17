#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "VRSuitStation.generated.h"
UCLASS()
class CONSERVATORY_API AVRSuitStation : public AActor {
 GENERATED_BODY()
public:
 AVRSuitStation();virtual void BeginPlay() override;virtual void Tick(float Delta) override;
 UFUNCTION(BlueprintCallable) bool WearSuit();
 UFUNCTION(BlueprintPure) bool CanUse() const;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) int32 RobotId=1;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TObjectPtr<class ARobotVRHub> Hub;
 UPROPERTY(VisibleAnywhere) TObjectPtr<class USkeletalMeshComponent> Suit;
private:
 float GetUseScore() const;
};
