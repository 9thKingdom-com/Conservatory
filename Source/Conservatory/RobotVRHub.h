#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Styling/SlateBrush.h"
#include "RobotVRHub.generated.h"
class AC17Robot;class ACharacter;class AAIController;class UTextureRenderTarget2D;class UStaticMeshComponent;class SWidget;
UCLASS()
class CONSERVATORY_API ARobotVRHub : public AActor {
 GENERATED_BODY()
public:
 ARobotVRHub();
 virtual void BeginPlay() override;virtual void Tick(float Delta) override;virtual void EndPlay(const EEndPlayReason::Type Reason) override;
 UFUNCTION(BlueprintCallable) bool SelectRobot(int32 Id);
 UFUNCTION(BlueprintCallable) bool EnterRobot(int32 Id);
 UFUNCTION(BlueprintCallable) bool ReturnToHuman();
 UFUNCTION(BlueprintCallable) bool OpenMonitor();
 UFUNCTION(BlueprintCallable) void CloseMonitor();
 UFUNCTION(BlueprintPure) bool IsRemote() const{return Human!=nullptr;}
 UFUNCTION(BlueprintPure) int32 GetSelectedRobotId() const{return SelectedId;}
 UFUNCTION(BlueprintPure) UTextureRenderTarget2D* GetMonitorTexture() const{return MonitorTexture;}
 UPROPERTY(VisibleAnywhere) TObjectPtr<UStaticMeshComponent> Screen;
private:
 void DrawMonitor();void RefreshRobots();bool CanUse() const;AC17Robot* FindRobot(int32 Id) const;
 UPROPERTY() TArray<TObjectPtr<AC17Robot>> Robots;
 UPROPERTY() TObjectPtr<ACharacter> Human;
 UPROPERTY() TObjectPtr<AC17Robot> ControlledRobot;
 UPROPERTY() TObjectPtr<AAIController> SavedAI;
 UPROPERTY() TObjectPtr<UTextureRenderTarget2D> MonitorTexture;
 UPROPERTY() TObjectPtr<class UTexture2D> TerrainMap;
 FVector HumanLocation;FRotator HumanView;int32 SelectedId=1;float DrawTimer=0,CycleTimer=0;
 FString CameraCommand;float CameraCommandTimer=0,RescanTimer=0;
 TSharedPtr<SWidget> Panel;FSlateBrush MonitorBrush;
};
