# Goal: meet the final boss of clinical XML — namespaces. This is 80% of CDA pain.
# Step 1 (by hand): create files/patients_ns.xml — SAME content as patients.xml,
# but wrapped in a default namespace, CDA-style:
#
# <patients xmlns="urn:example:patients">
#   <patient id="P001">
#     ... same as before ...
# </patients>
#
#
# 1. Run your extract_patients() on it AS-IS. Observe: findall("patient") -> [].
#    ZERO patients. NO error. The most dangerous failure in XML interop: silent emptiness.
# 2. Print root.tag and meet Clark notation: "{urn:example:patients}patients"
# 3. Fix the extraction with a namespace map:
#       NS = {"p": "urn:example:patients"}
#       root.findall("p:patient", NS)   # ...and qualify EVERY path in the function

from lxml import etree

def extract_patients(xml_path: str) -> list[dict]:
    """
    Transforms a patient XML file into a list of dictionaries.
    Handles default XML namespaces via an explicit nsmap.
    :param xml_path: File path of XML file.
    :return: List of dictionaries of the patients.
    :raises FileNotFoundError: File does not exist or cannot be opened.
    :raises ValueError: XML syntax error is detected while parsing.
    """
    if not isinstance(xml_path, str):
        raise TypeError("Parameter must be of type str")

    try:
        xml_tree = etree.parse(xml_path)
        xml_root = xml_tree.getroot()

        # Build nsmap from the root element's declared namespaces.
        # Use 'ns' as a generic prefix for the default namespace.
        nsmap = {"ns": xml_root.nsmap.get(None)} if None in xml_root.nsmap else {}
        # If there is no default namespace, fall back to empty prefix
        # to keep XPath expressions compatible with the original schema.
        prefix = "ns:" if nsmap else ""
        result = []
        for patient in xml_root.findall(f"{prefix}patient", namespaces=nsmap):
            # Extract name of the patient
            name_el = patient.find(f"{prefix}name", namespaces=nsmap)
            p_given = name_el.get("given") if name_el is not None else None
            p_family = name_el.get("family") if name_el is not None else None

            # Birthdate of the patient
            birth_date_el = patient.find(f"{prefix}birthDate", namespaces=nsmap)
            p_birthdate = birth_date_el.get("value") if birth_date_el is not None else None

            # Conditions of the patient
            conditions_container = patient.find(f"{prefix}conditions", namespaces=nsmap)
            condition_list = []
            if conditions_container is not None:
                condition_els = conditions_container.findall(f"{prefix}condition", namespaces=nsmap)
                condition_list = [
                    c.get("display") for c in condition_els if c.get("display")
                ]

            # Build patient json
            json_patient = {
                "given_name": p_given,
                "family_name": p_family,
                "birth_date": p_birthdate,
                "conditions": condition_list,
            }

            # Remove None key-value pairs and return dict
            result.append({k: v for k, v in json_patient.items() if v is not None})

        return result

    except OSError as e:
        raise FileNotFoundError(
            f"XML file does not exist or cannot be opened: {xml_path}"
        ) from e
    except etree.XMLSyntaxError as e:
        raise ValueError(f"Invalid XML syntax in {xml_path}") from e


fich = extract_patients("./files/patients.xml")

print(fich)