# Glossary Examples

## Get All Entities a Glossary Term is Associated With

```python
from scripts.modules.glossary import *

def example_get_all_entities_with_glossary_term():
    glossary_term_name = "Bill of Material"
    glossary_name = "Glossary"
    entities_with_glossary_term = glossary.get_all_entitities_with_glossary_term(glossary_term_name, glossary_name)
    print(entities_with_glossary_term)
```

<br />

## Remove a Glossary Term from All Entities it's Associated With

```python
from scripts.modules.glossary import *

def example_remove_term_from_all_entities():
    glossary_term_name = "Bill of Material"
    glossary_name = "Glossary"
    entities_with_glossary_term = glossary.get_all_entitities_with_glossary_term(glossary_term_name, glossary_name)
    result = glossary.remove_term_from_all_entities(entities_with_glossary_term, glossary_term_name, glossary_name)
    print(result)
```