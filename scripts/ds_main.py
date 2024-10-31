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

def main():
    # Call the function to update descriptions
    update_lineage_connector_descriptions(qa_client)

if __name__ == "__main__":
    main()
