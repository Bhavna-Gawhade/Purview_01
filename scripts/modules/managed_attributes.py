##! /usr/bin/env python3


# Function Imports
# ---------------

from .admin import *


# Package Imports
# ---------------

from pathlib import Path
from pyapacheatlas import *
from pyapacheatlas.core.typedef import AtlasAttributeDef, AtlasStructDef, TypeCategory
from pyapacheatlas.core import PurviewClient, AtlasEntity
from purview.utils import get_credentials, create_purview_client
import json


# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)


# Functions
# ---------------

def create_attribute(attribute_group_name: str, attribute_names: list):
    """
    Creates an attribute group with multiple attribute definitions.

    Args:
        attribute_group_name (str): The name of the attribute group.
        attribute_names (list): The names of the attributes to create.

    Returns:
        dict: The response of the upload operation.
    """
    try:
        attr_list = []
        for n in attribute_names: 
            attr_list.append(AtlasAttributeDef(name=n, options={"maxStrLength": "50", "applicableEntityTypes": "[\"DataSet\"]"}))

        bizdef = AtlasStructDef(
            name=attribute_group_name,
            category=TypeCategory.BUSINESSMETADATA,
            attributeDefs=attr_list
        )

        response = CLIENT.upload_typedefs(businessMetadataDefs=[bizdef], force_update=True)
        return response
    except ValueError as ve:
        raise ValueError("Error occurred during the upload process.") from ve
    except Exception as e:
        raise Exception("An error occurred during the upload process.") from e



def add_attributes_to_entity(entity: AtlasEntity, attribute_group_name: str, attribute_name: str, attribute_value: str):
    """
    Adds attributes to a business metadata group associated with an entity.

    Args:
        entity (AtlasEntity): The entity to which the attributes will be added.
        attribute_group_name (str): The name of the attribute group.
        attribute_name (str): The name of the attribute to add.
        attribute_value (str): The value of the attribute to add.

    Returns:
        dict: The response of the update operation.
    """
    try:
        response_update = CLIENT.update_businessMetadata(
            guid=entity.guid,
            businessMetadata={
                attribute_group_name: {attribute_name: attribute_value}
            }
        )
        return response_update
    except ValueError as ve:
        raise ValueError("Error occurred during the update process.") from ve
    except Exception as e:
        raise Exception("An error occurred during the update process.") from e


def delete_attribute(guid: str, attribute_group_name: str, attribute_name: str):
    """
    Deletes a specific attribute from a business metadata group associated with an entity.

    Args:
        guid (str): The unique identifier of the entity.
        attribute_group_name (str): The name of the attribute group.
        attribute_name (str): The name of the attribute to delete.

    Returns:
        dict: The response of the deletion operation.
    """
    try:
        response_deleted = CLIENT.delete_businessMetadata(
            guid=guid,
            businessMetadata={attribute_group_name: {attribute_name: ""}}
        )
        return response_deleted
    except ValueError as ve:
        raise ValueError("Error occurred during the deletion process.") from ve
    except Exception as e:
        raise Exception("An error occurred during the deletion process.") from e
 

# Main Processing
# ---------------
# Put the code to be executed inside a main() function, 
# and call it at the bottom of the module with an if __name__ == "__main__" block. 
def main():
    ### Testing
    endpoint = f"https://{REFERENCE_NAME_PURVIEW}.purview.azure.com/"
    qualified_name = "https://hbiqa01analyticsdls.dfs.core.windows.net/raw/Sales/US/AmazonAPI/VendorOrderPO/Ingest/{Year}/{Month}/{Day}/GetPurchaseOrdersCreatedAfterDaily.json"
    entity_properties = get_entity_properties(endpoint, qualified_name)


if __name__ == '__main__':
    main()