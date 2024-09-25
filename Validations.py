import re
# Custom exceptions for specific validation error cases
class NegativeValue(Exception): 
    pass

class InvalidValue(Exception): 
    pass

class NotAnIntegerValue(Exception):
    pass

class CommaSeparator(Exception):
    pass

class MoreThan8HoursWorkedOnHoliday(Exception):
    pass

class ZeroWeeksWorked(Exception):
    pass

def validate_and_convert(entry, variable_name, should_be_integer=False):
    try:
        entry_str = str(entry)
        
        # Check if the entry contains a comma as a decimal separator
        if ',' in entry_str:
            raise CommaSeparator(f"ERROR: Invalid data in {variable_name}\n Use a period (.) as a decimal separator, not a comma (,).")

        # Convert to float to ensure it's numeric
        value = float(entry)

        # If it should be an integer, check that it has no decimals
        if should_be_integer and value != int(value):
            raise NotAnIntegerValue(f"ERROR: Invalid data in {variable_name}\n An integer value was expected.")

        # Check if it's negative
        if value < 0:
            raise NegativeValue(f"ERROR: Invalid data in {variable_name}\n Numbers cannot be negative.")

        # Return the correct type (integer or float)
        return int(value) if should_be_integer else value

    except ValueError:
        raise InvalidValue(f"ERROR: Invalid data in {variable_name}: Ensure it is a numeric value.\n not negative and without letters or special characters.")

def validate_variables(variables):
    for variable_name in variables:
        value = validate_and_convert(variables[variable_name][0],variable_name, variables[variable_name][1])
        variables[variable_name][0] = value
        
        
    # return converted_variables
    return variables
