# Exercise: patient_utils.py
#   Move build_full_name, count_conditions and implement
#   parse_birth_date(value: str) -> date | None   (returns None if invalid)
# Objective: reuse functions in the exercise 07_report

from datetime import date, datetime

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
    if not isinstance(patient, dict):
        raise TypeError('Parameters must be of type dict')
    return len(patient.get("conditions", []))


def parse_birth_date(value: str) -> date | None:
    """
    :param value: String of the birthdate. Expected format is YYYY-MM-DD
    :return: Date time object of birthdate informed OR None if format is invalid
    """
    if not isinstance(value, str):
        raise TypeError("Parameter must be of type str")
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None