##! /usr/bin/env python3


# Function Imports
# ---------------
from utils import get_credentials, create_purview_client
from modules import *
from modules.lineage.shared_lineage_functions import *
import xml.etree.ElementTree as ET


# Imports
# ---------------

import re
import sys
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

def ensure_unique_sets(dimensions):
    for dimension_id, attribute_ids in dimensions.items():
        unique_attribute_ids = list(set(attribute_ids))
        dimensions[dimension_id] = unique_attribute_ids
    return dimensions


def parse_cube_xmla(xmla_file):
    tree = ET.parse(xmla_file)
    root = tree.getroot()
    dimensions = {} # structured as {dimension_ID: [list of attribute IDs]}

    # Find all Dimension elements
    for dimension_elem in root.findall('.//{http://schemas.microsoft.com/analysisservices/2003/engine}Dimension'):
        dimension_id_elem = dimension_elem.find('{http://schemas.microsoft.com/analysisservices/2003/engine}ID')
        if dimension_id_elem is None:
            dimension_id_elem = dimension_elem.find('{http://schemas.microsoft.com/analysisservices/2003/engine}DimensionID')
        if dimension_id_elem is not None:
            dimension_id = dimension_id_elem.text
            attributes = []

            # Find all Attribute elements within the dimension
            for attribute_elem in dimension_elem.findall('.//{http://schemas.microsoft.com/analysisservices/2003/engine}Attribute'):
                attribute_id_elem = attribute_elem.find('{http://schemas.microsoft.com/analysisservices/2003/engine}ID')
                if attribute_id_elem is None:
                    attribute_id_elem = attribute_elem.find('{http://schemas.microsoft.com/analysisservices/2003/engine}AttributeID')
                if attribute_id_elem is not None:
                    attribute_id = attribute_id_elem.text
                    attributes.append(attribute_id)

            # Check if dimension already exists in dimensions dictionary
            if dimension_id in dimensions:
                # Append attributes to existing list
                dimensions[dimension_id].extend(attributes)
            else:
                # Add dimension and its attributes to dimensions dictionary
                dimensions[dimension_id] = attributes

    return ensure_unique_sets(dimensions)


# Main Processing
# ---------------

def main():
    print()


if __name__ == '__main__':
    main()