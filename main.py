# Este script se ejecutara una vez diariamente
# El encargado de ejecutar el script será
# una tarea de crontab


import sftp_conn
import extract
import transform
import validate
import sql_etl


def main():

    reports_folder_path = '/home/vinkos/archivosVisitas/'

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

                # print("ABRIENDO ARCHIVO: ", report)  # TODO Borrar
                report_file = extract.get_file(
                    sftp, reports_folder_path + report)

                # Limpiar archivo
                report_file = transform.clean(
                    report_file)
                # Obtener los nombres de los encabezados y verificar que sean los esperados
                heads_names = extract.get_heads(report_file)
                if not validate.validate_heads(heads_names):
                    # print("Encabezados invalidos:", report)
                    # Si los encabezados no encajan copiamos todo el reporte
                    # a la lista de filas invalidas, excluyendo los encabezados
                    continue

                # Despues de comprobar que los encabezados son validos vamos a
                # iterar sobre cada fila, y comprobar que los valores de las
                # columnas sean validos
                report_file, invalid_rows = validate.validate_columns(
                    report_file, heads_names)

                # TODO Cargar informacion a tablas
                # sql_etl.insert_estadistica(report_file)
                # sql_etl.insert_visitantes(report_file)
                # sql_etl.insert_errores(invalid_rows)

        # TODO Hacer backup de los archivos en zip
        # TODO Copiar la copia de seguridad al directorio local
        # TODO Borrar archivos originales
    sftp.close()


if __name__ == "__main__":
    main()
