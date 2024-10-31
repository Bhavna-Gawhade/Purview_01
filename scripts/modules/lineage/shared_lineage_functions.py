##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client
from modules.entity import *


# Imports
# ---------------
import time
from pyapacheatlas.core import AtlasEntity
from pyapacheatlas.core import AtlasEntity
from pyapacheatlas.core.entity import AtlasEntity, AtlasProcess
from pathlib import Path


# Constants
# ---------------
 

# Functions
# ---------------

def remove_begin_statement(sql_string: str):
    """
    Remove the "BEGIN" statement from the SQL string.

    Args:
        sql_string (str): The SQL string.

    Returns:
        str: The SQL string with the "BEGIN" statement removed.
    """
    try:
        return sql_string.replace("BEGIN", " ")
    except AttributeError:
        raise ValueError("Invalid input. Expected a string.")  


def add_manual_lineage(client, source_entities: list, target_entities: list, process_type_name: str):
    """
    Add manual lineage by creating AtlasEntities for source and target entities,
    and an AtlasProcess connecting them.

    Args:
        source_entities (list): List of source entities.
        target_entities (list): List of target entities.
        process_type_name (str): Name of the process type.

    Returns:
        dict: Result of the entity upload operation.
    """
    try:
        sources = []
        targets = []

        for entity in source_entities:
            s = AtlasEntity(
                name = entity["name"],
                typeName = entity["entityType"],
                qualified_name = entity["qualifiedName"],
                guid = entity["id"]
            )
            sources.append(s)
            source_naming_str = s.name.replace(" ", "_") + "/" 

        for entity in target_entities:
            t = AtlasEntity(
                name = entity["name"],
                typeName = entity["entityType"],
                qualified_name = entity["qualifiedName"],
                guid = entity["id"]
            )
            targets.append(t)
            target_naming_str = t.name.replace(" ", "_") + "/"

        process = AtlasProcess(
            name = process_type_name,
            typeName = process_type_name,
            qualified_name = "sources:" + source_naming_str + "targets:" + target_naming_str + "process_type:" + process_type_name,
            inputs = sources,
            outputs = targets
        )

        result  = client.upload_entities(
            batch = targets + sources + [process]
        )
        
        return result

    except (KeyError, TypeError) as e:
        raise ValueError("Invalid input. Expected a list of source_entities and target_entities, and a string process_type_name.") from e


def get_lowercase_qualified_name(qualified_name_header: str, name: str):
    """
    Generate the lowercase qualified name by combining the qualified_name_header and name,
    and removing any square bracket characters.

    Args:
        qualified_name_header (str): The qualified name header.
        name (str): The name.

    Returns:
        str: The lowercase qualified name.
    """
    try:
        lowercase_qualified_name = qualified_name_header + str(name)
        lowercase_qualified_name = lowercase_qualified_name.replace("]", "")
        lowercase_qualified_name = lowercase_qualified_name.replace("[", "")
        return lowercase_qualified_name
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return ""


def get_and_add_lineage(table_names: tuple, qualified_name_headers: tuple, entity_type_name: str):
    """
    Get and add lineage between the given table names, using the qualified name headers and entity type name.

    Args:
        table_names (tuple): A tuple containing the source and target table names.
        qualified_name_headers (tuple): A tuple containing the qualified name headers for source and target.
        entity_type_name (str): The entity type name.

    Returns:
        Any: The result of adding lineage.
    """
    try:
        source_names_lowercase = table_names[0]
        target_names_lowercase = table_names[1]
        source_header = qualified_name_headers[0]
        target_header = qualified_name_headers[1]
        source_entities = []
        target_entities = []

        for name in source_names_lowercase:
            source_qualified_name_lowercase = get_lowercase_qualified_name(source_header, name)
            source_entity = get_entity_from_qualified_name(source_qualified_name_lowercase)
            source_entities.append(source_entity)
        
        for name in target_names_lowercase:
            target_qualified_name_lowercase = get_lowercase_qualified_name(target_header, name)
            target_entity = get_entity_from_qualified_name(target_qualified_name_lowercase)
            target_entities.append(target_entity)

        result = add_manual_lineage(source_entities, target_entities, entity_type_name)
        return result

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None


def add_manual_lineage_with_specific_client(client, source_entities: list, target_entities: list, process_type_name: str, source_type_name, target_type_name, target_name_without_special_char):
    '''
    Add manual lineage with a specific Purview Atlas client by creating AtlasEntities for source and target entities,
    and an AtlasProcess connecting them.

    Args:
        client: The specific Purview Atlas client for entity upload.
        source_entities (list): List of source entities.
        target_entities (list): List of target entities.
        process_type_name (str): Name of the process type.
        source_type_name (str): The type name of the source entities.
        target_type_name (str): The type name of the target entities.
        target_name_without_special_char (str): The name of the target entity without special characters.

    Returns:
        dict: Result of the entity upload operation.
    '''
    try:
        sources = []
        targets = []
        source_naming_str = ""
        target_naming_str = ""

        for entity in source_entities:
            s = AtlasEntity(
                name = entity["name"],
                typeName = entity["entityType"],
                qualified_name = entity["qualifiedName"],
                guid = entity["id"]
            )
            sources.append(s)
            source_naming_str = source_naming_str + "/" + s.name

        for entity in target_entities:
            t = AtlasEntity(
                name = entity["name"],
                typeName = entity["entityType"],
                qualified_name = entity["qualifiedName"],
                guid = entity["id"]
            )
            targets.append(t)
            target_naming_str = target_naming_str + "/" + t.name

        process = AtlasProcess(
            name = process_type_name,
            typeName = process_type_name,
            qualified_name = process_type_name + "://" + source_type_name + "_to_" + target_type_name + "/" + target_name_without_special_char,
            inputs = sources,
            outputs = targets
        )

        result  = client.upload_entities(
            batch = targets + sources + [process]
        )
        
        return result

    except (KeyError, TypeError) as e:
        raise ValueError("Invalid input. Expected a list of source_entities and target_entities, and a string process_type_name.") from e


def build_lineage_using_guids(client, source_guid, source_type, target_guid, target_type, process_type):
    '''
    Builds lineage between two assets using their GUIDs.

    Parameters:
        client (object): The client object for accessing the metadata service.
        source_guid (str): The GUID of the source asset.
        source_type (str): The type of the source asset.
        target_guid (str): The GUID of the target asset.
        target_type (str): The type of the target asset.
        process_type (str): The type of the process.

    Returns:
        None
    '''

    source_entity = client.get_entity(source_guid).get("entities")[0].get("attributes")
    target_entity = client.get_entity(target_guid).get("entities")[0].get("attributes")
    process_type_name = process_type

    s = AtlasEntity(
        name = source_entity.get("name"),
        typeName = source_type, 
        qualified_name = source_entity.get("qualifiedName"),
        guid = source_guid
    )
    source_naming_str = s.name.replace(" ", "_") + "/" 

    t = AtlasEntity(
        name = target_entity.get("name"),
        typeName = target_type,
        qualified_name = target_entity.get("qualifiedName"),
        guid = target_guid
    )
    target_naming_str = t.name.replace(" ", "_") + "/"

    process = AtlasProcess(
        name = process_type_name,
        typeName = process_type_name,
        qualified_name = "sources:" + source_naming_str + "targets:" + target_naming_str + "process_type:" + process_type_name,
        inputs = [s],
        outputs = [t]
    )

    result  = client.upload_entities(
        batch = [t] + [s] + [process]
    )

    print("Lineage built between " + source_entity["name"] + " and " + target_entity["name"])




#----------------------------------------------------------------------------------------
# List of custom process types to iterate through
PROCESS_TYPES = [
    # "ingestion_framework",
    # "dw_routine",
    # "dw_view_creation",
    # "dsp_connection",
    # "sharepoint_to_pbi",
    # "Databricks_to_PBI",
    # "SQL_Server_to_PBI",
    # "Oracle_Server_to_PBI",
    # "Cube_to_PBI",
    # "DL_Curated_to_DW_Stage",
    # "Oracle_to_DL_Stage",
    # "DL_Manual_File_to_DL_Stage",
    # "SQL_VW_to_DL_Stage",
    # "SQL_Table_to_DL_Stage",
    # "DL_Curated_to_DL_Curated",
    # "sql_database_extract",
    # "DW_to_PBI_Dataset",
    # "Tabular_Model_to_PBI_Dataset",
    # "Informatica_Connection",
    # "Column_Mapping",
    "DL_Stage_to_DL_Curated"
]

def update_lineage_connector_descriptions(client):
    """
    Updates the `userDescription` field of lineage connector entities in Microsoft Purview. 
    For each lineage connector entity of specified process types, this function sets the 
    `userDescription` to reflect details about the source and target of the entity.

    Parameters:
        client (PurviewClient): Authenticated Purview client instance for entity operations.

    Returns:
        None: Outputs the updated entity descriptions to console.
    """

    for process_type in PROCESS_TYPES:
        try:
            search_results = client.discovery.search_entities(query=process_type, limit=100)
        except Exception as e:
            print(f"Failed to search entities for process type '{process_type}': {e}")
            continue

        for entity in search_results:
            entity_guid = entity.get("guid") or entity.get("id")

            if not entity_guid:
                print("Skipping entity without 'guid' or 'id'")
                continue

            # Fetch the full entity details, including relationships
            try:
                entity_details = client.get_entity(entity_guid)
            except Exception as e:
                print(f"Failed to fetch entity details for GUID {entity_guid}: {e}")
                continue

            entity_info = entity_details.get("entities", [{}])[0]

            # Extract source and target details for description
            source_entity = next((rel for rel in entity_info["relationshipAttributes"].get("inputs", [])), None)
            target_entity = next((rel for rel in entity_info["relationshipAttributes"].get("outputs", [])), None)

            # Construct the description based on available source and target information
            description = "Source Type: {src_type}\n" \
                        "Source Name: {src_name}\n" \
                        "Target Type: {tgt_type}\n" \
                        "Target Name: {tgt_name}".format(
                src_type=source_entity["typeName"] if source_entity else "Unknown",
                src_name=source_entity["displayText"] if source_entity else "Unknown",
                tgt_type=target_entity["typeName"] if target_entity else "Unknown",
                tgt_name=target_entity["displayText"] if target_entity else "Unknown"
            )


            # Assign the new description to the entity attributes
            entity_info["attributes"]["userDescription"] = description

            # Update entity in Purview
            try:
                client.upload_entities([entity_info])
                print(f"Updated entity {entity_guid} with description: {description}\n")
            except Exception as e:
                print(f"Failed to update entity {entity_guid}: {e}")
