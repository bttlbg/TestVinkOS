import pysftp  # Para establecer conexiones via sftp
import pandas as pd  # Para manipular archivos csv


def get_file(sftp: pysftp.Connection, file):
    # Abrir archivos con pandas para facilitar su manipulacion
    archivo_sftp = sftp.open(file, mode='r')
    archivo_reporte = pd.read_csv(
        archivo_sftp, na_values='-')
    # Rellenamos los valores vacios para facilitar el control de errores?
    archivo_reporte = archivo_reporte.fillna('-')
    archivo_sftp.close()

    return archivo_reporte


def get_heads(report):
    heads = list(report.columns)
    return heads
