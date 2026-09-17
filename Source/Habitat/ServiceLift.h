#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ServiceLift.generated.h"

// Paired inspection lift stations. Resource simulation is deliberately separate.
UCLASS()
class HABITAT_API AServiceLift : public AActor {
 GENERATED_BODY()
public:
 AServiceLift();
 virtual void Tick(float DeltaSeconds) override;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Lift") FVector Destination;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Lift") float DestinationYaw = 0;
 UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Lift") FString DestinationName;
 UFUNCTION(BlueprintCallable, Category="Lift") bool Travel();
private:
 double ReadyAt = 0;
};
