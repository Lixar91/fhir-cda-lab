from datetime import datetime
# Goal: try/except — critical when parsing messy real-world clinical data.

raw_birth_dates = ["1995-03-12", "not-a-date", "1980-11-01", ""]

# For each value, try to split into [year, month, day].
# If it fails or is empty, print "Invalid date: <value>" and continue.
# The program must NOT crash. This is the mindset for parsing CDA/HL7.

date_format = '%Y-%m-%d'
result = []
for birth_date in raw_birth_dates:
    if type(birth_date) != str:
        raise ValueError('Parameter must be of type string')
    try:
        castedDate = datetime.strptime(birth_date, date_format)
        result.append([castedDate.year, castedDate.month, castedDate.day])
    except ValueError:
        result.append(f"Invalid date: '{birth_date}'")

print(result)