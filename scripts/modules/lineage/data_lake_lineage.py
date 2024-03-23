##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client
from modules import *
from modules.lineage.shared_lineage_functions import *
from pyapacheatlas.core.util import GuidTracker


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

def build_lineage_from_data_lake_curated_to_data_warehouse_stage(client, dl_curated_guid, dw_stage_guid):
    '''
    Build lineage from a data lake curated asset to a data warehouse stage asset.
    '''
    dl_type = "azure_datalake_gen2_path"
    dw_type = "azure_sql_dw_table"
    process_type_name = "DL_Curated_to_DW_Stage"
    build_lineage_using_guids(client, dl_curated_guid, dl_type, dw_stage_guid, dw_type, process_type_name)


def build_lineage_from_data_lake_stage_to_curated(client, stage_guid, curated_guid):
    '''
    Build lineage from a data lake stage asset to a data lake curated asset.
    '''
    stage_type = "azure_datalake_gen2_path"
    curated_type = "azure_datalake_gen2_path"
    process_type_name = "DL_Stage_to_DL_Curated"
    build_lineage_using_guids(client, stage_guid, stage_type, curated_guid, curated_type, process_type_name)


# Main Processing
# ---------------

def main():
    print()


if __name__ == '__main__':
    main()