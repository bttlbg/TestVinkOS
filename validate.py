import re
import datetime  # Para validar formatos de fechas
import pandas as pd  # Para manipular archivos csv

# Funcion para corroborar que los encabezados de los archivos
# tengan la estructura esperada


def validate_heads(heads):
    if heads != ["email", "jyv", "Badmail", "Baja", "Fecha envio", "Fecha open", "Opens", "Opens virales", "Fecha click", "Clicks", "Clicks virales", "Links", "IPs", "Navegadores", "Plataformas"]:
        return False

    return True


def validate_columns(report_file: pd.DataFrame, heads):
    # Definimos las funciones de validacion para cada columna
    validation_functions = {
        'email': validate_email,
        'Fecha envio': lambda x: x != '-' and validate_dates(x),
        'Fecha open': lambda x: x == '-' or validate_dates(x),
        'Fecha click': lambda x: x == '-' or validate_dates(x),
        'Opens': lambda x: isinstance(x, int),
        'Opens virales': lambda x: isinstance(x, int),
        'Clicks': lambda x: isinstance(x, int),
        'Clicks virales': lambda x: isinstance(x, int)
    }

    # Creamos una lista para almacenar los indices de fila invalidos
    invalid_rows = []

    for r_index, row in report_file.iterrows():
        valid_row = True

        # Iteramos a traves de las columnas y sus funciones de validacion correspondientes
        for c_name, validate_function in validation_functions.items():
            c_index = heads.index(c_name)
            if not validate_function(row[c_index]):
                valid_row = False
                break

        if not valid_row:
            # Si el registro es invalido, lo agregamos a la lista de indices invalidos
            invalid_rows.append(r_index)

    # Eliminamos todas las filas invalidas de una sola vez
    report_file = report_file.drop(invalid_rows)

    return report_file


# Funcion para validar un correo electronico utilizando
# expresiones regulares
def validate_email(email):
    patron_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron_regex, email) is not None


# Validar el formato de la fechas, si el valor
# de la fecha enviada a la funcion es NaN la tomamos
# como valor valido, pues significa que la columna esta vacia
def validate_dates(date):
    try:
        f_fecha = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M')
        return True
    except ValueError:
        return False
