#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "GameFramework/GameModeBase.h"
#include "Explorer.generated.h"
UCLASS()
class CONSERVATORY_API AExplorer : public ACharacter {
 GENERATED_BODY()
public:
 AExplorer();
 virtual void SetupPlayerInputComponent(UInputComponent* Input) override;
 virtual void Tick(float DeltaSeconds) override;
private:
 UPROPERTY() TObjectPtr<class UCidcoreIntercom> Intercom;
 void OpenIntercom();
 float InspectionTime=0;
 int32 InspectionStage=0;
 FVector InspectionStart=FVector::ZeroVector;
 void Forward(float V); void Right(float V); void Look(float V); void Turn(float V);
 void Run(); void Walk(); void ResetView();
};
UCLASS()
class CONSERVATORY_API AConservatoryGameMode : public AGameModeBase {
 GENERATED_BODY()
public: AConservatoryGameMode();
 virtual void BeginPlay() override;
 virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
private:
 TSharedPtr<class IInputProcessor> DesktopExitInput;
};

