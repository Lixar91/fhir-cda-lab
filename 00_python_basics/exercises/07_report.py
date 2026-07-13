# Exercise 07_report.py
#   from a JSON file of patients (reuse patients.json), using ONLY imports
#   from patient_utils, print a mini clinical report:
#     - Total patients loaded
#     - Patients with invalid birth_date (list their full names)
#     - Patients older than 60 (compute age from birth_date — careful!)
#     - Patient with the most conditions

import json
from builtins import len

from patient_utils import *

report = {}

# 1. Loading the patient data
with open('files/patients.json') as json_file:
    patients = json.load(json_file)

report['Total of patients loaded'] = len(patients)

# 2. Patients with invalid birth_date (list their full names)

report['List of patients with invalid birthdates'] = [
    build_full_name(patient.get('given_name', 'Given name is not informed'),
                    patient.get('family_name', 'Family name is not informed')) for
    patient in patients if
    parse_birth_date(patient['birth_date']) is None]

# 3. Patients older than 60
today = date.today()
report['List of patients older than 60'] = []
for patient in patients:
    patient_birth_date = parse_birth_date(patient['birth_date'])
    if patient_birth_date is not None:
        # Compute the age of the patient. It takes into account whether the patient's birthday has passed or not.
        age = today.year - patient_birth_date.year - (
            1 if ((today.month, today.day) >= (patient_birth_date.month, patient_birth_date.day)) else 0)
        if age >= 60:
            report['List of patients older than 60'].append(
                build_full_name(patient.get('given_name', 'Given name is not informed'),
                                patient.get('family_name', 'Family name is not informed')))

del today

# 4. Patient with the most conditions
top_conditions = 0
for patient in patients:
    condition_length = len(patient.get('conditions', []))
    if condition_length > top_conditions:
        top_conditions = condition_length
        report[
            'Patient with the most conditions'] = f"{build_full_name(patient.get('given_name', 'Given name is not informed'), patient.get('family_name', 'Family name is not informed'))}, which has {condition_length} condition(s)."

# Printing the report
print(json.dumps(report, indent=4))
