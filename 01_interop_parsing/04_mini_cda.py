# Goal: data migrates from attributes to TEXT NODES + a real-looking namespace.
# This is the actual shape of CDA. files/patients_cda.xml (by hand):
#
# <clinicalDocument xmlns="urn:hl7-org:v3">
#   <recordTarget>
#     <patientRole id="P001">
#       <patient>
#         <name><given>Nick</given><family>Doe</family></name>
#         <birthTime value="1995-03-12"/>
#       </patient>
#     </patientRole>
#   </recordTarget>
#   <!-- Ana P002: <birthTime value="not-a-date"/>. Luis P003: 1958-11-01, no conditions -->
# </clinicalDocument>
#
# 1. Write extract_patients_cda(xml_path: str) -> list[dict] producing the SAME
#    canonical dicts (ALL four keys always present — normalize at the boundary!)
#    -> hint: element.findtext("p:given", namespaces=NS) is your friend
# 2. Feed the SAME report. Zero changes to patient_utils.
# 3. Written deliverable, 5 lines in README: "patients_from_xml.json vs
#    patients.json — identical? Why / why not? What did I normalize and where?"
# The info cannot be added in README, so I created a new file called other_notes.md in docs folder

import json
from lxml import etree
from patient_utils import build_full_name, count_conditions, parse_birth_date, build_full_name_from_patient
from datetime import date


def extract_patients_cda(xml_path: str) -> list[dict]:
    """
    Transforms a patient CDA XML file into a list of dictionaries.
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

        patient = xml_root.find(f"{prefix}recordTarget/{prefix}patientRole/{prefix}patient", namespaces=nsmap)

        if patient is not None:
            # Name of the patient
            name_el = patient.find(f"{prefix}name", namespaces=nsmap)
            given_name = name_el.find(f"{prefix}given",
                                      namespaces=nsmap).text if name_el.find(f"{prefix}given",
                                                                             namespaces=nsmap) is not None else None
            family_name = name_el.find(f"{prefix}family",
                                       namespaces=nsmap).text if name_el.find(f"{prefix}family",
                                                                              namespaces=nsmap) is not None else None
            # Birthdate of the patient
            birth_date = patient.find(f"{prefix}birthTime", namespaces=nsmap).get("value") if patient.find(
                f"{prefix}birthTime", namespaces=nsmap) is not None else None

            json_patient = {"given_name": given_name,
                            "family_name": family_name,
                            "birth_date": birth_date,
                            "conditions": []
                            }
            return [json_patient]
        else:
            return []
    except OSError as e:
        raise FileNotFoundError(
            f"XML file does not exist or cannot be opened: {xml_path}"
        ) from e
    except etree.XMLSyntaxError as e:
        raise ValueError(f"Invalid XML syntax in {xml_path}") from e

################################

# Report generation

################################

report = {}

# 1. Loading the patient data
patients = extract_patients_cda("./files/patients_cda.xml")

# 1.1 Save the xml converted json into a file to diff it later
with open('files/patients_from_cda_xml.json', 'w') as json_file:
    json.dump(patients, json_file)

# The bellow report code is copied and pasted from the previous exercise and works perfectly
# It prints the exact output as on the previous exercise

report['Total of patients loaded'] = len(patients)

# 2. Patients with invalid birth_date (list their full names)

report['List of patients with invalid birthdates'] = [
    build_full_name_from_patient(patient) for
    patient in patients if
    parse_birth_date(patient.get('birth_date', '')) is None]

# 3. Patients older than 60
today = date.today()
report['List of patients older than 60'] = []
for patient in patients:
    patient_birth_date = parse_birth_date(patient.get('birth_date', ''))
    if patient_birth_date is not None:
        # Compute the age of the patient. It takes into account whether the patient's birthday has passed or not.
        age = today.year - patient_birth_date.year - (
                (today.month, today.day) < (patient_birth_date.month, patient_birth_date.day))
        if age > 60:
            report['List of patients older than 60'].append(
                build_full_name_from_patient(patient))

# 4. Patient with the most conditions
max_condition_patient = max(patients, key=count_conditions, default=None)
if max_condition_patient is not None:
    report['Patient with the most conditions'] = f"{build_full_name_from_patient(max_condition_patient)}, which has {count_conditions(max_condition_patient)} condition(s)."

# Printing the report
print(json.dumps(report, indent=4))