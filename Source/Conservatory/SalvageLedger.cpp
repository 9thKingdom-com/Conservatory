#include "SalvageLedger.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
static const FString SalvageSlot=TEXT("Conservatory_C17_Salvage_v1");
void USalvageLedger::Initialize(FSubsystemCollectionBase& C){
 Super::Initialize(C);Inspection=FParse::Param(FCommandLine::Get(),TEXT("RobotTaskInspection"));
 if(!Inspection && UGameplayStatics::DoesSaveGameExist(SalvageSlot,0))Data=Cast<USalvageSave>(UGameplayStatics::LoadGameFromSlot(SalvageSlot,0));
 if(!Data)Data=Cast<USalvageSave>(UGameplayStatics::CreateSaveGameObject(USalvageSave::StaticClass()));
}
bool USalvageLedger::WasDelivered(FName Site) const{return Data && Data->DeliveredSites.Contains(Site);}
int32 USalvageLedger::Count(FName Kind) const{return Data?Data->Inventory.FindRef(Kind):0;}
void USalvageLedger::RecordEvent(const FString& Event){LatestEvent=Event;LatestEventAt=GetGameInstance()->GetWorld()->GetTimeSeconds();}
bool USalvageLedger::Deliver(FName Site,FName Kind,int32 Quantity){
 if(!Data || Site.IsNone() || Quantity<1 || WasDelivered(Site))return false;
 Data->DeliveredSites.Add(Site);Data->Inventory.FindOrAdd(Kind)+=Quantity;
 SaveFailed=!Inspection && !UGameplayStatics::SaveGameToSlot(Data,SalvageSlot,0);
 RecordEvent(FString::Printf(TEXT("C-17 delivered %d %s to the exterior collection bay."),Quantity,*Kind.ToString()));return true;
}
FString USalvageLedger::Summary() const{return FString::Printf(TEXT("DELIVERED   Timber logs: %d   |   Stone pieces: %d   |   Copper spools: %d%s"),Count(TEXT("timber")),Count(TEXT("stone")),Count(TEXT("copper")),SaveFailed?TEXT("   (save failed; retained this session)"):TEXT(""));}
