#pragma once
#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "ExteriorTools.generated.h"
UCLASS()
class CONSERVATORYEDITOR_API UExteriorTools : public UBlueprintFunctionLibrary {
 GENERATED_BODY()
public:
 UFUNCTION(BlueprintCallable,Category="Exterior") static bool RegisterReddishGreyRockLayer();
 UFUNCTION(BlueprintCallable,Category="Exterior") static bool PaintStudyLayer(const FString& RawFile, const FString& LayerName);
 UFUNCTION(BlueprintCallable,Category="Exterior") static bool BuildTerrainNavigation();
 UFUNCTION(BlueprintCallable,Category="Exterior") static AActor* CreateTerrain(const FString& HeightFile, UMaterialInterface* Material);
 UFUNCTION(BlueprintCallable,Category="Exterior") static AActor* CreateInstances(UStaticMesh* Mesh, const TArray<FTransform>& Transforms, const FString& Label, bool Collision);
};
