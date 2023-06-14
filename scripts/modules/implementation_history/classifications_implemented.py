##! /usr/bin/env python3


CLASSIFICATIONS_IMPLEMENTED = {
  "Classifications": [
    {
      "name": "Total Stock",
      "rule_name": "Total_Stock",
      "created": True,
      "connected_to_glossary_term": False,
      "regex": "/\b.*Total Stock.*\b/|Total Stock|/\b.*Total Inventory.*\b/|Total Inventory|/\b.*TOT.*\b/|TOT|/\b.*INV.*\b/|INV|/\b.*TOTL.*\b/|TOTL|/\b.*STK.*\b/|STK"
    },
    {
      "name": "Volume",
      "rule_name": "Volume",
      "created": True,
      "connected_to_glossary_term": False,
      "regex": "/\.*VOLUME.*\b/|VoLume|/\.*VOL.*\b/|vol"
    }
  ]
}