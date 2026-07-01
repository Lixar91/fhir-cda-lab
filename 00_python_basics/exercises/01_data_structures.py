# Goal: refresh dict/list handling
# A patient as a dict. Print a clean summary line.

patient = {
    "given_name": "Nick",
    "family_name": "Doe",
    "birth_date": "1995-03-12",
    "conditions": ["hypertension", "type-2-diabetes"],
}

# 1. Print: "Doe, Nick (born 1995-03-12)"
# 2. Print the number of active conditions
# 3. Add a new condition "asthma" without overwriting the list

# Section 1

print(f"{patient['family_name']}, {patient['given_name']} (born {patient['birth_date']})")

# Section 2
print(f"The number of active conditions of the patient is {len(patient['conditions'])}")

# Section 3
print("The patient now has asthma. Let's add it to the active conditions")
patient["conditions"].append("asthma")

print(f"The number of active conditions of the patient is now {len(patient['conditions'])}. The new condition is {patient['conditions'][-1]}")
