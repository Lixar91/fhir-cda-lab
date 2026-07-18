# Goal: your first clinical XML with lxml — same patients, different wire format.

from lxml import etree

# 1. Parse the file with etree.parse() and get the root element
# The following method, although valid, can be done in a more easy way
# with open("files/patients.xml", "rb") as f:
#     patients = etree.parse(f)

# Easiest way to safely open an XML
patients = etree.parse("files/patients.xml")
root = patients.getroot()

# 2. Iterate over root.findall("patient") and, for each one, print:
#    tag, the "id" attribute, and the family name
#    -> explore: element.get("attr") vs element.find("child") vs element.findall()
#    -> P003 must not crash when looking for conditions (element.find returns None!)

# element.get("att") is used to read the attributes of the element. It doesn't return the value of any children's attributes!
# Use element.tag to return the node name, and element.text to get the value of the XML node.
# element.find("child") returns the first direct child element with matching name (ONLY ONE ELEMENT IS RETURNED!). Returns None if not found.
# Use ".//child" to search that element at any depth of the tree
# element.findall("child") returns all children elements with matching name. Always returns a list of size 0 or greater.
for patient in root.findall("patient"):
    print(f"{patient.tag}, {patient.get("id")}, {patient.find('name').get("family")}")
    # Accessing to conditions to see how I would handle the None case
    #conditions = patient.find("conditions")
    #print(f"{len(conditions if conditions is not None else [])} conditions")
