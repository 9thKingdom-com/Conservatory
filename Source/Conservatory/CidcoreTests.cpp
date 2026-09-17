#include "CidcoreIntercom.h"
#include "Misc/AutomationTest.h"
#if WITH_DEV_AUTOMATION_TESTS
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FCidcoreLocationTest,"Conservatory.CIDCORE.Location",EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter)
bool FCidcoreLocationTest::RunTest(const FString&) {
 TestEqual(TEXT("Passage"),UCidcoreIntercom::LocationAt(FVector(-10600,0,6350)),FString(TEXT("Conservatory connecting passage")));
 TestEqual(TEXT("North dome"),UCidcoreIntercom::LocationAt(FVector(-10600,1411,6350)),FString(TEXT("Conservatory north dome")));
 TestEqual(TEXT("Seed lab"),UCidcoreIntercom::LocationAt(FVector(-15400,-1500,4090)),FString(TEXT("01 Seed Laboratory")));
 TestEqual(TEXT("Waste treatment"),UCidcoreIntercom::LocationAt(FVector(-15400,1500,3490)),FString(TEXT("11 Waste treatment")));
 TestEqual(TEXT("Corridor not nearest room"),UCidcoreIntercom::LocationAt(FVector(-14500,-1500,4090)),FString(TEXT("Bunker circulation / service lift")));
 TestEqual(TEXT("Unknown area"),UCidcoreIntercom::LocationAt(FVector(0,0,100)),FString(TEXT("Outside / unclassified area")));
 return true;
}
#endif
