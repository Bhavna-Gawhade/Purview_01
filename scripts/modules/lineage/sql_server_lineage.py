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


# Functions
# ---------------

def build_lineage_from_sql_server_to_pbi(client, sql_asset_qualified_name, pbi_dataset_qualified_name):
    '''
    Build lineage from a SQL Server's asset to a Power BI dataset.
    '''

    source_entity = get_entity_from_qualified_name(client, sql_asset_qualified_name)
    target_entity = get_entity_from_qualified_name(client, pbi_dataset_qualified_name)
    process_type_name = "SQL_Server_to_PBI"
    result = add_manual_lineage(client, [source_entity], [target_entity], process_type_name)
    print("Lineage built between " + source_entity["name"] + " and " + target_entity["name"])


def build_lineage_from_sql_vw_to_data_lake_stage(client, sql_vw_guid, dl_stage_guid):
    '''
    Build lineage from a SQL view to a data lake stage asset.
    '''
    sql_vw_type = "mssql_view"
    dl_type = "azure_datalake_gen2_path"
    process_type_name = "SQL_VW_to_DL_Stage"
    build_lineage_using_guids(client, sql_vw_guid, sql_vw_type, dl_stage_guid, dl_type, process_type_name)


def build_lineage_from_sql_table_to_data_lake_stage(client, sql_table_guid, dl_stage_guid):
    '''
    Build lineage from a SQL table to a data lake stage asset.
    '''
    sql_table_type = "mssql_table"
    dl_type = "azure_datalake_gen2_path"
    process_type_name = "SQL_Table_to_DL_Stage"
    build_lineage_using_guids(client, sql_table_guid, sql_table_type, dl_stage_guid, dl_type, process_type_name)


# Main Processing
# ---------------

def main():
    print()


if __name__ == '__main__':
    main()