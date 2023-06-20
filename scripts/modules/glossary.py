##! /usr/bin/env python3


# Function Imports
# ---------------

from utils import get_credentials, create_purview_client
from modules.entity import *


# Package Imports
# ---------------

import json
import os
from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient
from pyapacheatlas.core.glossary import PurviewGlossaryTerm


# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)


# Functions
# ---------------

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


def get_all_guids_of_entities_with_glossary_term(glossary_term_name: str, glossary_name: str):
    json_str = '{"term": "'+ glossary_term_name +'", "glossary": "' + glossary_name + '"}'
    json_obj = json.loads(json_str)
    result = CLIENT.discovery.search_entities(query = glossary_term_name, search_filter=json_obj)

    all_guids_with_glossary_term = []
    mapping = {"id": "guid"}
    for r in result:
        # Change each entity's "id" to "guid" so assignTerms can find the guids of each entity
        updated_dict = change_key_names(r, mapping)
        all_guids_with_glossary_term.append(updated_dict)

    return all_guids_with_glossary_term


def get_all_entitities_with_glossary_term(glossary_term_name: str, glossary_name: str):
    all_guids = get_all_guids_of_entities_with_glossary_term(glossary_term_name, glossary_name)
    all_entities = []
    for guid_dict in all_guids:
        entities_from_guid = CLIENT.get_entity(guid_dict["guid"])["entities"]
        entity = entities_from_guid[0] # there should just be one entity per guid
        all_entities.append(entity)
    return all_entities


def remove_term_from_all_entities(entities_with_glossary_term: list, term_name: str, glossary_name: str):
    result = CLIENT.glossary.delete_assignedTerm(entities=entities_with_glossary_term, termName = term_name, glossary_name = glossary_name)
    return result



# Main Processing
# ---------------
# Put the code to be executed inside a main() function, 
# and call it at the bottom of the module with an if __name__ == "__main__" block. 

def main():
    print()

if __name__ == "__main__":
    main()