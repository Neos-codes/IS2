import classes as cs


#TO DO:
#   - Manejar programa completo por consola
#   - Hacer que imprima mas legible (aunque funciona tal como está)

# Una clase "week" contiene 7 objetos "day" y 1 objeto "Materia"

week_ = cs.week()

# Añadir 2 materia a la semana
week_.addMateria()
week_.addMateria()

# Printear materias añadidas
week_.print_materias()