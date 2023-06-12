# Collection Examples

## Getting Collections in a Flattened Structure

```python
from scripts.modules.collection import *

def example_get_flattened_collections():
    result = get_flattened_collections()
    print(result)
```

<br />

## Getting Collections in a Nested Structure

```python
from scripts.modules.collection import *

def example_get_nested_collections():
    result = get_nested_collections()
    print(result)
```

<br />

## Getting Existing Collection Names

```python
from scripts.modules.collection import *

def example_get_existing_collection_names():
    result = get_existing_collection_names()
    print(result)
```

<br />

## Creating a Collection

```python
from scripts.modules.collection import *

def example_create_collection():
    friendly_name = "Unclassified"
    parent_collection_name = "hbi-qa01-datamgmt-pview" # NOTE: this is the root directory name
    description = "This collection holds all resources that have been scanned, but not yet classified"
    result = create_collection(friendly_name, parent_collection_name, description)
    print(result)
```

<br />

## Get All Entities in a Collection

```python
from scripts.modules.collection import *

def example_get_all_entities_in_collection():
    collection_name = "rtywuy" # NOTE: this is the collection's name not its friendly name
    result = get_all_entities_in_collection(collection_name)
    print(result)
```

<br />

## Deleting a Collection

```python
from scripts.modules.collection import *

def example_delete_collection():
    collection_name = "" # NOTE: this is the collection's name not its friendly name
    result = sdelete_collection(collection_name)
    print(result)
```

## Creating Subcollections Based off a JSON File

```python
from scripts.modules.collection import *

def example_create_subcollections_from_json():
    friendly_name = "Source"
    with open("collections_structure.json", 'r') as file:
        data = json.load(file)
        json_string = json.dumps(data)
    generate_subcollections_from_json(friendly_name, json_string)
```

An example of "collections_structure.json" is below:
```json
  [
    {
      "friendly_name": "hbi-qa01-datamgmt-pview",
      "description": "The root collection.",
      "parent_collection_friendly_name": null,
      "subcollections": [
        {
          "friendly_name": "HBI Production",
          "description": "HBI Production",
          "parent_collection_friendly_name": "hbi-qa01-datamgmt-pview",
          "subcollections": [
            {
              "friendly_name": "HBI-Shared-Hub",
              "description": null,
              "parent_collection_friendly_name": "HBI Production",
              "subcollections": []
            }
          ]
        },
        {
          "friendly_name": "Shared-Hub",
          "description": null,
          "parent_collection_friendly_name": "hbi-qa01-datamgmt-pview",
          "subcollections": [
            {
              "friendly_name": "Human Resources",
              "description": null,
              "parent_collection_friendly_name": "Shared-Hub",
              "subcollections": []
            }
          ]
        },
        {
          "friendly_name": "Source",
          "description": null,
          "parent_collection_friendly_name": "hbi-qa01-datamgmt-pview",
          "subcollections": [
            {
              "friendly_name": "Finance",
              "description": null,
              "parent_collection_friendly_name": "Source",
              "subcollections": []
            },
            {
              "friendly_name": "Material Article",
              "description": null,
              "parent_collection_friendly_name": "Source",
              "subcollections": []
            }
          ]
        },
        {
          "friendly_name": "Unclassified",
          "description": null,
          "parent_collection_friendly_name": "hbi-qa01-datamgmt-pview",
          "subcollections": []
        }
      ]
    }
  ]
```