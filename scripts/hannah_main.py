##! /usr/bin/env python3


# Import Functions
# ---------------
from modules import entity, collection, glossary
from modules.classification.test_case_generator import *
from modules.classification.regex_generator import *
from modules.classification.shared_generator_functions import *
from modules.classification.classification import *
from modules.lineage.json_payload_lineage import *
from modules.lineage.shared_lineage_functions import *
from utils import get_credentials, create_purview_client
from generate_demo_entities import *


# Import Packages
# ---------------
from pathlib import Path
from pyapacheatlas.core.typedef import AtlasAttributeDef, AtlasStructDef, TypeCategory
from pyapacheatlas.core import AtlasEntity, AtlasProcess
from azure.core.exceptions import HttpResponseError
import json
import datetime
from pyapacheatlas.readers import ExcelConfiguration, ExcelReader


# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)


# Functions
# ---------------


# Main Function
# ---------------

def main():
    print()

    """
    #FINISH TESTING
    # SAVE THIS AS AN EXAMPLE AND AN ACTUAL FUNC


    file_path = "Classifications_from_Glossary_Terms.xlsx"
    classification_info_sheet_name = "TERM_INFO"
    classifications_dict = process_classifications_sheet(file_path, classification_info_sheet_name)
    for c in classifications_dict:
        classification_name = c["classification_name"]
        glossary_term_name = c["glossary_term"]
        print(classification_name)
        result = associate_classification_and_glossary_term(classification_name, glossary_term_name)
        print(result)

    """ 


    """
    names = get_all_typedefs()
    for n in names:
        if "sap_s4hana" in n:
            print(n)

    """
    """


    column = "column"
    tabular_schema = "tabular_schema"
    dl = "azure_datalake_gen2_resource_set"
    db = "sap_s4hana_instance_packages", "azure_sql_db_schemas"
    dw = "azure_sql_server_data_warehouses", "azure_sql_dw_schemas", "azure_sql_dw_schema_tables"
    power_bi = "powerbi_dataset"


    gen2_storage_account = "https://hbipdextdynamicactionsa.core.windows.net"
    gen2_service = "https://hbipdextdynamicactionsa.dfs.core.windows.net"
    sql_dw = "mssql://hbi-qa01-analytics-dwsrv.database.windows.net/hbiqa01dw"
    sql_server = "mssql://hbi-qa01-analytics-dwsrv.database.windows.net"
    s4_hana_instance = "sap_s4hana://vhhbrmd1ci_MD1_00_220/"
    matdoc_extract = "sap_s4hana://vhhbrmd1ci_MD1_00_220/MATDOC_EXTRACT"

    entity = get_entity_typename_from_qualified_name(matdoc_extract)
    print(entity)

    gen2_storage_account_typename = "azure_storage_account"
    gen2_service_typename = "azure_datalake_gen2_service"
    sql_server_typename = "azure_sql_server"

    """


    #generate_plm()
    #generate_mdg()
    #generate_s4()

    

    '''
    ec = ExcelConfiguration()
    reader = ExcelReader(ec)

    entities = reader.parse_bulk_entities("sample1_crafted_demo.xlsx")

    results = CLIENT.upload_entities(entities)

    print(json.dumps(results, indent=2))
    '''


    name = "Demand_Planning_Forecast"
    system_name = "DataLake"
    typename = "azure_datalake_gen2_resource_set"
    generate_entity(name, typename, system_name)


if __name__ == '__main__':
    main()
