# Generate Entity for Demo

```python
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

def example_generate_entity_for_demo():
    name = "stage.InventoryAvailability"
    system_name = "SQL_DW"
    typename = "azure_sql_dw_table"
    columns_dict = INVENTORY_SCHEMA
    generate_entity(name, typename, system_name, columns_dict)
```