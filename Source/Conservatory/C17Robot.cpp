#include "C17Robot.h"
#include "SalvageResource.h"
#include "SalvageLedger.h"
#include "Components/CapsuleComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Engine/TextureRenderTarget2D.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Animation/AnimSequence.h"
#include "UObject/ConstructorHelpers.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/StaticMesh.h"
#include "Engine/World.h"
#include "Engine/GameInstance.h"
#include "EngineUtils.h"
#include "AIController.h"
#include "Camera/CameraComponent.h"
#include "Components/InputComponent.h"
#include "NavigationSystem.h"
#include "NavigationPath.h"
#include "Navigation/PathFollowingComponent.h"
AC17Robot::AC17Robot(){
 PrimaryActorTick.bCanEverTick=true;GetCapsuleComponent()->InitCapsuleSize(24,76);
 RobotEyes=CreateDefaultSubobject<UCameraComponent>(TEXT("RobotEyes"));RobotEyes->SetupAttachment(RootComponent);RobotEyes->SetRelativeLocation(FVector(10,0,68));RobotEyes->bUsePawnControlRotation=true;RobotEyes->FieldOfView=90;
 static ConstructorHelpers::FObjectFinder<USkeletalMesh> RobotMesh(TEXT("/Game/Conservatory/Robots/C17/SK_C17.SK_C17"));
 static ConstructorHelpers::FObjectFinder<UAnimSequence> IdleAsset(TEXT("/Game/Conservatory/Robots/C17/A_C17_Idle.A_C17_Idle"));
 static ConstructorHelpers::FObjectFinder<UAnimSequence> WalkAsset(TEXT("/Game/Conservatory/Robots/C17/A_C17_Walk.A_C17_Walk"));
 static ConstructorHelpers::FObjectFinder<UAnimSequence> CarryAsset(TEXT("/Game/Conservatory/Robots/C17/A_C17_CarryWalk.A_C17_CarryWalk"));
 GetMesh()->SetSkeletalMesh(RobotMesh.Object);GetMesh()->SetRelativeLocation(FVector(0,0,-76));GetMesh()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
 Idle=IdleAsset.Object;Walk=WalkAsset.Object;Carry=CarryAsset.Object;
 GetCharacterMovement()->bRunPhysicsWithNoController=true;GetCharacterMovement()->MaxWalkSpeed=40;GetCharacterMovement()->MaxStepHeight=25;GetCharacterMovement()->bOrientRotationToMovement=true;GetCharacterMovement()->RotationRate=FRotator(0,100,0);bUseControllerRotationYaw=false;
 Capture=CreateDefaultSubobject<USceneCaptureComponent2D>(TEXT("FieldCamera"));Capture->SetupAttachment(RootComponent);Capture->SetRelativeLocation(FVector(32,0,62));Capture->FOVAngle=90;Capture->bCaptureEveryFrame=false;Capture->bCaptureOnMovement=false;Capture->CaptureSource=ESceneCaptureSource::SCS_FinalColorLDR;
 Capture->PostProcessSettings.bOverride_MotionBlurAmount=true;Capture->PostProcessSettings.MotionBlurAmount=0;
 Payload=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("CarriedLoad"));Payload->SetupAttachment(RootComponent);static ConstructorHelpers::FObjectFinder<UStaticMesh> Cube(TEXT("/Engine/BasicShapes/Cube.Cube"));Payload->SetStaticMesh(Cube.Object);Payload->SetRelativeLocation(FVector(43,0,12));Payload->SetRelativeScale3D(FVector(.36,.43,.32));Payload->SetCollisionEnabled(ECollisionEnabled::NoCollision);Payload->SetHiddenInGame(true);
}
void AC17Robot::BeginPlay(){
 Super::BeginPlay();
 if(UseMannequin){
  auto* MannyMesh=LoadObject<USkeletalMesh>(nullptr,TEXT("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple"));
  auto* IdleClip=LoadObject<UAnimSequence>(nullptr,TEXT("/Game/Characters/Mannequins/Animations/Manny/MM_Idle.MM_Idle"));
  auto* WalkClip=LoadObject<UAnimSequence>(nullptr,TEXT("/Game/Conservatory/Robots/Manny/A_MannyTerrainWalk.A_MannyTerrainWalk"));
  if(MannyMesh && IdleClip && WalkClip){GetMesh()->SetSkeletalMesh(MannyMesh);GetMesh()->SetRelativeLocation(FVector(0,0,-96));GetMesh()->SetRelativeRotation(FRotator(0,-90,0));GetCapsuleComponent()->SetCapsuleSize(34,96);Idle=IdleClip;Walk=Carry=WalkClip;}
  else UE_LOG(LogTemp,Error,TEXT("WANDER missing Manny mesh or matching locomotion clips"));
 }
 Home=LastPosition=GetActorLocation();Wait=FMath::FRandRange(.5f,3.f);SetClip(Idle);
 Capture->AttachToComponent(RobotEyes,FAttachmentTransformRules::KeepRelativeTransform);Capture->SetRelativeLocation(FVector::ZeroVector);Capture->SetRelativeRotation(FRotator::ZeroRotator);
 if(UseMannequin){
  GetMesh()->VisibilityBasedAnimTickOption=EVisibilityBasedAnimTickOption::AlwaysTickPoseAndRefreshBones;
  GetCharacterMovement()->RotationRate=FRotator(0,360,0);
  GetCharacterMovement()->MaxAcceleration=500;GetCharacterMovement()->BrakingDecelerationWalking=700;
 }
 if(TerrainWander){AIControllerClass=AAIController::StaticClass();SpawnDefaultController();GetCharacterMovement()->MaxWalkSpeed=WanderSpeed;}
 Feed=NewObject<UTextureRenderTarget2D>(this);Feed->RenderTargetFormat=RTF_RGBA8;Feed->ClearColor=FLinearColor::Black;Feed->InitAutoFormat(1024,576);Feed->TargetGamma=2.2f;Capture->TextureTarget=Feed;Capture->HideActorComponents(this);
}
void AC17Robot::SetClip(UAnimSequence* Clip,bool Loop){if(Clip && Current!=Clip){Current=Clip;GetMesh()->PlayAnimation(Clip,Loop);}if(Clip)GetMesh()->SetPlayRate(Clip==Walk?(UseMannequin?GetVelocity().Size2D()/240.f:GetCharacterMovement()->MaxWalkSpeed/40.f):Clip==Carry?GetCharacterMovement()->MaxWalkSpeed/30.f:1.f);}
bool AC17Robot::StartAction(FName Action){
 const TArray<FName> Allowed={TEXT("Idle"),TEXT("Walk"),TEXT("CarryWalk"),TEXT("Lift"),TEXT("ShelfPick"),TEXT("Chop"),TEXT("BreakStone")};if(!Allowed.Contains(Action))return false;
 // Custom C17 work clips cannot play on Manny's skeleton. Preserve task timing using idle.
 if(UseMannequin){GetCharacterMovement()->StopMovementImmediately();SetClip(Idle);WorkRemaining=3;return true;}
 const FString Asset=FString::Printf(TEXT("/Game/Conservatory/Robots/C17/A_C17_%s.A_C17_%s"),*Action.ToString(),*Action.ToString());auto* Clip=LoadObject<UAnimSequence>(nullptr,*Asset);if(!Clip)return false;
 GetCharacterMovement()->StopMovementImmediately();Current=nullptr;SetClip(Clip,false);WorkRemaining=Clip->GetPlayLength();return true;
}
bool AC17Robot::PlayWorkAnimation(FName Action){return Phase==ERobotTaskPhase::None && StartAction(Action);}
bool AC17Robot::AssignResource(ASalvageResource* Resource){
 if(Phase!=ERobotTaskPhase::None){TaskStatus=TEXT("A collection task is already running. Cancel it before choosing another.");return false;}
 if(!IsValid(Resource) || !Resource->Reserve(this)){TaskStatus=TEXT("That resource is depleted or assigned to another unit.");return false;}
 if(auto* AI=Cast<AAIController>(GetController()))AI->StopMovement();
 TaskResource=Resource;Phase=ERobotTaskPhase::Travelling;WorkRemaining=0;Wait=0;Stuck=0;LastTaskDistance=MAX_flt;Current=nullptr;
 TaskStatus=TEXT("Travelling to ")+Resource->DisplayName;GetGameInstance()->GetSubsystem<USalvageLedger>()->RecordEvent(TEXT("C-17 was assigned to collect ")+Resource->DisplayName+TEXT("."));return true;
}
bool AC17Robot::SubmitTask(const FString& Text){
 FString Query=Text.TrimStartAndEnd().ToLower();if(Query.Len()>160){TaskStatus=TEXT("Keep tasks under 160 characters.");return false;}
 Query.RemoveFromStart(TEXT("please "));
 for(const TCHAR* Prefix:{TEXT("collect "),TEXT("gather "),TEXT("fetch "),TEXT("pick up ")})if(Query.RemoveFromStart(Prefix))break;
 Query=Query.TrimStartAndEnd();FName Kind;
 if(Query==TEXT("timber") || Query==TEXT("wood") || Query==TEXT("logs") || Query==TEXT("timber logs"))Kind=TEXT("timber");
 else if(Query==TEXT("stone") || Query==TEXT("stones") || Query==TEXT("rocks"))Kind=TEXT("stone");
 else if(Query==TEXT("copper") || Query==TEXT("copper spool") || Query==TEXT("copper spools"))Kind=TEXT("copper");
 else {TaskStatus=TEXT("Supported tasks: collect timber, collect stone, or collect copper.");return false;}
 ASalvageResource* Best=nullptr;float Distance=MAX_flt;
 for(TActorIterator<ASalvageResource> It(GetWorld());It;++It)if(It->Kind==Kind && It->IsAvailable()){float D=FVector::DistSquared(GetActorLocation(),It->GetActorLocation());if(D<Distance){Distance=D;Best=*It;}}
 if(!Best){TaskStatus=TEXT("No unassigned ")+Kind.ToString()+TEXT(" remains at the collection sites.");return false;}return AssignResource(Best);
}
bool AC17Robot::CancelTask(){
 if(Phase==ERobotTaskPhase::None){TaskStatus=TEXT("No active collection task.");return false;}
 if(Phase==ERobotTaskPhase::Returning){TaskStatus=TEXT("Returning with a load. Delivery will finish before another task can start.");return false;}
 FailTask(TEXT("Task cancelled. The resource is still available."));return true;
}
void AC17Robot::FailTask(const FString& Reason){if(IsValid(TaskResource))TaskResource->Release(this);TaskResource=nullptr;Phase=ERobotTaskPhase::None;Payload->SetHiddenInGame(true);WorkRemaining=0;Stuck=0;Wait=3;GetCharacterMovement()->StopMovementImmediately();GetCharacterMovement()->MaxWalkSpeed=40;SetClip(Idle);TaskStatus=Reason;}
bool AC17Robot::MoveToTaskPoint(FVector Point,float D){
 FVector Direction=Point-GetActorLocation();const float Vertical=FMath::Abs(Direction.Z);Direction.Z=0;const float Distance=Direction.Size();
 if(Distance<24 && Vertical<120){GetCharacterMovement()->StopMovementImmediately();return true;}
 if(Distance<LastTaskDistance-D*.5f)Stuck=0;else Stuck+=D;LastTaskDistance=Distance;
 if(Stuck>8){FailTask(TEXT("Route blocked. The load remains at its collection site; choose another task."));return false;}
 GetCharacterMovement()->MaxWalkSpeed=Phase==ERobotTaskPhase::Returning?55:90;
 AddMovementInput(Direction.GetSafeNormal(),1,true);SetClip(Phase==ERobotTaskPhase::Returning?Carry:Walk);return false;
}
void AC17Robot::TickTask(float D){
 if(!IsValid(TaskResource)){FailTask(TEXT("The collection target is no longer available."));return;}
 if(Phase==ERobotTaskPhase::Travelling){
  if(MoveToTaskPoint(TaskResource->ApproachPoint(),D)){
   Phase=ERobotTaskPhase::Working;SetActorRotation(FRotator(0,(TaskResource->GetActorLocation()-GetActorLocation()).Rotation().Yaw,0));TaskStatus=TEXT("Collecting ")+TaskResource->DisplayName;
   if(!StartAction(TaskResource->WorkClip()))FailTask(TEXT("The work animation is unavailable. Nothing was collected."));
  }
 }else if(Phase==ERobotTaskPhase::Working){
  WorkRemaining-=D;if(WorkRemaining<=0){TaskResource->Lift(this);Payload->SetHiddenInGame(false);Phase=ERobotTaskPhase::Returning;Stuck=0;LastTaskDistance=MAX_flt;Current=nullptr;TaskStatus=TEXT("Returning ")+TaskResource->DisplayName+TEXT(" to the exterior collection bay.");}
 }else if(Phase==ERobotTaskPhase::Returning){
  if(MoveToTaskPoint(Home,D)){
   auto* Ledger=GetGameInstance()->GetSubsystem<USalvageLedger>();const FString Name=TaskResource->DisplayName;const int32 Quantity=TaskResource->Quantity;
   if(Ledger->Deliver(TaskResource->SiteId,TaskResource->Kind,Quantity)){TaskResource->Consume();TaskStatus=FString::Printf(TEXT("Delivered %d: %s. Ready for another task."),Quantity,*Name);}
   else {TaskResource->Release(this);TaskStatus=TEXT("Delivery was not credited; this site was already recorded.");}
   TaskResource=nullptr;Phase=ERobotTaskPhase::None;Payload->SetHiddenInGame(true);Wait=4;GetCharacterMovement()->MaxWalkSpeed=40;SetClip(Idle);
  }
 }
}
bool AC17Robot::SelectFeedPoint(FVector2D UV){
 if(UV.X<0 || UV.X>1 || UV.Y<0 || UV.Y>1)return false;
 const float T=FMath::Tan(FMath::DegreesToRadians(Capture->FOVAngle*.5f));
 const FVector Ray=(Capture->GetForwardVector()+Capture->GetRightVector()*((UV.X*2-1)*T)-Capture->GetUpVector()*((UV.Y*2-1)*T*576.f/1024.f)).GetSafeNormal();
 FHitResult Hit;FCollisionQueryParams Params;Params.AddIgnoredActor(this);
 if(GetWorld()->LineTraceSingleByChannel(Hit,Capture->GetComponentLocation(),Capture->GetComponentLocation()+Ray*15000,ECC_Visibility,Params))if(auto* R=Cast<ASalvageResource>(Hit.GetActor()))return AssignResource(R);
 TaskStatus=TEXT("Click directly on a resource in the camera view, or choose a task below.");return false;
}
void AC17Robot::Tick(float D){
 Super::Tick(D);RobotEyes->SetWorldRotation(IsPlayerControlled()?GetControlRotation():GetActorRotation());FeedTimer+=D;if(FeedActive && FeedTimer>=.067f){Capture->CaptureScene();FeedTimer=0;}
 // A worn VR suit gives the player exclusive control until they return to the human.
 if(IsPlayerControlled()){if(UseMannequin)SetClip(GetVelocity().Size2D()>5?Walk:Idle);return;}
 if(Phase!=ERobotTaskPhase::None){TickTask(D);return;}
 if(WorkRemaining>0){WorkRemaining-=D;if(WorkRemaining<=0){SetClip(Idle);Wait=2;}return;}
 if(TerrainWander && WanderEnabled && PatrolEnabled){TickTerrainWander(D);return;}
 if(!PatrolEnabled){SetClip(Idle);return;}if(Wait>0){Wait-=D;SetClip(Idle);return;}
 if(WanderEnabled){TickWander(D);return;}
 const FVector Target=Outward?Home+PatrolOffset:Home;FVector Direction=Target-GetActorLocation();Direction.Z=0;
 if(Direction.Size()<35){Outward=!Outward;Wait=3;Stuck=0;GetCharacterMovement()->StopMovementImmediately();SetClip(Idle);return;}
 if(FVector::Dist2D(LastPosition,GetActorLocation())<D*5)Stuck+=D;else Stuck=0;LastPosition=GetActorLocation();
 if(Stuck>4){Outward=!Outward;Wait=2;Stuck=0;return;}AddMovementInput(Direction.GetSafeNormal(),1,true);SetClip(Walk);
}
void AC17Robot::EndPlay(const EEndPlayReason::Type Reason){if(IsValid(TaskResource))TaskResource->Release(this);Super::EndPlay(Reason);}

bool AC17Robot::SafeWanderStep(FVector Direction,float Distance) const{
 const FVector Start=GetActorLocation(),End=Start+Direction*Distance,Offset=End-Home;
 if(FMath::Abs(Offset.X)>WanderExtent.X || FMath::Abs(Offset.Y)>WanderExtent.Y)return false;
 FCollisionQueryParams Params(SCENE_QUERY_STAT(WanderClearance),false,this);FHitResult Hit;
 const auto Shape=FCollisionShape::MakeCapsule(GetCapsuleComponent()->GetScaledCapsuleRadius()+5,GetCapsuleComponent()->GetScaledCapsuleHalfHeight()-12);
 if(GetWorld()->SweepSingleByChannel(Hit,Start+FVector(0,0,14),End+FVector(0,0,14),FQuat::Identity,ECC_Pawn,Shape,Params))return false;
 const float Feet=Start.Z-GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
 if(!GetWorld()->LineTraceSingleByChannel(Hit,FVector(End.X,End.Y,Feet+35),FVector(End.X,End.Y,Feet-45),ECC_Visibility,Params))return false;
 return Hit.ImpactNormal.Z>.75f && FMath::Abs(Hit.ImpactPoint.Z-(Home.Z-GetCapsuleComponent()->GetScaledCapsuleHalfHeight()))<WanderExtent.Z;
}
void AC17Robot::TickWander(float D){
 GetCharacterMovement()->MaxWalkSpeed=WanderSpeed;
 WanderTime-=D;
 if(FVector::Dist2D(LastPosition,GetActorLocation())<D*8)Stuck+=D;else Stuck=0;
 LastPosition=GetActorLocation();
 if(WanderTime<=0 || Stuck>1 || !SafeWanderStep(WanderDirection,90)){
  GetCharacterMovement()->StopMovementImmediately();SetClip(Idle);WanderDirection=FVector::ZeroVector;
  for(int32 Attempt=0;Attempt<24;++Attempt){
   const float Angle=FMath::FRandRange(-PI,PI);const FVector Candidate(FMath::Cos(Angle),FMath::Sin(Angle),0);
   if(SafeWanderStep(Candidate,140)){WanderDirection=Candidate;break;}
  }
  WanderTime=FMath::FRandRange(2.f,5.f);Wait=FMath::FRandRange(.6f,2.8f);Stuck=0;return;
 }
 if(!WanderDirection.IsNearlyZero()){AddMovementInput(WanderDirection,1,true);SetClip(GetVelocity().Size2D()>8?Walk:Idle);}
}

bool AC17Robot::IsInsideConservatoryKeepOut(FVector Point) const{
 if(!KeepOutOfConservatory)return false;
 for(int32 Index=0;Index<ConservatoryKeepOutMins.Num();++Index){
  if(Index>=ConservatoryKeepOutMaxs.Num())break;
  const FVector& Min=ConservatoryKeepOutMins[Index];
  const FVector& Max=ConservatoryKeepOutMaxs[Index];
  if(Point.X>=Min.X-ConservatoryKeepOutClearance && Point.X<=Max.X+ConservatoryKeepOutClearance
   && Point.Y>=Min.Y-ConservatoryKeepOutClearance && Point.Y<=Max.Y+ConservatoryKeepOutClearance)return true;
 }
 return false;
}
bool AC17Robot::IsInsideWanderBounds(FVector Point) const{
 if(IsInsideConservatoryKeepOut(Point))return false;
 if(!LimitTerrainWander)return true;
 // Keep the capsule and braking distance inside the requested perimeter.
 constexpr float Clearance=200.f;
 return Point.X>=WanderBoundsMin.X+Clearance && Point.X<=WanderBoundsMax.X-Clearance
     && Point.Y>=WanderBoundsMin.Y+Clearance && Point.Y<=WanderBoundsMax.Y-Clearance;
}
void AC17Robot::TickTerrainWander(float D){
 auto* AI=Cast<AAIController>(GetController());
 if(!AI){SetClip(Idle);return;}
 GetCharacterMovement()->MaxWalkSpeed=WanderSpeed;
 SetClip(GetVelocity().Size2D()>5?Walk:Idle);
 if(Wait>0){Wait-=D;return;}
 if(AI->GetMoveStatus()==EPathFollowingStatus::Moving){
  if(!IsInsideWanderBounds(GetActorLocation()+GetVelocity()*FMath::Max(D,0.5f))){
   AI->StopMovement();GetCharacterMovement()->StopMovementImmediately();WanderDestination=FVector::ZeroVector;Wait=0.5f;return;
  }
  RouteCheckTime+=D;
  if(RouteCheckTime>3){
   if(FVector::Dist2D(LastPosition,GetActorLocation())<60){AI->StopMovement();Wait=FMath::FRandRange(1.f,3.f);}
   LastPosition=GetActorLocation();RouteCheckTime=0;
  }
  return;
 }
 auto* Nav=FNavigationSystem::GetCurrent<UNavigationSystemV1>(GetWorld());
 if(!WanderDestination.IsNearlyZero()){WanderDestination=FVector::ZeroVector;Wait=FMath::FRandRange(1.f,4.f);return;}
 if(!Nav){Wait=5;return;}
 FNavLocation Goal;
 for(int32 Attempt=0;Attempt<32;++Attempt){
  if(!Nav->GetRandomReachablePointInRadius(GetActorLocation(),180000,Goal))continue;
  if(!IsInsideWanderBounds(Goal.Location))continue;
  if(FVector::Dist2D(GetActorLocation(),Goal.Location)<5000)continue;
  if(LimitTerrainWander){
   auto* Path=UNavigationSystemV1::FindPathToLocationSynchronously(GetWorld(),GetActorLocation(),Goal.Location,this);
   if(!Path || !Path->IsValid() || Path->IsPartial() || Path->PathPoints.Num()<2)continue;
   bool Inside=true;
   for(const FVector& Point:Path->PathPoints)if(!IsInsideWanderBounds(Point)){Inside=false;break;}
   if(!Inside)continue;
  }
  if(AI->MoveToLocation(Goal.Location,90,true,true,false,true,nullptr,false)==EPathFollowingRequestResult::RequestSuccessful){
   WanderDestination=Goal.Location;Wait=0;LastPosition=GetActorLocation();RouteCheckTime=0;
   UE_LOG(LogTemp,Display,TEXT("TERRAIN_ROBOT %d route from %s to %s"),RobotId,*GetActorLocation().ToString(),*Goal.Location.ToString());return;
  }
 }
 Wait=FMath::FRandRange(2.f,5.f);
}

void AC17Robot::SetupPlayerInputComponent(UInputComponent* Input){
 Super::SetupPlayerInputComponent(Input);
 Input->BindAxis("Forward",this,&AC17Robot::RemoteForward);Input->BindAxis("Right",this,&AC17Robot::RemoteRight);
 Input->BindAxis("Turn",this,&AC17Robot::RemoteTurn);Input->BindAxis("Look",this,&AC17Robot::RemoteLook);
 Input->BindAction("Jump",IE_Pressed,this,&ACharacter::Jump);Input->BindAction("Jump",IE_Released,this,&ACharacter::StopJumping);
}
void AC17Robot::RemoteForward(float Value){if(IsPlayerControlled())AddMovementInput(FRotationMatrix(FRotator(0,GetControlRotation().Yaw,0)).GetUnitAxis(EAxis::X),Value);}
void AC17Robot::RemoteRight(float Value){if(IsPlayerControlled())AddMovementInput(FRotationMatrix(FRotator(0,GetControlRotation().Yaw,0)).GetUnitAxis(EAxis::Y),Value);}
void AC17Robot::RemoteTurn(float Value){AddControllerYawInput(Value);}
void AC17Robot::RemoteLook(float Value){AddControllerPitchInput(Value);}
void AC17Robot::SetEmbodied(bool Active){
 if(Active)Tags.AddUnique(TEXT("RobotEmbodied"));else Tags.Remove(TEXT("RobotEmbodied"));
 GetCharacterMovement()->StopMovementImmediately();GetCharacterMovement()->bOrientRotationToMovement=!Active;bUseControllerRotationYaw=Active;
 GetMesh()->SetOwnerNoSee(Active);GetCharacterMovement()->MaxWalkSpeed=Active?260:WanderSpeed;
 // Manual movement must not count toward the autonomous route-stall timer.
 Stuck=0;LastTaskDistance=MAX_flt;LastPosition=GetActorLocation();
 if(!Active && Phase==ERobotTaskPhase::Working && IsValid(TaskResource)){
  // Re-approach the reserved resource before restarting work after manual movement.
  Phase=ERobotTaskPhase::Travelling;WorkRemaining=0;
  TaskStatus=TEXT("Resuming collection of ")+TaskResource->DisplayName;
 }
 Current=nullptr;
 WanderDestination=FVector::ZeroVector;Wait=1;RouteCheckTime=0;
}

