#include "ExteriorTools.h"
#include "Editor.h"
#include "Landscape.h"
#include "LandscapeInfo.h"
#include "Misc/FileHelper.h"
#include "Components/HierarchicalInstancedStaticMeshComponent.h"
#include "Builders/CubeBuilder.h"
#include "ActorFactories/ActorFactory.h"
#include "NavMesh/NavMeshBoundsVolume.h"
#include "NavigationSystem.h"
#include "EngineUtils.h"
#include "LandscapeEdit.h"
#include "LandscapeEditLayer.h"
#include "LandscapeLayerInfoObject.h"
bool UExteriorTools::RegisterReddishGreyRockLayer(){
 UWorld* World=GEditor->GetEditorWorldContext().World();
 if(!World || World->GetName()!=TEXT("L_Exterior_RobotVR"))return false;
 ALandscape* Land=nullptr;for(TActorIterator<ALandscape> It(World);It;++It){if(Land)return false;Land=*It;}
 if(!Land)return false;
 auto* Layer=LoadObject<ULandscapeLayerInfoObject>(nullptr,TEXT("/Game/Conservatory/Environment/MountainRock/LI_ReddishGreyRock.LI_ReddishGreyRock"));
 if(!Layer)return false;
 Layer->SetLayerName(TEXT("ReddishGreyRock"),true);
 Layer->SetBlendMethod(ELandscapeTargetLayerBlendMethod::None,true);
 FLandscapeTargetLayerSettings Settings;Settings.LayerInfoObj=Layer;
 Land->Modify();Land->AddTargetLayer(TEXT("ReddishGreyRock"),Settings);
 Layer->MarkPackageDirty();Land->MarkPackageDirty();Land->PostEditChange();
 return true;
}
bool UExteriorTools::PaintStudyLayer(const FString& RawFile, const FString& LayerName){
 UWorld* World=GEditor->GetEditorWorldContext().World();
 if(!World || World->GetName()!=TEXT("L_LandscapePaintStudy")) return false;
 if(LayerName!=TEXT("Gravel") && LayerName!=TEXT("Asphalt") && LayerName!=TEXT("Soil")) return false;
 TArray<uint8> Data; if(!FFileHelper::LoadFileToArray(Data,*RawFile) || Data.Num()!=505*505) return false;
 ALandscape* Land=nullptr; for(TActorIterator<ALandscape> It(World);It;++It){Land=*It;break;}
 if(!Land || !Land->GetEditLayer(0)) return false;
 FString Name=TEXT("LI_")+LayerName;
 FString PackageName=TEXT("/Game/Conservatory/Environment/LandscapePaintStudy/")+Name;
 UPackage* Package=CreatePackage(*PackageName);
 auto* Layer=FindObject<ULandscapeLayerInfoObject>(Package,*Name);
 if(!Layer) Layer=NewObject<ULandscapeLayerInfoObject>(Package,*Name,RF_Public|RF_Standalone|RF_Transactional);
 Layer->SetLayerName(FName(*LayerName),true);
 Layer->SetBlendMethod(ELandscapeTargetLayerBlendMethod::None,true);
 FLandscapeTargetLayerSettings Settings; Settings.LayerInfoObj=Layer;
 Land->Modify(); Land->AddTargetLayer(FName(*LayerName),Settings);
 { FLandscapeEditDataInterface Edit(Land->GetLandscapeInfo(),Land->GetEditLayer(0)->GetGuid());
   Edit.SetAlphaData(Layer,0,0,504,504,Data.GetData(),505); Edit.Flush(); }
 Layer->MarkPackageDirty(); Land->MarkPackageDirty(); Land->ForceLayersFullUpdate();
 return true;
}
bool UExteriorTools::BuildTerrainNavigation(){
 UWorld* World=GEditor->GetEditorWorldContext().World();
 ANavMeshBoundsVolume* Volume=nullptr;
 for(TActorIterator<ANavMeshBoundsVolume> It(World);It;++It)if(It->ActorHasTag(TEXT("TerrainRobotNavigation")))Volume=*It;
 if(!Volume){
  Volume=World->SpawnActor<ANavMeshBoundsVolume>();
  auto* Builder=NewObject<UCubeBuilder>();Builder->X=124000;Builder->Y=124000;Builder->Z=24000;
  UActorFactory::CreateBrushForVolumeActor(Volume,Builder);
  Volume->SetActorLocation(FVector(0,0,5000));Volume->SetActorLabel(TEXT("Robot navigation - whole terrain"));Volume->Tags.Add(TEXT("TerrainRobotNavigation"));Volume->SetFolderPath(TEXT("10 Wandering Mannequins"));
 }
 auto* Nav=FNavigationSystem::GetCurrent<UNavigationSystemV1>(World);
 if(!Nav){FNavigationSystem::AddNavigationSystemToWorld(*World,FNavigationSystemRunMode::EditorMode);Nav=FNavigationSystem::GetCurrent<UNavigationSystemV1>(World);}
 if(!Nav)return false;
 FlushAsyncLoading();Nav->RemoveNavigationBuildLock(ENavigationBuildLock::AsyncLoadLock,UNavigationSystemV1::ELockRemovalRebuildAction::NoRebuild);Nav->OnNavigationBoundsUpdated(Volume);Nav->OnWorldInitDone(FNavigationSystemRunMode::EditorMode);Nav->Tick(0.01f);UE_LOG(LogTemp,Display,TEXT("ROBOT_NAV bounds=%s registered=%d"),*Volume->GetComponentsBoundingBox(true).ToString(),Nav->GetNavigationBounds().Num());Nav->Build();return Nav->GetDefaultNavDataInstance(FNavigationSystem::DontCreate)!=nullptr;
}
AActor* UExteriorTools::CreateTerrain(const FString& HeightFile, UMaterialInterface* Material) {
 TArray<uint8> Bytes; if(!FFileHelper::LoadFileToArray(Bytes,*HeightFile) || Bytes.Num()!=505*505*2) return nullptr;
 TArray<uint16> Heights; Heights.SetNumUninitialized(505*505); FMemory::Memcpy(Heights.GetData(),Bytes.GetData(),Bytes.Num());
 UWorld* World=GEditor->GetEditorWorldContext().World();
 ALandscape* Land=World->SpawnActor<ALandscape>();
 Land->SetActorLocation(FVector(-63000,-63000,0)); Land->SetActorScale3D(FVector(250,250,100));
 Land->LandscapeMaterial=Material;
 TMap<FGuid,TArray<uint16>> HeightData; HeightData.Add(FGuid(),MoveTemp(Heights));
 TMap<FGuid,TArray<FLandscapeImportLayerInfo>> Layers; Layers.Add(FGuid(),TArray<FLandscapeImportLayerInfo>());
 Land->Import(FGuid::NewGuid(),0,0,504,504,1,63,HeightData,nullptr,Layers,ELandscapeImportAlphamapType::Additive,{});
 Land->SetActorLabel(TEXT("Landscape_WoodlandValley_1260m")); Land->SetFolderPath(TEXT("01 Landscape"));
 Land->PostEditChange(); return Land;
}
AActor* UExteriorTools::CreateInstances(UStaticMesh* Mesh, const TArray<FTransform>& Transforms, const FString& Label, bool Collision) {
 UWorld* World=GEditor->GetEditorWorldContext().World();
 AActor* Actor=World->SpawnActor<AActor>(); Actor->SetActorLabel(Label); Actor->SetFolderPath(TEXT("02 Woodland"));
 auto* Component=NewObject<UHierarchicalInstancedStaticMeshComponent>(Actor,TEXT("Instances"));
 Actor->SetRootComponent(Component); Actor->AddInstanceComponent(Component);
 Component->SetStaticMesh(Mesh); Component->SetMobility(EComponentMobility::Static);
 Component->SetCollisionProfileName(Collision ? TEXT("BlockAll") : TEXT("NoCollision"));
 Component->RegisterComponent(); Component->AddInstances(Transforms,false,true); return Actor;
}





