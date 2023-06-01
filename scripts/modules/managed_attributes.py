##! /usr/bin/env python3

# File Notes
# ---------------
__author__ = "User Name"
__version__ = "1.0"
__email__ = "dylan.gregorysmith@gmail.com"
__status__ = "Development"


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
# Define constants at the top of the module, 
# in all capital letters with underscores separating words.

storage_name = "<name of your Storage Account>"
storage_id = "<id of your Storage Account>"
rg_name = "<name of your resource group>"
rg_location = "<location of your resource group>"
REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)


# Classes
# ---------------
# Define classes after the constants. 


# Functions
# ---------------

def create_attribute(attribute_group_name: str, attribute_names: list):
    """
    Creates an attribute group with specified attribute names using the PurviewClient library.

    Args:
        attribute_group_name (str): The name of the attribute group to be created.
        attribute_names (list): A list of attribute names to be included in the attribute group.

    Returns:
        Any: The response from the upload_typedefs method of the PurviewClient, indicating the success or failure of the operation.
    """

    attr_list = []
    for n in attribute_names: 
        attr_list.append(AtlasAttributeDef(name=n,options={"maxStrLength": "50","applicableEntityTypes":"[\"DataSet\"]"}))

    bizdef = AtlasStructDef(
        name=attribute_group_name,
        category=TypeCategory.BUSINESSMETADATA,
        attributeDefs=attr_list
    )

    response = CLIENT.upload_typedefs(businessMetadataDefs=[bizdef], force_update=True)
    return response


def add_attributes_to_entity(entity: AtlasEntity, attribute_group_name: str, attribute_name: str, attribute_value: str):
    """
    Adds an attribute to the business metadata of a specified entity using the PurviewClient library.

    Args:
        entity (AtlasEntity): The entity to which the attribute is to be added.
        attribute_group_name (str): The name of the attribute group to which the attribute belongs.
        attribute_name (str): The name of the attribute to be added.
        attribute_value (str): The value of the attribute to be added.

    Returns:
        Any: The response from the update_businessMetadata method of the PurviewClient, indicating the success or failure of the operation.
    """

    response_update = CLIENT.update_businessMetadata(
        guid=entity.guid,
        businessMetadata={
            attribute_group_name:{attribute_name:attribute_value}
        }
    )
    return response_update


def delete_attribute(guid: str, attribute_group_name: str, attribute_name: str):
    """
    Deletes a specific attribute from the business metadata of an entity using the PurviewClient library.

    Args:
        client (PurviewClient): An instance of the PurviewClient class for interacting with the Purview service.
        guid (str): The GUID of the entity from which the attribute is to be deleted.
        attribute_group_name (str): The name of the attribute group to which the attribute belongs.
        attribute_name (str): The name of the attribute to be deleted.

    Returns:
        Any: The response from the delete_businessMetadata method of the PurviewClient, indicating the success or failure of the operation.
    """
    
    response_deleted = CLIENT.delete_businessMetadata(
        guid=guid,
        businessMetadata={attribute_group_name:{attribute_name:""}}
        )
    return response_deleted
 

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