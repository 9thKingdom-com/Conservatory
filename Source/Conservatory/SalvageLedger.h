#pragma once
#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "GameFramework/SaveGame.h"
#include "SalvageLedger.generated.h"
UCLASS()
class CONSERVATORY_API USalvageSave : public USaveGame {
 GENERATED_BODY()
public:
 UPROPERTY(SaveGame) TMap<FName,int32> Inventory;
 UPROPERTY(SaveGame) TArray<FName> DeliveredSites;
};
UCLASS()
class CONSERVATORY_API USalvageLedger : public UGameInstanceSubsystem {
 GENERATED_BODY()
public:
 virtual void Initialize(FSubsystemCollectionBase& Collection) override;
 bool WasDelivered(FName Site) const;
 bool Deliver(FName Site,FName Kind,int32 Quantity);
 void RecordEvent(const FString& Event);
 UFUNCTION(BlueprintPure) int32 Count(FName Kind) const;
 FString Summary() const;
 FString LatestEvent;
 double LatestEventAt=-1;
 bool SaveFailed=false;
private:
 UPROPERTY() TObjectPtr<USalvageSave> Data;
 bool Inspection=false;
};
