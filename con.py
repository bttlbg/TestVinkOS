# Este script se ejecutara una vez diariamente
# El encargado de ejecutar el script será
# una tarea de crontab

import pysftp
import csv
import re


# Funcion para corroborar que los encabezados de los archivos
# tengan la estructura esperada


def validarEncabezados(encabezado):
    if encabezado != ["email", "jyv", "Badmail", "Baja", "Fecha envio", "Fecha open", "Opens", "Opens virales", "Fecha click", "Clicks", "Clicks virales", "Links", "IPs", "Navegadores", "Plataformas"]:
        return False

    return True

# Funcion para validar un correo electronico utilizando
# expresiones regulares


def validarEmail(email):
    patron_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron_regex, email) is not None


def main():
    # Creamos una conexion hacia el servidor
    # el cual contiene los archivos con la informacion
    # de las visitas al sitio web
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp = pysftp.Connection(host="192.168.100.19",
                             username="lappy", password="gc", cnopts=cnopts)

    # TODO: borrar al final
    sftp.execute("notify-send \"Conexion establecida\"")

    # Comprobar que el directorio no este vacio
    visitas_dir_path = '/home/lappy/archivosVisitas/'
    lista_archivos = sftp.listdir(visitas_dir_path)

    if not lista_archivos:
        # sftp.execute("notify-send \"Directorio vacio\"")  # TODO: borrar al final
        print("Directorio vacio")
    else:
        # TODO: borrar
        # sftp.execute("notify-send \"Direcotorio con informacion\"")
        # Una vez creada la conexion comenzamos a validar el layout
        # de los archivos
        for i in lista_archivos:
            print("ABRIENDO ARCHIVO: ", i)
            # Abrir archivos para leer.
            # La informacion en los archivos
            # de texto aparece separada por comas por lo cual usaremos
            # la libreria csv
            # TODO: Activar para conexion SFTP
            archivo = sftp.open(visitas_dir_path + i, mode='r')
            linea_archivo = csv.reader(archivo, delimiter=',', quotechar='"')

            # La primera linea contiene los encabezados los cules deben ser
            # validados
            c_line = next(linea_archivo)
            if not validarEncabezados(c_line):
                print("Los encabezados del archivo", i, "son invalidos.")
                print("Saltando...")
                continue
            else:
                print(i, ": Encabezados validos")

            # En este punto estamos en el primer registro de los archivos
            while archivo:
                # FIXME: La iteracion se salta lineas
                print(c_line)
                c_line = next(linea_archivo)
                # Validacion de email
                # Si la direccion de email no es valida
                if not validarEmail(c_line[0]):
                    print("Invalid email")
                    continue
                else:
                    print(c_line[0], ": Valid email")
                

            archivo.close()

        # Validar informacion a cargar [Email, Fechas dd/mm/yyyy HH:mm]
        # Cargar informacion a tablas
        # Hacer backup de los archivos en zip
        # Borrar archivos originales

    sftp.execute("notify-send \"Conexion finalizada\"")
    sftp.close()


if __name__ == "__main__":
    main()
