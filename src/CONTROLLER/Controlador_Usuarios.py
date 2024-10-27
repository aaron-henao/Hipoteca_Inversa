# Lo importamos para poder incluir la ruta de busqueda python
import sys
sys.path.append("src")


import psycopg2

from CONTROLLER import Secret_Config
from MODEL.Usuario import Usuario

# CONSTANTES
#Edad maxima permitida
ESPERANZA_VIDA_HOMBRES = 84
ESPERANZA_VIDA_MUJERES = 86

#Edad minima permitida
EDAD_MINIMA = 62

#Valor minimo de la propiedad
VALOR_MINIMO_INMUEBLE = 10000000

#Tasa de interes maxima y minima permitidas
INTERES_MINIMO = 6
INTERES_MAXIMO = 43


#EXCEPCIONES
class Usuario_No_Actualizado_Exception(Exception):
    """ 

    Excepción personalizada para cuando el usuario no se actualiza

    """
    def __init__(self):
        super().__init__(f"El usuario no se pudo actualizar")

class Usuario_No_Insertado_Exception(Exception):
    """ 

    Excepción personalizada para cuando el usuario no se puede insertar a la tabla

    """
    def __init__(self):
        super().__init__(f"El usuario no se pudo Insertar")

class Usuario_No_Eliminado_Exception(Exception):
    """ 

    Excepción personalizada para cuando el usuario no se puede eliminar de la tabla

    """
    def __init__(self):
        super().__init__(f"El usuario no se pudo eliminar")

class Edad_Exception(Exception):
    """ 

    Excepción personalizada para la edad por debajo del mínimo o por encima del maximo

    """
    def __init__(self, edad):
        super().__init__(f"La edad: {edad} es invalida, para aplicar a una hipoteca inversa se necesita tener una edad entre {EDAD_MINIMA} y {ESPERANZA_VIDA_HOMBRES}")

class None_Exception(Exception):
    """ 

    Excepción personalizada para valores que sean None

    """
    def __init__(self):
        super().__init__(f" No pueden haber campos vacios ")

class Valor_Inmueble_Exception(Exception):
    """ 

    Excepción personalizada para valores del inmueble por debajo del minimo

    """
    def __init__(self):
        super().__init__(f" No pueden haber campos vacios inmueble por debajo del minimo ")

class Tasa_Exception(Exception):
    """ 

    Excepción personalizada para tasa de interés por encima del máximo, por debajo del mínimo y cero

    """
    def __init__(self, interes):
        super().__init__(f"La tasa de interes: {interes} es invalida, El interes no debe ser menor a {INTERES_MINIMO} ni debe ser mayo a {INTERES_MAXIMO} ")


class Controlador_Usuarios:

    def Obtener_Cursor():
        """

        Crea la conexion a la base de datos y retorna un cursor para ejecutar instrucciones

        """
        DATABASE = Secret_Config.PGDATABASE
        USER = Secret_Config.PGUSER
        PASSWORD = Secret_Config.PGPASSWORD
        HOST = Secret_Config.PGHOST
        PORT = Secret_Config.PGPORT
        PGHOST=Secret_Config.PGHOST

        #Se realiza la conexión con la base de datos
        connection = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)

        # Todas las instrucciones se ejecutan a tavés de un cursor
        cursor = connection.cursor()
        return cursor
    
    def Crear_Tabla():
        """ 

        Crea la tabla de usuarios en la BD 

        """
        try:
            #Se obtiene el cursor para tener la conexión con la base de datos
            cursor = Controlador_Usuarios.Obtener_Cursor()

            #Se ejecuta el query para crear la tabla en la base de datos
            cursor.execute("""create table Usuarios (cedula varchar( 20 )  NOT NULL primary key,
                            edad varchar( 2 ) not null,
                            estado_civil text not null,
                            edad_conyugue varchar( 2 ),
                            sexo_conyugue text,
                           valor_inmueble varchar( 20 ) not null,
                           tasa_interes varchar( 4 ) not null)
                        """)
            
            # Confirma los cambios realizados en la base de datos
            # Si no se llama, los cambios no quedan aplicados
            cursor.connection.commit()
            print("TABLA CREADA CORRECTAMENTE")
            print("\n")
        except:
             #Si llega aquí es porque la tabla ya existe y no se pudo crear
             cursor.connection.rollback()
             print("LA TABLA YA EXISTE")
             print("\n")
             return "Tabla Existente"
        
    def Limpiar_Tabla():
            """ 
            
            Borra la tabla de usuarios de la BD 
            
            """
            #Se obtiene el cursor para tener la conexión con la base de datos
            cursor = Controlador_Usuarios.Obtener_Cursor()

            #Se ejecuta el query para eliminar los registros que hay en la tabla
            cursor.execute("""delete from Usuarios""" )

            # Confirma los cambios realizados en la base de datos
            # Si no se llama, los cambios no quedan aplicados
            cursor.connection.commit()
            print("REGISTROS ELIMINADOS EXITOSAMENTE")
            print("\n")
        
    def Insertar_Usuario( usuario : Usuario ):
            """ 

            Recibe una instancia de la clase Usuario y la inserta en la tabla respectiva
            
            """
            #Se obtiene el cursor para tener la conexión con la base de datos
            cursor = Controlador_Usuarios.Obtener_Cursor()

            Controlador_Usuarios.verificarValores_vacios(usuario.cedula, usuario.estado_civil, usuario.edad, usuario.valor_inmueble, usuario.tasa_interes)
            Controlador_Usuarios.verificarEdad(int(usuario.edad))
            Controlador_Usuarios.verificarInmueble(float(usuario.valor_inmueble))
            Controlador_Usuarios.verificarInteres(float(usuario.tasa_interes))

            try:

                #Condicional para saber si el usuario tiene conyugue
                if (usuario.estado_civil.title() == "Casado" or usuario.estado_civil.title() == "Casada"): 
                    
                    #Si la condición anterior se cumple, insertan los datos del usuario y los datos del conyugue
                    cursor.execute( f"""insert into Usuarios (cedula, edad, estado_civil, edad_conyugue, sexo_conyugue, valor_inmueble, tasa_interes)
                                        values('{usuario.cedula}', '{usuario.edad}', '{usuario.estado_civil}', '{usuario.edad_conyugue}', '{usuario.sexo_conyugue}', '{usuario.valor_inmueble}', '{usuario.tasa_interes}')""" )

                    # Confirma los cambios realizados en la base de datos
                    # Si no se llama, los cambios no quedan aplicados
                    cursor.connection.commit()
                    print("USUARIO INSERTADO EXITOSAMENTE")
                    print("\n")

                else:
                    
                    #Si la condición anterior no se cumple, insertan solo los datos del usuario
                    cursor.execute( f"""insert into Usuarios (cedula, edad, estado_civil, valor_inmueble, tasa_interes)
                                        values('{usuario.cedula}', '{usuario.edad}', '{usuario.estado_civil}', '{usuario.valor_inmueble}', '{usuario.tasa_interes}')""" )

                    # Confirma los cambios realizados en la base de datos
                    # Si no se llama, los cambios no quedan aplicados
                    cursor.connection.commit()
                    print("USUARIO INSERTADO EXITOSAMENTE")
                    print("\n")
                     
            except:
                 cursor.connection.rollback()
                 raise Usuario_No_Insertado_Exception()
    
    def Buscar_Usuario( cedula_Buscada ):
        """ 

        Trae un usuario de la tabla de usuarios por la cedula 
        
        """
        #Se obtiene el cursor para tener la conexión con la base de datos
        cursor = Controlador_Usuarios.Obtener_Cursor()

        #Se ejecuta el query para buscar el usuario por su cédula
        cursor.execute(f"""select cedula, edad, estado_civil, edad_conyugue, sexo_conyugue, valor_inmueble, tasa_interes
                        from usuarios where cedula = '{cedula_Buscada}'""" )
        
        #Se obtiene cada campo del usuario
        fila = cursor.fetchone()
        resultado = Usuario( cedula=fila[0], edad=fila[1], estado_civil=fila[2],edad_conyugue=fila[3],
                            sexo_conyugue=fila[4], valor_inmueble=fila[5], tasa_interes=fila[6])
        #Se muestran los datos obtenidos
        print(resultado)
        return resultado
    
    def Eliminar_Usuario( cedula_buscada ):
        """ 

        Elimina un usuario de la tabla Usuarios
        
        """
        #Se obtiene el cursor para tener la conexión con la base de datos
        cursor = Controlador_Usuarios.Obtener_Cursor()
        try:
            cursor.execute(f"""delete from Usuarios where cedula='{cedula_buscada}'""")
            cursor.connection.commit()
            print("USUARIO ELIMINADO CORRECTAMENTE")

        except:
             raise Usuario_No_Eliminado_Exception()
             
         

    def Actualizar_Usuario( cedula_buscada, datos_actualizar: Usuario ):
        """ 

        Trae un usuario de la tabla de usuarios por la cedula y actualiza sus valores
        
        """
        #Se obtiene el cursor para tener la conexión con la base de datos
        cursor = Controlador_Usuarios.Obtener_Cursor()
        try:
            #Condicional para saber si se quiere actualizar la cédula del usuario
            if (datos_actualizar.cedula != None):
                cursor.execute(f"""update Usuarios set cedula='{datos_actualizar.cedula}' where cedula ='{cedula_buscada}'""")
                cursor.connection.commit()
                print("CEDULA ACTUALIZADA CORRECTAMENTE")

            #Condicional para saber si se quiere actualizar el estado civil del usuario
            elif (datos_actualizar.estado_civil != None):

                #Condicional para saber si el usuario consiguió conyugue
                if (datos_actualizar.estado_civil.title() == "Casado"):  
                    cursor.execute(f"""update Usuarios set estado_civil='{datos_actualizar.estado_civil}' where cedula ='{cedula_buscada}'""")

                    #Condicional para Comprobar que estén correctos los datos del conyugue
                    if (datos_actualizar.edad_conyugue != None and datos_actualizar.sexo_conyugue != None):
                        cursor.execute(f"""update Usuarios set edad_conyugue='{datos_actualizar.edad_conyugue}', sexo_conyugue='{datos_actualizar.sexo_conyugue}' where cedula ='{cedula_buscada}'""")
                        cursor.connection.commit()
                        print("ESTADO CIVIL ACTUALIZADO CORRECTAMENTE") 

                else:
                    cursor.execute(f"""update Usuarios set estado_civil='soltero', edad_conyugue='', sexo_conyugue='' where cedula ='{cedula_buscada}'""")
                    cursor.connection.commit()
                    print("ESTADO CIVIL ACTUALIZADO CORRECTAMENTE") 
            
            #Condicional para saber si se quiere actualizar el valor del inmueble del usuario
            elif (datos_actualizar.valor_inmueble != None):
                    cursor.execute(f"""update Usuarios set valor_inmueble='{datos_actualizar.valor_inmueble}' where cedula ='{cedula_buscada}'""")
                    cursor.connection.commit()
                    print("VALOR DEL INMUEBLE ACTUALIZADO CORRECTAMENTE") 

            #Condicional para saber si se quiere actualizar la tasa de interes
            elif (datos_actualizar.tasa_interes != None):
                    cursor.execute(f"""update Usuarios set tasa_interes='{datos_actualizar.tasa_interes}' where cedula ='{cedula_buscada}'""")
                    cursor.connection.commit()
                    print("TASA DE INTERES ACTUALIZADA CORRECTAMENTE") 

        except:
             raise Usuario_No_Actualizado_Exception()
        
    # Verifica que ningun campo haya quedado vacio
    def verificarValores_vacios(cedula, estado_civil, edad, valor_inmueble, tasa_interes):
        if cedula == None or estado_civil == None or edad == None or valor_inmueble == None or tasa_interes == None:
            raise None_Exception()

    # Verifica que la edad del usuario no esté por debajo del limite
    def verificarEdad(edad):
        if edad < EDAD_MINIMA or edad > ESPERANZA_VIDA_HOMBRES:
            raise Edad_Exception(edad)
        
    # Verifica que el valor del inmueble del usuario no esté por debajo del limite
    def verificarInmueble(valor_inmueble):
        if valor_inmueble <  VALOR_MINIMO_INMUEBLE:
            raise Valor_Inmueble_Exception()
    
    def verificarInteres(tasa_interes):
        if tasa_interes < INTERES_MINIMO or tasa_interes > INTERES_MAXIMO:
            raise Tasa_Exception(tasa_interes)