##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client


# Package Imports
# ---------------
from pyapacheatlas.core import AtlasEntity, AtlasClassification
from pyapacheatlas.core.entity import AtlasEntity, AtlasUnInit
import json
import csv
from pathlib import Path
import pandas as pd
import re
import random
import string
import os


# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)


# Functions
# ---------------

def process():
    storage_location_regex = r"/\b.*Storage[^A-Za-z0-9]?(Location|LOC).*\b/|Storage[^A-Za-z0-9]?(Location|LOC)|/\b.*Warehouse.*\b/|Warehouse|/\b.*SLOC.*\b/|SLOC"
    pipe0 = r"/\b.*Storage[^A-Za-z0-9]?(Location|LOC).*\b/"
    pipe1 = r"Storage[^A-Za-z0-9]?(Location|LOC)"
    pipe2 = r"/\b.*Warehouse.*\b/"
    pipe3 = r"Warehouse"
    pipe4 = r"/\b.*SLOC.*\b/"
    pipe5 = r"SLOC"


    testing_alt_storage_location_regex = r"/\b.*Storage[^A-Za-z0-9]?(Location|LOC).*\b/|/\b.*Warehouse.*\b/|/\b.*SLOC.*\b/"

    


# Main Processing
# ---------------

def main():
    print()
    

if __name__ == '__main__':
    # Call main function
    main()


