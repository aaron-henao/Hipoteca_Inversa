class Usuario:
    """

    Pertenece la Capa de Reglas de Negocio (Model)

    Representa a un usuario de la Hipoteca Inversa en la aplicación

    """
    def __init__(self, cedula, edad, estado_civil, edad_conyugue, sexo_conyugue, valor_inmueble, tasa_interes):
        self.cedula = cedula
        self.edad = edad
        self.estado_civil = estado_civil
        self.edad_conyugue = edad_conyugue
        self.sexo_conyugue = sexo_conyugue
        self.valor_inmueble = valor_inmueble
        self.tasa_interes = tasa_interes

    def __repr__(self):
        """

        Metodo para retornar los datos del usuario

        """
        #Condicional para saber si el usuario tiene conyugue
        if (self.estado_civil.title() == "Casado" or self.estado_civil.title() == "Casada"):    
            #Si la condición anterior se cumple, retorna todos los datos del usuario
            return str(f"CEDULA: {self.cedula} \n EDAD: {self.edad} \n ESTADO CIVIL: {self.estado_civil} \n EDAD CONYUGUE: {self.edad_conyugue} \n SEXO CONYUGUE: {self.sexo_conyugue} ")

        else:
            #Si la condición anterior no se cumple, retorna los datos del usuario sin incluir los datos que tienen que ver con el conyugue
            return str(f"CEDULA: {self.cedula} \n EDAD: {self.edad} \n ESTADO CIVIL: {self.estado_civil} ")

    def es_Igual(self, comparar_con):
        """

        Compara el objeto actual, con otra instancia de la clase Usuario

        """
        assert(self.cedula == comparar_con.cedula)
        assert(self.edad == comparar_con.edad)
        assert(self.estado_civil == comparar_con.estado_civil)
        assert(self.edad_conyugue == comparar_con.edad_conyugue)
        assert(self.sexo_conyugue == comparar_con.sexo_conyugue)
        assert(self.valor_inmueble == comparar_con.valor_inmueble)
        assert(self.tasa_interes == comparar_con.tasa_interes)