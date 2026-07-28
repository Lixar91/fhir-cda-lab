# Goal: XML in -> the SAME list-of-dicts you already know -> your existing toolbox.
# This is interoperability in miniature: same information, two wire formats,
# one internal model.
import json
from lxml import etree
from patient_utils import build_full_name, count_conditions, parse_birth_date, build_full_name_from_patient
from datetime import date

# 1. Write extract_patients(xml_path: str) -> list[dict]
#    Each dict must have the EXACT same shape as patients.json:
#    {"given_name": ..., "family_name": ..., "birth_date": ..., "conditions": [...]}
#    -> missing <conditions> must yield [], not crash
# 2. Reuse patient_utils (explicit imports!) to print the SAME mini report
#    from Exercise 7, but fed from XML. Zero changes to patient_utils allowed.
#    If you need to touch the toolbox, your extraction layer is leaking.
# 3. Bonus (only if energy allows): dump the extracted list to
#    files/patients_from_xml.json and diff it against patients.json. Identical?

def extract_patients(xml_path: str) -> list[dict]:
    """
    Transforms a patient XML file into a list of dictionaries.
    :param xml_path: File path of XML file.
    :return: List of dictionaries of the patients.
    :raises FileNotFoundError: File does not exist or cannot be opened.
    :raises etree.XMLSyntaxError: XML syntax error is detected while parsing.
    """
    if not isinstance(xml_path, str):
        raise TypeError('Parameter must be of type str')
    try:
        xml_file = etree.parse(xml_path)
        xml_root = xml_file.getroot()
        result = []
        for patient in xml_root.findall("patient"):
            # Extract name of the patient
            p_given = patient.find("name").get("given") if patient.find("name") is not None else None
            p_family = patient.find("name").get("family") if patient.find("name") is not None else None

            # Birthdate of the patient
            p_birthdate = patient.find("birthDate").get("value") if patient.find("birthDate") is not None else None

            # Conditions of the patient
            p_conditions = patient.findall("conditions/condition")
            condition_list = [condition.get("display") for condition in p_conditions]
            condition_list = list(filter(None, condition_list))

            # Build patient json
            json_patient = {"given_name": p_given,
                            "family_name": p_family,
                            "birth_date": p_birthdate,
                            "conditions": condition_list
                            }

            # Remove None key-value pairs and return dict
            result.append({k: v for k, v in json_patient.items() if v is not None})
        return result

    except FileExistsError:
        raise FileNotFoundError('XML file does not exist or cannot be opened.')
    except etree.XMLSyntaxError:
        raise ValueError('XML syntax error')

################################

# Report generation

################################

report = {}

# 1. Loading the patient data
patients = extract_patients("files/patients.xml")

# 1.1 Save the xml converted json into a file to diff it later
with open('files/patients_from_xml.json', 'w') as json_file:
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
# Using a traditional implementation
# top_conditions = 0
# for patient in patients:
#     # Use function built from patient_utils
#     condition_length = count_conditions(patient)
#     if condition_length > top_conditions:
#         top_conditions = condition_length
#         report[
#             'Patient with the most conditions'] = f"{build_full_name_from_patient(patient)}, which has {condition_length} condition(s)."
# The Pythonic way. It has C performance!
max_condition_patient = max(patients, key=count_conditions, default=None)
report[
    'Patient with the most conditions'] = f"{build_full_name(max_condition_patient.get('given_name', 'Given name is not informed'), max_condition_patient.get('family_name', 'Family name is not informed'))}, which has {count_conditions(max_condition_patient)} condition(s)."

# Printing the report
print(json.dumps(report, indent=4))
