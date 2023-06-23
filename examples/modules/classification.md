# Classification Examples


## Generating Bulk Creation of REGEX Strings for Classifications

```python
from modules.classification.regex_generator import *

def example_generate_all_regex():
    file_path = "Classifications_from_Glossary_Terms.xlsx"
    classification_info_sheet_name = "TERM_INFO"
    abbreviation_mappings_sheet_name = "ABBREVIATION_MAPPINGS"
    all_regex = generate_all_regex(file_path, classification_info_sheet_name, abbreviation_mappings_sheet_name)
    for x in all_regex:
        print(x)
        print("\n")
```

<br />

## Exporting Generated REGEX Strings for Classifications

```python
from modules.classification.regex_generator import *

def example_export_regex_to_excel():
    file_path = "Classifications_from_Glossary_Terms.xlsx"
    classification_info_sheet_name = "TERM_INFO"
    abbreviation_mappings_sheet_name = "ABBREVIATION_MAPPINGS"
    all_regex = generate_all_regex(file_path, classification_info_sheet_name, abbreviation_mappings_sheet_name)
    export_to_excel(all_regex, "all_regex_terms.xlsx")
```

<br />

## Generating Bulk Creation of Pass Testing Files for Classifications

The classifications should pass each of the testing column names in these generated files.

```python
from modules.classification.test_case_generator import *

def example_generate_all_pass_test_files():
    pass_file_names = generate_all_pass_test_files(CLASSIFICATION_EXCEL_FILE_NAME, MAPPINGS_EXCEL_FILE_NAME)
    print(pass_file_names)
```

<br />

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


## Extract an Excel Sheet from an Excel File

```python
def example_extract_sheet_from_excel():
    file_path = "example.xlsx"
    sheet_name = "Sheet1"
    extracted_sheet = extract_sheet_from_excel(file_path, sheet_name)
```