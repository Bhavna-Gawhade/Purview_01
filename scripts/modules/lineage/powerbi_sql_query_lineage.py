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
from modules.collection.collection_shared_functions import *
from modules.glossary_propagation.shared_glossary_functions import *
from modules.entity import *
from utils import get_credentials, create_purview_client
from pyapacheatlas.core.util import GuidTracker


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

def build_powerbi_lineage_from_sql_query(client, source_entities_qualified_paths, target_entity_qualified_path, target_name_without_special_char):
    # ie. target_name_without_special_char = "5114AmazonKPIReporting"
    """result = upload_custom_type_def_with_specific_client(client, SQL_DATABASE_EXTRACT_TYPEDEF)
    print(result)"""
    
    # for i in here, run get_entity_from_qualified_name, add to list of entities, then pass that to add_manual_lineage
    process_type_name = "sql_database_source"
    source_type_name = "AzureSQLDB"
    target_type_name = "PowerBI"

    source_entities_get = []
    for s in source_entities_qualified_paths:
        ent = get_entity_from_qualified_name_with_specific_client(client, s)
        source_entities_get.append(ent)
    
    target_entity = get_entity_from_qualified_name_with_specific_client(client, target_entity_qualified_path)
    result = add_manual_lineage_with_specific_client(client, source_entities_get, [target_entity], process_type_name, source_type_name, target_type_name, target_name_without_special_char)
    print(result)


# Main Function
# ---------------

def main():
    print()


if __name__ == '__main__':
    main()
