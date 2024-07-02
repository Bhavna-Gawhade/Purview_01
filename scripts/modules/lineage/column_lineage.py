from pyapacheatlas.core import AtlasEntity, AtlasProcess
import pandas as pd
import json


from modules.entity import *


def extract_column_mappings_from_excel(file_path):
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)
        
        # Initialize an empty list to store mappings
        mappings = []
        
        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            mapping = {
                "Source": row['source_column'],
                "Sink": row['target_column']
            }
            mappings.append(mapping)
        
        return mappings
    
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None


def build_column_lineage_using_mappings(client, mappings, source_qual_name, target_qual_name):
    # Pull both entities first
    source = get_entity_from_qualified_name(client, source_qual_name)
    target = get_entity_from_qualified_name(client, target_qual_name)

    # Save the details as an AtlasEntity
    s = AtlasEntity(
        name = source["name"],
        typeName = source["entityType"],
        qualified_name = source["qualifiedName"],
        guid = source["id"]
    )
    source_naming_str = s.name.replace(" ", "_") + "/"

    t = AtlasEntity(
        name = target["name"],
        typeName = target["entityType"],
        qualified_name = target["qualifiedName"],
        guid = target["id"]
    )
    target_naming_str = t.name.replace(" ", "_") + "/"

    # Register the process to save connection details
    """proc = AtlasProcess(
        name = process_type_name,
        typeName = process_type_name,
        qualified_name = "sources:" + source_naming_str + "targets:" + target_naming_str + "process_type:" + process_type_name,
        inputs = [s],
        outputs = [t]
    )"""

    # Get the column mappings
    #mappings = [{"Source": "cust_id", "Sink": "cust_id"},{...}]
    col_map = {
        "DatasetMapping": {
            "Source": s.qualifiedName, 
            "Sink": t.qualifiedName
        },
        "ColumnMapping": mappings  
    }
 
    # Update the process with the mappings
    #proc.attributes.update("columnMapping": json.dumps(col_map))
   
    # Register the process to save connection details
    process_type_name = "System_Connection"
    proc = AtlasProcess(
        name = process_type_name,
        typeName = process_type_name,
        qualified_name = "sources:" + source_naming_str + "targets:" + target_naming_str + "process_type:" + process_type_name,
        inputs = [s],
        outputs = [t],
        attributes = {"columnMapping": mappings}
    )

    # Push the lineage to Purview
    results = client.upload_entities([proc, s, t])
    print(json.dumps(results, indent=2))



def alt_build_column_lineage_using_mappings(client, mappings, source_qual_name, target_qual_name):
    # Pull both entities first
    source = get_entity_from_qualified_name(client, source_qual_name)
    target = get_entity_from_qualified_name(client, target_qual_name)

    # Save the details as an AtlasEntity
    s = AtlasEntity(
        name = source["name"],
        typeName = source["entityType"],
        qualified_name = source["qualifiedName"],
        guid = source["id"]
    )
    source_naming_str = s.name.replace(" ", "_") + "/"

    t = AtlasEntity(
        name = target["name"],
        typeName = target["entityType"],
        qualified_name = target["qualifiedName"],
        guid = target["id"]
    )
    target_naming_str = t.name.replace(" ", "_") + "/"

    # Register the process to save connection details
    process_type_name = "System_Connection"
    proc = AtlasProcess(
        name = process_type_name,
        typeName = process_type_name,
        qualified_name = "sources:" + source_naming_str + "targets:" + target_naming_str + "process_type:" + process_type_name,
        inputs = [s],
        outputs = [t]
    )

    # Get the column mappings
    #mappings = [{"Source": "cust_id", "Sink": "cust_id"},{...}]
    col_map = {
        "DatasetMapping": {
            "Source": s.qualifiedName, 
            "Sink": t.qualifiedName
        },
        "ColumnMapping": mappings  
    }
 
    # Update the process with the mappings
    #proc.relationshipAttributes.update({"attributes": {"columnMapping": json.dumps(mappings)}})
    #proc.addCustomAttribute(columnMapping = json.dumps(mappings))
    #s.addCustomAttribute(attributes = {"columnMapping": json.dumps(mappings)})
    #proc.addRelationship(attributes = json.dumps(col_map))
    s.addRelationship(attributes = json.dumps(col_map))

    # Push the lineage to Purview
    results = client.upload_entities([proc, s, t])
    print(json.dumps(results, indent=2))