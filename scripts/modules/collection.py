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
import random
import string


# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)
ROOT_COLLECTION_NAME = "hbi-qa01-datamgmt-pview"


# Functions
# ---------------

def get_collections():
    """
    Retrieves a list of collections.

    Returns:
        list: A list of dictionaries representing the collections.
    """
    collections = []
    generator = CLIENT.collections.list_collections()
    for g in generator:
        collection = {
            "name": g["name"],
            "friendly_name": g["friendlyName"],
            "description": g["description"]
        }
        collections.append(collection)
    return collections


def get_existing_collection_names():
    collections = get_collections()
    collection_names = []
    for c in collections:
        collection_names.append(c["name"])
    return collection_names


def create_unique_collection_name():
    existing_names = get_existing_collection_names()
    while True:
        # Generate a 6-character random name
        new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        # Check if the generated name is unique
        if new_name not in existing_names:
            return new_name


def create_collection(friendly_name: str, parent_collection_name: str, description: str):
    """
    Creates or updates a collection with the specified details.

    Args:
        friendly_name (str): The friendly name of the collection.
        parent_collection_name (str): The name of the parent collection.
        description (str): The description of the collection.

    Returns:
        dict: The result of creating or updating the collection.
    """
    name = create_unique_collection_name()
    result = CLIENT.collections.create_or_update_collection(name, friendly_name, parent_collection_name, description)
    return result


def change_key_names(dictionary: dict, key_mapping: dict) -> dict:
    """
    Changes the key names in a dictionary based on a given key mapping.

    Args:
        dictionary (dict): The input dictionary.
        key_mapping (dict): A dictionary containing the mapping of old key names to new key names.

    Returns:
        dict: The dictionary with updated key names.
    """
    new_dict = {}
    for old_key, new_key in key_mapping.items():
        if old_key in dictionary:
            new_dict[new_key] = dictionary[old_key]
        else:
            new_dict[new_key] = None
    return new_dict


def get_all_entities_in_collection(collection_name: str):
    json_str = '{"collectionId": "' + collection_name + '"}'
    json_obj = json.loads(json_str)
    result = CLIENT.discovery.search_entities(query = collection_name, search_filter=json_obj)

    all_entities_in_collection = []
    mapping = {"id": "guid"}
    for r in result:
        # Change each entity's "id" to "guid" so assignTerms can find the guids of each entity
        updated_dict = change_key_names(r, mapping)
        all_entities_in_collection.append(updated_dict)

    return all_entities_in_collection


def delete_collection(collection_name: str):
    result = CLIENT.collections.delete_collection(collection_name)
    return result


# Main Processing
# ---------------
# Put the code to be executed inside a main() function, 
# and call it at the bottom of the module with an if __name__ == "__main__" block. 
def main():
    print()
    

if __name__ == '__main__':
    # Call main function
    main()