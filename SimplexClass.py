from simplex import principal


class Simplex:
    quantity_variables = 0
    quantity_constrains = 0
    col_values = 0
    z_equation = 0

    # parameterized constructor
    def __init__(self, quantity_variables, quantity_constrains, col_values, z_equation):
        self.quantity_variables = quantity_variables
        self.quantity_constrains = quantity_constrains
        self.col_values = col_values
        self.z_equation = z_equation

    def display(self):
        print("Cantidad de variables: " + str(self.quantity_variables))
        print("Cantidad de contrains: " + str(self.quantity_constrains))
        print("Columnas: " + str(self.col_values))
        print("Función objetivo: " + str(self.z_equation))

    def calculate(self):
        print("Aca se podrian empezar a hacer las operaciones")
        principal()
        # self.col_values = self.cantidad_variables + self.cantidad_constrains

    # creating object of the class
