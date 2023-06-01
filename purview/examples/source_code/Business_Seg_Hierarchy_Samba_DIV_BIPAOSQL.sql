/****** Object:  Table [mount].[Business_Seg_Hierarchy_Samba_DIV_BIPAOSQL]   Script Date: 9/23/2020 1:42:56 PM ******/

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[mount].[Business_Seg_Hierarchy_Samba_DIV_BIPAOSQL]') AND type in (N'U'))
BEGIN
CREATE EXTERNAL TABLE [mount].[Business_Seg_Hierarchy_Samba_DIV_BIPAOSQL]
(
   [business_seg_hierarchy_id] [int] NOT NULL,
   [Division_id] [int] NOT NULL,
   [BusKey] [varchar](61) NULL,
   [business_seg_desc] [varchar](30) NULL,
   [strategic_business_unit_desc] [varchar](30) NULL,
   [SBU_Division_Group_desc] [varchar](40) NULL,
   [SBU_Division_Group_Sort] [int] NULL,
   [SBU_Division_SubGroup_desc] [varchar](40) NULL,
   [SBU_Division_SubGroup_Sort] [int] NULL,
   [SBU_Alt_Bus_Grouping_desc] [varchar](40) NULL,
   [SBU_Alt_Bus_Grouping_Sort] [int] NULL,
   [business_seg_order] [int] NULL,
   [reporting_sort_order] [int] NULL,
   [Division] [varchar](30) NULL,
   [Division_sort] [int] NULL,
   [Division_Group] [varchar](40) NULL,
   [Division_Group_sort] [int] NULL,
   [Business_Group] [varchar](40) NULL,
   [business_seg_group_sort] [int] NULL,
   [Operator] [varchar](1) NULL,
   [currency] [varchar](3) NULL
)
WITH (DATA_SOURCE = [ADLStorageGen2SSM],LOCATION = N'Master/Business/Seg_Hierarchy_Samba_DIV_BIPAOSQL/US/Business_Seg_Hierarchy_Samba_DIV_BIPAOSQL',FILE_FORMAT = [TextFileFormat_parquet],REJECT_TYPE = VALUE,REJECT_VALUE = 2)
END
GO
