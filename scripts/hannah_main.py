##! /usr/bin/env python3


# Import Functions
# ---------------
from modules import entity, classification, collection


# Import Packages
# ---------------
from pathlib import Path
from pyapacheatlas.core.typedef import AtlasAttributeDef, AtlasStructDef, TypeCategory
from pyapacheatlas.core import AtlasEntity, AtlasProcess
from azure.core.exceptions import HttpResponseError
from utils import get_credentials, create_purview_client
import json


# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)


# Functions
# ---------------


# Main Function
# ---------------

def main():
    print()

    """ Get Collections Example """
    collections = collection.get_collections()
    print(collections)

    """ Create Collection Example - NEED TO TEST """
    friendly_name = "Unclassified"
    friendly_name_snake_case = "unclassified"
    # Note, "hbi-qa01-datamgmt-pview" is the name of the root directory and has the same name as the account, and cannot be changed
    parent_collection_name = "hbi-qa01-datamgmt-pview" 
    name = parent_collection_name + "/" + friendly_name_snake_case
    description = "This collection will hold all of HBI's resources that have been scanned, but not classified yet"
    result = collection.create_collection(name, friendly_name, parent_collection_name, description)
    print(result)

    
if __name__ == '__main__':
    main()
