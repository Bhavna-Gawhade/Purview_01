# Entity Examples

## Create an Entity to Use for Testing

```python
import json
import datetime
from modules import entity

def example_create_entity_for_testing():
    # Using a previously uploaded custom type def. If a new typedef was created for this, make sure to upload it first
    name = "TESTING_PURVIEW_DEV"   
    type_name = "dev_testing_typedef"
    timestamp = datetime.datetime.now().isoformat()
    qualified_name = "testing_for_purview_dev/" + timestamp
    result = create_entity(name, type_name, qualified_name)
    print(result)   

```

<br />

## Create and Upload a Custom Typedef

```python
import json
from modules import entity

TESTING_DEF = EntityTypeDef(
  name = "dev_testing_typedef",
  superTypes = ["DataSet"]
)

def example_upload_custom_typedef():
    result = upload_custom_type_def(TESTING_DEF)
    print(json.dumps(result))
```