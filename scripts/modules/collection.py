##! /usr/bin/env python3


# Function Imports
# ---------------
from modules import entity
from utils import get_credentials, create_purview_client


# Package Imports
# ---------------
from pyapacheatlas.core import AtlasEntity, AtlasClassification
from pyapacheatlas.core.entity import AtlasEntity, AtlasUnInit
import json
from pathlib import Path


# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)


# Functions
# ---------------

def get_collections():
    """
    Retrieves a list of collections.

    Returns:
        list: A list of dictionaries representing the collections.
    """
    collections = []
    try:
        generator = CLIENT.collections.list_collections()
        for g in generator:
            collection = {
                "name": g["name"],
                "friendly_name": g["friendlyName"],
                "description": g["description"]
            }
            collections.append(collection)
    except Exception as e:
        print(f"An error occurred while retrieving collections: {e}")
    return collections


def create_collection(name: str, friendly_name: str, parent_collection_name: str, description: str):
    """
    Creates or updates a collection with the specified details.

    Args:
        name (str): The name of the collection.
        friendly_name (str): The friendly name of the collection.
        parent_collection_name (str): The name of the parent collection.
        description (str): The description of the collection.

    Returns:
        dict: The result of creating or updating the collection.
    """
    try:
        result = CLIENT.collections.create_or_update_collection(name, friendly_name, parent_collection_name, description)
        return result
    except Exception as e:
        print(f"An error occurred while creating or updating the collection: {e}")
        return None


# Main Processing
# ---------------
# Put the code to be executed inside a main() function, 
# and call it at the bottom of the module with an if __name__ == "__main__" block. 
def main():
    print()
    

if __name__ == '__main__':
    # Call main function
    main()