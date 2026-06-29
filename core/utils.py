import re
from .models import JobPost


def clean_salary(raw_salary_string):
    # Initialize your fallback variables as None or default strings
    min_salary = None
    max_salary = None
    currency = None
    salary_period = "monthly" 
    
    # Extract digits
    int_fetch = re.findall(r'\d[\d,]*', raw_salary_string)
    
    if int_fetch:
        if len(int_fetch) == 1:
            cleaned_num = int_fetch[0].replace(',', '')
            min_salary = max_salary = int(cleaned_num)
        elif len(int_fetch) >= 2:
            cleaned_num1 = int_fetch[0].replace(',', '')
            cleaned_num2 = int_fetch[1].replace(',', '')
            min_salary = int(cleaned_num1)
            max_salary = int(cleaned_num2)


    # Heuristic check
    if "$" in raw_salary_string:
        currency = "USD"
    elif "PHP" in raw_salary_string or "₱" in raw_salary_string or "?" in raw_salary_string:
        currency = "PHP"
    else:
        if min_salary and min_salary > 5000:
            currency = "PHP"
        elif min_salary and min_salary <= 5000:
            currency = "USD"
        else:
            currency = "UNKNOWN"

    # Period logic
    if "hr" in raw_salary_string or "hour" in raw_salary_string:
        salary_period = "hourly"

    # Return everything cleanly as a package
    return {
        "min_salary": min_salary,
        "max_salary": max_salary,
        "currency": currency,
        "salary_period": salary_period
    }

    






















