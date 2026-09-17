#include "CidcoreIntercom.h"
#include "HttpModule.h"
#include "Interfaces/IHttpResponse.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"
#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/Pawn.h"
#include "MediaPlayer.h"
#include "MediaSoundComponent.h"
#include "Widgets/SWeakWidget.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/Layout/SScrollBox.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/Text/STextBlock.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Input/SCheckBox.h"
#include "Widgets/Input/SEditableTextBox.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Engine/World.h"

UCidcoreIntercom::UCidcoreIntercom() { PrimaryComponentTick.bCanEverTick=true; }
void UCidcoreIntercom::BeginPlay() {
 Super::BeginPlay();
 Media=NewObject<UMediaPlayer>(this); Media->PlayOnOpen=true;
 Media->OnMediaOpenFailed.AddDynamic(this,&UCidcoreIntercom::AudioFailed);
 Media->OnMediaOpened.AddDynamic(this,&UCidcoreIntercom::AudioOpened);
 Sound=NewObject<UMediaSoundComponent>(GetOwner()); Sound->SetMediaPlayer(Media); Sound->RegisterComponent(); Sound->Start();
#if !UE_BUILD_SHIPPING
 if(FParse::Param(FCommandLine::Get(),TEXT("CidcoreBench"))) {
  Token=FPlatformMisc::GetEnvironmentVariable(TEXT("CIDCORE_BENCH_TOKEN"));
  Status=Token.IsEmpty()?TEXT("Bench token missing. Sign in or set CIDCORE_BENCH_TOKEN before launch."):TEXT("Development bench session ready.");
 }
#endif
 Location=LocationAt(GetOwner()->GetActorLocation());
}
FString UCidcoreIntercom::LocationAt(const FVector& P) {
 // Bounds match BunkerLayout.json and ModularPlacement.json (centimetres).
 static const TCHAR* Rooms[]={TEXT("01 Seed Laboratory"),TEXT("02 Library & study"),TEXT("03 Sleeping quarters"),TEXT("04 Food reserve"),TEXT("05 Clinic"),TEXT("06 Kitchen & washrooms"),TEXT("07 Water & pumping"),TEXT("08 Air & oxygen"),TEXT("09 Power reserve"),TEXT("10 Workshop"),TEXT("11 Waste treatment"),TEXT("12 Equipment stores")};
 for(int Floor=0;Floor<2;++Floor) for(int Row=0;Row<3;++Row) for(int Side=0;Side<2;++Side) {
  const float Z=Floor==0?4000:3400;
  if(FMath::Abs(P.X-(Side==0?-15400:-13600))<600 && FMath::Abs(P.Y-(-1500+Row*1500))<700 && P.Z>Z && P.Z<Z+360) return Rooms[Floor*6+Row*2+Side];
 }
 if(P.X>-16200 && P.X<-12800 && P.Y>-3100 && P.Y<3100 && P.Z>3350 && P.Z<4450) return TEXT("Bunker circulation / service lift");
 if(P.Z>6240 && P.Z<7800) {
  if(FMath::Abs(P.X+10600)<204 && FMath::Abs(P.Y)<235) return TEXT("Conservatory connecting passage");
  for(int Side=-1;Side<=1;Side+=2) if(FVector2D(P.X+10600,P.Y-Side*1411.05).Size()<1175) return Side<0?TEXT("Conservatory south dome"):TEXT("Conservatory north dome");
 }
 return TEXT("Outside / unclassified area");
}
void UCidcoreIntercom::TickComponent(float D,ELevelTick T,FActorComponentTickFunction* F) {
 Super::TickComponent(D,T,F);
#if !UE_BUILD_SHIPPING
 if(FParse::Param(FCommandLine::Get(),TEXT("CidcoreSmokeTest")) && FParse::Param(FCommandLine::Get(),TEXT("CidcoreBench"))) {
  BenchTime+=D;
  if(BenchStage==0 && BenchTime>3) {Show();Voice=true;if(!Token.IsEmpty())Entry->SetText(FText::FromString(TEXT("Hello?")));if(!Token.IsEmpty())Submit();BenchStage=1;}
  if(BenchStage==1 && BenchTime>8 && !Busy && AudioDeadline==0) {
   auto Result=MakeShared<FJsonObject>();Result->SetBoolField(TEXT("reply_received"),!Reply.IsEmpty());Result->SetBoolField(TEXT("audio_opened"),AudioVerified);Result->SetStringField(TEXT("status"),Status);Result->SetStringField(TEXT("location"),Location);
   FString Out;FJsonSerializer::Serialize(Result,TJsonWriterFactory<>::Create(&Out));FFileHelper::SaveStringToFile(Out,*(FPaths::ProjectSavedDir()/TEXT("CidcoreSmokeTest.json")));
   FScreenshotRequest::RequestScreenshot(FPaths::ProjectSavedDir()/TEXT("Screenshots/CidcoreIntercom.png"),true,false);BenchStage=2;BenchTime=0;
  }
  if((BenchStage==2 && BenchTime>3) || BenchTime>110) FPlatformMisc::RequestExit(false);
 }
#endif
 const FString Next=LocationAt(GetOwner()->GetActorLocation());
 if(Next!=Location) { RecentEvent=FString::Printf(TEXT("Player moved from %s to %s."),*Location,*Next); Location=Next; }
 if(AudioDeadline>0 && FPlatformTime::Seconds()>AudioDeadline) AudioFailed(TEXT(""));
 if(!Open && GEngine) GEngine->AddOnScreenDebugMessage(uint64(GetUniqueID()),0.f,FColor(185,225,218),TEXT("[C] CIDCORE intercom"));
}
void UCidcoreIntercom::Toggle() { if(Open) Close(); else Show(); }
void UCidcoreIntercom::Show() {
 if(!GEngine || !GEngine->GameViewport) return;
 Open=true;
 auto Text=[](const FString& S){return FText::FromString(S);};
 Panel=SNew(SBox).HAlign(HAlign_Center).VAlign(VAlign_Center)[
 SNew(SBox).WidthOverride(680).HeightOverride(550)[SNew(SBorder).BorderImage(FCoreStyle::Get().GetBrush("WhiteBrush")).Padding(24).BorderBackgroundColor(FLinearColor(.025f,.055f,.06f,.98f))[
 SNew(SVerticalBox)
 +SVerticalBox::Slot().AutoHeight().Padding(0,0,0,12)[SNew(STextBlock).Font(FCoreStyle::GetDefaultFontStyle("Regular",14)).Text(Text(TEXT("CIDCORE  /  INTERCOM"))).Font(FCoreStyle::GetDefaultFontStyle("Bold",22))]
 +SVerticalBox::Slot().AutoHeight().Padding(0,0,0,12)[SNew(SHorizontalBox)
 +SHorizontalBox::Slot().AutoWidth().VAlign(VAlign_Center)[SNew(SBox).WidthOverride(14).HeightOverride(14)[SNew(SBorder).BorderImage(FCoreStyle::Get().GetBrush("WhiteBrush")).BorderBackgroundColor_Lambda([this](){return Busy?FLinearColor(1.f,.45f,.04f,1.f):FLinearColor(.012f,.018f,.018f,1.f);})]]
 +SHorizontalBox::Slot().FillWidth(1).Padding(10,0)[SNew(STextBlock).Font(FCoreStyle::GetDefaultFontStyle("Bold",14)).Text_Lambda([this](){return FText::FromString(Busy?(Token.IsEmpty()?TEXT("AUTHENTICATING"):TEXT("TRANSMIT / AWAITING REPLY")):TEXT("TRANSMIT / IDLE"));})]]
 +SVerticalBox::Slot().AutoHeight().Padding(0,0,0,10)[SNew(STextBlock).Font(FCoreStyle::GetDefaultFontStyle("Regular",14)).Text_Lambda([this](){return FText::FromString(Location);})]
 +SVerticalBox::Slot().AutoHeight().Padding(0,0,0,10)[SNew(STextBlock).Font(FCoreStyle::GetDefaultFontStyle("Regular",14)).AutoWrapText(true).Text_Lambda([this](){return FText::FromString(Status);})]
 +SVerticalBox::Slot().FillHeight(1).Padding(0,8)[SNew(SScrollBox)+SScrollBox::Slot()[SNew(STextBlock).Font(FCoreStyle::GetDefaultFontStyle("Regular",14)).AutoWrapText(true).Text_Lambda([this](){return FText::FromString(Reply);})]]
 +SVerticalBox::Slot().AutoHeight().Padding(0,8)[SAssignNew(Entry,SEditableTextBox).IsEnabled_Lambda([this](){return !Busy;}).HintText_Lambda([this](){return FText::FromString(Token.IsEmpty()?TEXT("Your 9th Kingdom email"):TEXT("Speak to CIDCORE (up to 4000 characters)"));}).OnTextCommitted_Lambda([this](const FText&,ETextCommit::Type How){if(How==ETextCommit::OnEnter) Submit();})]
 +SVerticalBox::Slot().AutoHeight().Padding(0,8)[SNew(SCheckBox).IsChecked_Lambda([this](){return Voice?ECheckBoxState::Checked:ECheckBoxState::Unchecked;}).OnCheckStateChanged_Lambda([this](ECheckBoxState S){Voice=S==ECheckBoxState::Checked;if(!Voice){Media->Close();AudioDeadline=0;}})[SNew(STextBlock).Font(FCoreStyle::GetDefaultFontStyle("Regular",14)).Text(Text(TEXT("Play CIDCORE's voice")))]]
 +SVerticalBox::Slot().AutoHeight()[SNew(SHorizontalBox)
 +SHorizontalBox::Slot().FillWidth(1)[SNew(SButton).IsEnabled_Lambda([this](){return !Busy;}).Text_Lambda([this](){return FText::FromString(Token.IsEmpty()?TEXT("Sign in"):TEXT("Send"));}).OnClicked_Lambda([this](){Submit();return FReply::Handled();})]
 +SHorizontalBox::Slot().AutoWidth().Padding(8,0)[SNew(SButton).Text(Text(TEXT("Sign out"))).OnClicked_Lambda([this](){Logout();return FReply::Handled();})]
 +SHorizontalBox::Slot().AutoWidth()[SNew(SButton).Text(Text(TEXT("Return to game"))).OnClicked_Lambda([this](){Close();return FReply::Handled();})]]
 +SVerticalBox::Slot().AutoHeight().Padding(0,12,0,0)[SNew(STextBlock).Font(FCoreStyle::GetDefaultFontStyle("Regular",14)).AutoWrapText(true).Text(Text(TEXT("Messages and location are sent to CIDCORE and saved in your shared companion memory. New players: 9thkingdom.com/signup.html")))]
 ]]];
 GEngine->GameViewport->AddViewportWidgetContent(Panel.ToSharedRef(),100);
 if(auto* PC=Cast<APlayerController>(Cast<APawn>(GetOwner())->GetController())) { PC->SetInputMode(FInputModeUIOnly().SetWidgetToFocus(Entry)); PC->bShowMouseCursor=true; PC->FlushPressedKeys(); }
}
void UCidcoreIntercom::Close() {
 if(Panel.IsValid() && GEngine && GEngine->GameViewport) GEngine->GameViewport->RemoveViewportWidgetContent(Panel.ToSharedRef());
 Panel.Reset(); Entry.Reset(); Open=false;
 if(auto* Pawn=Cast<APawn>(GetOwner())) if(auto* PC=Cast<APlayerController>(Pawn->GetController())) { PC->SetInputMode(FInputModeGameOnly()); PC->bShowMouseCursor=false; }
}
void UCidcoreIntercom::Logout() {
 if(Pending) { Pending->OnProcessRequestComplete().Unbind(); Pending->CancelRequest(); Pending.Reset(); }
 Busy=false; Token.Empty(); Reply.Empty(); Media->Close(); AudioDeadline=0; Status=TEXT("Signed out. Sign in to connect to CIDCORE."); if(Entry) Entry->SetText(FText::GetEmpty());
}
void UCidcoreIntercom::Submit() {
 if(Busy || !Entry) return;
 const FString Message=Entry->GetText().ToString().TrimStartAndEnd();
 if(Message.IsEmpty()) { Status=Token.IsEmpty()?TEXT("Enter your email."):TEXT("Enter a message for CIDCORE."); return; }
 auto Body=MakeShared<FJsonObject>();
 if(Token.IsEmpty()) { if(Message.Len()>254 || !Message.Contains(TEXT("@"))) {Status=TEXT("Enter a valid email address.");return;} Body->SetStringField(TEXT("email"),Message); Post(TEXT("https://9thkingdom.com/api/player/login.php"),Body,true); }
 else {
  if(Message.Len()>4000) {Status=TEXT("Please keep your message within 4000 characters.");return;}
  Body->SetStringField(TEXT("session_token"),Token); Body->SetStringField(TEXT("message"),Message); Body->SetBoolField(TEXT("enable_tts"),Voice);
  auto Context=MakeShared<FJsonObject>(); Context->SetStringField(TEXT("location"),LocationAt(GetOwner()->GetActorLocation()));
  if(!RecentEvent.IsEmpty()) Context->SetStringField(TEXT("recent_event"),RecentEvent.Left(300));
  Body->SetObjectField(TEXT("context"),Context); Media->Close(); AudioDeadline=0;
  Post(TEXT("https://cidcore.com/API/game/companion.php"),Body,false);
 }
}
void UCidcoreIntercom::Post(const FString& Url,const TSharedRef<FJsonObject>& Body,bool Login) {
 FString Json; FJsonSerializer::Serialize(Body,TJsonWriterFactory<>::Create(&Json));
 Busy=true; Status=Login?TEXT("Signing in..."):TEXT("Connecting to CIDCORE. A reply may take up to a minute...");
 Pending=FHttpModule::Get().CreateRequest(); Pending->SetURL(Url); Pending->SetVerb(TEXT("POST")); Pending->SetHeader(TEXT("Content-Type"),TEXT("application/json")); Pending->SetContentAsString(Json); Pending->SetTimeout(65.f);
 Pending->OnProcessRequestComplete().BindUObject(this,&UCidcoreIntercom::Receive,Login);
 if(!Pending->ProcessRequest()) {Pending.Reset();Busy=false;Status=TEXT("The intercom is quiet. Connection could not start; try again.");}
}
void UCidcoreIntercom::Receive(FHttpRequestPtr Request,FHttpResponsePtr Response,bool Connected,bool Login) {
 Pending.Reset(); Busy=false;
 const int Code=Response.IsValid()?Response->GetResponseCode():0;
 if(Code==401) {Token.Empty();Reply.Empty();Status=TEXT("Your session has expired. Sign in again.");if(Entry)Entry->SetText(FText::GetEmpty());return;}
 if(!Connected || Code!=200) {
  if(Code==429) Status=TEXT("The intercom is quiet. Hourly call limit reached; try later.");
  else if(Login && Code==404) Status=TEXT("No player found. Register at https://9thkingdom.com/signup.html.");
  else if(Login && Code==403) Status=TEXT("This account is suspended. Contact 9th Kingdom support.");
  else if(Code==400) Status=Login?TEXT("Please check your email."):TEXT("The message was rejected. Check its length and try again.");
  else Status=TEXT("The intercom is quiet. Connection failed or service unavailable. You can try again; a timed-out message may already have been saved.");
  return;
 }
 TSharedPtr<FJsonObject> Json; bool Success=false; FString Value;
 if(!FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Response->GetContentAsString()),Json) || !Json || !Json->TryGetBoolField(TEXT("success"),Success) || !Success || !Json->TryGetStringField(Login?TEXT("token"):TEXT("response"),Value) || Value.IsEmpty()) { Status=TEXT("The intercom is quiet. An unreadable response arrived; try again.");return; }
 if(Login) {Token=Value;Status=TEXT("Connected. You can speak to CIDCORE.");}
 else {
  Reply=Value; Status=TEXT("CIDCORE replied.");
  const TSharedPtr<FJsonObject>* Audio=nullptr; FString Url; bool AudioOK=false;
  if(Voice) {
   if(Json->TryGetObjectField(TEXT("audio"),Audio) && (*Audio)->TryGetBoolField(TEXT("success"),AudioOK) && AudioOK && (*Audio)->TryGetStringField(TEXT("audio_url"),Url) && Url.StartsWith(TEXT("/static/audio/responses/")) && !Url.Contains(TEXT("..")) && !Url.Contains(TEXT("?")) && !Url.Contains(TEXT("#"))) {
    AudioDeadline=FPlatformTime::Seconds()+30; if(!Media->OpenUrl(TEXT("https://cidcore.com")+Url)) AudioFailed(TEXT(""));
   } else Status=TEXT("CIDCORE replied. Voice unavailable; subtitles are shown.");
  }
 }
 if(Entry) Entry->SetText(FText::GetEmpty());
}
void UCidcoreIntercom::AudioFailed(FString Url) { AudioDeadline=0;Media->Close();Status=TEXT("CIDCORE replied. Voice could not play; subtitles are shown."); }
void UCidcoreIntercom::AudioOpened(FString Url) {AudioVerified=true;AudioDeadline=0;if(!Voice)Media->Close();}
void UCidcoreIntercom::EndPlay(const EEndPlayReason::Type Reason) {Logout();Close();if(Sound)Sound->Stop();Super::EndPlay(Reason);}




