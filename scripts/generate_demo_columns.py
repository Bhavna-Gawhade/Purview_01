FORECASTING_SCHEMA = {
    "ITEM_ID": "decimal",
    "STYLE_CD":"nvarchar",
    "COLOR_CD":"nvarchar",
    "SIZE_CD":"nvarchar",
    "ATTRIBUTE_CD":"nvarchar",
    "OPEN_ORDERS_UNITS":"decimal",
    "OPEN_EVENT_UNITS":"decimal",
    "TIL_UNITS":"decimal",
    "SAFETY_STOCK_UNITS":"decimal",
    "CYCLE_STOCK_UNITS":"decimal",
    "LEAD_TIME":"decimal",
    "AMD_UNITS":"decimal",
    "MAXBUILDS_UNITS":"decimal",
    "FORECAST_UNITS":"decimal",
    "HYBRID_FORECAST_UNITS":"decimal",
    "DEMAND_DATE":"date",
    "AS_OF_DATE":"date",
    "CREATE_TIMESTAMP":"date",
    "CREATE_USERID":"nvarchar",
    "DPR_NET_OPEN_ORDERS_UNITS":"decimal",
    "CUSTOMER_SHIP_DATE":"date",
    "DPR_GROSS_OPEN_ORDERS_UNITS":"decimal",
    "GROSS_DPR_DEMAND":"decimal",
    "NET_DPR_DEMAND":"decimal",
    "ORIGINAL_EVENT_UNITS":"decimal",
    "PIPELINE_INVENTORY":"decimal",
    "PLANT_CD":"nvarchar",
    "DC_TIL_UNITS":"decimal",
    "PREVIOUS_TIL_UNITS":"decimal",
    "UPDATE_TIMESTAMP":"date",
    "UPDATE_USERID":"nvarchar",
    "AWD_UNITS": "decimal"
}


INVENTORY_SCHEMA = {
    'MANDT': 'CLNT',
    'KEY1': 'RAW',
    'KEY2': 'RAW',
    'KEY3': 'RAW',
    'KEY4': 'RAW',
    'KEY5': 'RAW',
    'KEY6': 'RAW',
    'RECORD_TYPE': 'CHAR',
    'BUKRS': 'CHAR',
    'MATBF': 'CHAR',
    'WERKS': 'CHAR',
    'LGORT_SID': 'CHAR',
    'CHARG_SID': 'CHAR',
    'LIFNR_SID': 'CHAR',
    'MAT_KDAUF': 'CHAR',
    'MAT_KDPOS': 'NUMC',
    'MAT_PSPNR': 'NUMC',
    'KUNNR_SID': 'CHAR',
    'SOBKZ': 'CHAR',
    'LBBSA_SID': 'CHAR',
    'DISUB_OWNER_SID': 'CHAR',
    'RESOURCENAME_SID': 'CHAR',
    'PERIV': 'CHAR',
    'GJPER': 'NUMC',
    'GJPER_CURR_PER': 'NUMC',
    'STOCK_IND_L2': 'CHAR',
    'STOCK_VKWRT_L1': 'CURR',
    'STOCK_VKWRT_L2': 'CURR',
    'STOCK_QTY_L1': 'QUAN',
    'STOCK_QTY_L2': 'QUAN',
    '/CWM/STOCK_QTY_L1': 'QUAN',
    '/CWM/STOCK_QTY_L2': 'QUAN',
    'KZBWS': 'CHAR',
    'XOBEW': 'CHAR',
    'CPUDT_L1': 'DATS',
    'CPUDT_L2': 'DATS',
    'MEINS': 'UNIT',
    'WAERS': 'CUKY',
    'CONSUMPTION_QTY': 'QUAN',
    '/CWM/MEINS': 'UNIT',
    '/CWM/CONSUMPTION_QTY': 'QUAN',
    '/CWM/MEINS_SID': 'UNIT',
    'NAME1': 'CHAR',
    'BWKEY': 'CHAR',
    'KUNNR': 'CHAR',
    'LIFNR': 'CHAR',
    'FABKL': 'CHAR',
    'NAME2': 'CHAR',
    'STRAS': 'CHAR',
    'PFACH': 'CHAR',
    'PSTLZ': 'CHAR',
    'ORT01': 'CHAR'
}


MATERIAL_MASTER_SCHEMA = {
    "MANDT":"CLNT",
    "MATNR":"CHAR",
    "ERSDA":"DATS",
    "CREATED_AT_TIME":"TIMS",
    "ERNAM":"CHAR",
    "LAEDA":"DATS",
    "AENAM":"CHAR",
    "VPSTA":"CHAR",
    "MTART":"CHAR",
    "MBRSH":"CHAR",
    "MATKL":"CHAR",
    "BISMT":"CHAR",
    "MEINS":"UNIT",
    "BSTME":"UNIT",
    "VKORG":"CHAR",
    "VTWEG":"CHAR",
    "VERSG":"CHAR",
    "BONUS":"CHAR",
    "PROVG":"CHAR",
    "SKTOF":"CHAR",
    "WERKS":"CHAR",
    "PSTAT":"CHAR",
    "LVORM":"CHAR",
    "BWTTY":"CHAR",
    "VPRSV":"CHAR",
    "VERPR":"CURR",
    "STPRS":"CURR",
    "PEINH":"DEC"
}
