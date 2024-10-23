# Lo importamos para poder incluir la ruta de busqueda python
import sys
sys.path.append("src")

# Se importa el modulo donde se realizarán los procesos
from CONTROLLER.Controlador_Usuarios import Controlador_Usuarios
from MODEL.Usuario import Usuario

# Se le da una bienvenida al usuario y se le muestra un menú con las opciones
def Bienvenida():
    print("-------------------------------------------")
    print("    BIENVENIDO AL BANCO   ")
    print("¿Qué deseas hacer?")
    print(" 1. Obtener una hipoteca inversa \n 0. Salir")
    opcion = int(input("Elija una opción: "))
    print("--------------------------------------")
    # Se llama a la siguiente función y se le pasa como parametro la opción que el usuario eligió
    return desiciones(opcion)

def desiciones(opcion):
    # Se hace uso del metodo try para lanzar una excepción si algo falla
    try:
        # Se usa el ciclo while para verificar cual opción escogio el usuario
        while opcion != 0:
            # Se verifica si la opción escogida por el usuario no está definida
            if opcion < 0 or opcion > 1:
                print("------------------------------------------------------------------")
                print("                  EL BANCO            ")
                print("La opción ingresada no es correcta, intente de nuevo")
                print("-------------------------------------------------------------------")
                # Se llama nuevamente al metodo de Bienvenida para reiniciar el proceso
                Bienvenida()
            # Se verifica si el usuario quiere calcular una hipoteca inversa
            if opcion == 1:
                print("---------------------------------------------------------------------")
                print("                     EL BANCO                 ")
                print("DATOS PERSONALES")
                # Se obtienen los datos de entrada
                cedula = int(input("Por favor ingrese su cedula: "))
                edad = int(input("Por favor ingrese su edad actual: "))
                estado_civil = input("Por favor ingrese su estado civil: ")
                estado_civil = estado_civil.title()
                #Condicional para saber si el usuario tiene conyugue
                if estado_civil == "Casado" or estado_civil == "Casada":
                    #Si la condición anterior se cumple, se obtienen los datos del conyugue
                    edad_conyugue = int(input("Por favor ingrese la edad de su conyugue: "))
                    sexo_conyugue = input("Por favor ingrese el genero de su conyugue: ")
                else:
                    #Si la condición anterior no se cumple, se definen los datos del conyugue como None
                    edad_conyugue = None
                    sexo_conyugue = None
                print("-------------------------------------------------------------------------")

                #Se crea el usuario en la base de datos
                usuario = Usuario(cedula, edad, estado_civil, edad_conyugue, sexo_conyugue)
                Controlador_Usuarios.Insertar_Usuario(usuario)
                # Se llama nuevamente al metodo de Bienvenida para reiniciar el proceso
                Bienvenida()

        # Se le da al usuario un mensaje de despedida al usuario cuando finaliza todo el proceso
        print("------------------------------------------------------------------")
        print("                  EL BANCO            ")
        print("Gracias por visitarnos, vuelva pronto")
        print("-------------------------------------------------------------------")
        return
    # Se lanza un mensaje de error cuando algo falla
    except ValueError:
        print("------------------------------------------------------------------")
        print("                  EL BANCO            ")
        print("Hubo un ERROR, revisa que los datos ingresados sean correctos")
        print("-------------------------------------------------------------------")
        # Se llama nuevamente al metodo de Bienvenida para reiniciar el proceso
        Bienvenida()
    except Exception as exc:
        print("------------------------------------------------------------------")
        print("                  EL BANCO            ")
        print(f"{exc}, intentalo nuevamente")
        print("-------------------------------------------------------------------")
        # Se llama nuevamente al metodo de Bienvenida para reiniciar el proceso
        Bienvenida()

#Condicional para comprobar si la tabla "Usuarios" ya está creada
if Controlador_Usuarios.Crear_Tabla == "Tabla Existente":
    # Si la condición anterior se cumple, solo se llama la funcion para dar inicio al programa
    Bienvenida()

else:
    #Si la condición anterior no se cumple, se crea la base de datos
    Controlador_Usuarios.Crear_Tabla()
    # Se llama la funcion para dar inicio al programa
    Bienvenida()

