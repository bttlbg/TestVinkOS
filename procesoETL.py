# Este script se ejecutara una vez diariamente
# El encargado de ejecutar el script será
# una tarea de crontab

import pysftp           # Para establecer conexiones via sftp
import pandas as pd     # Para manipular archivos csv
import re               # Para validar cadenas de caracteres via regex
import datetime         # Para validar formatos de fechas

# Funcion para limpiar los archivos de registro
# La funcion recibe un archivo 'sucio' y devuelve
# un archivo 'limpio'


def limpiarArchivo(archivo_registro):
    # Eliminar registros duplicados en caso de existir
    archivo_registro = archivo_registro.drop_duplicates()

    # Convertir columnas a sus tipos de datos correspondientes
    archivo_registro['Opens'] = archivo_registro['Opens'].astype(int)
    archivo_registro['Opens virales'] = archivo_registro['Opens virales'].astype(
        int)
    archivo_registro['Clicks'] = archivo_registro['Clicks'].astype(int)
    archivo_registro['Clicks virales'] = archivo_registro['Clicks virales'].astype(
        int)

    return archivo_registro

# Funcion para corroborar que los encabezados de los archivos
# tengan la estructura esperada


def validarEncabezados(encabezado):
    # TODO ACTIVAR para comprobar encabezados
    # if encabezado != ["email", "jyv", "Badmail", "Baja", "Fecha envio", "Fecha open", "Opens", "Opens virales", "Fecha click", "Clicks", "Clicks virales", "Links", "IPs", "Navegadores", "Plataformas"]:
    #    return False

    return True

# Funcion para validar un correo electronico utilizando
# expresiones regulares


def validarEmail(email):
    patron_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron_regex, email) is not None

# Validar el formato de la fechas, si el valor
# de la fecha enviada a la funcion es NaN la tomamos
# como valor valido, pues significa que la columna esta vacia


def validarFormatoFechas(fecha):
    try:
        f_fecha = datetime.datetime.strptime(fecha, '%d/%m/%Y %H:%M')
        return True
    except ValueError:
        return False


def main():
    # Creamos una conexion hacia el servidor
    # el cual contiene los archivos con la informacion
    # de las visitas al sitio web
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp = pysftp.Connection(host="",
                             username="", password="", cnopts=cnopts)

    # Comprobar que el directorio no este vacio
    ruta_carpeta_registros = '/home/lappy/archivosVisitas/'
    lista_archivos_registros = sftp.listdir(ruta_carpeta_registros)

    # Si la carpeta no contiene nigun archivos finalizamos el proceso
    if not lista_archivos_registros:
        print("Directorio vacio")
    else:
        # Una vez creada la conexion comenzamos a validar el layout
        # de los archivos
        for archivo in lista_archivos_registros:

            # Comprobamos que los archivos encontrados en el directorio
            # tienen el nombre valido. Si es asi procedemos a trabajar con ellos.
            if "report_" in archivo:

                print("ABRIENDO ARCHIVO: ", archivo)  # TODO Borrar
                # Abrir archivos con pandas para facilitar su manipulacion
                archivo_sftp = sftp.open(
                    ruta_carpeta_registros + archivo, mode='r')
                archivo_reporte = pd.read_csv(
                    archivo_sftp, na_values='-')
                # Rellenamos los valores vacios para facilitar el control de errores?
                archivo_reporte = archivo_reporte.fillna('-')

                # Limpiar archivo
                archivo_reporte = limpiarArchivo(
                    archivo_reporte)

                # Obtener los nombres de los encabezados y verificar que sean los esperados
                nombres_columnas = list(archivo_reporte.columns)
                if not validarEncabezados(nombres_columnas):
                    print("Encabezados invalidos:", archivo)
                    continue

                # Despues de comprobar que los encabezados son validos vamos a
                # iterar sobre cada fila, y comprobar que los valores de en las
                # columnas sean validos
                for f_index, fila in enumerate(archivo_reporte.iterrows()):
                    for num_col, nombre_col in enumerate(nombres_columnas):

                        # Una banderilla para saber si el registro contiene
                        # algun campo invalido
                        registro_valido = True

                        if nombre_col == 'Fecha envio':
                            if fila[1][num_col] == '-' or not validarFormatoFechas(fila[1][num_col]):
                                registro_valido = False
                        elif nombre_col in ['Fecha open', 'Fecha click']:
                            if fila[1][num_col] != '-' and not validarFormatoFechas(fila[1][num_col]):
                                registro_valido = False
                        elif nombre_col in ['Opens', 'Opens virales', 'Clicks', 'Clicks virales']:
                            if not isinstance(fila[1][num_col], int):
                                registro_valido = False

                        # Si el registro es invalido, nos encargamos de el 🔫
                        if not registro_valido:
                            # Lo enviamos a un archivo diferente el cual cargaremos despues
                            # a la tabla de errores
                            print("--------------------------------")
                            print("Registro valido:",
                                  registro_valido, "\n", fila)
                            # Borramos a los registros invalidos para que no se suban a la DB
                            # Pero antes los enviamos a otro lado para despues subirlas al registro de errores
                            archivo_reporte = archivo_reporte.drop(f_index)
                #print(archivo_reporte)
                archivo_sftp.close()

        # TODO Cargar informacion a tablas
        # TODO Hacer backup de los archivos en zip
        # TODO Borrar archivos originales
    sftp.close()


if __name__ == "__main__":
    main()
