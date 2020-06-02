# import sys  # provee acceso a funciones y objetos mantenidos por del intérprete.
import numpy as np  # da mayor soporte para el manejo de vectores y matrices
import json  # permite la manipulación de tipos de datos json

# from fractions import Fraction  # para convertir números decimales a fracciones

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

count = 0

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
    Función principal que recibe la información necesaria para aplicar el método simplex

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

    :return: None
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


def find_pivot(last_column, pivot_column):
    """
    Encuentra el elemento pivote teniedo en cuenta la columna pivote y la función objetivo
    :param last_column: función objetivo.
    :param pivot_column: columna pivote
    :return:elemento pivote, elemento menor, resultados de las divisiones
    """

    division_column_results = []

    i = 0
    for _ in last_column:
        try:
            # empieza a hacer las divisiones para determinar la fila pivote
            val = float(last_column[i] / pivot_column[i])
            # pone un valor muy grande para ignorarlo cuando se busque el valor mayor a cero para determinar
            # la fila pivote
            if val <= 0:
                val = 10000000000
            else:
                val = val
            division_column_results.append(val)
        except ZeroDivisionError:
            # pone un valor muy grande para ignorarlo cuando se busque el valor mayor a cero para determinar la
            # fila pivote
            val = 10000000000
            division_column_results.append(val)
        i += 1
    # obtiene el valor menor de la lista
    min_div_val = min(division_column_results)
    # Obtiene la posición del valor menor de la lista
    index_min_div_val = division_column_results.index(min_div_val)
    pivot_element = pivot_column[index_min_div_val]
    return pivot_element, index_min_div_val, division_column_results


def applying_gauss(table_rows, pivot_row, position_min_last_row, pivot_element):
    """
    Aplica gauss para solucionar la matriz
    :param table_rows: matriz
    :param pivot_row: fila pivote
    :param position_min_last_row: posición del valor más menor en la función Z
    :param pivot_element: elemento pivote
    :return: nueva matriz con los nuevos valores
    """
    for fila in table_rows:
        if fila is not pivot_row and fila is not table_rows[-1]:
            # divide los elementos de la columna pivote en el elemento pivote
            form = fila[position_min_last_row] / pivot_element
            final_val = np.array(pivot_row) * form  # multiplica el resultado anterior por la fila pivote
            # redondea el resultado usando la cantidad de variables especificadas
            new_col = (np.round((np.array(fila) - final_val), decimals)).tolist()
            # remplaza la fila por la nueva fila. Aplicación de Gauss
            table_rows[table_rows.index(fila)] = new_col

        # si la fila actual es la fila pivote, lo que hace es dividirla por el elemento pivote
        elif fila is pivot_row:
            new_col = (np.round((np.array(fila) / pivot_element), decimals)).tolist()
            table_rows[table_rows.index(fila)] = new_col
        else:  # detecta que la fila es la función objetivo
            # obtiene el valor absoluto del valor que esta en la columna pivote y lo divide por el pivote
            form = abs(fila[position_min_last_row]) / pivot_element
            final_val = np.array(pivot_row) * form
            new_col = (np.round((np.array(fila) + final_val), decimals)).tolist()
            table_rows[table_rows.index(fila)] = new_col
    return table_rows


def maximization(table_rows, table_columns):
    """
    Se encarga de all el proceso de determinar los pivotes, aplicar la solución con Gauss hasta terminar

    :param table_rows: Arreglo bidimensional de los valores de las filas de las tablas que se construyen para determinar
    la fila y columna pivote
    :param table_columns: Arreglo bidimensional de los valores de las columnas de las tablas
    que se construyen para determinar la fila y columna pivote
    :return: None
    """
    row_app = []
    global count

    # Obtiene la ultima columna de la tabla (matriz), la función objetivo
    last_row = table_rows[-1]
    # obtiene el elemento menor
    min_last_row = min(last_row)
    min_manager = 1

    print_tables(table_rows)

    count = 2
    pivot_element = 2

    while min_last_row < 0 < pivot_element != 1 and min_manager == 1 and count < 6:
        last_row = table_rows[-1]  # Obtiene la ultima fila
        last_column = table_columns[-1]  # Obtiene la ultima columna
        min_last_row = min(last_row)  # Obtiene el elemento menor de la ultima fila

        # Obtiene la posición del elemento menor de la fila (función objetivo)
        position_min_last_row = last_row.index(min_last_row)
        # Asigna a la variable cual es la columna objetivo
        pivot_column = table_columns[position_min_last_row]
        pivot_column_position = table_columns.index(pivot_column)
        # lista que va almacenando los resultados de las divisiones par luego determinar el menor y asi la fila pivote

        pivot_and_index_and_division_results = find_pivot(last_column[:-1], pivot_column)
        division_column_results = pivot_and_index_and_division_results[2]
        pivot_element = pivot_and_index_and_division_results[0]
        pivot_row = table_rows[pivot_and_index_and_division_results[1]]
        pivot_position_row = table_rows.index(pivot_row)
        row_app[:] = []  # [:] significa hacer una copia

        # Se hace la aplicación de Gauss
        table_rows = applying_gauss(table_rows, pivot_row, position_min_last_row, pivot_element)

        table_columns[:] = []
        re_filas_tabla = np.array(table_rows).T.tolist()
        #  Se hace una lista bidimensional de las columnas
        table_columns = table_columns + re_filas_tabla

        if min(division_column_results) != 10000000000:
            min_manager = 1
        else:
            min_manager = 0

        add_pivots_array(pivot_element, pivot_column, pivot_row)

        # SACA LA VARIABLE Y ENTRA LA VARIABLE DE LA COLUMNA
        solutions[pivot_position_row] = constrains_names[pivot_column_position]

        print_tables(table_rows, False)

        count += 1
        last_row = table_rows[-1]
        last_column = table_columns[-1]
        min_last_row = min(last_row)
        position_min_last_row = last_row.index(min_last_row)
        pivot_column = table_columns[position_min_last_row]

        if find_pivot(last_column[:-1], pivot_column)[0] < 0:
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


def add_pivots_array(pivot_element, pivot_column, pivot_row):
    """
    Concatena elementos a array resultado final
    :param pivot_element: elemento pivote de la solución del paso
    :param pivot_column: columna pivote de la solución del paso
    :param pivot_row: fila pivote de la solución del paso actual
    :return:
    """
    print("\n")
    print('pivot element: %s' % pivot_element)
    print('pivot column: ', pivot_column)
    print('pivot row: ', pivot_row)

    temp = data[-1]
    temp['pivot_element'] = pivot_element
    temp['pivot_column'] = pivot_column
    temp['pivot_row'] = pivot_row
    json.dumps(temp)
    data[-1] = temp


def print_tables(table_rows, is_first=True):
    global count

    if is_first:
        print(" 1 tabla aumentada")
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
    else:
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
