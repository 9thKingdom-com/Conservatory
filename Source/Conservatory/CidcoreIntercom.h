#pragma once
#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Interfaces/IHttpRequest.h"
#include "CidcoreIntercom.generated.h"
class SWidget;
class SEditableTextBox;
class UMediaPlayer;
class UMediaSoundComponent;

UCLASS(ClassGroup=(Conservatory))
class CONSERVATORY_API UCidcoreIntercom : public UActorComponent {
 GENERATED_BODY()
public:
 UCidcoreIntercom();
 virtual void BeginPlay() override;
 virtual void EndPlay(const EEndPlayReason::Type Reason) override;
 virtual void TickComponent(float Delta, ELevelTick Tick, FActorComponentTickFunction* Function) override;
 UFUNCTION(BlueprintCallable) void Toggle();
 bool IsTransmitting() const { return Busy; }
 static FString LocationAt(const FVector& Position);
private:
 void Show();
 void Close();
 void Submit();
 void Logout();
 void Post(const FString& Url, const TSharedRef<class FJsonObject>& Body, bool Login);
 void Receive(FHttpRequestPtr Request, FHttpResponsePtr Response, bool Connected, bool Login);
 UFUNCTION() void AudioFailed(FString Url);
 UFUNCTION() void AudioOpened(FString Url);
 FString Token, Status=TEXT("Sign in to connect to CIDCORE."), Reply, Location, RecentEvent;
 bool Busy=false, Voice=false, Open=false;
 double AudioDeadline=0;
 float BenchTime=0; int32 BenchStage=0; bool AudioVerified=false;
 TSharedPtr<SWidget> Panel;
 TSharedPtr<SEditableTextBox> Entry;
 FHttpRequestPtr Pending;
 UPROPERTY() TObjectPtr<UMediaPlayer> Media;
 UPROPERTY() TObjectPtr<UMediaSoundComponent> Sound;
};



