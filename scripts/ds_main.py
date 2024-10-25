##! /usr/bin/env python3
 
 
# Import Functions
# ---------------
from modules.lineage.informatica_lineage import *
from modules.entity import *
from utils import get_credentials, create_purview_client
import requests
from pyapacheatlas.core.util import AtlasException
from typing import List
# Import Packages
# ---------------
from pathlib import Path
 
 
# Constants
# ---------------
 
REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
qa_client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)
 
REFERENCE_NAME_PURVIEW = "hbi-pd01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
prod_client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)
   
 
 
# Functions
# ---------------
def upload_relationships(client, entity_a_guid: str, entity_c_guid: str):
    rel_type = "oracle_synonym_source_synonym"
    relationship = {
            "typeName": rel_type,
            "attributes": {},  # You can add any relevant attributes here if needed
            #"guid": -1,  # Set to -1 or remove it if not needed
            "end1": {
                "guid": entity_a_guid
            },
            "end2": {
                "guid": entity_c_guid
            }
        }
    try:
        response = client.upload_relationship(relationship)
        print(f"Successfully added relationship '{rel_type}' between {entity_a_guid} and {entity_c_guid}.")
        print(f"Response: {response}")
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 409:
            # Handle the conflict when the relationship already exists
            print(f"Relationship '{rel_type}' already exists between {entity_a_guid} and {entity_c_guid}.")
        else:
            # Re-raise the exception for other HTTP errors
            raise
    except AtlasException as atlas_err:
        print(f"AtlasException occurred: {str(atlas_err)}")
    # for rel_type in relationship_types:
    #     try:
    #         # Create the relationship as a dictionary with the correct structure
    #         relationship = {
    #             "typeName": rel_type,
    #             "attributes": {},  # You can add any relevant attributes here if needed
    #             #"guid": -1,  # Set to -1 or remove it if not needed
    #             "end1": {
    #                 "guid": entity_a_guid
    #             },
    #             "end2": {
    #                 "guid": entity_c_guid
    #             }
    #         }
    #         # Upload the relationship
    #         response = client.upload_relationship(relationship)
    #         print(f"Successfully added relationship '{rel_type}' between {entity_a_guid} and {entity_c_guid}. Response: {response}")
    #     except Exception as e:
    #         print(f"Failed to add relationship '{rel_type}' between {entity_a_guid} and {entity_c_guid}: {e}")

def main():
    

    # Assuming `client` is an instance of the `Client` class already authenticated
    upload_relationships(prod_client, "cc2ef53b-b32f-46f4-94fb-38f6f6f60000", "d89c2829-46eb-4ee0-a05c-4c451c68113f")
#oracle table source_qual_name: oracle://10.1.17.127/SLBA/DAY_DIMENSION guid=cc2ef53b-b32f-46f4-94fb-38f6f6f60000
#oracle synonym target_qual_name: oracle://10.1.17.127/SLBA/STG_HAA_INVENTORY guid=d89c2829-46eb-4ee0-a05c-4c451c68113f
if __name__ == "__main__":
    main()
