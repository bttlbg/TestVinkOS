import pandas as pd  # Para manipular archivos csv


# Funcion para limpiar los archivos de registro
# La funcion recibe un archivo 'sucio' y devuelve
# un archivo 'limpio'


def clean(report_file: pd.DataFrame):
    # Eliminar registros duplicados en caso de existir
    report_file = report_file.drop_duplicates()

    # Convertir columnas a sus tipos de datos correspondientes
    report_file['Opens'] = report_file['Opens'].astype(int)
    report_file['Opens virales'] = report_file['Opens virales'].astype(
        int)
    report_file['Clicks'] = report_file['Clicks'].astype(int)
    report_file['Clicks virales'] = report_file['Clicks virales'].astype(
        int)

    return report_file
