#include "RobotTerminal.h"
#include "C17Robot.h"
#include "SalvageLedger.h"
#include "Components/StaticMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/TextureRenderTarget2D.h"
#include "Engine/World.h"
#include "Engine/GameInstance.h"
#include "Engine/GameViewportClient.h"
#include "Engine/Engine.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "UObject/ConstructorHelpers.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/Images/SImage.h"
#include "Widgets/Text/STextBlock.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Input/SEditableTextBox.h"
ARobotTerminal::ARobotTerminal(){
 PrimaryActorTick.bCanEverTick=true;RootComponent=CreateDefaultSubobject<USceneComponent>(TEXT("WallMount"));
 static ConstructorHelpers::FObjectFinder<UStaticMesh> Cube(TEXT("/Engine/BasicShapes/Cube.Cube"));static ConstructorHelpers::FObjectFinder<UStaticMesh> Plane(TEXT("/Engine/BasicShapes/Plane.Plane"));
 auto* Frame=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Frame"));Frame->SetupAttachment(RootComponent);Frame->SetStaticMesh(Cube.Object);Frame->SetRelativeScale3D(FVector(.06,1.4,.9));
 static ConstructorHelpers::FObjectFinder<UMaterialInterface> Metal(TEXT("/Game/Conservatory/Robots/C17/M_C17_Graphite.M_C17_Graphite"));Frame->SetMaterial(0,Metal.Object);
 Screen=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Display"));Screen->SetupAttachment(RootComponent);Screen->SetStaticMesh(Plane.Object);Screen->SetRelativeLocation(FVector(3.2,0,0));Screen->SetRelativeRotation(FRotator(90,0,0));Screen->SetRelativeScale3D(FVector(.675,1.2,1));
 auto* Label=CreateDefaultSubobject<UTextRenderComponent>(TEXT("Label"));Label->SetupAttachment(RootComponent);Label->SetRelativeLocation(FVector(3.5,0,-41));Label->SetWorldSize(4);Label->SetHorizontalAlignment(EHTA_Center);Label->SetVerticalAlignment(EVRTA_TextCenter);Label->SetText(FText::FromString(TEXT("[F]  FIELD OPERATIONS  /  C-17")));Label->SetTextRenderColor(FColor(220,230,210));
 FeedBrush.ImageSize=FVector2D(1024,576);FeedBrush.DrawAs=ESlateBrushDrawType::Image;
}
void ARobotTerminal::BeginPlay(){Super::BeginPlay();ScreenMaterial=Screen->CreateDynamicMaterialInstance(0);}
bool ARobotTerminal::CanUse() const{
 auto* PC=UGameplayStatics::GetPlayerController(this,0);APawn* Pawn=PC?PC->GetPawn():nullptr;if(!Pawn || FVector::Dist(Pawn->GetActorLocation(),GetActorLocation())>260)return false;
 FVector Eye;FRotator View;PC->GetPlayerViewPoint(Eye,View);if(FVector::DotProduct(View.Vector(),(GetActorLocation()-Eye).GetSafeNormal())<.55)return false;
 FHitResult Hit;FCollisionQueryParams Params;Params.AddIgnoredActor(Pawn);return GetWorld()->LineTraceSingleByChannel(Hit,Eye,GetActorLocation(),ECC_Visibility,Params) && Hit.GetActor()==this;
}
void ARobotTerminal::Tick(float D){
 Super::Tick(D);auto* PC=UGameplayStatics::GetPlayerController(this,0);if(!PC || !PC->GetPawn())return;
 if(IsValid(Robot)){
  Robot->SetFeedActive(Open || FVector::Dist(PC->GetPawn()->GetActorLocation(),GetActorLocation())<1100);
  if(!FeedBound && Robot->GetFeed()){if(ScreenMaterial)ScreenMaterial->SetTextureParameterValue(TEXT("CameraFeed"),Robot->GetFeed());FeedBrush.SetResourceObject(Robot->GetFeed());FeedBound=true;}
 }
 if(Open || (GetWorld()->GetGameViewport() && GetWorld()->GetGameViewport()->IgnoreInput()))return;
 if(CanUse()){if(GEngine)GEngine->AddOnScreenDebugMessage(uint64(GetUniqueID()),.1f,FColor(215,230,190),TEXT("[F] C-17 field operations"));if(PC->WasInputKeyJustPressed(EKeys::F))OpenConsole();}
}
FString ARobotTerminal::InventoryText() const{return GetGameInstance()->GetSubsystem<USalvageLedger>()->Summary();}
bool ARobotTerminal::OpenConsole(){
 if(Open || !CanUse() || !IsValid(Robot) || !Robot->GetFeed() || !GEngine || !GEngine->GameViewport)return false;
 Open=true;Robot->SetFeedActive(true);FeedBrush.SetResourceObject(Robot->GetFeed());
 auto Text=[](const TCHAR* T){return FText::FromString(T);};
 Panel=SNew(SBox).HAlign(HAlign_Center).VAlign(VAlign_Center)[SNew(SBox).WidthOverride(1040)[SNew(SBorder).BorderImage(FCoreStyle::Get().GetBrush("WhiteBrush")).BorderBackgroundColor(FLinearColor(.016f,.032f,.035f,1)).Padding(20)[SNew(SVerticalBox)
 +SVerticalBox::Slot().AutoHeight().Padding(0,0,0,8)[SNew(SHorizontalBox)
 +SHorizontalBox::Slot().FillWidth(1)[SNew(STextBlock).Font(FCoreStyle::GetDefaultFontStyle("Bold",20)).Text(Text(TEXT("FIELD OPERATIONS  /  C-17")))]
 +SHorizontalBox::Slot().AutoWidth()[SNew(SButton).Text(Text(TEXT("Return to habitat"))).OnClicked_Lambda([this](){CloseConsole();return FReply::Handled();})]]
 +SVerticalBox::Slot().AutoHeight().Padding(0,0,0,8)[SNew(STextBlock).AutoWrapText(true).Text_Lambda([this](){return FText::FromString(IsValid(Robot)?Robot->GetTaskStatus():TEXT("Field unit unavailable."));})]
 +SVerticalBox::Slot().AutoHeight().HAlign(HAlign_Center)[SNew(SBox).WidthOverride(960).HeightOverride(540)[SNew(SImage).Image(&FeedBrush).OnMouseButtonDown_Lambda([this](const FGeometry& G,const FPointerEvent& E){if(E.GetEffectingButton()==EKeys::LeftMouseButton && IsValid(Robot)){const FVector2D P=G.AbsoluteToLocal(E.GetScreenSpacePosition());const FVector2D Size=G.GetLocalSize();if(Size.X>0 && Size.Y>0)Robot->SelectFeedPoint(FVector2D(P.X/Size.X,P.Y/Size.Y));return FReply::Handled();}return FReply::Unhandled();})]]
 +SVerticalBox::Slot().AutoHeight().Padding(0,8)[SNew(STextBlock).Text(Text(TEXT("Click a resource in the live view, choose a task, or type one below.")))]
 +SVerticalBox::Slot().AutoHeight()[SNew(SHorizontalBox)
 +SHorizontalBox::Slot().FillWidth(1)[SAssignNew(TaskEntry,SEditableTextBox).HintText(Text(TEXT("collect timber / collect stone / collect copper"))).OnTextCommitted_Lambda([this](const FText&,ETextCommit::Type C){if(C==ETextCommit::OnEnter)SendTypedTask();})]
 +SHorizontalBox::Slot().AutoWidth().Padding(8,0)[SNew(SButton).Text(Text(TEXT("Send task"))).OnClicked_Lambda([this](){SendTypedTask();return FReply::Handled();})]]
 +SVerticalBox::Slot().AutoHeight().Padding(0,8)[SNew(SHorizontalBox)
 +SHorizontalBox::Slot().FillWidth(1)[SNew(SButton).Text(Text(TEXT("Collect timber"))).OnClicked_Lambda([this](){if(IsValid(Robot))Robot->SubmitTask(TEXT("collect timber"));return FReply::Handled();})]
 +SHorizontalBox::Slot().FillWidth(1).Padding(6,0)[SNew(SButton).Text(Text(TEXT("Collect stone"))).OnClicked_Lambda([this](){if(IsValid(Robot))Robot->SubmitTask(TEXT("collect stone"));return FReply::Handled();})]
 +SHorizontalBox::Slot().FillWidth(1)[SNew(SButton).Text(Text(TEXT("Collect copper"))).OnClicked_Lambda([this](){if(IsValid(Robot))Robot->SubmitTask(TEXT("collect copper"));return FReply::Handled();})]
 +SHorizontalBox::Slot().AutoWidth().Padding(8,0,0,0)[SNew(SButton).Text(Text(TEXT("Cancel task"))).OnClicked_Lambda([this](){if(IsValid(Robot))Robot->CancelTask();return FReply::Handled();})]]
 +SVerticalBox::Slot().AutoHeight()[SNew(STextBlock).AutoWrapText(true).Text_Lambda([this](){return FText::FromString(InventoryText());})]
 ]]];
 GEngine->GameViewport->AddViewportWidgetContent(Panel.ToSharedRef(),100);auto* PC=UGameplayStatics::GetPlayerController(this,0);if(auto* C=Cast<ACharacter>(PC->GetPawn()))C->GetCharacterMovement()->StopMovementImmediately();PC->FlushPressedKeys();PC->SetInputMode(FInputModeUIOnly().SetWidgetToFocus(TaskEntry));PC->bShowMouseCursor=true;return true;
}
void ARobotTerminal::SendTypedTask(){if(IsValid(Robot) && TaskEntry){if(Robot->SubmitTask(TaskEntry->GetText().ToString()))TaskEntry->SetText(FText::GetEmpty());}}
void ARobotTerminal::CloseConsole(){if(Panel && GEngine && GEngine->GameViewport)GEngine->GameViewport->RemoveViewportWidgetContent(Panel.ToSharedRef());Panel.Reset();TaskEntry.Reset();Open=false;if(auto* PC=UGameplayStatics::GetPlayerController(this,0)){PC->SetInputMode(FInputModeGameOnly());PC->bShowMouseCursor=false;}}
void ARobotTerminal::EndPlay(const EEndPlayReason::Type Reason){if(Open)CloseConsole();if(IsValid(Robot))Robot->SetFeedActive(false);Super::EndPlay(Reason);}

