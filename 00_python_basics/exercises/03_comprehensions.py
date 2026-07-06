# Goal: list/dict comprehensions — you'll use these constantly when
# mapping CDA sections to FHIR resources later.

patients = [
    {"name": "Doe", "age": 31},
    {"name": "Smith", "age": 67},
    {"name": "Garcia", "age": 54},
]

# 1. Build a list with only the names -> ["Doe", "Smith", "Garcia"]
patient_names = [patient["name"] for patient in patients]
print(patient_names)
# 2. Build a list of names of patients older than 60
elder_patients = [patient["name"] for patient in patients if patient["age"] > 60]
print(elder_patients)
# 3. Build a dict {name: age} from the list
name_dictionary = {}
for patient in patients:
    name_dictionary[patient["name"]] = patient["age"]
# name_dictionary = {name:age for name, age in patients}
print(name_dictionary)