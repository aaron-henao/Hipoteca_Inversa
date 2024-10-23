import sys
sys.path.append("src")

from logic.reverse_mortgage import ReverseMortgageCalculator
from logic.input_validator import InputValidator
from logic.exceptions import (
    DataTypeError,
    InvalidPropertyValueError,
    ExcessivePropertyValueError,
    InvalidInterestRateError,
    InvalidPropertyConditionError,
    InvalidMaritalStatusError,
)

def main():
    print("=== Reverse Mortgage Calculator ===\n")
    try:
        # Property Value
        property_value_text = input(
            "Enter the property value (200,000,000 - 900,000,000): "
        ).strip()
        if not property_value_text:
            raise DataTypeError("Property value is required.")
        try:
            property_value = float(property_value_text)
        except ValueError:
            raise DataTypeError(f"Invalid property value: '{property_value_text}'. Expected a number.")

        # Property Condition
        property_condition = input(
            "Enter the property condition (excellent, good, average): "
        ).strip().lower()
        if not property_condition:
            raise InvalidPropertyConditionError("Property condition is required.")

        # Marital Status
        marital_status = input(
            "Enter your marital status (married, single, divorced): "
        ).strip().lower()
        if not marital_status:
            raise InvalidMaritalStatusError("Marital status is required.")

        # Owner's Age
        owner_age_text = input("Enter the owner's age: ").strip()
        if not owner_age_text:
            raise DataTypeError("Owner's age is required.")
        try:
            owner_age = int(owner_age_text)
        except ValueError:
            raise DataTypeError(f"Invalid owner's age: '{owner_age_text}'. Expected an integer.")

        # Spouse's Age 
        spouse_age = None
        if marital_status == 'married':
            spouse_age_text = input("Enter the spouse's age: ").strip()
            if not spouse_age_text:
                raise DataTypeError("Spouse's age is required for married status.")
            try:
                spouse_age = int(spouse_age_text)
            except ValueError:
                raise DataTypeError(f"Invalid spouse's age: '{spouse_age_text}'. Expected an integer.")

        # Interest Rate
        interest_rate_text = input(
            "Enter the interest rate (e.g., 0.05 for 5%): "
        ).strip()
        if not interest_rate_text:
            raise DataTypeError("Interest rate is required.")
        try:
            interest_rate = float(interest_rate_text)
        except ValueError:
            raise DataTypeError(f"Invalid interest rate: '{interest_rate_text}'. Expected a number.")

        # Validate the inputs
        validator = InputValidator(
            property_value=property_value,
            property_condition=property_condition,
            marital_status=marital_status,
            owner_age=owner_age,
            spouse_age=spouse_age,
            interest_rate=interest_rate,
        )
        validator.validate_inputs()

        # Calculate the monthly payment
        calculator = ReverseMortgageCalculator(
            property_value=property_value,
            property_condition=property_condition,
            marital_status=marital_status,
            owner_age=owner_age,
            spouse_age=spouse_age,
            interest_rate=interest_rate,
        )
        monthly_payment = calculator.calculate_monthly_payment()

        print(f"\nThe monthly reverse mortgage payment is: {monthly_payment}")

    except (
        DataTypeError,
        InvalidPropertyValueError,
        ExcessivePropertyValueError,
        InvalidInterestRateError,
        InvalidPropertyConditionError,
        InvalidMaritalStatusError,
    ) as e:
        print(f"\nError: {str(e)}")

if __name__ == '__main__':
    main()
