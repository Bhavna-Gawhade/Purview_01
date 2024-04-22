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


# Functions
# ---------------

def load_json(json_file_path):
    '''
    Loads JSON data from a file.

    Parameters:
    - json_file_path (str): The file path to the JSON file.

    Returns:
    dict: A dictionary containing the loaded JSON data.   
    '''
    try:
        with open(json_file_path, "r") as json_file:
            model_data = json.load(json_file)

        return model_data

    except FileNotFoundError:
        print(f"The file '{json_file_path}' does not exist.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def extract_source_schema_and_table_name(partitions_dict):
    '''
    Extracts source schema and table name information from a partitions dictionary.

    Parameters:
    - partitions_dict (list): List of partition dictionaries.

    Returns:
    tuple: A tuple containing the extracted source schema and table name.
    '''
    partition = partitions_dict[0]
    source_schema = ""
    table_name = ""

    if "source" in partition:        
        if "expression" in partition.get("source"):
            source_info = partition.get("source").get("expression")
            for string in source_info:
                pattern = r'Schema="([^"]+)"'
                match = re.search(pattern, string)
                if match:
                    source_schema = match.group(1)  # Extract the value inside double quotes
                
                pattern = r'Item="([^"]+)"'
                match = re.search(pattern, string)
                if match:
                    table_name = match.group(1)  # Extract the value inside double quotes
                
    return (source_schema, table_name)


def get_all_tables_from_tabular_model(client, tables, start_of_source_qualified_name, existing_pbi_tables_file_path, target_pbi_dataset_qualified_name):
    '''
    Retrieves details of all tables from a tabular model, including their source schema and table name.

    Parameters:
    - client: The Atlas client for making API calls.
    - tables (list): List of tables from the tabular model.
    - start_of_source_qualified_name (str): The common prefix for constructing the qualified name of the source entities.

    Returns:
    list: A list of dictionaries, each containing details of a table, including powerbi_table_name, source_schema, source_table_name, and source entity details.
    '''
    all_tables = []
    for t in tables:
        source_info = extract_source_schema_and_table_name(t.get("partitions"))
        source_schema = source_info[0]
        source_table_name = source_info[1]

        if source_schema != "" and source_table_name != "":
            source_qualified_name = start_of_source_qualified_name + source_schema + "/" + source_table_name
            source_entity_details = get_entity_from_qualified_name(client, source_qualified_name)
            if source_entity_details != None:
                table_details = {
                    "powerbi_table_name": t.get("name"),
                    "source_schema": source_schema,
                    "source_table_name": source_table_name,

                    # The below items all have to do with the source's details. Need to use these specific keys to work with the lineage func.
                    "name": source_table_name, 
                    "entityType": source_entity_details["entityType"],
                    "qualifiedName": source_qualified_name,
                    "id": source_entity_details["id"]
                }
                all_tables.append(table_details)
            else:
                print("Error: Need to create PBI table for " + source_schema + "/" + source_table_name)
 
    return all_tables


def build_lineage_from_pbi_table_to_dataset(client, source_dict, target_dict, target_name):
    '''
    Builds a lineage relationship from a Power BI table to a Power BI dataset.

    Parameters:
    - client: The Atlas client for making API calls.
    - source_dict (dict): Dictionary containing details of the Power BI table.
    - target_dict (dict): Dictionary containing details of the Power BI dataset.
    - target_name (str): The name of the Power BI dataset.
    '''
    process_type_name = "PBI_Table_to_PBI_Dataset_Connection"
    source_type_name = "PowerBITable"
    target_type_name = "PowerBIDataset"
    name_to_use_in_qualified_name = source_dict["name"] + "_to_" + target_name.replace(" ", "")

    result = add_manual_lineage_with_specific_client(client, [source_dict], [target_dict], process_type_name, source_type_name, target_type_name, name_to_use_in_qualified_name)
    print(result)
    print()


def create_powerbi_table(client, table, target_dataset_qualified_name):
    entity_type = "Power_BI_Table"
    powerbi_table_name_without_spaces = table["powerbi_table_name"].replace(" ", "")
    unique_qualified_name = target_dataset_qualified_name + "/" + powerbi_table_name_without_spaces + "Table/"
    e = AtlasEntity(
        name = table["powerbi_table_name"],
        typeName = entity_type,
        qualified_name = unique_qualified_name,
        guid = GuidTracker().get_guid()
    )
    
    result  = client.upload_entities(
        batch = [e]
    )
    print(result)


def bulk_create_powerbi_tables(client, tables, target_dataset_name_without_special_char, target_dataset_qualified_name, existing_pbi_tables_file_path):
    '''
    Creates Power BI table entities in Apache Atlas and returns a list of created entities.

    Parameters:
    - client: The Atlas client for making API calls.
    - tables (list): List of dictionaries containing details of Power BI tables.
    - target_dataset_name_without_special_char (str): The name of the target Power BI dataset without special characters.
    - target_dataset_qualified_name (str): The qualified name of the target Power BI dataset.

    Returns:
    - power_bi_tables (list): List of AtlasEntity objects representing the created Power BI table entities.
    '''
    entity_type = "Power_BI_Table" # custom type can be found under entity.py

    power_bi_tables = []
    for t in tables:
        powerbi_table_name_without_spaces = t["powerbi_table_name"].replace(" ", "")
        pbi_table_created = is_pbi_table_already_created(existing_pbi_tables_file_path, powerbi_table_name_without_spaces)
        if not pbi_table_created: 
            unique_qualified_name = target_dataset_qualified_name + "/" + powerbi_table_name_without_spaces + "Table/"
            e = AtlasEntity(
                name = t["powerbi_table_name"],
                typeName = entity_type,
                qualified_name = unique_qualified_name,
                guid = GuidTracker().get_guid()
            )
            power_bi_tables.append(e)
            
            result  = client.upload_entities(
                batch = [e]
            )
            print(result)
            append_to_existing_pbi_tables_json(existing_pbi_tables_file_path, powerbi_table_name_without_spaces)

        
    return power_bi_tables


def get_custom_power_bi_tables(client):
    '''
    Retrieves Power BI table entities of a custom type from Apache Atlas.

    Parameters:
    - client: The Atlas client for making API calls.

    Returns:
    - entities (list): List of dictionaries representing Power BI table entities.
    '''
    entity_type = "Power_BI_Table"
    entities = client.discovery.browse(entityType=entity_type).get("value")
    return entities


def build_lineage_from_sql_to_pbi_table(client, source_dict, target_dict, target_name):
    '''
    Builds lineage from an SQL database table to a Power BI table in Apache Atlas.

    Parameters:
    - client: The Apache Atlas client for making API calls.
    - source_dict (dict): Dictionary representing the source SQL table entity.
    - target_dict (dict): Dictionary representing the target Power BI table entity.
    - target_name (str): The name of the target Power BI table.

    Returns:
    - result (dict): Result of the lineage creation operation.
    '''
    process_type_name = "SQL_to_PBI_Table_Connection"
    source_type_name = "AzureSQLDB"
    target_type_name = "PowerBITable"

    target_name_without_special_char = target_name.replace(" ", "")

    result = add_manual_lineage_with_specific_client(client, [source_dict], [target_dict], process_type_name, source_type_name, target_type_name, target_name_without_special_char)
    print(result)
    print()


def append_to_existing_pbi_tables_json(file_path, string_to_append):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Append the pbi table name to the list of existing pbi tables in Purview
    data["existing_pbi_tables_in_purview"].append(string_to_append)
    
    # Write the updated JSON back to the file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def is_pbi_table_in_json_list(file_path, pbi_table_name):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    if pbi_table_name in data["existing_pbi_tables_in_purview"]:
        return True
    else:
        return False
    

def is_pbi_table_already_created(existing_pbi_tables_file_path, pbi_table_name):
    in_json_list = is_pbi_table_in_json_list(existing_pbi_tables_file_path, pbi_table_name)
    if in_json_list:
        return True # pbi table already created
    else:
        return False # pbi table not created


def prod_build_powerbi_lineage_from_tabular_model(client, model_bim_file_path, target_dataset_name_without_special_char, target_pbi_dataset_qualified_name):
    '''
    Build lineage relationships in Apache Atlas from SQL database tables to Power BI tables and from Power BI tables to Power BI datasets.

    Note:
    - Ensure that the Power BI tables and datasets are created in Atlas before running this script.
    - The function relies on custom entity types "AzureSQLDB" for SQL database tables and "PowerBITable" for Power BI tables.

    Returns:
    - None 
    '''
    # NOTE:
    # Need to factor schemas into the qualified names.

    # EXAMPLE: model_bim_file_path = "Model.bim"
    tabular_model = load_json(model_bim_file_path)
    existing_pbi_tables_file_path = "modules/lineage/existing_pbi_tables_from_model.json"

    # Only uncomment if need to bulk create new Power BI tables
    bulk_create_powerbi_tables(client, all_tables_extracted, target_dataset_name_without_special_char, target_dataset_qualified_name, existing_pbi_tables_file_path)
    

    # EXAMPLE: target_dataset_name_without_special_char ="4440InvenModelTabularModel"
    start_of_source_qualified_name = "mssql://hbi-pd01-analytics-dwsrv.database.windows.net/hbipd01dw/"
    pre_extraction_tables_list = tabular_model.get("model").get("tables")
    all_tables_extracted = get_all_tables_from_tabular_model(client, pre_extraction_tables_list, start_of_source_qualified_name, existing_pbi_tables_file_path)
    
    for tbl in all_tables_extracted:
        pbi_table_name = tbl.get("powerbi_table_name")
        pbi_table_created = is_pbi_table_already_created(existing_pbi_tables_file_path, pbi_table_name)
        if not pbi_table_created:
            create_powerbi_table(client, tbl, target_pbi_dataset_qualified_name)
            append_to_existing_pbi_tables_json(existing_pbi_tables_file_path, pbi_table_name)


    # This builds SQL to PBI Table
    source_entities = all_tables_extracted # info for the SQL DBs
    target_entities = get_custom_power_bi_tables(client) # info for the PBI tables
    for t in target_entities:
        for s in source_entities:
            if t["name"] == s["powerbi_table_name"]:
                build_lineage_from_sql_to_pbi_table(client, s, t, t["name"])
    
    # This builds PBI Table to PBI
    power_bi_tables = get_custom_power_bi_tables(client) # info for the PBI tables
    target_dict = get_entity_from_qualified_name(client, target_pbi_dataset_qualified_name)
    for source_dict in power_bi_tables:
        build_lineage_from_pbi_table_to_dataset(client, source_dict, target_dict, target_dataset_name_without_special_char)
                

# Main Function
# ---------------

def main():
    print()


if __name__ == '__main__':
    main()
