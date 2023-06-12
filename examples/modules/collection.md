# Collection Examples

## Getting Collections

```python
from scripts.modules.collection import *

def example_get_collections():
    collections = get_collections()
    print(collections)
```

## Creating a Collection

```python
from scripts.modules.collection import *

def example_create_collection():
    # Name the collection
    friendly_name = "Unclassified"
    name = "unclassified"

    # Note, "hbi-qa01-datamgmt-pview" is the name of the root directory and has the same name as the account, and cannot be changed
    parent_collection_name = "hbi-qa01-datamgmt-pview" 
    description = "This collection will hold all of HBI's resources that have been scanned, but not classified yet"

    result = create_collection(name, friendly_name, parent_collection_name, description)
    print(result)
```

