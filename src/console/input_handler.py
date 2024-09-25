# input_handler.py
import sys
sys.path.append("src")
from logic.input_validator import MIN_PROPERTY_VALUE, MAX_PROPERTY_VALUE, MIN_AGE_LIMIT, MIN_INTEREST_RATE, MAX_INTEREST_RATE

def get_input(prompt: str, expected_type: type = str, valid_values: list = None):
    """
    Generalized input function to handle different data types and validation.
    
    Args:
        prompt (str): The input prompt message.
        expected_type (type): The expected type of the input (e.g., int, float, str).
        valid_values (list): List of valid values for string inputs.
        
    Returns:
        The user input converted to the expected type.
    """
    while True:
        user_input = input(prompt).strip()
        
        if expected_type == float:
            # Check for invalid characters like commas
            if ',' in user_input:
                print(f"Error: Invalid characters found in input: '{user_input}'. Please use a decimal point instead of a comma.")
                continue
            
            try:
                value = float(user_input)
                
                # Custom validation based on the prompt
                if "interest rate" in prompt.lower():
                    if value <= MIN_INTEREST_RATE or value > MAX_INTEREST_RATE:
                        print(f"Error: Interest rate must be between {MIN_INTEREST_RATE} and {MAX_INTEREST_RATE}. You entered: {value}.")
                        continue
                
                return value
            except ValueError:
                print(f"Error: Invalid value entered: '{user_input}'. Expected a valid float.")
        
        elif expected_type == int:
            # Check for invalid characters like commas
            if ',' in user_input:
                print(f"Error: Invalid characters found in input: '{user_input}'. Please remove commas.")
                continue
            
            try:
                value = int(user_input)
                
                # Custom validation for integer inputs
                if "property value" in prompt.lower():
                    if value <= 0:
                        print(f"Error: Property value must be a positive number. You entered: {value}.")
                        continue
                    elif value < MIN_PROPERTY_VALUE or value > MAX_PROPERTY_VALUE:
                        print(f"Error: Property value must be between {MIN_PROPERTY_VALUE:,} and {MAX_PROPERTY_VALUE:,}. You entered: {value}.")
                        continue
                
                elif "age" in prompt.lower():
                    if value < MIN_AGE_LIMIT:
                        print(f"Error: Age must be at least {MIN_AGE_LIMIT}. You entered: {value}.")
                        continue
                
                return value
            except ValueError:
                print(f"Error: Invalid value entered: '{user_input}'. Expected a valid integer.")
        
        elif expected_type == str:
            value = user_input.lower()
            
            if valid_values and value not in valid_values:
                print(f"Error: Invalid value entered: '{value}'. Valid options are: {', '.join(valid_values)}.")
            else:
                return value
                
        else:
            print("Error: Unsupported expected_type provided.")
