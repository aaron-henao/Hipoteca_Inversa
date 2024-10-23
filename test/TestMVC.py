import unittest

# Lo importamos para poder incluir la ruta de busqueda python
import sys
sys.path.append("src")

from MODEL.Usuario import Usuario
from CONTROLLER.Controlador_Usuarios import Controlador_Usuarios, None_Exception, Edad_Exception, Valor_Inmueble_Exception, Tasa_Exception

import psycopg2

class Controller_Test(unittest.TestCase):

    #Test Fixtire
    def setUpClass():
        """ 
        
        Se ejecuta siempre antes de cada metodo de prueba 
        
        """
        Controlador_Usuarios.Crear_Tabla()
        Controlador_Usuarios.Limpiar_Tabla()

    #CASOS DE PRUEBA NORMALES  
    def testInsert_And_Select_Usuario1( self ):
        """ 

        Prueba que se cree correctamente la tabla en la BD 

        """
        # Insertar un Usuario en la tabla
        usuario_prueba  = Usuario( cedula="1234657", edad="65", estado_civil="soltero",
                                 edad_conyugue=None, sexo_conyugue=None, valor_inmueble="100000000", tasa_interes="25")
        Controlador_Usuarios.Insertar_Usuario( usuario_prueba )

        # Verificar si la tabla quedo creada correctamente
        usuario_buscado = Controlador_Usuarios.Buscar_Usuario( usuario_prueba.cedula )

        # Comparar si el usuario que se insertó, contiene la misma información, que el retornado
        usuario_buscado.es_Igual( usuario_prueba )

    

    #Casos de Error
    def testInsert_And_Select_Usuario2( self ):
        """ 

        Prueba que se cree correctamente la tabla en la BD 

        """
        # Insertar un Usuario en la tabla
        usuario_prueba  = Usuario( cedula="55555555", edad="70", estado_civil="casado",
                                 edad_conyugue="23", sexo_conyugue="mujer", valor_inmueble="200000000", tasa_interes="12")
        Controlador_Usuarios.Insertar_Usuario( usuario_prueba )

        # Verificar si la tabla quedo creada correctamente
        usuario_buscado = Controlador_Usuarios.Buscar_Usuario( usuario_prueba.cedula )

        # Comparar si el usuario que se insertó, contiene la misma información, que el retornado
        usuario_buscado.es_Igual( usuario_prueba )

    def testUpdate_Usuario( self ):
        """ 

        Prueba que se cree correctamente la tabla en la BD 

        """
        # Actualiza los datos de un usuario en la base de datos
        datos_actualizar  = Usuario( cedula=None, edad=None, estado_civil="casado",
                                 edad_conyugue="66", sexo_conyugue="mujer", valor_inmueble=None, tasa_interes=None)
        Controlador_Usuarios.Actualizar_Usuario( cedula_buscada="1234657", datos_actualizar=datos_actualizar )

    def testDelete_Usuario( self ):
        """ 

        Prueba que se cree correctamente la tabla en la BD 

        """
        # Elimina un ususario de la base de datos
        Controlador_Usuarios.Eliminar_Usuario( cedula_buscada="55555555" )


    #CASOS DE ERROR
    def testNone_Error1( self ):
        """ 

        Prueba que se cree correctamente la tabla en la BD 

        """
        # Insertar un Usuario en la tabla
        usuario_prueba  = Usuario( cedula=None, edad="68", estado_civil="casada",
                                 edad_conyugue="62", sexo_conyugue="hombre", valor_inmueble="1000000000", tasa_interes="33")

        self.assertRaises(None_Exception, Controlador_Usuarios.Insertar_Usuario, usuario_prueba)

    def testEdad_Error( self ):
        """ 

        Prueba que se cree correctamente la tabla en la BD 

        """
        # Insertar un Usuario en la tabla
        usuario_prueba  = Usuario( cedula="1038867289", edad="55", estado_civil="soltero",
                                 edad_conyugue=None, sexo_conyugue=None, valor_inmueble="84000000", tasa_interes="35")

        self.assertRaises(Edad_Exception, Controlador_Usuarios.Insertar_Usuario, usuario_prueba)

    def testValor_Inmueble_Error( self ):
        """ 

        Prueba que se cree correctamente la tabla en la BD 

        """
        # Insertar un Usuario en la tabla
        usuario_prueba  = Usuario( cedula="1038867289", edad="66", estado_civil="soltero",
                                 edad_conyugue=None, sexo_conyugue=None, valor_inmueble="7000000", tasa_interes="40")

        self.assertRaises(Valor_Inmueble_Exception, Controlador_Usuarios.Insertar_Usuario, usuario_prueba)

    def testTasa_Interes_Error( self ):
        """ 

        Prueba que se cree correctamente la tabla en la BD 

        """
        # Insertar un Usuario en la tabla
        usuario_prueba  = Usuario( cedula="1038867289", edad="66", estado_civil="soltero",
                                 edad_conyugue=None, sexo_conyugue=None, valor_inmueble="125000000000", tasa_interes="48")

        self.assertRaises(Tasa_Exception, Controlador_Usuarios.Insertar_Usuario, usuario_prueba)

# Este fragmento de codigo permite ejecutar la prueba individualmente
if __name__ == '__main__':
    unittest.main()