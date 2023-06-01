/****** Object:  StoredProcedure [dbo].[usp_Facility_SAP_HBI_DW_DLY_FACILITY_SAP]    Script Date: 9/23/2020 1:42:57 PM ******/

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[usp_Facility_SAP_HBI_DW_DLY_FACILITY_SAP]') AND type in (N'P', N'PC'))
BEGIN
EXEC dbo.sp_executesql @statement = N'CREATE PROCEDURE [dbo].[usp_Facility_SAP_HBI_DW_DLY_FACILITY_SAP] AS' 
END
GO
ALTER PROC [dbo].[usp_Facility_SAP_HBI_DW_DLY_FACILITY_SAP] AS
BEGIN
TRUNCATE TABLE stage.Facility_SAP_HBI_DW_DLY_FACILITY_SAP; 
--Insert from Polybase mount.'' schema 

declare @InputRowCount int = 0
declare @NewRowCount int = 0


INSERT INTO stage.Facility_SAP_HBI_DW_DLY_FACILITY_SAP(
      [XFAC_PLANT]
      ,[XFAC_NAME]
      ,[XFAC_NAME2]
      ,[XFAC_ADDR]
      ,[XFAC_CITY]
      ,[XFAC_COUNTRY]
      ,[XFAC_DIVISION]
      ,[XFAC_LBU]
      ,[XFAC_FAC_CDE]
      ,[XFAC_SHPPNT]
      ,[XFAC_TSP]
      ,[FACILITY_TYPE]
  )
SELECT [XFAC_PLANT]
      ,[XFAC_NAME]
      ,[XFAC_NAME2]
      ,[XFAC_ADDR]
      ,[XFAC_CITY]
      ,[XFAC_COUNTRY]
      ,[XFAC_DIVISION]
      ,[XFAC_LBU]
      ,[XFAC_FAC_CDE]
      ,[XFAC_SHPPNT]
      ,[XFAC_TSP]
      ,[FACILITY_TYPE]
  FROM [mount].[Facility_SAP_HBI_DW_DLY_FACILITY_SAP];

END


SELECT 
@InputRowCount = COUNT(1)
FROM   mount.Inventory_sto_header_SAP

SELECT 
@NewRowCount = COUNT(1)
FROM  stage.mount_Inventory_sto_header_SAP

SELECT 
[SourceRecordsRead] = @InputRowCount,
[RowsInsertedCount] = @NewRowCount
GO
