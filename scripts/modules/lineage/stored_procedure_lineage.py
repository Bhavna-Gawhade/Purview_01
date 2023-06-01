##! /usr/bin/env python3


# Function Imports
# ---------------
from purview.utils import get_credentials, create_purview_client
from modules import *
from shared_lineage_functions import *


# Imports
# ---------------

from pyapacheatlas.core import PurviewClient
from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import AtlasEntity
from pyapacheatlas.core import AtlasEntity
from pyapacheatlas.core.entity import AtlasEntity, AtlasProcess
from getpass import getpass
from pathlib import Path
from sqllineage.runner import LineageRunner


# Constants
# ---------------
# Define constants at the top of the module, 
# in all capital letters with underscores separating words.

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)


# Functions
# ---------------

def confirm_source_not_target(source_tables: list, target_tables: list):
    """
    Confirm that the tables in the source_tables list are not present in the target_tables list.

    Args:
        source_tables (list): List of source table names.
        target_tables (list): List of target table names.

    Returns:
        list: Filtered list of source tables that are not present in the target tables.
    """
    try:
        filtered_tables = []
        for table in source_tables:
            if table not in target_tables:
                filtered_tables.append(table)
        return filtered_tables
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None


def extract_source_and_target_from_stored_procedure(sql_file_path: str):
    """
    Extract the source and target tables from a stored procedure SQL file.

    Args:
        sql_file_path (str): The file path to the SQL file.

    Returns:
        tuple: A tuple containing the source tables and target tables.
    """
    try:
        with open(sql_file_path, 'r') as file:
            sql_string = file.read()
        
        sql_string = remove_begin_statement(sql_string)
        lineage = LineageRunner(sql_string)
        source_tables = lineage.source_tables
        target_tables = lineage.target_tables

        # Confirm that no source tables are the same entity as the target table
        source_tables = confirm_source_not_target(source_tables, target_tables)
        return source_tables, target_tables
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None, None


def dylan_column_mapping():
    '''
    Need to test
    '''

    # Get your service principal client id, tenant id, and client secret
    # Be sure to store these securely and avoid committing them to version control
    client_id = getpass("Enter your client id: ")
    client_secret = getpass("Enter your client secret: ")
    tenant_id = getpass("Enter your tenant id: ")
    catalog_name = getpass("Enter your catalog name: ")

    # Create the OAuth object to be used in the client.
    oauth = ServicePrincipalAuthentication(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    # Make the client.
    client = PurviewClient(
        account_name=catalog_name,
        authentication=oauth
    )
    
    # Your SQL query
    sql_query = "SELECT column1, column2 FROM table1 JOIN table2 ON table1.id = table2.id;"

    # Parse the SQL query
    tables_columns = None
    # tables_columns = parse_sql(sql_query)

    # Create the entities and column mapping
    entities = []
    column_mapping = []
    for table, columns in tables_columns.items():
        entity = AtlasEntity(
            name=table,
            typeName="hive_table",
            qualifiedName=f"pyapacheatlas://{table}",
            guid=CLIENT.get_guid()
        )
        entities.append(entity)
        
        for column in columns:
            column_mapping.append(
                {"ColumnMapping": [{"Source": "*", "Sink": column}],
                "DatasetMapping": {"Source": "*", "Sink": entity.qualifiedName}
                }
            )

    # Create the process entity with the column mapping
    process_entity = AtlasProcess(
        name="my_process",
        typeName="Process",
        qualified_name="my_process",
        guid=client.get_guid(),
        attributes={"columnMapping": column_mapping},
        inputs=[{"guid": entity.guid, "typeName": "hive_table"} for entity in entities],
        outputs=[]
    )

    # Upload the entities and the process entity to Atlas
    client.upload_entities([*entities, process_entity])


def extract_column_lineage(sql_file_path: str):
    """
    Need to test
    """
    # Read the SQL file and store its contents as a string
    with open(sql_file_path, 'r') as file:
        sql_string = file.read()

    # Create an instance of LineageRunner
    lineage = LineageRunner(sql_string)
    column_lineage = lineage.get_column_lineage()

    # Get the column lineage
    column_lineage = lineage.get_column_lineage()

    return column_lineage


# Main Processing
# ---------------
# Put the code to be executed inside a main() function, 
# and call it at the bottom of the module with an if __name__ == "__main__" block. 

def main():
    print()


if __name__ == '__main__':
    main()

