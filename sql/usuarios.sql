--- Tabla de usuarios 

create table Usuarios (

    cedula varchar( 20 )  NOT NULL primary key,
    edad varchar( 2 ) not null,
    estado_civil text not null,
    edad_conyugue varchar( 2 ),
    sexo_conyugue text,
    valor_inmueble varchar( 20 ) not null,
    tasa_interes varchar( 4 ) not null

);