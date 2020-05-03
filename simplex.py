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

    col_values = col_values1
    z_equation = z_equation1
    quantity_constrains = quantity_constrains1
    quantity_variables = quantity_variables1

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


def maximization(filas_tabla, columnas_tabla):
    row_app = []
    ultima_fila = filas_tabla[-1]  # Obtiene la ultima columna de la tabla (matriz) es decir la funcion objetivo
    min_last_row = min(ultima_fila)  # obtiene el elemento menor
    min_manager = 1
    print(" 1 TABLEAU")
    try:
        final_pd = pd.DataFrame(np.array(filas_tabla), columns=constrains_names,
                                index=solutions)  # Organiza graficamente con pandas la tabla con sus encabezados y filas
        print(final_pd)  # imprime la tabla
        result = json.loads(final_pd.to_json(orient='split'))
        print(result)
        data.append(result)

    except:
        print('  ', constrains_names)
        i = 0
        for cols in filas_tabla:
            print(solutions[i], cols)
            i += 1
    count = 2
    pivot_element = 2
    while min_last_row < 0 < pivot_element != 1 and min_manager == 1 and count < 6:
        print("*********************************************************")
        ultima_fila = filas_tabla[-1]  # Obtiene la ultima columna
        ultima_columna = columnas_tabla[-1]  # Obtiene la ultima columna (lo hace usando la matriz transpuesta)
        min_last_row = min(ultima_fila)  # Obtiene el elemento menor de la
        posicion_menor_funcion_objetivo = ultima_fila.index(
            min_last_row)  # Obtiene la posicion del elemento menor de la fila (funcion objetivo)
        columna_pivote = columnas_tabla[
            posicion_menor_funcion_objetivo]  # Asigna a la variable cual es la columna objetivo
        posicion_pivote_col = columnas_tabla.index(columna_pivote)
        columna_resultado_divisiones = []  # lista que va almacenando los resultados de las divisiones par luego determinar el menor y asi la fila pivote
        i = 0
        for _ in ultima_columna[:-1]:  # toma todos los elementos de la lista, menos el ultimo
            try:
                val = float(ultima_columna[i] / columna_pivote[
                    i])  # empieza a hacer las divisiones para determinar la fila pivote
                if val <= 0:
                    val = 10000000000  # pone un valor muy grande para ignorarlo cuadno se busque el valor mayor a cero para determinar la fila pivote
                else:
                    val = val
                columna_resultado_divisiones.append(val)
            except ZeroDivisionError:  # si la division es por cero, entre a la excepcion
                val = 10000000000  # pone un valor muy grande para ignorarlo cuadno se busque el valor maypr a cero para determinar la fila pivote
                columna_resultado_divisiones.append(val)
            i += 1
        min_div_val = min(columna_resultado_divisiones)  # obtiene el valor menor de la lista
        index_min_div_val = columna_resultado_divisiones.index(
            min_div_val)  # Obtiene la posicion del valor menor de la lista
        pivot_element = columna_pivote[
            index_min_div_val]  # Se obtiene el elemento pivote usando la columna pivote y seleccionando el valor de la fila pivote
        fila_pivote = filas_tabla[index_min_div_val]
        posicion_pivote_fila = filas_tabla.index(fila_pivote)
        row_app[:] = []  # [:] significa hacer una copia
        for fila in filas_tabla:
            if fila is not fila_pivote and fila is not filas_tabla[-1]:
                form = fila[
                           posicion_menor_funcion_objetivo] / pivot_element  # divide los elemento de la columna pivote en el elemento pivote
                final_val = np.array(fila_pivote) * form  # multplica el resultado anterior por la fila pivote
                new_col = (np.round((np.array(fila) - final_val),
                                    decimals)).tolist()  # redonde el resultado usando la cantidad de variables especificacdas
                filas_tabla[filas_tabla.index(
                    fila)] = new_col  # remplaza la fila por la nueva fila(es como si se estubiera haciendo gauss aqui)

            elif fila is fila_pivote:  # si la fila actual es la fila pivote, lo que hace es dividirla por el elemento pivote
                new_col = (np.round((np.array(fila) / pivot_element), decimals)).tolist()
                filas_tabla[filas_tabla.index(fila)] = new_col
            else:  # detecta que la fila es la funcion objetivo
                form = abs(fila[
                               posicion_menor_funcion_objetivo]) / pivot_element  # obtiene el valor absoluto del valor que esta en la columna pivote y lo divide por el pivote
                final_val = np.array(fila_pivote) * form
                new_col = (np.round((np.array(fila) + final_val), decimals)).tolist()
                filas_tabla[filas_tabla.index(fila)] = new_col
        columnas_tabla[:] = []
        re_filas_tabla = np.array(filas_tabla).T.tolist()
        columnas_tabla = columnas_tabla + re_filas_tabla  # NUEVA TABLA PARA REALIZAR SIMPLEX

        if min(columna_resultado_divisiones) != 10000000000:
            min_manager = 1
        else:
            min_manager = 0
        print(type(data[-1]))
        temp = data[-1]
        # temp = json.loads(data[-1])
        print('pivot element: %s' % pivot_element)
        temp['pivot_element'] = pivot_element
        print('pivot column: ', columna_pivote)
        temp['pivot_column'] = columna_pivote
        print('pivot row: ', fila_pivote)
        temp['pivot_row'] = fila_pivote
        json.dumps(temp)
        data[-1] = temp
        print("\n")
        solutions[posicion_pivote_fila] = constrains_names[
            posicion_pivote_col]  # SACA LA VARIABLE Y ENTRA LA VARIABLE DE LA COLUMNA

        print(" %d TABLA AU" % count)
        try:
            final_pd = pd.DataFrame(np.array(filas_tabla), columns=constrains_names, index=solutions)
            result = json.loads(final_pd.to_json(orient='split'))
            print(result)
            data.append(result)
            print(final_pd)
        except:
            print("%d TABLEAU" % count)
            print('  ', constrains_names)
            i = 0
            for cols in filas_tabla:
                print(solutions[i], cols)
                i += 1
        count += 1
        ultima_fila = filas_tabla[-1]
        ultima_columna = columnas_tabla[-1]
        min_last_row = min(ultima_fila)
        posicion_menor_funcion_objetivo = ultima_fila.index(min_last_row)
        columna_pivote = columnas_tabla[posicion_menor_funcion_objetivo]
        columna_resultado_divisiones = []
        i = 0
        for _ in ultima_columna[:-1]:
            try:
                val = float(ultima_columna[i] / columna_pivote[i])
                if val <= 0:
                    val = 10000000000
                else:
                    val = val
                columna_resultado_divisiones.append(val)
            except ZeroDivisionError:
                val = 10000000000
                columna_resultado_divisiones.append(val)
            i += 1
        min_div_val = min(columna_resultado_divisiones)
        index_min_div_val = columna_resultado_divisiones.index(min_div_val)
        pivot_element = columna_pivote[index_min_div_val]
        # # -------------------------No se emplean denuevo------------------------
        # fila_pivote = filas_tabla[index_min_div_val]
        # posicion_pivote_fila = filas_tabla.index(fila_pivote)
        # row_app[:] = []  # [:] significa hacer una copia
        # -------------------------------------------------
        if pivot_element < 0:
            print(no_solution)

    if not pandas_av:
        print("""
        Please install pandas to make your tables look good
        install using command $pip install pandas 
        """)


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
