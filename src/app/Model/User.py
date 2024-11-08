import sys
sys.path.append("src")

from psycopg import connect, DatabaseError
from logic import reverse_mortgage
from logic.reverse_mortgage import ReverseMortgageCalculator 
from app.Secret_Config import PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE
from app.Model.Mortgage import ReverseMortgage, ReverseMortgageCalculator
from logic.input_validator import InputValidator, DataTypeError, InvalidInterestRateError, InvalidMaritalStatusError, InvalidPropertyConditionError, InvalidPropertyValueError, ExcessivePropertyValueError 

class Usuario:
    def __init__(self, cedula, edad, estado_civil, valor_inmueble, condicion_inmueble, tasa_interes, edad_conyuge, sexo_conyuge):
        self.cedula = cedula
        self.edad = edad
        self.estado_civil = estado_civil
        self.valor_inmueble = valor_inmueble
        self.condicion_inmueble = condicion_inmueble
        self.tasa_interes = tasa_interes
        self.edad_conyuge= edad_conyuge
        self.sexo_conyuge= sexo_conyuge 

    @staticmethod
    def connect_db():
        """Establishes a connection to the NeonTech database."""
        try:
            return connect(
                host=PGHOST,
                port=PGPORT,
                user=PGUSER,
                password=PGPASSWORD,
                dbname=PGDATABASE
            )
        except DatabaseError as e:
            print(f"Error connecting to database: {e}")
            return None
        
    @staticmethod
    def Crear_Tabla():
        """Creates the Usuarios and Mortgage tables if they do not exist."""
        commands = [
            """
            CREATE TABLE IF NOT EXISTS Usuarios (
                cedula INT PRIMARY KEY,
                edad VARCHAR(2) NOT NULL,
                estado_civil TEXT NOT NULL,
                edad_conyuge VARCHAR(2),
                sexo_conyuge TEXT,
                valor_inmueble VARCHAR(20) NOT NULL,
                condicion_inmueble TEXT NOT NULL,
                tasa_interes VARCHAR(4) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Mortgage (
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES Usuarios(cedula) ON DELETE CASCADE,
                total_payment FLOAT NOT NULL
            )
            """
        ]
        
        conn = Usuario.connect_db()
        if conn:
            try:
                with conn.cursor() as cur:
                    for command in commands:
                        cur.execute(command)
                conn.commit()
                print("Tables created successfully.")
            except DatabaseError as e:
                print(f"Error creating tables: {e}")
            finally:
                conn.close()
        else:
            print("Failed to connect to the database.")

    def insertar_usuario(self):

        self.Crear_Tabla()
        """Inserts a Usuario record into the Usuarios table after validating inputs."""
        try:
            
            # Validar las entradas antes de continuar con la inserción
            input_validator = InputValidator(
                self.cedula, self.edad, self.estado_civil, self.edad_conyuge, self.sexo_conyuge,
                self.valor_inmueble, self.condicion_inmueble, self.tasa_interes
            )
            input_validator.validate_inputs()  # Llama al validador para comprobar la validez de los datos.

            # Si los datos son válidos, realiza la inserción en la base de datos
            conn = Usuario.connect_db()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        if self.estado_civil.lower() == "married" and self.edad_conyuge and self.sexo_conyuge:
                            cursor.execute(
                                """INSERT INTO Usuarios 
                                (cedula, edad, estado_civil, edad_conyuge, sexo_conyuge, valor_inmueble, condicion_inmueble, tasa_interes)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                                (self.cedula, self.edad, self.estado_civil, self.edad_conyuge, self.sexo_conyuge,
                                 self.valor_inmueble, self.condicion_inmueble, self.tasa_interes)
                            )
                        else:
                            cursor.execute(
                                """INSERT INTO Usuarios 
                                (cedula, edad, estado_civil, valor_inmueble, condicion_inmueble, tasa_interes)
                                VALUES (%s, %s, %s, %s, %s, %s)""",
                                (self.cedula, self.edad, self.estado_civil, self.valor_inmueble, self.condicion_inmueble, self.tasa_interes)
                            )

                    conn.commit()
                    print("Usuario insertado exitosamente.")
                except DatabaseError as e:
                    print(f"Error al insertar usuario: {e}")
                    conn.rollback()
                finally:
                    conn.close()

        except (DataTypeError, InvalidPropertyValueError, ExcessivePropertyValueError, InvalidInterestRateError, InvalidPropertyConditionError, InvalidMaritalStatusError) as e:
            print(f"Error de validación: {e}")
  
    def leer_usuario(cedula):
        """Obtiene los detalles del usuario desde la base de datos por cédula."""
        conn = Usuario.connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """SELECT * FROM Usuarios WHERE cedula = %s""", 
                        (cedula,)
                    )
                    usuario = cursor.fetchone()
                    if usuario:
                        return {
                            'cedula': usuario[0],
                            'edad': usuario[1],
                            'estado_civil': usuario[2],
                            'valor_inmueble': usuario[3],
                            'condicion_inmueble': usuario[4],
                            'tasa_interes': usuario[5],
                            'edad_conyuge': usuario[6],
                            'sexo_conyuge': usuario[7]
                        }
                    else:
                        return None
            except DatabaseError as e:
                print(f"Error al leer el usuario: {e}")
            finally:
                conn.close()

    def actualizar_usuario(self):
        """Actualiza los datos del usuario en la base de datos y recalcula la cuota de la hipoteca."""
        conn = Usuario.connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """UPDATE Usuarios SET edad = %s, estado_civil = %s, edad_conyuge = %s, 
                        sexo_conyuge = %s, valor_inmueble = %s, condicion_inmueble = %s, tasa_interes = %s
                        WHERE cedula = %s""",
                        (self.edad, self.estado_civil, self.edad_conyuge, self.sexo_conyuge,
                        self.valor_inmueble, self.condicion_inmueble, self.tasa_interes, self.cedula)
                    )
                    
                    conn.commit()  # Confirmar cambios
                    print("Usuario actualizado exitosamente.")
            except Exception as e:
                print(f"Error al actualizar el usuario: {e}")
                conn.rollback()  # Deshacer cambios si ocurre un error
            finally:
                conn.close()  # Cerramos la conexión


    @staticmethod
    def buscar_usuario(cedula):
        """Busca un usuario por su cédula y devuelve un objeto Usuario."""
        conn = Usuario.connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """SELECT * FROM Usuarios WHERE cedula = %s""",
                        (cedula,)
                    )
                    usuario_data = cursor.fetchone()  # Obtener los datos del usuario
                    if usuario_data:
                        # Crear un objeto Usuario con los datos obtenidos
                        usuario = Usuario(*usuario_data)  # Asegúrate de que esto coincida con el constructor
                        return usuario
                    else:
                        return None  # No se encontró el usuario
            except Exception as e:
                print(f"Error al leer el usuario: {e}")
                return None
            finally:
                conn.close()

    def eliminar_usuario(self):
        """Elimina un usuario de la base de datos y también elimina su registro en la tabla Mortgage."""
        conn = Usuario.connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    # Eliminar el registro en la tabla Mortgage
                    cursor.execute(
                        """DELETE FROM Mortgage WHERE user_id = %s""",
                        (self.cedula,)  # Usamos self.cedula porque es un método de instancia
                    )

                    # Eliminar el usuario de la tabla Usuarios
                    cursor.execute(
                        """DELETE FROM Usuarios WHERE cedula = %s""",
                        (self.cedula,)  # Usamos self.cedula porque es un método de instancia
                    )
                    conn.commit()  # Confirmamos los cambios
                    print("Usuario eliminado exitosamente.")
            except Exception as e:
                print(f"Error al eliminar el usuario: {e}")
                conn.rollback()  # Deshacer los cambios si ocurre un error
            finally:
                conn.close()  # Cerramos la conexión




