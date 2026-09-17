#include "RobotVRHub.h"
#include "C17Robot.h"
#include "VRSuitStation.h"
#include "SalvageResource.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "AIController.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SphereComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/TextureRenderTarget2D.h"
#include "Engine/Texture2D.h"
#include "Engine/StaticMesh.h"
#include "Engine/Canvas.h"
#include "CanvasItem.h"
#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "Kismet/GameplayStatics.h"
#include "Kismet/KismetRenderingLibrary.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "UObject/ConstructorHelpers.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/Images/SImage.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Text/STextBlock.h"

ARobotVRHub::ARobotVRHub(){
 PrimaryActorTick.bCanEverTick=true;RootComponent=CreateDefaultSubobject<USceneComponent>(TEXT("WallMount"));
 static ConstructorHelpers::FObjectFinder<UStaticMesh> Cube(TEXT("/Engine/BasicShapes/Cube.Cube")),Plane(TEXT("/Engine/BasicShapes/Plane.Plane"));
 static ConstructorHelpers::FObjectFinder<UMaterialInterface> FrameMat(TEXT("/Game/Conservatory/Robots/C17/M_C17_Graphite.M_C17_Graphite"));
 auto* Frame=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MonitorFrame"));Frame->SetupAttachment(RootComponent);Frame->SetStaticMesh(Cube.Object);Frame->SetRelativeScale3D(FVector(.10,3.32,1.92));Frame->SetMaterial(0,FrameMat.Object);
 Screen=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("LiveScreen"));Screen->SetupAttachment(RootComponent);Screen->SetStaticMesh(Plane.Object);Screen->SetRelativeLocation(FVector(5.6,0,0));Screen->SetRelativeRotation(FRotator(0,-90,90));Screen->SetRelativeScale3D(FVector(3.2,1.8,1)); auto* Range=CreateDefaultSubobject<USphereComponent>(TEXT("InteractionRange"));Range->SetupAttachment(RootComponent);Range->SetSphereRadius(480.f);Range->SetCollisionEnabled(ECollisionEnabled::NoCollision);Range->SetHiddenInGame(true);
}
void ARobotVRHub::BeginPlay(){
 Super::BeginPlay();RefreshRobots();
#if WITH_EDITOR
 // Transient fixture for the opt-in saved-map regression; never saved in the level.
 if(FParse::Param(FCommandLine::Get(),TEXT("R11Inspection")))if(auto* Robot=FindRobot(11)){
  if(auto* Fixture=GetWorld()->SpawnActor<ASalvageResource>(Robot->GetActorLocation()+FVector(800,0,-76),FRotator::ZeroRotator))Fixture->SiteId=TEXT("R11_Runtime_Test");
 }
#endif
 if(auto* FrameMaterial=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Conservatory/Robots/VR/M_RackEnamel.M_RackEnamel"))){TInlineComponentArray<UStaticMeshComponent*> Parts(this);for(auto* Part:Parts)if(Part!=Screen)Part->SetMaterial(0,FrameMaterial);}
 MonitorTexture=UKismetRenderingLibrary::CreateRenderTarget2D(this,1600,900,RTF_RGBA8,FLinearColor::Black,false);
 TerrainMap=LoadObject<UTexture2D>(nullptr,TEXT("/Game/Conservatory/Robots/VR/T_TerrainMap.T_TerrainMap"));
 auto* Mat=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Conservatory/Robots/VR/M_SecurityScreen.M_SecurityScreen"));
 if(Mat){Screen->SetMaterial(0,Mat);auto* MID=Screen->CreateDynamicMaterialInstance(0);MID->SetTextureParameterValue(TEXT("ScreenImage"),MonitorTexture);}
 MonitorBrush.SetResourceObject(MonitorTexture);MonitorBrush.ImageSize=FVector2D(1600,900);SelectRobot(1);DrawMonitor();
}
AC17Robot* ARobotVRHub::FindRobot(int32 Id) const{for(auto& Robot:Robots)if(IsValid(Robot) && Robot->RobotId==Id)return Robot;return nullptr;}
void ARobotVRHub::RefreshRobots(){
 for(int32 i=Robots.Num()-1;i>=0;--i)if(!IsValid(Robots[i]))Robots.RemoveAt(i);
 for(TActorIterator<AC17Robot> It(GetWorld());It;++It){
  if(It->RobotId<1 || It->RobotId>11)continue;
  if(!Robots.Contains(*It))Robots.Add(*It);
 }
}
bool ARobotVRHub::SelectRobot(int32 Id){if(Id<1 || Id>11 || !FindRobot(Id) || IsRemote())return false;SelectedId=Id;CycleTimer=0;return true;}
bool ARobotVRHub::CanUse() const{
 auto* PC=UGameplayStatics::GetPlayerController(this,0);APawn* Pawn=PC?PC->GetPawn():nullptr;if(!Pawn || IsRemote() || FVector::Dist(Pawn->GetActorLocation(),GetActorLocation())>480)return false;
 FVector Eye;FRotator View;PC->GetPlayerViewPoint(Eye,View);if(FVector::DotProduct(View.Vector(),(GetActorLocation()-Eye).GetSafeNormal())<.6)return false;
 FHitResult Hit;FCollisionQueryParams Params;Params.AddIgnoredActor(Pawn);return GetWorld()->LineTraceSingleByChannel(Hit,Eye,GetActorLocation(),ECC_Visibility,Params) && Hit.GetActor()==this;
}
void ARobotVRHub::Tick(float D){
 Super::Tick(D);auto* PC=UGameplayStatics::GetPlayerController(this,0);if(!PC)return;
 // World Partition can stream actors in late; keep the robot roster self-healing.
 RescanTimer+=D;if(RescanTimer>2.f){RescanTimer=0;RefreshRobots();}
 const bool WatchingMonitor=!Panel && !PC->bShowMouseCursor && CanUse();
 CameraCommandTimer-=D;
 if(!WatchingMonitor || CameraCommandTimer<=0)CameraCommand.Reset();
 if(IsRemote()){
  if(!IsValid(ControlledRobot) || PC->WasInputKeyJustPressed(EKeys::R) || ControlledRobot->GetActorLocation().Z<-5000){ReturnToHuman();return;}
  if(GEngine)GEngine->AddOnScreenDebugMessage(uint64(GetUniqueID()),.1f,FColor(190,235,210),FString::Printf(TEXT("ROBOT %02d  |  WASD move - mouse look - Space jump  |  [R] Remove VR suit / return to Control Room"),SelectedId));
 }else if(WatchingMonitor){
  // Select R1 immediately; a following zero or one extends it to R10 or R11. No Enter required.
  if(PC->WasInputKeyJustPressed(EKeys::R)){CameraCommand=TEXT("R");CameraCommandTimer=2.f;}
  const FKey Digits[]={EKeys::Zero,EKeys::One,EKeys::Two,EKeys::Three,EKeys::Four,EKeys::Five,EKeys::Six,EKeys::Seven,EKeys::Eight,EKeys::Nine};
  const FKey NumDigits[]={EKeys::NumPadZero,EKeys::NumPadOne,EKeys::NumPadTwo,EKeys::NumPadThree,EKeys::NumPadFour,EKeys::NumPadFive,EKeys::NumPadSix,EKeys::NumPadSeven,EKeys::NumPadEight,EKeys::NumPadNine};
  for(int32 Digit=0;Digit<10;++Digit)if(!CameraCommand.IsEmpty() && (PC->WasInputKeyJustPressed(Digits[Digit]) || PC->WasInputKeyJustPressed(NumDigits[Digit]))){
   const int32 Id=CameraCommand==TEXT("R")?Digit:(CameraCommand==TEXT("R1") && Digit<=1?10+Digit:0);
   if(Id>=1 && SelectRobot(Id)){CameraCommand=FString::Printf(TEXT("R%d"),Id);CameraCommandTimer=2.f;}
   else CameraCommand.Reset();
  }
  if(GEngine)GEngine->AddOnScreenDebugMessage(uint64(GetUniqueID()),.1f,FColor(190,235,210),FString::Printf(TEXT("Type R1-R11: eye camera (no Enter) | Viewing R%d | [F] Inspect monitor%s"),SelectedId,CameraCommand==TEXT("R")?TEXT(" | R_ "):TEXT("")));
  if(PC->WasInputKeyJustPressed(EKeys::F))OpenMonitor();
 }
 const bool Nearby=PC->GetPawn() && FVector::Dist(PC->GetPawn()->GetActorLocation(),GetActorLocation())<2000;
 for(auto& Robot:Robots)if(IsValid(Robot))Robot->SetFeedActive(Robot->RobotId==SelectedId && (Nearby || IsRemote() || Panel.IsValid()));
 if(WatchingMonitor)CycleTimer=0;
 if(!IsRemote() && !Panel && !WatchingMonitor){CycleTimer+=D;if(CycleTimer>8)SelectRobot(SelectedId%11+1);}
 DrawTimer+=D;if(DrawTimer>.15f){DrawMonitor();DrawTimer=0;}
}
void ARobotVRHub::DrawMonitor(){
 if(!MonitorTexture || !GEngine)return;UCanvas* Canvas=nullptr;FVector2D Size;FDrawToRenderTargetContext Context;
 UKismetRenderingLibrary::BeginDrawCanvasToRenderTarget(this,MonitorTexture,Canvas,Size,Context);if(!Canvas)return;
 auto Fill=[Canvas](FVector2D P,FVector2D S,FLinearColor Color){FCanvasTileItem Tile(P,S,Color);Tile.BlendMode=SE_BLEND_Opaque;Canvas->DrawItem(Tile);};
 auto Text=[Canvas](FString Value,float X,float Y,float Scale=1.5f,FLinearColor Color=FLinearColor(.75,.88,.82,1)){Canvas->K2_DrawText(GEngine->GetMediumFont(),Value,FVector2D(X,Y),FVector2D(Scale),Color);};
 Fill(FVector2D::ZeroVector,Size,FLinearColor(.012,.023,.028,1));
 Text(TEXT("FIELD SECURITY  /  ROBOT NETWORK"),32,22,2);Text(FString::Printf(TEXT("%d / 11 UNITS ONLINE"),Robots.Num()),1160,28,1.4);
 const FVector2D MapOrigin(32,100);const float MapSize=680;
 if(TerrainMap)Canvas->K2_DrawTexture(TerrainMap,MapOrigin,FVector2D(MapSize),FVector2D::ZeroVector,FVector2D::UnitVector,FLinearColor::White,BLEND_Opaque);
 auto MapPoint=[MapOrigin,MapSize](FVector P){return MapOrigin+FVector2D((P.X+63000)/126000,(63000-P.Y)/126000)*MapSize;};
 for(auto& Robot:Robots)if(IsValid(Robot)){
  FVector2D P=MapPoint(Robot->GetActorLocation());FLinearColor Color=Robot->RobotId==SelectedId?FLinearColor(1,.66,.14):FLinearColor(.35,1,.7);
  Fill(P-FVector2D(5),FVector2D(10),Color);Text(FString::Printf(TEXT("%02d"),Robot->RobotId),P.X+7,P.Y-10,1.25,Color);
  Canvas->K2_DrawLine(P,P+FVector2D(Robot->GetActorForwardVector().X,-Robot->GetActorForwardVector().Y)*16,2,Color);
 }
 const FVector2D Habitat=MapPoint(FVector(-10600,0,0));Canvas->K2_DrawBox(Habitat-FVector2D(6),FVector2D(12),2,FLinearColor::White);Text(TEXT("HABITAT"),Habitat.X+10,Habitat.Y,1);
 Text(TEXT("N ^   WHOLE TERRAIN / 1.26 km"),32,802,1.25);
 auto* Selected=FindRobot(SelectedId);
 Text(FString::Printf(TEXT("ROBOT %02d / EYE CAMERA"),SelectedId),752,82,1.7);
 if(Selected && Selected->GetFeed())Canvas->K2_DrawTexture(Selected->GetFeed(),FVector2D(752,130),FVector2D(816,459),FVector2D::ZeroVector,FVector2D::UnitVector,FLinearColor::White,BLEND_Opaque);
 Text(IsRemote()?TEXT("MANUAL CONTROL / TASK PAUSED"):TEXT("AUTONOMOUS / SELECT A NUMBERED VR SUIT"),752,610,1.2);
 if(Selected){
  FString Status=Selected->GetTaskStatus();
  if(Selected->GetTaskPhase()==ERobotTaskPhase::None && Status.StartsWith(TEXT("Patrolling.")))Status=Selected->PatrolEnabled?TEXT("Roaming / no assigned task"):TEXT("Standby / no assigned task");
  Text(TEXT("TASK: ")+Status.Left(85),752,642,.95f);
 }
 for(int32 Id=1;Id<=11;++Id){
  auto* R=FindRobot(Id);const int32 Column=(Id-1)%2,Row=(Id-1)/2;const FVector P=R?R->GetActorLocation():FVector::ZeroVector;
  Text(R?FString::Printf(TEXT("%02d  X %+.0fm  Y %+.0fm"),Id,P.X/100,P.Y/100):FString::Printf(TEXT("%02d  OFFLINE"),Id),752+Column*410,676+Row*26,1.1,Id==SelectedId?FLinearColor(1,.66,.14):FLinearColor(.65,.8,.76));
 }
 Text(TEXT("Type R1-R11: camera   |   [F] Inspect / wear suit   |   In robot: [R] return"),32,860,1.15);
 UKismetRenderingLibrary::EndDrawCanvasToRenderTarget(this,Context);
}
bool ARobotVRHub::OpenMonitor(){
 if(Panel || !CanUse() || !GEngine || !GEngine->GameViewport)return false;
 auto Buttons=SNew(SHorizontalBox);
 for(int32 Id=1;Id<=11;++Id)Buttons->AddSlot().FillWidth(1).Padding(3)[SNew(SButton).Text(FText::FromString(FString::Printf(TEXT("View %02d"),Id))).OnClicked_Lambda([this,Id](){SelectRobot(Id);return FReply::Handled();})];
 Panel=SNew(SBox).HAlign(HAlign_Center).VAlign(VAlign_Center)[SNew(SBorder).Padding(12)[SNew(SVerticalBox)
 +SVerticalBox::Slot().AutoHeight()[SNew(SBox).WidthOverride(1100).HeightOverride(619)[SNew(SImage).Image(&MonitorBrush)]]
 +SVerticalBox::Slot().AutoHeight().Padding(0,8)[Buttons]
 +SVerticalBox::Slot().AutoHeight()[SNew(SButton).Text(FText::FromString(TEXT("Take control of R11 - lift service robot"))).OnClicked_Lambda([this](){EnterRobot(11);return FReply::Handled();})]
 +SVerticalBox::Slot().AutoHeight()[SNew(SButton).Text(FText::FromString(TEXT("Close monitor - approach a numbered suit and press F to wear it"))).OnClicked_Lambda([this](){CloseMonitor();return FReply::Handled();})]]];
 GEngine->GameViewport->AddViewportWidgetContent(Panel.ToSharedRef(),100);auto* PC=UGameplayStatics::GetPlayerController(this,0);if(auto* C=Cast<ACharacter>(PC->GetPawn()))C->GetCharacterMovement()->StopMovementImmediately();PC->FlushPressedKeys();PC->SetInputMode(FInputModeUIOnly().SetWidgetToFocus(Panel));PC->bShowMouseCursor=true;return true;
}
void ARobotVRHub::CloseMonitor(){if(Panel && GEngine && GEngine->GameViewport)GEngine->GameViewport->RemoveViewportWidgetContent(Panel.ToSharedRef());Panel.Reset();if(auto* PC=UGameplayStatics::GetPlayerController(this,0)){PC->SetInputMode(FInputModeGameOnly());PC->bShowMouseCursor=false;PC->FlushPressedKeys();}}
bool ARobotVRHub::EnterRobot(int32 Id){
 auto* PC=UGameplayStatics::GetPlayerController(this,0);auto* Robot=FindRobot(Id);auto* Body=PC?Cast<ACharacter>(PC->GetPawn()):nullptr;
 if(IsRemote() || !Robot || !Body || Cast<AC17Robot>(Body) || (Id!=11 && Robot->GetTaskPhase()!=ERobotTaskPhase::None))return false;
 // A relocated physical suit authorizes access using its own proximity, view and
 // line-of-sight checks; it does not have to remain beside the wall monitor.
 if(FVector::Dist(Body->GetActorLocation(),GetActorLocation())>2000){
  bool AtPairedSuit=false;
  for(TActorIterator<AVRSuitStation> It(GetWorld());It;++It){
   if(It->Hub==this && It->RobotId==Id && It->CanUse()){AtPairedSuit=true;break;}
  }
  if(!AtPairedSuit)return false;
 }
 // Keep the human body resident while the player is away: World Partition may otherwise stream out its cells.
 if(Body->CanChangeIsSpatiallyLoadedFlag())Body->SetIsSpatiallyLoaded(false);
 CloseMonitor();SelectedId=Id;Human=Body;HumanLocation=Body->GetActorLocation();HumanView=PC->GetControlRotation();Human->GetCharacterMovement()->StopMovementImmediately();
 ControlledRobot=Robot;SavedAI=Cast<AAIController>(Robot->GetController());if(SavedAI){SavedAI->StopMovement();SavedAI->UnPossess();}
 Robot->SetEmbodied(true);PC->Possess(Robot);PC->SetControlRotation(Robot->GetActorRotation());PC->SetInputMode(FInputModeGameOnly());PC->bShowMouseCursor=false;PC->FlushPressedKeys();
 if(PC->GetPawn()!=Robot){ReturnToHuman();return false;}UE_LOG(LogTemp,Display,TEXT("VR_ENTER robot=%d human=%s"),Id,*HumanLocation.ToString());return true;
}
bool ARobotVRHub::ReturnToHuman(){
 auto* PC=UGameplayStatics::GetPlayerController(this,0);if(!PC || !IsValid(Human))return false;
 auto* Robot=ControlledRobot.Get();PC->Possess(Human);Human->SetActorLocation(HumanLocation,false,nullptr,ETeleportType::TeleportPhysics);Human->GetCharacterMovement()->StopMovementImmediately();PC->SetControlRotation(HumanView);PC->FlushPressedKeys();PC->SetInputMode(FInputModeGameOnly());PC->bShowMouseCursor=false;
 if(IsValid(Robot)){Robot->SetEmbodied(false);if(IsValid(SavedAI))SavedAI->Possess(Robot);else Robot->SpawnDefaultController();}
 Human=nullptr;ControlledRobot=nullptr;SavedAI=nullptr;CycleTimer=0;UE_LOG(LogTemp,Display,TEXT("VR_RETURN robot=%d"),SelectedId);return true;
}
void ARobotVRHub::EndPlay(const EEndPlayReason::Type Reason){CloseMonitor();for(auto& Robot:Robots)if(IsValid(Robot))Robot->SetFeedActive(false);Super::EndPlay(Reason);}


