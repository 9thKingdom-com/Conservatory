#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "C17Robot.generated.h"
class UAnimSequence;class ASalvageResource;class USceneCaptureComponent2D;class UTextureRenderTarget2D;class UStaticMeshComponent;
UENUM(BlueprintType)
enum class ERobotTaskPhase : uint8 { None, Travelling, Working, Returning };
UCLASS()
class CONSERVATORY_API AC17Robot : public ACharacter {
 GENERATED_BODY()
public:
 AC17Robot();
 virtual void BeginPlay() override;
 virtual void Tick(float DeltaSeconds) override;
 virtual void EndPlay(const EEndPlayReason::Type Reason) override;
 virtual void SetupPlayerInputComponent(UInputComponent* Input) override;
 void SetEmbodied(bool Active);
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="VR") TObjectPtr<class UCameraComponent> RobotEyes;
 UFUNCTION(BlueprintCallable,Category="C17") bool PlayWorkAnimation(FName Action);
 UFUNCTION(BlueprintCallable,Category="C17") bool AssignResource(ASalvageResource* Resource);
 UFUNCTION(BlueprintCallable,Category="C17") bool SubmitTask(const FString& Text);
 UFUNCTION(BlueprintCallable,Category="C17") bool CancelTask();
 UFUNCTION(BlueprintCallable,Category="C17") bool SelectFeedPoint(FVector2D UV);
 UFUNCTION(BlueprintPure,Category="C17") ERobotTaskPhase GetTaskPhase() const{return Phase;}
 UFUNCTION(BlueprintPure,Category="C17") FString GetTaskStatus() const{return TaskStatus;}
 UFUNCTION(BlueprintPure,Category="C17") UTextureRenderTarget2D* GetFeed() const{return Feed;}
 void SetFeedActive(bool Active){FeedActive=Active;}
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="C17") TObjectPtr<USceneCaptureComponent2D> Capture;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="C17") bool PatrolEnabled=true;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="C17") FVector PatrolOffset=FVector(0,600,0);
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Wandering") bool UseMannequin=false;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Wandering") bool WanderEnabled=false;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Wandering") FVector WanderExtent=FVector(450,450,100);
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Wandering") float WanderSpeed=130;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Wandering") bool TerrainWander=false;
 // World-space XY limits, set from the current Landscape with its perimeter inset.
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Wandering") bool LimitTerrainWander=false;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Wandering") FVector WanderBoundsMin=FVector::ZeroVector;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Wandering") FVector WanderBoundsMax=FVector::ZeroVector;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Wandering") bool KeepOutOfConservatory=false;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Wandering") float ConservatoryKeepOutClearance=200.f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Wandering") TArray<FVector> ConservatoryKeepOutMins;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Wandering") TArray<FVector> ConservatoryKeepOutMaxs;
 UFUNCTION(BlueprintPure,Category="Wandering") bool IsInsideConservatoryKeepOut(FVector Point) const;
 UFUNCTION(BlueprintPure,Category="Wandering") bool IsInsideWanderBounds(FVector Point) const;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Wandering") int32 RobotId=0;
 UFUNCTION(BlueprintPure,Category="Wandering") FVector GetWanderDestination() const{return WanderDestination;}
private:
 void RemoteForward(float Value);void RemoteRight(float Value);void RemoteTurn(float Value);void RemoteLook(float Value);
 void TickTerrainWander(float Delta);
 FVector WanderDestination=FVector::ZeroVector;
 float RouteCheckTime=0;
 void TickWander(float Delta);
 bool SafeWanderStep(FVector Direction,float Distance) const;
 FVector WanderDirection=FVector::ZeroVector;
 float WanderTime=0;
 void SetClip(UAnimSequence* Clip,bool Loop=true);
 bool StartAction(FName Action);
 void TickTask(float Delta);
 bool MoveToTaskPoint(FVector Point,float Delta);
 void FailTask(const FString& Reason);
 UPROPERTY() TObjectPtr<UAnimSequence> Idle;
 UPROPERTY() TObjectPtr<UAnimSequence> Walk;
 UPROPERTY() TObjectPtr<UAnimSequence> Carry;
 UPROPERTY() TObjectPtr<UAnimSequence> Current;
 UPROPERTY() TObjectPtr<UTextureRenderTarget2D> Feed;
 UPROPERTY() TObjectPtr<UStaticMeshComponent> Payload;
 UPROPERTY() TObjectPtr<ASalvageResource> TaskResource;
 ERobotTaskPhase Phase=ERobotTaskPhase::None;
 FString TaskStatus=TEXT("Patrolling. Choose a resource or give a collection task.");
 FVector Home,LastPosition;
 bool Outward=true,FeedActive=false;
 float Wait=0,WorkRemaining=0,Stuck=0,FeedTimer=0,LastTaskDistance=MAX_flt;
};
