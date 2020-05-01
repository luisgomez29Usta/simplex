import sys
import numpy as np
import json
from fractions import Fraction

try:
    import pandas as pd

    pandas_av = True
except ImportError:
    pandas_av = False
    pass

# quantity_variables = 2
decimals = 9
problem_type = 1
# quantity_constrains = 3
constrains_names = ['constrain1', 'constrain2', 'constrain3']  # nombre de las variables, no la usaremos
# col_values = [1.0, 0.0, 4.0, 0.0, 2.0, 12.0, 3.0, 2.0, 18.0]; z_equation = [-3, -5]  # ecuacion z
final_rows = []  #
solutions = []  # 'X3', 'X4', 'X5', 'Z'
data = []
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

    :param quantity_variables1:
    :param quantity_constrains1:
    :param col_values1:
    :param z_equation1:
    :return:
    """
    global decimals
    global quantity_constrains
    global quantity_variables  # Cantidad de contrains y variables respectivamente
    global contrains_names
    global col_values
    global z_equation
    global data

    col_values = col_values1
    z_equation = z_equation1
    quantity_constrains = quantity_constrains1
    quantity_variables = quantity_variables1
    # tipo de problema: 1 para maximizar y 2 para minimizar

    contrains_names = [x + str(i) for i in range(1, quantity_variables + 1)]  # Depende de la cantidad de variables
    # const_names = ['X1', 'X2'] #Depende de la cantidad de variables
    if problem_type == 1:  # Entra a maximizacion
        return problem_maximization()

    elif problem_type == 2:
        return problem_minimization()

    else:
        sys.exit("you enter a wrong problem choice ->" + str(problem_type))


def problem_maximization():
    while len(z_equation) <= (
            quantity_variables + quantity_constrains):  # se hace porque la cantidad de variables finales (variables mas variebles de olgura) son la suma de estos
        z_equation.append(0)

    # Crea la tabla para empezar el metodo simplex
    filas_finales = stdz_rows(col_values)
    i = len(contrains_names) + 1
    # agrega las estiquetas X de variables de holgura
    while len(contrains_names) < len(filas_finales[0]) - 1:
        contrains_names.append('X' + str(i))
        solutions.append('X' + str(i))
        i += 1
    solutions.append(' Z')
    contrains_names.append('Solution')
    filas_finales.append(z_equation)  # Se agrega a la tabla la funcion restricion transformada
    columnas_finales = np.array(
        filas_finales).T.tolist()  # Se transforma la matriz y luego se convierte a una lista
    print('\n##########################################')
    maximization(filas_finales, columnas_finales)
    return data


def problem_minimization():
    for i in contrains_names:
        try:
            val = float(Fraction(input("enter the value of %s in Z equation: >" % i)))
        except ValueError:
            print("please enter a number")
            val = float(Fraction(input("enter the value of %s in Z equation: >" % i)))
        z_equation.append(val)
    z_equation.append(0)

    while len(z_equation) <= (quantity_variables + quantity_constrains):
        z_equation.append(0)
    print("__________________________________________________")
    for variable in constrains_names:
        for temp in contrains_names:
            try:
                val = float(Fraction(input("enter the value of %s in %s: >" % (temp, variable))))
            except ValueError:
                print("please ensure you enter a number")
                val = float(Fraction(input("enter the value of %s in %s: >" % (temp, variable))))
            col_values.append(val)
        equate_prod = float(Fraction(input('equate %s to: >' % variable)))
        col_values.append(equate_prod)

    filas_finales = stdz_rows2(col_values)
    i = len(contrains_names) + 1
    while len(contrains_names) < quantity_constrains + quantity_variables:
        contrains_names.append('X' + str(i))
        solutions.append('X' + str(i))
        i += 1
    solutions.append(' Z')
    solutions[:] = []
    add_from = len(contrains_names) + 1
    while len(contrains_names) < len(filas_finales[0][:-1]):
        removable_vars.append('X' + str(add_from))
        contrains_names.append('X' + str(add_from))
        add_from += 1
    removable_vars.append(' Z')
    removable_vars.append('Z1')
    contrains_names.append('Solution')
    for ems in removable_vars:
        solutions.append(ems)
    while len(z_equation) < len(filas_finales[0]):
        z_equation.append(0)
    filas_finales.append(z_equation)
    filas_finales.append(z2_equation)
    columnas_finales = np.array(filas_finales).T.tolist()
    print('\n##########################################')
    minimization(filas_finales, columnas_finales)
    print(data)


def maximization(filas_tabla, columnas_tabla):
    row_app = []
    ultima_fila = filas_tabla[-1]  # Obtiene la ultima culumna de la tabla (matriz) es decir la funcion objetivo
    min_last_row = min(ultima_fila)  # obtiene el elemento menor
    min_manager = 1
    print(" 1 TABLEAU")
    try:
        final_pd = pd.DataFrame(np.array(filas_tabla), columns=contrains_names,
                                index=solutions)  # Organiza graficamente con pandas la tabla con sus encabezados y filas
        print(final_pd)  # imprime la tabla
        result = json.loads(final_pd.to_json(orient='split'))
        print(result)
        data.append(result)

    except:
        print('  ', contrains_names)
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
        solutions[posicion_pivote_fila] = contrains_names[
            posicion_pivote_col]  # SACA LA VARIABLE Y ENTRA LA VARIABLE DE LA COLUMNA

        print(" %d TABLA AU" % count)
        try:
            final_pd = pd.DataFrame(np.array(filas_tabla), columns=contrains_names, index=solutions)
            result = json.loads(final_pd.to_json(orient='split'))
            print(result)
            data.append(result)
            print(final_pd)
        except:
            print("%d TABLEAU" % count)
            print('  ', contrains_names)
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


def minimization(final_cols, final_rows):
    row_app = []
    last_col = final_cols[-1]
    min_last_row = min(last_col)
    min_manager = 1
    print("1 TABLEAU")
    try:
        fibal_pd = pd.DataFrame(np.array(final_cols), columns=contrains_names, index=solutions)
        print(fibal_pd)
    except:
        print('  ', contrains_names)
        i = 0
        for cols in final_cols:
            print(solutions[i], cols)
            i += 1
    count = 2
    pivot_element = 2
    while min_last_row < 0 < pivot_element and min_manager == 1:
        print("*********************************************************")
        last_col = final_cols[-1]
        last_row = final_rows[-1]
        min_last_row = min(last_col[:-1])
        index_of_min = last_col.index(min_last_row)
        pivot_row = final_rows[index_of_min]
        index_pivot_col = final_rows.index(pivot_row)
        row_div_val = []
        i = 0
        for _ in last_row[:-2]:
            try:
                val = float(last_row[i] / pivot_row[i])
                if val <= 0:
                    val = 10000000000
                else:
                    val = val
                row_div_val.append(val)
            except ZeroDivisionError:
                val = 10000000000
                row_div_val.append(val)
            i += 1
        min_div_val = min(row_div_val)
        index_min_div_val = row_div_val.index(min_div_val)
        pivot_element = pivot_row[index_min_div_val]
        pivot_col = final_cols[index_min_div_val]
        index_pivot_raw = final_cols.index(pivot_col)
        row_app[:] = []
        for col in final_cols:
            if col is not pivot_col and col is not final_cols[-1]:
                form = col[index_of_min] / pivot_element
                final_form = np.array(pivot_col) * form
                new_col = (np.round((np.array(col) - final_form), decimals)).tolist()
                final_cols[final_cols.index(col)] = new_col
            elif col is pivot_col:
                new_col = (np.round((np.array(col) / pivot_element), decimals)).tolist()
                final_cols[final_cols.index(col)] = new_col
            else:
                form = abs(col[index_of_min]) / pivot_element
                final_form = np.array(pivot_col) * form
                new_col = (np.round((np.array(col) + final_form), decimals)).tolist()
                final_cols[final_cols.index(col)] = new_col
        final_rows[:] = []
        re_final_rows = np.array(final_cols).T.tolist()
        final_rows = final_rows + re_final_rows
        if min(row_div_val) != 10000000000:
            min_manager = 1
        else:
            min_manager = 0
        print('pivot element: %s' % pivot_element)
        print('pivot column: ', pivot_row)
        print('pivot row: ', pivot_col)
        print("\n")
        removable = solutions[index_pivot_raw]
        solutions[index_pivot_raw] = contrains_names[index_pivot_col]
        if removable in removable_vars:
            idex_remove = contrains_names.index(removable)
            for colms in final_cols:
                colms.remove(colms[idex_remove])
            contrains_names.remove(removable)
        print("%d TABLEAU" % count)
        try:
            fibal_pd = pd.DataFrame(np.array(final_cols), columns=contrains_names, index=solutions)
            print(fibal_pd)
        except:
            print('  ', contrains_names)
            i = 0
            for cols in final_cols:
                print(solutions[i], cols)
                i += 1
        count += 1
        final_rows[:] = []
        new_final_rows = np.array(final_cols).T.tolist()
        for _list in new_final_rows:
            final_rows.append(_list)

        last_col = final_cols[-1]
        last_row = final_rows[-1]
        min_last_row = min(last_col[:-1])
        index_of_min = last_col.index(min_last_row)
        pivot_row = final_rows[index_of_min]
        row_div_val = []
        i = 0
        for _ in last_row[:-2]:
            try:
                val = float(last_row[i] / pivot_row[i])
                if val <= 0:
                    val = 10000000000
                else:
                    val = val
                row_div_val.append(val)
            except ZeroDivisionError:
                val = 10000000000
                row_div_val.append(val)
            i += 1
        min_div_val = min(row_div_val)
        index_min_div_val = row_div_val.index(min_div_val)
        pivot_element = pivot_row[index_min_div_val]
        if pivot_element < 0:
            print(no_solution)

    if not pandas_av:
        print("""
        Please install pandas to make your tables look good
        install using command $pip install pandas 
        """)


def stdz_rows2(column_values):
    final_cols = [column_values[x:x + quantity_variables + 1] for x in
                  range(0, len(column_values), quantity_variables + 1)]
    sum_z = (0 - np.array(final_cols).sum(axis=0)).tolist()
    for _list in sum_z:
        z2_equation.append(_list)

    for cols in final_cols:
        while len(cols) < (quantity_variables + (2 * quantity_constrains) - 1):
            cols.insert(-1, 0)

    i = quantity_variables
    for sub_col in final_cols:
        sub_col.insert(i, -1)
        z2_equation.insert(-1, 1)
        i += 1

    for sub_col in final_cols:
        sub_col.insert(i, 1)
        i += 1

    while len(z2_equation) < len(final_cols[0]):
        z2_equation.insert(-1, 0)

    return final_cols


def stdz_rows(column_values):
    """
    range(#,#, salto: cuanto va a ser el salto)
    """
    final_cols = [column_values[x:x + quantity_variables + 1]
                  # toma los valores desde la posicion inicial en el for hasta la cantidad de variables mas 1, es decir la cantidad de varibles que deben ir por fila
                  for x in
                  range(0, len(column_values),
                        quantity_variables + 1)]  # crea una matriz donde cada fila es una restriccion

    for cols in final_cols:
        while len(cols) < (quantity_variables + quantity_constrains):
            cols.insert(-1, 0)

    i = quantity_variables

    for sub_col in final_cols:  # agrega los unos que se suelen agregar cuando se agregan variables de olgura
        sub_col.insert(i, 1)
        i += 1  # aumente para agregar el uno en la siguiente columna

    return final_cols

# I use python list and arrays(numpy) in most of this program
# it became simple coz python has a strong power in list and array manipulation and solution
