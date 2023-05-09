import pandas as pd  # Para manipular archivos csv


# Funcion para limpiar los archivos de registro
# La funcion recibe un archivo 'sucio' y devuelve
# un archivo 'limpio'


def clean(report_file: pd.DataFrame):
    # Eliminar registros duplicados en caso de existir
    report_file = report_file.drop_duplicates()

    # Convertir columnas a sus tipos de datos correspondientes
    report_file['Opens'] = pd.to_numeric(
        report_file['Opens'], errors='coerce').fillna(0).astype(int)

    report_file['Opensvirales'] = pd.to_numeric(
        report_file['Opensvirales'], errors='coerce').fillna(0).astype(int)

    report_file['Clicks'] = pd.to_numeric(
        report_file['Clicks'], errors='coerce').fillna(0).astype(int)

    report_file['Clicksvirales'] = pd.to_numeric(
        report_file['Clicksvirales'], errors='coerce').fillna(0).astype(int)

    report_file['Links'] = pd.to_numeric(
        report_file['Links'], errors='coerce').fillna(0).astype(int)

    return report_file
