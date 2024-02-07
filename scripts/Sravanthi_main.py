##! /usr/bin/env python3


# Import Functions
# ---------------

from modules import entity
from modules.classification.test_case_generator import *
from modules.classification.regex_generator import *
from modules.classification.shared_generator_functions import *
from modules.classification.classification import *
from modules.lineage.json_payload_lineage import *
from modules.lineage.shared_lineage_functions import *
from modules.lineage.powerbi_sql_query_lineage import *
from modules.lineage.powerbi_tabular_model_lineage import *
from modules.lineage.data_warehouse_internal_lineage import *
from modules.lineage.sap_hana_internal_lineage import *
from modules.lineage.sharepoint_lineage import *
from modules.lineage.pkms_lineage import *
from modules.glossary_propagation.shared_glossary_functions import *
from modules.glossary_propagation.sap_hana_glossary_propagation import *
from modules.glossary_propagation.sap_s4hana_glossary_propagation import *
from modules.glossary_propagation.datalake_glossary_propagation import *
from modules.glossary_propagation.sql_dw_glossary_propagation import *
from modules.entity import *
from modules.collection.collection_shared_functions import *
from modules.collection.sap_s4hana_collection_sorting import *
from modules.collection.azure_dw_collection_sorting import *
from utils import get_credentials, create_purview_client
from pyapacheatlas.core.util import GuidTracker

from pyapacheatlas.readers import ExcelConfiguration, ExcelReader


# Import Packages
# ---------------

from pathlib import Path
from pyapacheatlas.core.typedef import AtlasAttributeDef, AtlasStructDef, TypeCategory, AtlasRelationshipAttributeDef
from pyapacheatlas.core import AtlasEntity, AtlasProcess
from azure.core.exceptions import HttpResponseError
import json
from datetime import datetime
import re
import time
import sys
from pyapacheatlas.readers import ExcelConfiguration, ExcelReader


# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
qa_client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)

REFERENCE_NAME_PURVIEW = "hbi-pd01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
prod_client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)
    
# Main Function
# ---------------

def main():
    print()


    """sharepoint_entity_name = "Control Table ASIN Distribution."
    actual_sharepoint_link = "https://hanes.sharepoint.com/:x:/r/sites/GrowthTeamSupport/_layouts/15/Doc.aspx?sourcedoc=%7B124ACCA7-B22B-4B87-A2F8-ADCCC2CF5563%7D&file=Control%20Table%20ASIN%20Distribution..xlsx&wdLOR=c2860C007-B39E-422A-8453-942CA6124878&action=default&mobileredirect=true"
    pbi_dataset_qualified_name = "https://app.powerbi.com/groups/8864c31d-1a84-42cb-8ae3-a769271b334f/datasets/d2e8f683-32cb-4647-a7d6-c85f701239a7"
    pbi_short_name = "5114AmazonKPIReporting"
    create_sharepoint_entity_and_build_lineage_to_pbi(prod_client, sharepoint_entity_name, actual_sharepoint_link, pbi_dataset_qualified_name, pbi_short_name)
    """

    #pull_entities_from_purview("prod", "hbi-pd01-datamgmt-pview", prod_client)
    #pull_entities_from_purview("qa", "hbi-qa01-datamgmt-pview", qa_client)
    #pull_lineage_connections_from_purview("prod", "hbi-pd01-datamgmt-pview", prod_client)
    #pull_sap_s4hana_columns_of_table("prod", "MARA")
    #pull_sap_s4hana_table_columns_without_glossary_terms("prod", "MARA")

    '''
    # example: sql queries to pbi report - connects dw to pbi
    source_entities_qualified_paths = ["mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/Common/DimWinningPortfolioSkuList",
                                       "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/mount/Business_Seg_Hierarchy_Samba_DIV_BIPAOSQL",
                                       "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/stage/Facility_SAP_HBI_DW_DLY_FACILITY_SAP",
                                       "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/Common/FactFGInventoryAvailability",
                                       "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/Common/DimFacility",
                                       "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/Common/DimShipperFlag"
                                       ]
    target_entity_qualified_path = "https://app.powerbi.com/groups/87418287-152f-44c8-931d-7fd6228dda48/datasets/5bf85a38-bac9-4101-afc2-0a9ab0717a1a"
    target_name_without_special_char = "4406InventoryAvailabilityDataset"
    build_powerbi_lineage_from_sql_query(prod_client, source_entities_qualified_paths, target_entity_qualified_path, target_name_without_special_char)
    '''

    # example: internal data warehouse lineage for table
    # !
    # RUN THIS AGAIN - STILL NEED TO DEBUG FOR 51.12 LINEAGE
    # !
    # !
    table_file_name = "dbo.usp_Facility_SAP_HBI_DW_DLY_FACILITY_SAP.sql"
    prod_parse_data_warehouse_table_internal_lineage(prod_client, table_file_name)
    
    # example: internal data warehouse lineage for table
    view_file_name = "dbo.vw_DimCustomerAccount_scv.sql"
    #prod_parse_data_warehouse_view_internal_lineage(prod_client, view_file_name)

    #glossary_propagation_of_sap_hana(prod_client, "prod", "11_15_23_Purview_Glossary_Import_716_Terms.xlsx")
    #glossary_propagation_of_sap_s4hana(prod_client, "prod", "11_15_23_Purview_Glossary_Import_716_Terms.xlsx")
    #pull_entities_from_purview("prod", "hbi-pd01-datamgmt-pview", prod_client)

    file_name = "ProcessPayloads/Curated/Business/DimBusiness.json"
    #datalake_to_data_warehouse_lineage_from_payload(prod_client, )
    
    #manually_connect_dl_to_dw_via_qualified_names(prod_client, source_qual, target_qual)


if __name__ == '__main__':
    main()
