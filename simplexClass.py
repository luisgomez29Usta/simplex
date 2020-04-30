from .simplex import *


class Simplex:
    cantidad_variables = 0
    cantidad_constrains = 0
    col_values = 0
    ecuacion_Z = 0

    # parameterized constructor
    def __init__(self, cant_variables, cant_contrains, col_values,  ecuacion_Z):
        self.cantidad_variables = cant_variables
        self.cantidad_constrains = cant_contrains
        self.col_values = col_values
        self.ecuacion_Z = ecuacion_Z

    def display(self):
        print("Cantidad de variables: " + str(self.cantidad_variables))
        print("Cantidad de contrains: " + str(self.cantidad_constrains))
        print("Columnas: " + str(self.col_values))
        print("Función objetivo: " + str(self.ecuacion_Z))

    def calculate(self):
        print("Aca se podrian empezar a hacer las operaciones")
        principal()
        # self.col_values = self.cantidad_variables + self.cantidad_constrains

    # creating object of the class


