import sys  # provee acceso a funciones y objetos mantenidos por del intérprete.
import numpy as np  # da mayor soporte para el manejo de vectores y matrices
import json  # permite la manipulación de tipos de datos json
from fractions import Fraction  # para convertir números decimales a fracciones

try:
    import pandas as pd  # se utiliza para operaciones y manipulaciones de datos estructurados.

    # Es muy habitual usarlo en la fase de depuración y preparación de los datos.

    pandas_av = True
except ImportError:
    pandas_av = False  # Si ocurre un error al importar el modulo, se deshabilite pandas_av
    pass

# Declaración de variables
decimals = 2
quantity_constrains = 0
quantity_variables = 0
col_values = []
z_equation = []
constrains_names = []
data = []

problem_type = 1  # 1. Maximización  2. Minimización
final_rows = []  #
solutions = []  # almacenara nombres variables de holgura y solución [x3, x4, Solución]
x = 'X'
z2_equation = []
removable_vars = []
no_solution = """
        ---unboundedness ----
Your problem might not be having solution due to wrong 
formulation of constrains,

This mostly occurs when you leave out some relevant constrains 
please check again the formulation of constrains
            """


def principal(quantity_variables1, quantity_constrains1, col_values1, z_equation1):
    """
    Función principal que recibe la información necesaria para aplicar el método simple
    :param quantity_variables1: Cantidad de variables del problema
    :param quantity_constrains1: Cantidad de funciones restricción
    :param col_values1: Coeficientes de las variables de las funciones restricción
    :param z_equation1: Coeficientes de las variables de la función objetivo
    :return: Objeto json con los datos del paso a paso para mostrar al cliente
    """
    global decimals
    global quantity_constrains
    global quantity_variables
    global constrains_names
    global col_values
    global z_equation
    global data
    global solutions

    col_values = col_values1
    z_equation = z_equation1
    quantity_constrains = quantity_constrains1
    quantity_variables = quantity_variables1

    data = []
    constrains_names = []
    solutions = []

    constrains_names = [x + str(i) for i in range(1, quantity_variables + 1)]
    if problem_type == 1:
        problem_maximization()
        return data
    elif problem_type == 2:
        pass
        # return problem_minimization()


def problem_maximization():
    """
    Realiza las operaciones para maximizar el resultado.
    :return: Nothing
    """

    # se fija la cantidad de variables X finales que están determinadas por la suma
    while len(z_equation) <= (quantity_variables + quantity_constrains): z_equation.append(0)

    filas_finales = construct_table(col_values)

    i = len(constrains_names) + 1

    # agrega las etiquetas de las variables de Holgura más la etiqueta de "Solución"
    while len(constrains_names) < len(filas_finales[0]) - 1:
        constrains_names.append('X' + str(i))
        solutions.append('X' + str(i))
        i += 1
    solutions.append(' Z')
    constrains_names.append('Solution')

    # Se agrega al final del array bidimensional construido la función restricción transformada
    filas_finales.append(z_equation)

    # Se TRANSFORMA el array bidimensional, es decir las filas pasan a ser columnas y viceversa, con el fin de
    # facilitar la extracción de las columnas. Posteriormente el resultado se convierte a una lista
    columnas_finales = np.array(filas_finales).T.tolist()
    maximization(filas_finales, columnas_finales)


def maximization(table_rows, table_columns):
    """
    Se encarga de todo el proceso de determinar los pivotes, aplicar la solución con Gauss hasta terminar :param
    table_rows: Arreglo bidimensional de los valores de las filas de las tablas que se construyen para determinar la
    fila y columna pivote :param table_columns:  Arreglo bidimensional de los valores de las columnas de las tablas
    que se construyen para determinar la fila y columna pivote
    :return: None
    """
    row_app = []
    final_pd = None

    # Obtiene la ultima columna de la tabla (matriz), la función objetivo
    last_row = table_rows[-1]
    # obtiene el elemento menor
    min_last_row = min(last_row)
    min_manager = 1
    print(" 1 TABLA aumentada")
    try:
        # Organiza gráficamente con "pandas" la tabla con sus encabezados y filas
        final_pd = pd.DataFrame(np.array(table_rows), columns=constrains_names, index=solutions)
        print(final_pd)  # imprime la tabla
        result = json.loads(final_pd.to_json(orient='split'))
        print(result)
        data.append(result)
    except Exception as ex:
        print(ex)
        print('  ', constrains_names)
        i = 0
        for cols in table_rows:
            print(solutions[i], cols)
            i += 1

    count = 2
    pivot_element = 2
    while min_last_row < 0 < pivot_element != 1 and min_manager == 1 and count < 6:
        print("\n")
        last_row = table_rows[-1]  # Obtiene la ultima fila
        last_column = table_columns[-1]  # Obtiene la ultima columna
        min_last_row = min(last_row)  # Obtiene el elemento menor de la ultima fila

        # Obtiene la posición del elemento menor de la fila (función objetivo)
        position_less_objective_function = last_row.index(min_last_row)
        # Asigna a la variable cual es la columna objetivo
        pivot_column = table_columns[position_less_objective_function]
        pivot_column_position = table_columns.index(pivot_column)
        # lista que va almacenando los resultados de las divisiones par luego determinar el menor y asi la fila pivote
        division_column_results = []
        i = 0
        for _ in last_column[:-1]:  # toma todos los elementos de la lista, menos el último
            try:
                # empieza a hacer las divisiones para determinar la fila pivote
                val = float(last_column[i] / pivot_column[i])
                if val <= 0:
                    # pone un valor muy grande para ignorarlo cuando se busque el valor mayor a cero para determinar
                    # la fila pivote
                    val = 10000000000
                else:
                    val = val
                division_column_results.append(val)
            except ZeroDivisionError:  # si la division es por cero, entre a la excepción
                # pone un valor muy grande para ignorarlo cuando se busque el valor mayor a cero para determinar la
                # fila pivote
                val = 10000000000
                division_column_results.append(val)
            i += 1
        min_div_val = min(division_column_results)  # obtiene el valor menor de la lista
        # Obtiene la posición del valor menor de la lista
        index_min_div_val = division_column_results.index(min_div_val)
        # Se obtiene el elemento pivote usando la columna pivote y seleccionando el valor de la fila pivote
        pivot_element = pivot_column[index_min_div_val]
        fila_pivote = table_rows[index_min_div_val]
        pivot_position_row = table_rows.index(fila_pivote)
        row_app[:] = []  # [:] significa hacer una copia
        for fila in table_rows:
            if fila is not fila_pivote and fila is not table_rows[-1]:
                # divide los elemento de la columna pivote en el elemento pivote
                form = fila[position_less_objective_function] / pivot_element
                final_val = np.array(fila_pivote) * form  # multiplica el resultado anterior por la fila pivote
                # redondea el resultado usando la cantidad de variables especificadas
                new_col = (np.round((np.array(fila) - final_val), decimals)).tolist()
                # remplaza la fila por la nueva fila. Aplicación de Gauss
                table_rows[table_rows.index(fila)] = new_col

            # si la fila actual es la fila pivote, lo que hace es dividirla por el elemento pivote
            elif fila is fila_pivote:
                new_col = (np.round((np.array(fila) / pivot_element), decimals)).tolist()
                table_rows[table_rows.index(fila)] = new_col
            else:  # detecta que la fila es la función objetivo
                # obtiene el valor absoluto del valor que esta en la columna pivote y lo divide por el pivote
                form = abs(fila[position_less_objective_function]) / pivot_element
                final_val = np.array(fila_pivote) * form
                new_col = (np.round((np.array(fila) + final_val), decimals)).tolist()
                table_rows[table_rows.index(fila)] = new_col
        table_columns[:] = []
        re_filas_tabla = np.array(table_rows).T.tolist()
        # NUEVA TABLA PARA REALIZAR LA SIGUIENTE INTERACCIÓN
        table_columns = table_columns + re_filas_tabla

        if min(division_column_results) != 10000000000:
            min_manager = 1
        else:
            min_manager = 0

        print('pivot element: %s' % pivot_element)
        print('pivot column: ', pivot_column)
        print('pivot row: ', fila_pivote)
        print("\n")

        temp = data[-1]
        temp['pivot_element'] = pivot_element
        temp['pivot_column'] = pivot_column
        temp['pivot_row'] = fila_pivote
        data[-1] = json.dumps(temp)
        # SACA LA VARIABLE Y ENTRA LA VARIABLE DE LA COLUMNA
        solutions[pivot_position_row] = constrains_names[pivot_column_position]

        print(" %d TABLA AUMENTADA" % count)
        try:
            final_pd = pd.DataFrame(np.array(table_rows), columns=constrains_names, index=solutions)
            print(final_pd)

            result = json.loads(final_pd.to_json(orient='split'))
            data.append(result)
        except Exception as exep:
            print(exep)
            print("%d TABLA AU" % count)
            print('  ', constrains_names)
            i = 0
            for cols in table_rows:
                print(solutions[i], cols)
                i += 1
        count += 1
        last_row = table_rows[-1]
        last_column = table_columns[-1]
        min_last_row = min(last_row)
        position_less_objective_function = last_row.index(min_last_row)
        pivot_column = table_columns[position_less_objective_function]
        division_column_results = []
        i = 0
        for _ in last_column[:-1]:
            try:
                val = float(last_column[i] / pivot_column[i])
                if val <= 0:
                    val = 10000000000
                else:
                    val = val
                division_column_results.append(val)
            except ZeroDivisionError:
                val = 10000000000
                division_column_results.append(val)
            i += 1
        min_div_val = min(division_column_results)
        index_min_div_val = division_column_results.index(min_div_val)
        pivot_element = pivot_column[index_min_div_val]
        if pivot_element < 0:
            print(no_solution)

    if not pandas_av:
        print("No installed Pandas module")


def construct_table(column_values):
    """
    A partir de la información ingresada por el usuario, se construye la "tabla" en array bidimensional. Se agregan
    los respectivos unos en cada función restricción debido a que se agregan variables de holgura
    """

    #  Transforma la lista column_values a un array multidimensional
    final_cols = [column_values[i:(i + quantity_variables + 1)]
                  for i in range(0, len(column_values), quantity_variables + 1)]

    #  Se agregan ceros a las variables de las funciones restricción donde se agregaron variables de holgura
    for cols in final_cols:
        while len(cols) < (quantity_variables + quantity_constrains):
            cols.insert(-1, 0)

    i = quantity_variables

    # agrega los unos cuando se agregan variables de holgura
    for sub_col in final_cols:
        sub_col.insert(i, 1)
        i += 1

    return final_cols
