
import sys
sys.path.append("src")

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.Model.User import Usuario
from app.Model.Mortgage import ReverseMortgage

# Blueprint for user-related routes
user_bp = Blueprint("user_bp", __name__)

@user_bp.route('/user', methods=['GET', 'POST'])
def create_user():
    
    if request.method == 'POST':
        data = request.form
        try:
            # Convertir y validar los datos
            cedula = int(data["cedula"])
            edad = int(data["edad"])
            estado_civil = data["estado_civil"].lower()
            edad_conyuge = int(data["edad_conyuge"]) if data.get("edad_conyuge") else None
            sexo_conyuge = data.get("sexo_conyuge")
            valor_inmueble = float(data["valor_inmueble"])
            condicion_inmueble = data["condicion_inmueble"].lower()
            tasa_interes = float(data["tasa_interes"])

            # Crear y guardar el usuario
            usuario = Usuario(
                cedula,
                edad,
                estado_civil,
                edad_conyuge,
                sexo_conyuge,
                valor_inmueble,
                condicion_inmueble,
                tasa_interes
            )
            usuario.insertar_usuario()
            
            # Insertar cálculo de hipoteca inversa
            reverse = ReverseMortgage(cedula,edad, estado_civil, edad_conyuge, sexo_conyuge,
                                 valor_inmueble, condicion_inmueble, tasa_interes)
                    
            reverse.insertar_reverse_mortgage()
            
            return jsonify({
                "message": "Usuario insertado exitosamente",
                "cedula": cedula,
                "estado": "completo"
            }), 201

        except ValueError as ve:
            return jsonify({"error": f"Error en la conversión de datos: {ve}"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    return render_template('user/create_user.html')


@user_bp.route('/user/<int:cedula>', methods=['GET'])
def get_user(cedula):
    # Llamar al método del modelo para obtener el usuario por cédula
    usuario = Usuario.leer_usuario(cedula)

    if usuario:
        # Si el usuario es encontrado, pasar los datos a la plantilla
        return render_template('user_details.html', user=usuario)
    else:
        # Si no se encuentra el usuario, redirigir con un mensaje de error
        flash("Usuario no encontrado", "error")
        return redirect(url_for('views_bp.user_details'))
    
def actualizar_usuario(self):
    """Actualiza los datos del usuario en la base de datos """
    conn = Usuario.connect_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                # Actualizar los datos del usuario
                cursor.execute(
                    """UPDATE Usuarios SET edad = %s, estado_civil = %s, edad_conyuge = %s, 
                    sexo_conyuge = %s, valor_inmueble = %s, condicion_inmueble = %s, tasa_interes = %s
                    WHERE cedula = %s""",
                    (self.edad, self.estado_civil, self.edad_conyuge, self.sexo_conyuge,
                     self.valor_inmueble, self.condicion_inmueble, self.tasa_interes, self.cedula)
                )
                
                conn.commit()  # Confirmar cambios
                print("Usuario actualizado exitosamente.")
        except:
            print(f"Error al actualizar el usuario")
            conn.rollback()  # Deshacer cambios si ocurre un error
        finally:
            conn.close()


def eliminar_usuario(self):
    """Elimina un usuario de la base de datos y también elimina su registro en la tabla Mortgage."""
    conn = Usuario.connect_db()
    if conn:
        try:
            with conn.cursor() as cursor:
                
                # Eliminar el usuario de la tabla Usuarios
                cursor.execute(
                    """DELETE FROM Usuarios WHERE cedula = %s""",
                    (self.cedula,)  # Usamos una tupla para evitar problemas con el formato
                )
                conn.commit()  # Confirmamos cambios
                print("Usuario eliminado exitosamente.")
        except Exception as e:
            print(f"Error al eliminar el usuario: {e}")
            conn.rollback()  # Deshacer los cambios si ocurre un error
        finally:
            conn.close()  # Cerramos la conexión a la base de datos
