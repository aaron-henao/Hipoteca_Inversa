import sys
sys.path.append("src")

from psycopg import connect, DatabaseError
from app.Secret_Config import PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE
from logic import reverse_mortgage
from logic.reverse_mortgage import ReverseMortgageCalculator  # Importa la clase que contiene la lógica del cálculo

from logic.reverse_mortgage import ReverseMortgageCalculator
from psycopg import connect, DatabaseError
from app.Secret_Config import PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE

class ReverseMortgage:
    def __init__(self, cedula, edad, estado_civil, valor_inmueble, condicion_inmueble, tasa_interes, edad_conyuge, sexo_conyuge):
        self.cedula = cedula
        self.edad = edad
        self.estado_civil = estado_civil
        self.valor_inmueble = valor_inmueble 
        self.condicion_inmueble = condicion_inmueble
        self.tasa_interes = tasa_interes
        self.edad_conyuge = edad_conyuge
        self.sexo_conyuge = sexo_conyuge

    @staticmethod
    def connect_db():
        """Establishes a connection to the database."""
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

    def insertar_reverse_mortgage(self):
        """Calculates and inserts the mortgage payment into the Mortgage table."""
        try:
            # Calculate the mortgage using ReverseMortgageCalculator
            calculator = ReverseMortgageCalculator(
                cedula=self.cedula,
                edad=self.edad,
                estado_civil=self.estado_civil,
                edad_conyuge=self.edad_conyuge,
                sexo_conyuge=self.sexo_conyuge,
                valor_inmueble=self.valor_inmueble,
                condicion_inmueble=self.condicion_inmueble,
                tasa_interes=self.tasa_interes
            )

            monthly_payment = calculator.calculate_monthly_payment()

            # Connect to the database and insert the mortgage record
            conn = ReverseMortgage.connect_db()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO Mortgage (user_id, total_payment)
                            VALUES (%s, %s)
                            ON CONFLICT (user_id) DO UPDATE SET total_payment = EXCLUDED.total_payment""",
                            (self.cedula, monthly_payment)
                        )
                    conn.commit()
                    print("Reverse mortgage inserted or updated successfully.")
                except DatabaseError as e:
                    print(f"Error while inserting reverse mortgage: {e}")
                    conn.rollback()
                finally:
                    conn.close()
        except Exception as e:
            print(f"Error in calculating mortgage: {e}")

    def leer_mortgage(self):
        """Fetches the mortgage record from the database based on user ID (cedula)."""
        conn = ReverseMortgage.connect_db()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT total_payment FROM Mortgage WHERE user_id = %s", (self.cedula,))
                    mortgage = cursor.fetchone()
                    if mortgage:
                        return mortgage[0]
                    else:
                        print("Mortgage not found.")
                        return None
            except DatabaseError as e:
                print(f"Error fetching mortgage: {e}")
            finally:
                conn.close()
        else:
            print("Database connection failed.")
