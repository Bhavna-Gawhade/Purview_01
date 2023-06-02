# Classification Examples

## Associate a Classification with a Glossary Term

As of this writing, there is currently no way to directly associate a classification with a glossary term via Purview's SDK or pyapacheatlas. However, this function pulls all of the entities associated with a specified classification and then applies a specified glossary term to those same entities.

```python
from scripts.modules.classification import *

def example_associate_classification_entities_with_glossary_term():
    # Specify the names of the classification and glossary term you would like to connect
    classification_name = "BOM"
    glossary_term_name = "Bill of Material"
    
    # Associate the classification and glossary term
    result = associate_classification_and_glossary_term(classification_name, glossary_term_name)
    print(result)
```