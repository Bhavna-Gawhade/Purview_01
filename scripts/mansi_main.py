##! /usr/bin/env python3


# Import Functions
# ---------------

from modules import entity
from modules.classification.test_case_generator import *
from modules.classification.regex_generator import *
from modules.classification.shared_generator_functions import *
from modules.classification.classification import *

from modules.lineage.cube_lineage import *
from modules.lineage.databricks_lineage import *
from modules.lineage.data_lake_lineage import *
from modules.lineage.data_warehouse_internal_lineage import *
from modules.lineage.json_payload_lineage import *
from modules.lineage.informatica_lineage import *
from modules.lineage.oracle_server_lineage import *
from modules.lineage.pkms_lineage import *
from modules.lineage.powerbi_sql_query_lineage import *
from modules.lineage.analysis_services_tabular_model_lineage import *
from modules.lineage.sap_hana_internal_lineage import *
from modules.lineage.shared_lineage_functions import *
from modules.lineage.sharepoint_lineage import *
from modules.lineage.sql_server_lineage import *

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
    


# Functions
# ---------------

def in_progress_get_entity_from_qualified_name(client, qualified_name):
    """
    Retrieves an entity from the catalog based on the provided qualified name.

    Args:
        qualified_name (str): The qualified name of the entity.

    Returns:
        dict: The entity found based on the qualified name.
    """
    entities_found = client.discovery.search_entities(query=qualified_name)
    entities = []
    for entity in entities_found:
        # Since the input qualified_name is all lowercase, we cannot do a direct str comparison, we must check length
        # This is to avoid qualified names that have the same beginning and different extensions
        # Allow length to differ by 1 for potential '/' at the end
        if (len(entity["qualifiedName"]) == len(qualified_name)) or (len(entity["qualifiedName"]) == len(qualified_name) + 1):
            entities.append(entity)
            return entities[0]

    return None


# Main Function
# ---------------

def main():
    qual_name = "https://hbipd01analyticsdls.dfs.core.windows.net/curated/Business/US/DimBusiness/"
    entity = in_progress_get_entity_from_qualified_name(qa_client, qual_name)
    print(entity)


  

if __name__ == '__main__':
    main()
