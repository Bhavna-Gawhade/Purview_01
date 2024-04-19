import xml.etree.ElementTree as ET

def get_source_and_target_groupings(file_path):

    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    for folder in root.findall('.//FOLDER'):
        # Initialize variables to store groups of fields
        sources = []
        targets = []
        groupings = []

        # Iterate through each element in the folder
        for elem in folder:
            # Check if the element is a SOURCE or TARGET
            if elem.tag == 'SOURCE':
                sources.append(elem)
            elif elem.tag == 'TARGET':
                targets.append(elem)
            else:
                # If neither SOURCE nor TARGET, skip
                continue

            # If the next element is of the opposite type or there are no more elements
            if (elem.getnext() is None) or (elem.getnext().tag != elem.tag):
                # Process the collected fields
                grouping = [sources, targets]
                print("SOURCE:")
                for source in sources:
                    print("Name:", source.attrib.get('NAME'))
                    print("Data Type:", source.attrib.get('DATATYPE'))
                    print("Description:", source.attrib.get('DESCRIPTION'))
                    print("--------------------")
                
                print("TARGET:")
                for target in targets:
                    print("Name:", target.attrib.get('NAME'))
                    print("Data Type:", target.attrib.get('DATATYPE'))
                    print("Description:", target.attrib.get('DESCRIPTION'))
                    print("--------------------")
                
                groupings.append(grouping)
                
                # Clear the lists for the next group
                sources.clear()
                targets.clear()

    return groupings


def parse_informatica_xml_export(file_path):
    groupings = get_source_and_target_groupings(file_path)