import classes as cs

def main():

    week_ = cs.week()

    # Añadir 2 materia a la semana
    week_.addMateria()
    week_.addMateria()

    # Printear materias añadidas
    week_.print_materias()



main()