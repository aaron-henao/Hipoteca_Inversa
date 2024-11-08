import sys
sys.path.append("src")

import psycopg
from psycopg import connect, OperationalError, DatabaseError

from app.Secret_Config import PGDATABASE, PGHOST, PGPASSWORD, PGPORT, PGUSER
from MODEL.Usuario import Usuario

# CONSTANTS
ESPERANZA_VIDA_HOMBRES = 84
ESPERANZA_VIDA_MUJERES = 86
EDAD_MINIMA = 62
VALOR_MINIMO_INMUEBLE = 10000000
INTERES_MINIMO = 0
INTERES_MAXIMO = 1

# EXCEPTIONS
class Usuario_No_Actualizado_Exception(Exception):
    def __init__(self):
        super().__init__("El usuario no se pudo actualizar")

class Usuario_No_Insertado_Exception(Exception):
    def __init__(self):
        super().__init__("El usuario no se pudo insertar")

class Usuario_No_Eliminado_Exception(Exception):
    def __init__(self):
        super().__init__("El usuario no se pudo eliminar")

class Edad_Exception(Exception):
    def __init__(self, edad):
        super().__init__(f"La edad {edad} es inválida; debe estar entre {EDAD_MINIMA} y {ESPERANZA_VIDA_HOMBRES}")

class None_Exception(Exception):
    def __init__(self):
        super().__init__("No pueden haber campos vacíos")

class Valor_Inmueble_Exception(Exception):
    def __init__(self):
        super().__init__("El valor del inmueble está por debajo del mínimo permitido")

class Tasa_Exception(Exception):
    def __init__(self, interes):
        super().__init__(f"La tasa de interés {interes} es inválida; debe estar entre {INTERES_MINIMO} y {INTERES_MAXIMO}")

class Controlador_Usuarios:

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
        except OperationalError as e:
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
                edad_conyugue VARCHAR(2),
                sexo_conyugue TEXT,
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
        
        conn = Controlador_Usuarios.connect_db()
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

    @staticmethod
    def Limpiar_Tablas():
        """Clears all records from both Usuarios and Mortgage tables."""
        conn = Controlador_Usuarios.connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM Mortgage")
                    cursor.execute("DELETE FROM Usuarios")
                conn.commit()
                print("All records deleted from Usuarios and Mortgage tables.")
            except DatabaseError as e:
                print(f"Error clearing tables: {e}")
                conn.rollback()
            finally:
                conn.close()
        else:
            print("No se pudo establecer conexión con la base de datos.")

    @staticmethod
    def Insertar_Usuario(usuario: Usuario):
        """Inserts a Usuario record into the Usuarios table."""
        conn = Controlador_Usuarios.connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    # Check if spouse data should be included
                    if usuario.estado_civil.lower() == "married" and usuario.edad_conyugue is not None and usuario.sexo_conyugue is not None:
                        cursor.execute(
                            """INSERT INTO Usuarios 
                            (cedula, edad, estado_civil, edad_conyugue, sexo_conyugue, valor_inmueble, condicion_inmueble, tasa_interes)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                            (usuario.cedula, usuario.edad, usuario.estado_civil,
                            usuario.edad_conyugue, usuario.sexo_conyugue,
                            usuario.valor_inmueble, usuario.condicion_inmueble, usuario.tasa_interes)
                        )
                    else:
                        cursor.execute(
                            """INSERT INTO Usuarios 
                            (cedula, edad, estado_civil, valor_inmueble, condicion_inmueble, tasa_interes)
                            VALUES (%s, %s, %s, %s, %s, %s)""",
                            (usuario.cedula, usuario.edad, usuario.estado_civil,
                            usuario.valor_inmueble, usuario.condicion_inmueble, usuario.tasa_interes)
                        )
                conn.commit()
                print("Usuario insertado exitosamente.")
            except DatabaseError as e:
                print(f"Error al insertar usuario: {e}")
                conn.rollback()
            finally:
                conn.close()
        else:
            print("No se pudo establecer conexión con la base de datos.")

    def Buscar_Usuario(cedula_buscada):
        """ 
        Trae un usuario de la tabla Usuarios por la cédula 
        """
        conn = Controlador_Usuarios.connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """SELECT cedula, edad, estado_civil, edad_conyugue, 
                                sexo_conyugue, valor_inmueble, tasa_interes 
                        FROM Usuarios WHERE cedula = %s""", (cedula_buscada,)
                    )
                    fila = cursor.fetchone()
                    if fila:
                        resultado = Usuario(
                            cedula=fila[0], edad=fila[1], estado_civil=fila[2],
                            edad_conyugue=fila[3], sexo_conyugue=fila[4], 
                            valor_inmueble=fila[5], tasa_interes=fila[6]
                        )
                        print(resultado)
                        return resultado
                    else:
                        print("Usuario no encontrado.")
                        return None
            except DatabaseError as e:
                print(f"Error al buscar usuario: {e}")
            finally:
                conn.close()
        else:
            print("No se pudo establecer conexión con la base de datos.")
    
    def Eliminar_Usuario(cedula_buscada):
        """ 
        Elimina un usuario de la tabla Usuarios por su cédula 
        """
        conn = Controlador_Usuarios.connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM Usuarios WHERE cedula = %s", (cedula_buscada,))
                conn.commit()
                print("USUARIO ELIMINADO CORRECTAMENTE")
            except DatabaseError as e:
                print(f"Error al eliminar usuario: {e}")
                conn.rollback()
            finally:
                conn.close()
        else:
            print("No se pudo establecer conexión con la base de datos.")
             
         

    def Actualizar_Usuario(cedula_buscada, datos_actualizar: Usuario):
        """ 
        Actualiza los valores de un usuario en la tabla Usuarios por su cédula 
        """
        conn = Controlador_Usuarios.connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    # Actualiza cada campo según su disponibilidad
                    if datos_actualizar.cedula:
                        cursor.execute(
                            "UPDATE Usuarios SET cedula = %s WHERE cedula = %s", 
                            (datos_actualizar.cedula, cedula_buscada)
                        )
                        conn.commit()
                        print("CEDULA ACTUALIZADA CORRECTAMENTE")

                    elif datos_actualizar.estado_civil:
                        # Verifica el estado civil y actualiza los campos según corresponda
                        if datos_actualizar.estado_civil.title() == "Casado":
                            cursor.execute(
                                "UPDATE Usuarios SET estado_civil = %s WHERE cedula = %s", 
                                (datos_actualizar.estado_civil, cedula_buscada)
                            )
                            if datos_actualizar.edad_conyugue and datos_actualizar.sexo_conyugue:
                                cursor.execute(
                                    "UPDATE Usuarios SET edad_conyugue = %s, sexo_conyugue = %s WHERE cedula = %s", 
                                    (datos_actualizar.edad_conyugue, datos_actualizar.sexo_conyugue, cedula_buscada)
                                )
                        else:
                            cursor.execute(
                                "UPDATE Usuarios SET estado_civil = 'soltero', edad_conyugue = NULL, sexo_conyugue = NULL WHERE cedula = %s", 
                                (cedula_buscada,)
                            )
                        conn.commit()
                        print("ESTADO CIVIL ACTUALIZADO CORRECTAMENTE") 

                    elif datos_actualizar.valor_inmueble is not None:
                        cursor.execute(
                            "UPDATE Usuarios SET valor_inmueble = %s WHERE cedula = %s", 
                            (datos_actualizar.valor_inmueble, cedula_buscada)
                        )
                        conn.commit()
                        print("VALOR DEL INMUEBLE ACTUALIZADO CORRECTAMENTE")

                    elif datos_actualizar.tasa_interes is not None:
                        cursor.execute(
                            "UPDATE Usuarios SET tasa_interes = %s WHERE cedula = %s", 
                            (datos_actualizar.tasa_interes, cedula_buscada)
                        )
                        conn.commit()
                        print("TASA DE INTERES ACTUALIZADA CORRECTAMENTE")

            except DatabaseError as e:
                print(f"Error al actualizar usuario: {e}")
                conn.rollback()
            finally:
                conn.close()
        else:
            print("No se pudo establecer conexión con la base de datos.")

    @staticmethod
    def verificarValores_vacios(cedula, estado_civil, edad, valor_inmueble, condicion_inmueble, tasa_interes):
        """Verifies that none of the important fields are empty."""
        if not all([cedula, estado_civil, edad, valor_inmueble, condicion_inmueble, tasa_interes]):
            raise None_Exception("Uno o más campos obligatorios están vacíos.")

    @staticmethod
    def verificarEdad(edad):
        """Checks if the age is within permitted limits."""
        if not (EDAD_MINIMA <= edad <= ESPERANZA_VIDA_HOMBRES):
            raise Edad_Exception(f"La edad {edad} no está dentro del rango permitido.")

    @staticmethod
    def verificarInmueble(valor_inmueble):
        """Verifies that the property value is at or above the minimum."""
        if valor_inmueble < VALOR_MINIMO_INMUEBLE:
            raise Valor_Inmueble_Exception("El valor del inmueble es inferior al permitido.")

    @staticmethod
    def verificarInteres(tasa_interes):
        """Checks if the interest rate is within permitted limits."""
        if not (INTERES_MINIMO <= tasa_interes <= INTERES_MAXIMO):
            raise Tasa_Exception("La tasa de interés no está dentro del rango permitido.")
