import classes as cs


# Una clase "week" contiene 7 objetos "day" y 1 objeto "Materia"
week_ = cs.week()

if week_.get_nMaterias() == 0:
    print("Bienvenido! Aun no ha agregado ninguna materia a su horario, ahora agregaremos una")
    week_.addMateria()

while 1:
    option = -1
    while 1:
        # Escoger opcion
        print("Que desea hacer? (Ingrese numero)")
        print("1. Ver mi horario   2. Ver mis materias   3. Añadir un materia   4. Añadir horas a una materia   5. Salir")
        option = int(input())
        # Verificar entrada
        if option > 0 and option < 6:
            break
        else:
            print("Opcion invalida, ingrese nuevamente")

    if option == 1:
        week_.print_horario()    # Revisar este metodo
    elif option == 2:
        week_.print_materias()
    elif option == 3:
        week_.addMateria()
    elif option == 4:
        week_.add_hora()
    else:
        exit()