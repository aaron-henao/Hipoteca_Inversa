import sys
sys.path.append("src")

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.Controller.User_controller import Usuario
from app.Model.User import Usuario
from app.Model.Mortgage import ReverseMortgage
from logic.input_validator import InputValidator

views_bp = Blueprint('views_bp', __name__)

@views_bp.route('/user_form', methods=['GET', 'POST'])
def user_form():
    # Si el formulario es enviado con un POST
    if request.method == 'POST':
        try:
            # Captura y convierte los datos del formulario
            cedula = int(request.form.get('cedula'))
            edad = int(request.form.get('edad'))
            estado_civil = request.form.get('estado_civil')
            
            # Solo intenta convertir edad_conyuge si estado_civil es "married"
            edad_conyuge = None
            if estado_civil == 'married':
                edad_conyuge = request.form.get('edad_conyuge')
                if edad_conyuge:
                    edad_conyuge = int(edad_conyuge)
                else:
                    raise ValueError("Edad del cónyuge debe ser un número positivo si está casado")

            sexo_conyuge = request.form.get('sexo_conyuge')
            valor_inmueble = float(request.form.get('valor_inmueble'))
    
            # En la función user_form
            condicion_inmueble = str(request.form.get('condicion_inmueble', '')).strip().lower()

            tasa_interes = float(request.form.get('tasa_interes'))

            # Validación de entradas
            input_validator = InputValidator(
                cedula, edad, estado_civil, edad_conyuge, sexo_conyuge,
                valor_inmueble, condicion_inmueble, tasa_interes
            )
            input_validator.validate_inputs()

            # Creación y guardado del usuario si la validación es exitosa
            usuario = Usuario(
                cedula=cedula,
                edad=edad,
                estado_civil=estado_civil,
                edad_conyuge=edad_conyuge,
                sexo_conyuge=sexo_conyuge,
                valor_inmueble=valor_inmueble,
                condicion_inmueble=condicion_inmueble,
                tasa_interes=tasa_interes
            )
            usuario.insertar_usuario()

            # Registro de la hipoteca
            

            flash("Usuario registrado exitosamente.", "success")
            return redirect(url_for('views_bp.user_form'))

        except ValueError as e:
            # Si ocurre un error, devuelve el mensaje de error y los datos ingresados previamente
            flash(f"Error en los datos ingresados: {str(e)}", "error")
            return render_template('user_form.html', cedula=cedula, edad=edad, estado_civil=estado_civil,
                                   edad_conyuge=edad_conyuge, sexo_conyuge=sexo_conyuge, 
                                   valor_inmueble=valor_inmueble, condicion_inmueble=condicion_inmueble, 
                                   tasa_interes=tasa_interes)
    
    # Si el método es GET, solo se renderiza el formulario sin datos previos
    return render_template('user_form.html', cedula=None, edad=None, estado_civil=None,
                           edad_conyuge=None, sexo_conyuge=None, valor_inmueble=None, 
                           condicion_inmueble=None, tasa_interes=None)

@views_bp.route('/user_details_search', methods=['GET', 'POST'])
def user_details():
    if request.method == 'POST':
        # Obtener la cédula desde el formulario
        cedula = request.form.get('cedula')

        # Llamar a la función del modelo para leer los datos del usuario
        usuario = Usuario.leer_usuario(cedula)

        if usuario:
            # Si se encuentra el usuario, pasarlo a la vista
            return render_template('user_details.html', user=usuario)
        else:
            # Si no se encuentra el usuario, mostrar un mensaje de error
            flash("Usuario no encontrado.", "error")
            return redirect(url_for('views_bp.user_details'))
    
    # Si la solicitud es GET, mostrar el formulario de búsqueda
    return render_template('user_details_search.html')


@views_bp.route('/search_user', methods=['GET', 'POST'])
def search_user():
    if request.method == 'POST':
        cedula = request.form.get('cedula')
        usuario = Usuario.leer_usuario(cedula)  # Verifica si el usuario existe por cédula
        if usuario:
            return render_template('user_delete.html', user=usuario)
        else:
            flash("Usuario no encontrado.", "error")
            return redirect(url_for('views_bp.search_user'))

    return render_template('search_user.html')

@views_bp.route('/update_user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        # Obtener la cédula desde el formulario
        cedula = int(request.form['cedula'])
        usuario = Usuario.buscar_usuario(cedula)  # Obtiene el usuario por cédula

        if not usuario:
            flash("Usuario no encontrado.", "error")
            return redirect(url_for('views_bp.search_user'))

        try:
            # Asignar nuevos valores desde el formulario
            usuario.edad = int(request.form['edad'])
            usuario.estado_civil = request.form['estado_civil']
            usuario.edad_conyuge = int(request.form['edad_conyuge']) if request.form['edad_conyuge'] else None
            usuario.sexo_conyuge = request.form['sexo_conyuge']
            usuario.valor_inmueble = float(request.form['valor_inmueble'])
            usuario.condicion_inmueble = request.form['condicion_inmueble']
            usuario.tasa_interes = float(request.form['tasa_interes'])

            # Llamar a la función de actualización
            usuario.actualizar_usuario()

            flash("Usuario actualizado exitosamente.", "success")
            return redirect(url_for('views_bp.user_details_search'))  # Redirigir al listado o detalle

        except Exception as e:
            flash(f"Error al actualizar los datos: {str(e)}", "error")
            return redirect(url_for('views_bp.update_user'))  # Redirigir a la página de actualización

    else:
        # GET: Si el método es GET, es decir, cuando se accede al formulario para actualizar
        cedula = request.args.get('cedula')  # Obtener cédula desde la URL o formulario
        if cedula:
            usuario = Usuario.buscar_usuario(int(cedula))  # Obtener los datos del usuario por cédula
            if not usuario:
                flash("Usuario no encontrado.", "error")
                return redirect(url_for('views_bp.search_user'))  # Redirigir si no se encuentra
            return render_template('update_user.html', user=usuario)  # Pasar el usuario a la plantilla
        else:
            flash("Debe proporcionar una cédula válida.", "error")
            return redirect(url_for('views_bp.search_user'))  # Redirigir a la búsqueda si no se pasa cédula





@views_bp.route('/delete_user/<int:cedula>', methods=['POST'])
def delete_user(cedula):
    try:
        # Crear una instancia del objeto Usuario usando la cédula
        usuario = Usuario.buscar_usuario(cedula)  # Esto debe devolver un objeto Usuario

        if usuario:  # Si el usuario existe
            # Llamar al método de eliminación sobre el objeto usuario
            usuario.eliminar_usuario()  # Aquí no pasamos la cédula, porque estamos trabajando con el objeto usuario
            flash("Usuario eliminado exitosamente.", "success")
        else:
            flash("Usuario no encontrado.", "error")

        return redirect(url_for('views_bp.search_user'))  # Redirigir después de eliminar

    except Exception as e:
        flash(f"Error al eliminar el usuario: {str(e)}", "error")
        return redirect(url_for('views_bp.search_user'))  # Redirigir si hay error al eliminar


