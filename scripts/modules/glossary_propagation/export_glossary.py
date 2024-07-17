##! /usr/bin/env python3

# Function Imports
# ---------------

from pyapacheatlas.core import AtlasEntity ,AtlasClassification
from pyapacheatlas.core.entity import AtlasEntity, AtlasProcess
from pyapacheatlas.core.typedef import EntityTypeDef, AtlasAttributeDef
from pyapacheatlas.readers import ExcelConfiguration,ExcelReader
from utils import get_credentials,create_purview_client
from pyapacheatlas.core.glossary import *

# Imports
# ---------------

import pandas as pd
import json
from pathlib import Path
import random
import string
from datetime import date

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


def get_all_glossary_terms(client):
    result=client.glossary.get_glossaries(-1,0,"ASC")
    term_guids = [term['termGuid'] for term in result[0]['terms']]
    csv_file = f"./ExportGlossaryFiles/glossary_terms_"+str(date.today())+".csv"
    try:
        result=client.glossary.export_terms(term_guids,csv_file )
    except Exception as e:
        print(e)
