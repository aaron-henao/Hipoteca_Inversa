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
    def __init__(self, cedula, edad, estado_civil, edad_conyuge, sexo_conyuge, valor_inmueble, condicion_inmueble, tasa_interes):
        self.cedula = cedula
        self.edad = edad
        self.estado_civil = estado_civil
        self.valor_inmueble = valor_inmueble
        self.condicion_inmueble = condicion_inmueble
        self.tasa_interes = tasa_interes
        self.edad_conyuge= edad_conyuge
        self.sexo_conyugue= sexo_conyuge 

    def validate_inputs(self):
        try:
            assert isinstance(self.cedula, int), "Cédula debe ser un número entero"
            assert isinstance(self.edad, int) and self.edad > 0, "Edad debe ser un número positivo"
            assert self.estado_civil in ["single", "married", "divorced"], "Estado civil no válido"
            if self.estado_civil == "married":
                assert self.edad_conyuge is not None, "Edad del cónyuge es requerida si está casado"
                assert isinstance(self.edad_conyuge, int) and self.edad_conyuge > 0, "Edad del cónyuge debe ser un número positivo"
            assert isinstance(self.valor_inmueble, (int, float)) and self.valor_inmueble > 0, "Valor del inmueble debe ser un número positivo"
            assert isinstance(self.tasa_interes, (int, float)) and self.tasa_interes > 0, "Tasa de interés debe ser un número positivo"
            assert isinstance(self.condicion_inmueble, str), "Condición del inmueble debe ser un texto"
            
        except AssertionError as e:
            raise ValueError(f"Error en la validación: {str(e)}")
        
        if not isinstance(self.valor_inmueble, float):
            raise DataTypeError(f"Property value must be a number. You entered: {self.valor_inmueble}.")
        
        if not isinstance(self.edad, int) or (self.edad_conyuge is not None and not isinstance(self.edad_conyuge, int)):
            raise DataTypeError(f"Owner age must be an integer. You entered: owner age = {self.edad}, spouse age = {self.edad_conyuge}.")
        
        if not isinstance(self.tasa_interes, (int, float)):
            raise DataTypeError(f"Interest rate must be a number. You entered: {self.tasa_interes}.")
        
        if self.valor_inmueble <= 0:
            raise InvalidPropertyValueError(f"Property value must be a positive number. You entered: {self.valor_inmueble}.")
        
        if not (MIN_PROPERTY_VALUE <= self.valor_inmueble <= MAX_PROPERTY_VALUE):
            raise ExcessivePropertyValueError(f"Property value must be between {MIN_PROPERTY_VALUE} and {MAX_PROPERTY_VALUE}. You entered: {self.valor_inmueble}.")
        
        if self.edad_conyuge is not None:
            min_age = min(self.edad, self.edad_conyuge)
            if min_age > MAX_AGE:
                raise InvalidPropertyValueError(f"Owner and spouse age must not exceed {MAX_AGE}.")
            
            if self.edad < MIN_AGE_LIMIT or self.edad_conyuge < MIN_AGE_LIMIT:
                raise InvalidPropertyValueError(f"Owner and spouse must be at least {MIN_AGE_LIMIT} years old. You entered: owner age = {self.edad}, spouse age = {self.edad_conyuge}.")
        else:
            if self.edad > MAX_AGE:
                raise InvalidPropertyValueError(f"Owner age must not exceed {MAX_AGE}.")
            if self.edad < MIN_AGE_LIMIT:
                raise InvalidPropertyValueError(f"Owner must be at least {MIN_AGE_LIMIT} years old. You entered: owner age = {self.edad}.")
        
        if not (MIN_INTEREST_RATE < self.tasa_interes <= MAX_INTEREST_RATE):
            raise InvalidInterestRateError(f"Interest rate must be between {MIN_INTEREST_RATE} and {MAX_INTEREST_RATE}. You entered: {self.tasa_interes}.")
        
        valid_conditions = ["excellent", "good", "average"]
        if self.condicion_inmueble not in valid_conditions:
            raise InvalidPropertyConditionError(f"Invalid property condition: '{self.condicion_inmueble}'. Must be one of {', '.join(valid_conditions)}.")
        
        valid_marital_statuses = ["married", "single", "divorced"]
        if self.estado_civil not in valid_marital_statuses:
            raise InvalidMaritalStatusError(f"Invalid marital status: '{self.estado_civil}'. Must be one of {', '.join(valid_marital_statuses)}.")

