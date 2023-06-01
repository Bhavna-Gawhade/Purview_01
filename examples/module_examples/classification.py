##! /usr/bin/env python3

# Import Packages
# ---------------


# Import Functions
# ---------------
from modules.classification import *


# Constants
# ---------------


# Functions
# ---------------

def example_associate_classification_entities_with_glossary_term():
    classification_name = "BOM"
    glossary_term_name = "Bill of Material"
    
    result = associate_classification_and_glossary_term(classification_name, glossary_term_name)
    print(result)


# Main Function
# ---------------

def main():
    print()


if __name__ == '__main__':
    main()