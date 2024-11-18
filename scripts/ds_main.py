##! /usr/bin/env python3
 
 
# Import Functions
# ---------------
from modules.lineage.business_assets import *
from modules.entity import *
from utils import get_credentials, create_purview_client
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
    # Call the function to to create the application service
    #create_application_service(client=qa_client)
    list_types(qa_client)

if __name__ == "__main__":
    main()
