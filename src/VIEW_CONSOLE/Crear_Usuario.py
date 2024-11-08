import sys
sys.path.append("src")

# Import the mortgage calculation and user control modules
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
from CONTROLLER.Controlador_Usuarios import Controlador_Usuarios
from MODEL.Usuario import Usuario

def get_user_data():
    """Collects and validates user data for reverse mortgage calculation."""
    # Collect general details
    cedula = int(input("Por favor ingrese su cedula: "))
    age = int(input("Enter the owner's age:  (62 - 84): ")) 
    marital_status = input("Enter your marital status (married, single, divorced): ").strip().lower()
    
    # Conditionally get spouse details
    spouse_age, spouse_gender = None, None

    if marital_status == "married":
        spouse_gender = input("Enter your spouse's gender (male, female): ").strip().lower()
        try:
            spouse_age = int(input("Enter the spouse's age: "))
        except ValueError:
            print("Invalid input for spouse's age. Please enter a valid integer.")

        
    
    property_value = float(input("Enter the property value (200,000,000 - 900,000,000): "))
    property_condition = input("Enter the property condition (excellent, good, average): ")
    interest_rate = float(input("Enter the interest rate (e.g., 0.05 for 5%): "))

    return cedula, age, marital_status, spouse_age, spouse_gender, property_value, property_condition, interest_rate

def main():
    print("=== BIENVENIDO AL SISTEMA DE HIPOTECA INVERSA ===\n")

    Controlador_Usuarios.Crear_Tabla()

    try:
        cedula, age, marital_status, spouse_age, spouse_gender, property_value, property_condition, interest_rate = get_user_data()
        
        validator = InputValidator(
            cedula=cedula,
            age = age,
            property_value=property_value,
            property_condition=property_condition,
            marital_status=marital_status,
            spouse_age=spouse_age,
            spouse_gender = spouse_gender,
            interest_rate=interest_rate 
        )

        validator.validate_inputs()


        # Save user data in the database
        usuario = Usuario(
            cedula=cedula,
            edad=age,
            estado_civil=marital_status.title(),
            edad_conyugue=spouse_age,
            sexo_conyugue=spouse_gender,
            valor_inmueble=property_value,
            condicion_inmueble = property_condition,
            tasa_interes=interest_rate,
        )
        Controlador_Usuarios.Insertar_Usuario(usuario)
        print("\nUsuario registrado exitosamente en la base de datos.")

        # Calculate reverse mortgage payment
        calculator = ReverseMortgageCalculator(
            cedula=cedula,
            age = age,
            property_value=property_value,
            property_condition=property_condition,
            marital_status=marital_status,
            spouse_age=spouse_age,
            spouse_gender = spouse_gender,
            interest_rate=interest_rate
        )
        monthly_payment = calculator.calculate_monthly_payment()
        print(f"\nEl pago mensual estimado de la hipoteca inversa es: {monthly_payment}")

    except (
        DataTypeError,
        InvalidPropertyValueError,
        ExcessivePropertyValueError,
        InvalidInterestRateError,
        InvalidPropertyConditionError,
        InvalidMaritalStatusError,
    ) as e:
        print(f"\nError: {str(e)}")

    except ValueError as exc:
        print(f"\nError de valor: {str(exc)}. Inténtelo de nuevo.")
        
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {str(e)}. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()