# input_validator.py
import sys
sys.path.append("src")
from logic.exceptions import DataTypeError, InvalidPropertyValueError, ExcessivePropertyValueError, InvalidInterestRateError, InvalidPropertyConditionError, InvalidMaritalStatusError

# Define constants
MIN_PROPERTY_VALUE = 200_000_000
MAX_PROPERTY_VALUE = 900_000_000
MAX_AGE = 85
MIN_AGE_LIMIT = 18
MIN_INTEREST_RATE = 0
MAX_INTEREST_RATE = 1

class InputValidator:
    def __init__(self, property_value, property_condition, marital_status, owner_age, spouse_age, interest_rate):
        self.property_value = property_value
        self.property_condition = property_condition
        self.marital_status = marital_status
        self.owner_age = owner_age
        self.spouse_age = spouse_age
        self.interest_rate = interest_rate

    def validate_inputs(self):
        if not isinstance(self.property_value, (int, float)):
            raise DataTypeError(f"Property value must be a number. You entered: {self.property_value}.")
        
        if not isinstance(self.owner_age, int) or (self.spouse_age is not None and not isinstance(self.spouse_age, int)):
            raise DataTypeError(f"Owner age must be an integer. You entered: owner age = {self.owner_age}, spouse age = {self.spouse_age}.")
        
        if not isinstance(self.interest_rate, (int, float)):
            raise DataTypeError(f"Interest rate must be a number. You entered: {self.interest_rate}.")
        
        if self.property_value <= 0:
            raise InvalidPropertyValueError(f"Property value must be a positive number. You entered: {self.property_value}.")
        
        if not (MIN_PROPERTY_VALUE <= self.property_value <= MAX_PROPERTY_VALUE):
            raise ExcessivePropertyValueError(f"Property value must be between {MIN_PROPERTY_VALUE} and {MAX_PROPERTY_VALUE}. You entered: {self.property_value}.")
        
        if self.spouse_age is not None:
            min_age = min(self.owner_age, self.spouse_age)
            if min_age > MAX_AGE:
                raise InvalidPropertyValueError(f"Owner and spouse age must not exceed {MAX_AGE}.")
            
            if self.owner_age < MIN_AGE_LIMIT or self.spouse_age < MIN_AGE_LIMIT:
                raise InvalidPropertyValueError(f"Owner and spouse must be at least {MIN_AGE_LIMIT} years old. You entered: owner age = {self.owner_age}, spouse age = {self.spouse_age}.")
        else:
            if self.owner_age > MAX_AGE:
                raise InvalidPropertyValueError(f"Owner age must not exceed {MAX_AGE}.")
            if self.owner_age < MIN_AGE_LIMIT:
                raise InvalidPropertyValueError(f"Owner must be at least {MIN_AGE_LIMIT} years old. You entered: owner age = {self.owner_age}.")
        
        if not (MIN_INTEREST_RATE < self.interest_rate <= MAX_INTEREST_RATE):
            raise InvalidInterestRateError(f"Interest rate must be between {MIN_INTEREST_RATE} and {MAX_INTEREST_RATE}. You entered: {self.interest_rate}.")
        
        valid_conditions = ["excellent", "good", "average"]
        if self.property_condition not in valid_conditions:
            raise InvalidPropertyConditionError(f"Invalid property condition: '{self.property_condition}'. Must be one of {', '.join(valid_conditions)}.")
        
        valid_marital_statuses = ["married", "single", "divorced"]
        if self.marital_status not in valid_marital_statuses:
            raise InvalidMaritalStatusError(f"Invalid marital status: '{self.marital_status}'. Must be one of {', '.join(valid_marital_statuses)}.")

