import pysftp  # Para establecer conexiones via sftp
import pandas as pd  # Para manipular archivos csv

# FIXME BORRAR!
USER = 'lappy'
SERVER = '192.168.100.19'
PASS = 'gc'

def get_sftp_conn():
    # Creamos una conexion hacia el servidor
    # el cual contiene los archivos con la informacion
    # de las visitas al sitio web
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp = pysftp.Connection(host=SERVER,
                             username=USER, password=PASS, cnopts=cnopts)

    return sftp
