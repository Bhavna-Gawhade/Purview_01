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

    result = collection.get_collections()
    print(result)


    '''
    collection_name = "rtywuy"
    result = collection.get_all_entities_in_collection(collection_name)
    print(result)
    '''

    result = collection.get_collections()
    print(result)


    
if __name__ == '__main__':
    main()
