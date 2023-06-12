##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client


# Package Imports
# ---------------
from pyapacheatlas.core.typedef import EntityTypeDef
from pathlib import Path


# Constants
# ---------------
# Define constants at the top of the module, 
# in all capital letters with underscores separating words.

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)

SYNAPSE_STORED_PROCEDURE_DEF = EntityTypeDef(
  name = "synapse_stored_procedure",
  superTypes = ["Process"]
)

SYNAPSE_EXTERNAL_TABLE_DEF = EntityTypeDef(
  name = "synapse_external_table",
  superTypes = ["Process"]
)

INGESTION_FRAMEWORK_DEF = EntityTypeDef(
  name = "ingestion_framework",
  superTypes = ["Process"]
)


# Functions
# ---------------

def get_entity_from_qualified_name(qualified_name):
    """
    Retrieves an entity from the catalog based on the provided qualified name.

    Args:
        qualified_name (str): The qualified name of the entity.

    Returns:
        dict: The entity found based on the qualified name.
"""
    entities_found = CLIENT.discovery.search_entities(query=qualified_name)

    # Extract entities from the generator
    entities = []
    for entity in entities_found:
        # Since the input qualified_name is all lowercase, we cannot do a direct str comparison, we must check length
        # This is to avoid qualified names that have the same beginning and different extensions
        # Allow length to differ by 1 for potential '/' at the end
        if (len(entity["qualifiedName"]) == len(qualified_name)) or (len(entity["qualifiedName"]) == len(qualified_name) + 1):
            entities.append(entity)

    if len(entities) > 1:
        raise ValueError(f"More than one entity was returned. There should only be one entity returned from a qualified name. The qualified name used was: {qualified_name}")
    elif len(entities) == 0:
        raise ValueError(f"No entity was found with this qualified name: {qualified_name}")

    # Extract the entity found by the search catalog
    entity = entities[0]

    return entity


def upload_custom_type_def(type_def: EntityTypeDef):
    """
    Uploads a custom entity type definition to the catalog.

    Args:
        type_def (EntityTypeDef): The custom entity type definition to upload.

    Returns:
        dict: The result of the upload operation.
    """
    result = CLIENT.upload_typedefs(
        entityDefs=[type_def],
        force_update=True
    )
    return result


# Main Processing
# ---------------

def main():
    print()


if __name__ == '__main__':
    main()