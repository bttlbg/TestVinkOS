import pandas as pd  # Para manipular archivos csv
# Conexion SQL
import mariadb
from mariadb import Error
import sys

# FIXME Arreglar variable con credenciales
USER = 'usuario'
SERVER = 'localhost'
PASS = 'password'
DATABASE = 'db'


# Crear informacion para una fila de visitantes
def make_visitante_info(conn: mariadb.Cursor):
    conn.ex

# Conexion a la DB y Carga de info


def insert_estadistica(report_file: pd.DataFrame):
    try:
        conn = mariadb.connect(
            user=USER,
            password=PASS,
            host=SERVER,
            port=22,
            database=DATABASE
        )
        cursor = conn.cursor()

        # Iterar sobre las filas del dataframe y hacer eñ insert
        for index, row in report_file.iterrows():
            email = row['email']
            jyv = row['jyv']
            badmail = row['Badmail']
            baja = row['Baja']
            fecha_envio = row['Fechaenvio']
            fecha_open = row['Fechaopen']
            opens = row['Opens']
            fecha_virales = row['Opensvirales']
            fecha_click = row['Fechaclick']
            clicks = row['Clicks']
            clicks_virales = row['Clicksvirales']
            links = row['Links']
            ips = row['IPs']
            navegadores = row['Navegadores']
            plataformas = row['Plataformas']

            insert_query = """INSERT INTO estadistica (email, jyv, Badmail, Baja, 
                                Fechaenvio, Fechaopen, Opens, Opensvirales, Fechaclick, 
                                Clicks, Clicksvirales, Links, IPs, Navegadores, Plataformas) 
                              VALUES (?,?,?,?,STR_TO_DATE(?, '%d/%m/%Y %H:%i'),
                                STR_TO_DATE(?, '%d/%m/%Y %H:%i'),?,?,
                                IF(? = '-' OR ? IS NULL, '1970-01-01', STR_TO_DATE(?, '%d/%m/%Y %H:%i')),
                                ?,?,?,?,?,?)"""

            cursor.execute(insert_query, (email, jyv, badmail, baja, fecha_envio, fecha_open, opens, fecha_virales,
                                          fecha_click, fecha_click, fecha_click,
                                          clicks, clicks_virales, links, ips, navegadores, plataformas))
            conn.commit()
        print("Datos insertados correctamente en la tabla estadistica")

    except mariadb.Error as e:
        print(f"Error al conectar con MariaDB: {e}")
    finally:
        if conn:
            conn.close()


def insert_visitantes(report_file: pd.DataFrame):
    try:
        conn = mariadb.connect(
            user=USER,
            password=PASS,
            host=SERVER,
            port=22,
            database=DATABASE
        )
        cursor = conn.cursor()

        # Iterar sobre las filas del dataframe y hacer eñ insert
        for index, row in report_file.iterrows():
            email = row['email']

            # FIXME Escribir query adecuada
            insert_query = """INSERT INTO visitante (email, fechaPrimeraVisita, fechaUltimaVisita, 
                                visitasTotales, visitasAnioActual, visitasMesActual) 
                              VALUES (?,?,?,?,?,?)"""

            cursor.execute(insert_query, (email))
            conn.commit()
        print("Datos insertados correctamente en la tabla visitante")

    except mariadb.Error as e:
        print(f"Error al conectar con MariaDB: {e}")
    finally:
        if conn:
            conn.close()


def insert_errores(invalid_rows: list):
    try:
        conn = mariadb.connect(
            user=USER,
            password=PASS,
            host=SERVER,
            port=22,
            database=DATABASE
        )
        cursor = conn.cursor()

        # Iterar sobre los elemtentos de la fial y hacer el insert
        for row in invalid_rows:
            insert_query = """INSERT INTO errores (registros) 
                              VALUES (?)"""

            cursor.execute(insert_query, (row,))
            conn.commit()
        print("Datos insertados correctamente en la tabla errores")

    except mariadb.Error as e:
        print(f"Error al conectar con MariaDB: {e}")
    finally:
        if conn:
            conn.close()
