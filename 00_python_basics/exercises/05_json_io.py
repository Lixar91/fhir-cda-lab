# Goal: read/write JSON files — the literal format of FHIR resources.
# Create a file "patients.json" by hand with this content, then process it.

# patients.json:
# [
#   {"given_name": "Nick", "family_name": "Doe", "birth_date": "1995-03-12", "conditions": ["hypertension"]},
#   {"given_name": "Ana", "family_name": "Smith", "birth_date": "not-a-date", "conditions": []},
#   {"given_name": "Luis", "family_name": "Garcia", "birth_date": "1958-11-01"}
# ]
# NOTE: patient 3 has NO "conditions" key on purpose.

import json

# 1. Load patients.json using json.load() (use a "with open(...)" block)

with open('files/patients.json') as json_file:
    patients = json.load(json_file)

# 2. For each patient, print "FAMILY, Given — N condition(s)"
#    -> reuse the .get() pattern from the review; patient 3 must print 0, not crash

for patient in patients:
    print(f"{patient['family_name'].upper()}, {patient['given_name'].title()} - {len(patient.get('conditions', []))}")

# 3. Write a new file "valid_patients.json" containing ONLY patients
#    whose birth_date parses correctly (reuse your strptime logic)

from datetime import datetime

valid_patients = []

for patient in patients:
    try:
        _ = datetime.strptime(patient.get('birth_date'), '%Y-%m-%d')
        valid_patients.append(patient)
    except ValueError:
        continue

with open('files/valid_patients.json', 'w') as json_file:
    json.dump(valid_patients, json_file)
