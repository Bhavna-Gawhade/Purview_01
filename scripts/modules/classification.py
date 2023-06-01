##! /usr/bin/env python3


# Function Imports
# ---------------
from modules import entity
from utils import get_credentials, create_purview_client


# Package Imports
# ---------------
from pyapacheatlas.core import AtlasEntity
from pyapacheatlas.core.entity import AtlasEntity, AtlasUnInit
from pyapacheatlas.core import AtlasClassification
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


def get_all_entities_with_classification(classification_name: str):
    """
    Retrieves all entities with a specified classification.

    Args:
        classification_name (str): The name of the classification.

    Returns:
        all_entities_with_classification (list): List of entities with the specified classification.
    """
    json_str = '{"classification": "' + classification_name + '"}'
    json_obj = json.loads(json_str)
    result = CLIENT.discovery.search_entities(query = classification_name, search_filter=json_obj)

    all_entities_with_classification = []
    mapping = {"id": "guid"}
    for r in result:
        # Change each entity's "id" to "guid" so assignTerms can find the guids of each entity
        updated_dict = change_key_names(r, mapping)
        all_entities_with_classification.append(updated_dict)

    return all_entities_with_classification


def associate_classification_and_glossary_term(classification_name: str, glossary_term_name: str):
    """
    Gets all entities associated with a classification and associates the specified glossary term with those entities too.

    Args:
        classification_name (str): The name of the classification.
        glossary_term_name (str): The name of the glossary term.

    Returns:
        result: The result of associating the classification with the glossary term.
    """
    entities_with_classification = get_all_entities_with_classification(classification_name)
    result = CLIENT.assignTerm(entities = entities_with_classification, termName = glossary_term_name, glossary_name = "Glossary")
    return result


def get_entity_classification(qualified_name: str):
    """
    Retrieves the classifications associated with an entity based on the qualified name.

    Args:
        qualified_name (str): The qualified name of the entity.

    Returns:
        classifications: The classifications of the entity.
    """
    ent = entity.get_entity_from_qualified_name(qualified_name)
    classifications = ent["classification"]
    return classifications


# Main Processing
# ---------------
# Put the code to be executed inside a main() function, 
# and call it at the bottom of the module with an if __name__ == "__main__" block. 
def main():
    print()
    

if __name__ == '__main__':
    # Call main function
    main()