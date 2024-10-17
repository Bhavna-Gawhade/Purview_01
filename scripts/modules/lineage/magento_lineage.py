#!/usr/bin/env python3

# Function Imports
from utils import get_credentials, create_purview_client
from modules import *
from pyapacheatlas.core import AtlasEntity
from pathlib import Path
import pandas as pd

def parse_excel_file(file):
    """
    Parse the given Excel file to extract entity names and their columns.
    """
    df = pd.read_excel(file)
    entity_dict = {}

    for _, row in df.iterrows():
        table_name = row['TABLE_NAME']
        column_name = row['COLUMN_NAME']

        if table_name not in entity_dict:
            entity_dict[table_name] = []
        entity_dict[table_name].append(column_name)

    return entity_dict

def upload_entities_to_purview(client, entity_dict):
    """
    Upload entities and their relationships to Purview.
    """
    for entity_name, columns in entity_dict.items():
        record_qualified_name = f"your_prefix://{entity_name}"
        record = AtlasEntity(entity_name, "DataSet", record_qualified_name)

        # Upload the main entity
        record_assignment = client.upload_entities([record])
        record_guid = next(iter(record_assignment.get('guidAssignments').values()))

        # Upload columns as child entities
        column_entities = []
        for column in columns:
            column_qualified_name = f"{record_qualified_name}#{column}"
            column_entity = AtlasEntity(column, "column", column_qualified_name)
            column_entities.append(column_entity)
            # Create relationship to the parent entity
            column_entity.addRelationship(table=record)

        # Upload column entities
        if column_entities:
            client.upload_entities(column_entities)

        print(f"Uploaded entity: {entity_name} with columns: {columns}")

def main():
    # Define file path
    path_to_file = r'C:\path\to\your\file.xlsx'

    # Get credentials and create Purview client
    CREDS = get_credentials(cred_type='default')
    client = create_purview_client(credentials=CREDS, mod_type='pyapacheatlas', purview_account="your_account")

    # Parse the Excel file
    entity_dict = parse_excel_file(path_to_file)

    # Upload entities to Purview
    upload_entities_to_purview(client, entity_dict)

if __name__ == '__main__':
    main()
