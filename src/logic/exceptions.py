# exceptions.py

class DataTypeError(Exception):
    """Exception raised for errors in data types."""
    pass

class InvalidPropertyValueError(Exception):
    """Exception raised for invalid property values (e.g., zero or negative)."""
    pass

class InvalidInterestRateError(Exception):
    """Exception raised for invalid interest rates."""
    pass

class InvalidPropertyConditionError(Exception):
    """Exception raised for invalid property conditions."""
    pass

class InvalidMaritalStatusError(Exception):
    """Exception raised for invalid marital status."""
    pass

class ExcessivePropertyValueError(Exception):
    """Exception raised for property values that exceed the acceptable limit."""
    pass

class LowPropertyValueError(Exception):
    """Exception raised for property values that fall below the acceptable limit."""
    pass

class InvalidInputError(Exception):
    """Custom exception for invalid inputs."""
    pass
