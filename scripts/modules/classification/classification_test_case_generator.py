##! /usr/bin/env python3


# Function Imports
# ---------------
from modules import entity
from utils import get_credentials, create_purview_client


# Package Imports
# ---------------
from pyapacheatlas.core import AtlasEntity, AtlasClassification
from pyapacheatlas.core.entity import AtlasEntity, AtlasUnInit
import json
import csv
from pathlib import Path
import pandas as pd

# Constants
# ---------------

REFERENCE_NAME_PURVIEW = "hbi-qa01-datamgmt-pview"
PROJ_PATH = Path(__file__).resolve().parent
CREDS = get_credentials(cred_type= 'default')
CLIENT = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account= REFERENCE_NAME_PURVIEW)
CLASSIFICATION_EXCEL_FILE = "Classification_Regex_Rules.xlsx"

# Functions
# ---------------

def create_column_names():
    print()


def process_excel_file(file_path):
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        column1_value = row['Column1']
        column2_value = row['Column2']
        column3_value = row['Column3']


def get_excel_column_names(file_path):
    df = pd.read_excel(file_path)
    column_names = df.columns.tolist()
    return column_names


def generate_test_case_csv_file(keywords: list, common_abbreviations: list):
    # Specify the column names
    column_names = ['Column1', 'Column2', 'Column3']

    # Specify the data rows
    data_rows = [
        [1, 'A', True],
        [2, 'B', False],
        [3, 'C', True]
    ]

    # Specify the output file name
    filename = 'output.csv'

    # Open the CSV file in write mode
    with open(filename, 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Write the column names
        writer.writerow(column_names)

        # Write the data rows
        writer.writerows(data_rows)

    print(f'CSV file "{filename}" created successfully.')


# Main Processing
# ---------------

def main():
    print()
    

if __name__ == '__main__':
    # Call main function
    main()