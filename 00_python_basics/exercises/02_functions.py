# Goal: refresh functions, parameters, return values.
# Build a tiny helper you'll actually reuse later.

def build_full_name(given: str, family: str) -> str:
    """
    :param given: Given name of the patient
    :param family: Family of the patient
    :return: 'FAMILY, Given' format used in many clinical systems.
    """
    if type(given) != str or type(family) != str:
        raise ValueError('Parameters must be of type str')
    return f"{family.upper()}, {given.title()}"

def count_conditions(patient: dict) -> int:
    """
    :param patient: Dictionary of patient conditions
    :return: Number of conditions a patient dict has (0 if none).
    """
    if type(patient) != dict:
        raise ValueError('Parameters must be of type dict')
    return len(patient.keys())

print(count_conditions({"hola": "mundo", "holigwi": 1}))
print(build_full_name("hola", "mundo"))