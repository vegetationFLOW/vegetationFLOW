from datetime import datetime

def checkDateRange(startYear: int, endYear: int) -> None:
    """
    Validates that the provided start and end years fall within the acceptable range.

    The acceptable range is between 2013 (inclusive) and the last complete calendar year 
    (current year - 1).

    Args:
        startYear (int): The starting year to validate.
        endYear (int): The ending year to validate.

    Raises:
        ValueError: If startYear is not between 2013 and the last complete year.
        ValueError: If endYear is not between startYear and the last complete year.
    """
    curr_year = datetime.today().year - 1  # Last complete calendar year

    if not (2013 <= startYear <= curr_year):
        raise ValueError(f"Invalid Start Year: must be between 2013 and {curr_year}")

    if not (startYear <= endYear <= curr_year):
        raise ValueError(f"Invalid End Year: must be between {startYear} and {curr_year}")