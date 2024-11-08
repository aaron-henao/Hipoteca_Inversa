import sys
sys.path.append("src")

from flask import Blueprint, request, jsonify
from app.Model.Mortgage import ReverseMortgage
from app.Model.User import Usuario  # Import the Usuario model
from logic import reverse_mortgage
from logic.reverse_mortgage import ReverseMortgageCalculator  # Import the ReverseMortgage model

# Blueprint for mortgage-related routes
mortgage_bp = Blueprint("mortgage_bp", __name__)

@mortgage_bp.route('/mortgage/<int:cedula>', methods=['POST'])
def create_or_update_mortgage(cedula):
    """Calculates and inserts/updates the mortgage payment in the database."""
    try:
        # Retrieve user data from the database using cedula
        usuario = Usuario(cedula=cedula)
        user_data = usuario.leer_usuario()  # Fetch user data
        
        if user_data:
            # Instantiate ReverseMortgage with user data
            reverse_mortgage = ReverseMortgageCalculator(
                cedula=cedula,
                edad=user_data["edad"],
                estado_civil=user_data["estado_civil"],
                valor_inmueble=user_data["valor_inmueble"],
                condicion_inmueble=user_data["condicion_inmueble"],
                tasa_interes=user_data["tasa_interes"],
                edad_conyugue=user_data.get("edad_conyugue"),
                sexo_conyugue=user_data.get("sexo_conyugue")
            )
            # Calculate and insert/update the mortgage record in the database
            ReverseMortgage.insertar_reverse_mortgage()
            
            return jsonify({"message": "Mortgage calculation completed successfully"}), 201
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@mortgage_bp.route('/mortgage/<int:cedula>', methods=['GET'])
def get_mortgage(cedula):
    """Retrieves the mortgage payment for a given user."""
    try:
        reverse_mortgage = ReverseMortgage(cedula=cedula)
        total_payment = reverse_mortgage.leer_mortgage()  # Fetch mortgage payment from database
        
        if total_payment is not None:
            return jsonify({"cedula": cedula, "monthly_payment": total_payment}), 200
        else:
            return jsonify({"error": "Mortgage not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
