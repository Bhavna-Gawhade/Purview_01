##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client
from modules import *
from modules.lineage.shared_lineage_functions import *


# Imports
# ---------------

from pathlib import Path


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

def build_lineage_from_oracle_server_to_pbi(client, oracle_asset_qualified_name, pbi_dataset_qualified_name):
    '''
    Builds lineage from an Oracle Server's asset to a Power BI dataset.

    Parameters:
        client (object): The client object for accessing the metadata service.
        oracle_asset_qualified_name (str): The qualified name of the Oracle Server asset.
        pbi_dataset_qualified_name (str): The qualified name of the Power BI dataset.

    Returns:
        None
    '''

    source_entity = get_entity_from_qualified_name(client, oracle_asset_qualified_name)
    target_entity = get_entity_from_qualified_name(client, pbi_dataset_qualified_name)
    process_type_name = "Oracle_Server_to_PBI"
    result = add_manual_lineage(client, [source_entity], [target_entity], process_type_name)
    print("Lineage built between " + source_entity["name"] + " and " + target_entity["name"])



# Main Processing
# ---------------

def main():
    print()


if __name__ == '__main__':
    main()