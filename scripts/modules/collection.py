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

def find_collection(collections, parent_collection):
    for collection in collections:
        if collection["name"] == parent_collection:
            return collection
        subcollections = collection.get("subcollections", [])
        if subcollections:
            found_collection = find_collection(subcollections, parent_collection)
            if found_collection:
                return found_collection
    return None


def structure_collection_data(generator):
    collections = []
    for item in generator:
        parent_collection = item.get("parentCollection", {}).get("referenceName")
        collection = {
            "name": item["name"],
            "friendly_name": item["friendlyName"],
            "description": item["description"],
            "parent_collection": parent_collection,
            "subcollections": []
        }
        if parent_collection:
            parent = find_collection(collections, parent_collection)
            if parent:
                parent["subcollections"].append(collection)
            else:
                collections.append(collection)
        else:
            collections.append(collection)

    return collections


def nest_collections(data):
    collections = {}
    for item in data:
        name = item.get('name')
        friendly_name = item.get('friendlyName')
        description = item.get('description')
        parent_collection = item.get('parentCollection', {}).get('referenceName')
        if name not in collections:
            collections[name] = {
                'name': name,
                'friendly_name': friendly_name,
                'description': description,
                'parent_collection': parent_collection,
                'subcollections': []
            }
        else:
            collections[name]['friendly_name'] = friendly_name
            collections[name]['description'] = description
            collections[name]['parent_collection'] = parent_collection

        if parent_collection:
            if parent_collection not in collections:
                collections[parent_collection] = {
                    'name': parent_collection,
                    'friendly_name': None,
                    'description': None,
                    'parent_collection': None,
                    'subcollections': []
                }
            collections[parent_collection]['subcollections'].append(collections[name])

    return [collection for collection in collections.values() if not collection['parent_collection']]


def flatten_collections(data):
    collections = {}
    data = list(data)  # Convert generator to list
    for item in data:
        name = item['name']
        friendly_name = item['friendlyName']
        description = item['description']
        parent_collection = item.get('parentCollection', {}).get('referenceName')

        if name not in collections:
            collections[name] = {
                'name': name,
                'friendly_name': friendly_name,
                'description': description,
                'parent_collection': parent_collection,
                'subcollections': []
            }

        if parent_collection:
            if parent_collection not in collections:
                collections[parent_collection] = {
                    'name': parent_collection,
                    'friendly_name': '',
                    'description': '',
                    'parent_collection': None,
                    'subcollections': []
                }

            collections[parent_collection]['subcollections'].append(name)

    return list(collections.values())


def get_nested_collections():
    """s
    Retrieves a list of collections that are nested.

    Returns:
        list: A list of dictionaries representing the collections.
    """
    generator = CLIENT.collections.list_collections()
    collections = nest_collections(generator)
    return collections


def get_flattened_collections():
    """
    Retrieves a list of collections that is a flattened hierarchy.

    Returns:
        list: A list of dictionaries representing the collections.
    """
    generator = CLIENT.collections.list_collections()
    collections = flatten_collections(generator)
    return collections


def get_existing_collection_names():
    collections = get_flattened_collections()
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

def main():
    print()
    

if __name__ == '__main__':
    # Call main function
    main()