# Exercise 07_report.py
#   from a JSON file of patients (reuse patients.json), using ONLY imports
#   from patient_utils, print a mini clinical report:
#     - Total patients loaded
#     - Patients with invalid birth_date (list their full names)
#     - Patients older than 60 (compute age from birth_date — careful!)
#     - Patient with the most conditions

import json
from patient_utils import build_full_name, count_conditions, parse_birth_date, build_full_name_from_patient
from datetime import date

report = {}

# 1. Loading the patient data
with open('files/patients.json') as json_file:
    patients = json.load(json_file)

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
