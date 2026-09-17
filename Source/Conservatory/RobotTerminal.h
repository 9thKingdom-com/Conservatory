#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Styling/SlateBrush.h"
#include "RobotTerminal.generated.h"
class AC17Robot;class UStaticMeshComponent;class UMaterialInstanceDynamic;class SWidget;class SEditableTextBox;
UCLASS()
class CONSERVATORY_API ARobotTerminal : public AActor {
 GENERATED_BODY()
public:
 ARobotTerminal();
 virtual void BeginPlay() override;
 virtual void Tick(float Delta) override;
 virtual void EndPlay(const EEndPlayReason::Type Reason) override;
 UFUNCTION(BlueprintCallable) bool OpenConsole();
 UFUNCTION(BlueprintCallable) void CloseConsole();
 UFUNCTION(BlueprintPure) bool IsConsoleOpen() const{return Open;}
 UFUNCTION(BlueprintPure) FString InventoryText() const;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Field operations") TObjectPtr<AC17Robot> Robot;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Field operations") TObjectPtr<UStaticMeshComponent> Screen;
private:
 bool CanUse() const;
 void SendTypedTask();
 UPROPERTY() TObjectPtr<UMaterialInstanceDynamic> ScreenMaterial;
 TSharedPtr<SWidget> Panel;
 TSharedPtr<SEditableTextBox> TaskEntry;
 FSlateBrush FeedBrush;
 bool Open=false,FeedBound=false;
};
