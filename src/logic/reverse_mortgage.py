# reverse_mortgage.py
import sys
sys.path.append("src")
from logic.input_validator import InputValidator, MIN_PROPERTY_VALUE, MAX_PROPERTY_VALUE, MAX_AGE, MIN_AGE_LIMIT, MIN_INTEREST_RATE, MAX_INTEREST_RATE
from logic.exceptions import (
    DataTypeError,
    InvalidPropertyValueError,
    ExcessivePropertyValueError,
    InvalidInterestRateError,
    InvalidPropertyConditionError,
    InvalidMaritalStatusError
)

class ReverseMortgageCalculator:
    #constants
    AGE_THRESHOLD_1 = 70
    AGE_THRESHOLD_2 = 65
    LIFE_EXPECTANCY_1 = 15
    LIFE_EXPECTANCY_2 = 20
    LIFE_EXPECTANCY_DEFAULT = 25

    def __init__(self, cedula, edad, estado_civil, valor_inmueble, condicion_inmueble, tasa_interes, edad_conyuge, sexo_conyuge):
        """
        Initialize the reverse mortgage calculator with the necessary parameters.
        
        Args:
            property_value (int or float): The value of the property.
            property_condition (str): The condition of the property.
            marital_status (str): The marital status of the owner.
            owner_age (int): The age of the owner.
            spouse_age (int, optional): The age of the spouse. Defaults to None.
            interest_rate (float): The interest rate of the mortgage. Defaults to 0.05.
        """
        self.cedula = cedula
        self.edad = edad
        self.estado_civil = estado_civil
        self.valor_inmueble = valor_inmueble 
        self.condicion_inmueble = condicion_inmueble
        self.tasa_interes = tasa_interes
        self.edad_conyuge = edad_conyuge
        self.sexo_conyuge = sexo_conyuge
        
        # Validate inputs
        self.validate_inputs()

    def validate_inputs(self):
        """
        Validate the inputs provided to the reverse mortgage calculator.
        
        Raises:
            DataTypeError: If any input has an incorrect data type.
            InvalidPropertyValueError: If the property value is invalid.
            ExcessivePropertyValueError: If the property value exceeds the acceptable limit.
            InvalidInterestRateError: If the interest rate is invalid.
            InvalidPropertyConditionError: If the property condition is invalid.
            InvalidMaritalStatusError: If the marital status is invalid.
        """
        validator = InputValidator(
            self.cedula,
            self.edad,
            self.estado_civil,
            self.valor_inmueble, 
            self.condicion_inmueble,
            self.tasa_interes,
            self.edad_conyuge,
            self.sexo_conyuge,
        )
        
        validator.validate_inputs()

    def get_life_expectancy(self, edad):
        """
        Return life expectancy based on age.
        
        Args:
            age (int): The age of the person.
        
        Returns:
            int: Estimated life expectancy in years.
        """
        if edad >= self.AGE_THRESHOLD_1:
            return self.LIFE_EXPECTANCY_1
        elif edad >= self.AGE_THRESHOLD_2:
            return self.LIFE_EXPECTANCY_2
        else:
            return self.LIFE_EXPECTANCY_DEFAULT

    def calculate_monthly_payment(self):
        """
        Calculate the monthly reverse mortgage payment.
        
        Returns:
            float: The calculated monthly mortgage payment.
        """
        # Adjust property value based on condition
        condition_adjustment = {"excellent": 1, "good": 0.9, "average": 0.8}
        adjusted_value = self.valor_inmueble * condition_adjustment[self.condicion_inmueble]

        # Calculate life expectancy
        if self.edad_conyuge is not None:
            youngest_age = min(self.edad, self.edad_conyuge)
        else:
            youngest_age = self.edad

        life_expectancy_years = self.get_life_expectancy(youngest_age)
        life_expectancy_months = life_expectancy_years * 12

        # Calculate mortgage payment
        loan_percentage = 0.50 #This value depends on the entity, this value is determined by the entity, the entity can change the value, so it can increase or go up.
        mortgage_amount = adjusted_value * loan_percentage
        monthly_interest_rate = (1 + self.tasa_interes) ** (1/12) - 1
        monthly_payment = mortgage_amount * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -life_expectancy_months)

        total_payment = monthly_payment * life_expectancy_months
        if total_payment > mortgage_amount:
            monthly_payment = mortgage_amount / life_expectancy_months

        return round(monthly_payment, 2)







