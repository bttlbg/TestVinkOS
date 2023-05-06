# Este script se ejecutara una vez diariamente
# El encargado de ejecutar el script será
# una tarea de crontab

import pandas as pd  # Para manipular archivos csv


# Conexion SQL
import mariadb
import sys

import sftp_conn
import extract
import transform
import validate



# Conexion a la DB y Carga de info
def cargar_tablas(archivo_registro):
    try:
        conn = mariadb.connect(
            user=USER,
            password=PASS,
            host=SERVER,
            port=3306,
            database=DATABASE

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()

    # Insercion de datos en la table de visitantes
    for r_index, row in archivo_registro.iterrows():
        sentencia_sql = """INSERT INTO visitante (email, fechaPrimeraVisita, fechaUltimaVisita, visitasTotales, visitasAnioActual, visitasMesActual) 
                            VALUES (?,?,?,?,?,?) 
                            ON DUPLICATE KEY UPDATE 
                                fechaUltimaVisita = ?, 
                                vistasTotales = visitasTotales + ?"""
        email = row['email']

        
        cur.execute(
            sentencia_sql, (email))

    # Insercion de datos en la table de esadistica

    # Insercion de registros invalidos en la tabla de errores


def main():
    
    reports_folder_path = '/home/lappy/archivosVisitas/'

    sftp = sftp_conn.get_sftp_conn()
    reports_list = sftp.listdir(reports_folder_path)

    # Comprobar que el directorio no este vacio
    # Si la carpeta no contiene nigun archivos finalizamos el proceso
    if not reports_list:
        print("Directorio vacio")
    else:
        # Una vez creada la conexion comenzamos a validar el layout
        # de los archivos
        for report in reports_list:

            # Comprobamos que los archivos encontrados en el directorio
            # tienen el nombre valido. Si es asi procedemos a trabajar con ellos.
            if "report_" in report:

                print("ABRIENDO ARCHIVO: ", report)  # TODO Borrar
                report_file = extract.get_file(sftp, reports_folder_path + report)

                # Limpiar archivo
                report_file = transform.clean(
                    report_file)

                # Obtener los nombres de los encabezados y verificar que sean los esperados
                heads_names = extract.get_heads(report_file)
                if not validate.validate_heads(heads_names):
                    print("Encabezados invalidos:", report)
                    # Si los encabezados no encajan copiamos todo el reporte
                    # a la lista de filas invalidas, excluyendo los encabezados
                    continue

                # Despues de comprobar que los encabezados son validos vamos a
                # iterar sobre cada fila, y comprobar que los valores de en las
                # columnas sean validos
                report_file = validate.validate_columns(report_file, heads_names)
                print(report_file)

                # Una vez corregido el archivo podemos cargar su info a las tablas
                # cargar
        # TODO Cargar informacion a tablas
        # TODO Hacer backup de los archivos en zip
        # TODO Borrar archivos originales
    sftp.close()


if __name__ == "__main__":
    main()
