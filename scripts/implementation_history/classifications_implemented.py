##! /usr/bin/env python3


LAST_UPDATED = "06/14/2023"
CLASSIFICATIONS_IMPLEMENTED = {
  "Classifications": [
    {
      "name": "Volume",
      "rule_name": "Volume",
      "created": True,
      "connected_to_glossary_term": False,
      "regex": "/\.*VOLUME.*\b/|VoLume|/\.*VOL.*\b/|vol"
    },
    {
      "name": "Valuation Class",
      "rule_name": "Valuation_Class",
      "created": True,
      "connected_to_glossary_term": False,
      "regex": "/\b.*Valuation Class.*\b/|Valuation Class|/\b.*VAL.*\b/|VAL"
    },
    {
      "name": "SKU",
      "rule_name": "SKU",
      "created": True,
      "connected_to_glossary_term": False,
      "regex": "/\.*SKU.*\b|\b[a-z]*SKU[a-zA-Z]*\b/|sku"
    },
    {
      "name": "Total Stock",
      "rule_name": "Total_Stock",
      "created": True,
      "connected_to_glossary_term": False,
      "regex": "/\b.*Total Stock.*\b/|Total Stock|/\b.*Total Inventory.*\b/|Total Inventory|/\b.*TOT.*\b/|TOT|/\b.*INV.*\b/|INV|/\b.*TOTL.*\b/|TOTL|/\b.*STK.*\b/|STK"
    },
    {
      "name": "Storage Location",
      "rule_name": "Storage_Location",
      "created": True,
      "connected_to_glossary_term": False,
      "regex": "/\b.*Storage Location.*\b/|Storage Location|/\b.*Warehouse.*\b/|Warehouse|/\b.*LOC.*\b/|LOC"
    },
    {
      "name": "Standard Price",
      "rule_name": "Standard_Price",
      "created": True,
      "connected_to_glossary_term": False,
      "regex": ".*\b(?:Material\b)*.*Standard.*(Price|Pricing).*|.*STD.*"
    },
    {
      "name": "Sales Organization",
      "rule_name": "Sales_Organization",
      "created": True,
      "connected_to_glossary_term": False,
      "regex": "/\b.*Sales Organization.*\b/|Sales Organization|/\b.*ORG.*\b/|ORG"
    },
    {
      "name": "Profit center",
      "rule_name": "Profit_center",
      "created": True,
      "connected_to_glossary_term": False,
      "regex": "/\b.*Profit.*Center.*\b/|Profit.*Center|/\b.*CTR.*\b/|CTR"
    },
    {
      "name": "Material Type",
      "rule_name": "Material_Type",
      "created": True,
      "connected_to_glossary_term": False,
      "regex": "/\b.*Material Type.*\b/|Material Type|/\b.*MAT.*\b/|MAT"
    },
    {
      "name": "Division",
      "rule_name": "Division",
      "created": True,
      "connected_to_glossary_term": False,
      "regex": "/\b.*Division.*\b/|Division|/\.*DIV.*\b/|DIV"
    },
    {
      "name": "Material Number",
      "rule_name": "Material_Number",
      "created": True,
      "connected_to_glossary_term": False,
      "regex": "/\b.*Material.*Number.*\b/|Material.*Number|/\b.*Article.*Number.*\b/|Article.*Number|/\b.*MAT.*\b/|MAT|/\b.*SKU.*\b/|sku|/\b.*NO.*\b/|No|/\b.*Article.*\b/|Article"
    }
  ]
}