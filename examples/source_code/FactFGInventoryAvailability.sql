CREATE PROC [Common].[LoadFactFGInventoryAvailability] AS
BEGIN

MERGE Common.FactFGInventoryAvailability T
   USING stage.FactFGInventoryAvailability S ON S.InventoryAvailabilityKey = T.InventoryAvailabilityKey
   WHEN MATCHED AND NOT EXISTS
   (
   SELECT    
		S.[Plant],
		S.[Material],
		S.[GridValue],
		S.[ATPDate],
		S.[StorLoc],
		S.[DemandQty],
		S.[ATPQty],
		S.[AvailableInvQty],
		S.[AllocatedQty],
		S.[UnallocatedQty],
		S.[PurchaseReqQty],
		S.[BlockedStockQty],
		S.[QualityInspQty],
		S.[ItemID],
		S.[ItemKey],
		S.[FacilityID],
		S.[FacilityKey],
		S.[AsOfDate],
		S.[AsOfDateKey]
   INTERSECT
   SELECT    
		T.[Plant],
		T.[Material],
		T.[GridValue],
		T.[ATPDate],
		T.[StorLoc],
		T.[DemandQty],
		T.[ATPQty],
		T.[AvailableInvQty],
		T.[AllocatedQty],
		T.[UnallocatedQty],
		T.[PurchaseReqQty],
		T.[BlockedStockQty],
		T.[QualityInspQty],
		T.[ItemID],
		T.[ItemKey],
		T.[FacilityID],
		T.[FacilityKey],
		T.[AsOfDate],
		T.[AsOfDateKey]		
   ) THEN
   UPDATE SET
		Plant=S.[Plant],
		Material=S.[Material],
		GridValue=S.[GridValue],
		ATPDate=S.[ATPDate],
		StorLoc=S.[StorLoc],
		DemandQty=S.[DemandQty],
		ATPQty=S.[ATPQty],
		AvailableInvQty=S.[AvailableInvQty],
		AllocatedQty=S.[AllocatedQty],
		UnallocatedQty=S.[UnallocatedQty],
		PurchaseReqQty=S.[PurchaseReqQty],
		BlockedStockQty=S.[BlockedStockQty],
		QualityInspQty=S.[QualityInspQty],
		ItemID=S.[ItemID],
		ItemKey=S.[ItemKey],
		FacilityID=S.[FacilityID],
		FacilityKey=S.[FacilityKey],
		AsOfDate=S.[AsOfDate],
		AsOfDateKey=S.[AsOfDateKey],
        [UpdatedOn] = SYSDATETIMEOFFSET();
		
		  
   INSERT INTO [Common].[FactFGInventoryAvailability]
   (
		[Plant],
		[Material],
		[GridValue],
		[ATPDate],
		[StorLoc],
		[DemandQty],
		[ATPQty],
		[AvailableInvQty],
		[AllocatedQty],
		[UnallocatedQty],
		[PurchaseReqQty],
		[BlockedStockQty],
		[QualityInspQty],
		[ItemID],
		[ItemKey],
		[FacilityID],
		[FacilityKey],
		[AsOfDate],
		[AsOfDateKey],
		[InventoryAvailabilityKey],
		[CreatedOn],
		[UpdatedOn]
   )
   SELECT
		S.[Plant],
		S.[Material],
		S.[GridValue],
		S.[ATPDate],
		S.[StorLoc],
		S.[DemandQty],
		S.[ATPQty],
		S.[AvailableInvQty],
		S.[AllocatedQty],
		S.[UnallocatedQty],
		S.[PurchaseReqQty],
		S.[BlockedStockQty],
		S.[QualityInspQty],
		S.[ItemID],
		S.[ItemKey],
		S.[FacilityID],
		S.[FacilityKey],
		S.[AsOfDate],
		S.[AsOfDateKey],
		S.[InventoryAvailabilityKey],
		SYSDATETIMEOFFSET(),
		SYSDATETIMEOFFSET()
	FROM 
		[stage].[FactFGInventoryAvailability] S
		LEFT OUTER JOIN [Common].[FactFGInventoryAvailability] T
			on S.InventoryAvailabilityKey = T.[InventoryAvailabilityKey]
	WHERE 
		T.[InventoryAvailabilityKey] IS NULL
	;
   
UPDATE STATISTICS Common.FactFGInventoryAvailability;
   
END