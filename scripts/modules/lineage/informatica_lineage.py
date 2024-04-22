import xml.etree.ElementTree as ET
import re


def get_source_and_target_groupings(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    groupings = []
    group = []
    last_tag = ""
    
    for folder in root.findall('.//FOLDER'):
        # Iterate through each element in the folder
        for elem in folder:
            # Save the element's attributes
            elem_dict = {
                "type":  elem.tag,
                "table": elem.attrib.get('NAME'),
                "server": elem.attrib.get('DBDNAME'),
                "schema": elem.attrib.get('OWNERNAME')
            }

            # Check if the element is a SOURCE or TARGET
            if elem.tag == 'SOURCE' and last_tag == 'TARGET':
                # Save the current grouping and then clear it to start another grouping
                groupings.append(group.copy())
                group = []
                group.append(elem_dict)
            elif elem.tag == 'SOURCE' and (last_tag == 'SOURCE' or last_tag == ''):
                group.append(elem_dict)
            elif elem.tag == 'TARGET':
                group.append(elem_dict)
            else:
                continue
            # Save the tag type
            last_tag = elem.tag

    return groupings


def get_sources_targets_and_mappings(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    sources_and_targets = []
    mappings = []
    
    for folder in root.findall('.//FOLDER'):
        for elem in folder:
            # Check if the element is a SOURCE, TARGET, or MAPPING
            if elem.tag == 'SOURCE' or elem.tag == 'TARGET':
                elem_dict = {
                    "type":  elem.tag,
                    "table": elem.attrib.get('NAME'),
                    "server": elem.attrib.get('DBDNAME'),
                    "schema": elem.attrib.get('OWNERNAME')
                }
                sources_and_targets.append(elem_dict)
            elif elem.tag == 'MAPPING':
                mappings.append(elem.attrib.get('DESCRIPTION'))
                
    return sources_and_targets, mappings


def grab_sources_and_targets_for_each_mapping(mappings, file_path):
    # Regular expression pattern to match "from X to Y" statements
    pattern_from_to = r'from\s+(\S+)\s+to\s+(\S+)\b'

    # Regular expression pattern to match "from X and Z to Y" statements
    pattern_from_and_to = r'from\s+(\S+)\s+and\s+(\S+)\s+to\s+(\S+)\b'

    # Grab which sources and targets are grouped together. Can't rely on the order of sources and targets in the XML export.
    grouped_sources_and_targets = []

    for mapping in mappings:
        # Grab the to's and from's for each mapping, and output error message for mappings without both
        match_from_to = re.search(pattern_from_to, mapping)
        match_from_and_to = re.search(pattern_from_and_to, mapping)
    
        # Check if "from X to Y" statement exists
        if match_from_to:
            source = match_from_to.group(1)
            target = match_from_to.group(2)
            grouped_sources_and_targets.append({"sources": [source], "target": target})
            print(f"Found 'from {source} to {target}': Source={source}, Target={target}")
            
        # Check if "from X and Z to Y" statement exists
        elif match_from_and_to:
            source1 = match_from_and_to.group(1)
            source2 = match_from_and_to.group(2)
            target = match_from_and_to.group(3)
            grouped_sources_and_targets.append({"sources": [source1, source2], "target": target})
            print(f"Found 'from {source1} and {source2} to {target}': Sources={source1}, {source2}, Target={target}")
            
        else:
            print("Error: No 'from X to Y' statement found in:", mapping, ". With file: ", file_path)

    return grouped_sources_and_targets


def build_lineage_between_source_and_target_groupings(grouped_sources_and_targets, sources_and_target_details):
    for group in grouped_sources_and_targets:
        # Currently handles 1-2 sources and 1 target
        source_table_list = group.get("sources")
        target_table = group.get("target")


def parse_informatica_xml_export(file_path):
    # Separate the XML export into groupings of sources and targets
    sources_and_targets, mappings = get_sources_targets_and_mappings(file_path)

    # Since the source/target pairings are exported in unpredictable orders, we must 
    # rely on the mapping descriptions to identify which sources are for which targets
    grouped_sources_and_targets = grab_sources_and_targets_for_each_mapping(mappings, file_path)
    
    # Build lineage from the source and target groupings
    build_lineage_between_source_and_target_groupings(grouped_sources_and_targets, sources_and_targets)
