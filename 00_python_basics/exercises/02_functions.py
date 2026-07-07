# Goal: refresh functions, parameters, return values.
# Build a tiny helper you'll actually reuse later.

# Reviewer's note: It's better to use `isinstance` rather than `type`.
# Check https://switowski.com/blog/type-vs-isinstance for more info

def build_full_name(given: str, family: str) -> str:
    """
    :param given: Given name of the patient
    :param family: Family of the patient
    :return: 'FAMILY, Given' format used in many clinical systems.
    """
    if not isinstance(given, str) or not isinstance(family, str):
        raise TypeError("Parameters must be of type str")
    return f"{family.upper()}, {given.title()}"

def count_conditions(patient: dict) -> int:
    """
    :param patient: Dictionary of patient conditions (patient dictionary from exercise 01)
    :return: Number of conditions a patient dict has (0 if none).
    """
    if type(patient) != dict:
        raise ValueError('Parameters must be of type dict')
    return len(patient.get("conditions", []))

patient = {
    "given_name": "Nick",
    "family_name": "Doe",
    "birth_date": "1995-03-12",
    "conditions": ["hypertension", "type-2-diabetes"],
}
print(count_conditions(patient))
print(build_full_name("hola", "mundo"))