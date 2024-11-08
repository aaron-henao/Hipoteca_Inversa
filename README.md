# Reverse Mortgage Calculator
# versión 1.0
## Who Made This?
**Author:** Yonatan Calimeño and Juan Diego

## What Is It and What Is It For?
This project is an application to calculate the monthly payments of a reverse mortgage, considering factors such as the property's value, the property's condition, marital status, the ages of the owner and spouse, and the interest rate.

## How Do I Run It?

### Prerequisites
Make sure you have Python and kivy  installed on your system. 

**Kivy Installation:** Provided instructions to install Kivy using `pip`
Sometimes it doesn't let you download Kivy with the basic command "pip install Kivy", so my recommendation is that you use the Anaconda Python interpreter, and from the Anaconda console execute the command: "pip install Kivy", I also leave you the Kivy documentation here:https://kivy.org/doc/stable/gettingstarted/installation.html

### Running the Program
To run the program outside of the development environment:

1. Navigate to the folder:
   Once you have cloned the file, open the command prompt (cmd) or Anaconda Prompt, and navigate to the folder where you saved the file, for example:

    ```bash
    cd C:\Users\yonatan\Desktop\language_two\PRACTICE_CLEANCODE-main
    ```

2. Run the main script:
    ```bash
    python src/console/main.py
    ```

## How Is It Made?

### Project Architecture
The project is organized into two main folders:

- **src**: Contains the application's source code.
  - **console**: Contains the main script `main.py` for user interaction.
  - **logic**: Contains the logic for reverse mortgage calculation (`reverse_mortgage.py`).
- **test**: Contains unit tests to validate the functionality of the code.

### Module Organization
- `src/console/main.py`: Main file for user interaction. Collects user inputs and displays the results.
- `src/logic/reverse_mortgage.py`: Contains the logic functions for reverse mortgage calculation, including input validation and payment calculation.

### Dependencies
 -`kivy` and `unittest` as dependencies

## Usage
To run the unit tests from the `tests` folder, use the following command:

```bash
python test/unit_tests.py

To run the main file:
python src/console/main.py
python src/console/main_console.py"
```
# versión 2.0
# ACTUALIZACIONES 

### ¿Que es y para que sirve?

Este es un proyecto que está diseñado para calcular una Hipoteca Inversa y emplea una base de datos de ejemplo estructurada mediante el patrón MVC, que se conecta a una base de datos PostgreSQL.

### Dependencias 
```
- python 3
- psycopg2 --> PIP INSTALL PSYCOPG2
```

### Estructa del proyecto:
se creo tres nuevas carpetas con los nombres de: 

- src: Esta carpeta contiene el código fuente de la aplicación.
 Está organizada en capas para facilitar el mantenimiento y la escalabilidad del proyecto. La estructura de carpetas dentro de src es la siguiente:

- CONTROLLER: Contiene el codigo fuente con la conexion (**secret_config-simple**) a la base de datos y los querys que se pueden ejecutar.

- MODEL: Contiene el codigo fuente para modelar los usuarios que se van a ingresar a la base de datos.

- VIEW_CONSOLE: Contiene el codigo fuente de la interfaz por consola.

- test: Esta carpeta contiene las pruebas unitarias para validar el correcto funcionamiento del código.

## Paso a paso:
### Prerrequisitos:

Antes de ejecutar el codigo asegurese de tener una base de datos PostgreSQL y sus respectivos datos de acceso en neon.tech
Copie el archivo Secret_Config-sample.py y establezca en este archivo los datos de conexion a su base de datos.

### Para acceder a los test:
 ```
python test\TestMVC.py
 ```

### Acceder a la consola : 

```
python src\VIEW_CONSOLE\Crear_Usuario.py
```


# MODIFICACIONES

To run the web application install FLASK

pip install flask

Put your db dates on the script Secret_Config-sample.py and rename that Secret_Config.py

Navigate to the path where you have the file

and run scr/app/main.py

Open the path on the localhost:

Running on http://127.0.0.1:5000

To add a user to the database:

http://127.0.0.1:5000/user_form

To search for a user by ID

http://127.0.0.1:5000/user_details_search

To delete a user
http://127.0.0.1:5000/search_user

To update a user
http://127.0.0.1:5000/update_user



### Nombre Creadores:
- Edison Ospina Arroyave.
- Juan Manuel Garcia.

## Nombre Colaboradores
- Juan Felpi Ruiz
- Esteban parra 
-
