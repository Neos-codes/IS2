from horario import Week, DAYS, check_save, load_save, save
import ui

# Una clase "week" contiene 7 objetos "day" y 1 objeto "Materia"
def main():
    if check_save():
        week = load_save()
    else:
        week = Week()
    while True:
        # Escoger opcion
        operation = ui.choose_from(**ui.MAIN_MENU)
        if operation:
            operation(week)
        else:
            if save(week):
                print("El programa a terminado exitosamente.")
                return 0
            else:
                print("No se a podido guardar el horario.")
                return 1

if __name__ == "__main__":
    main()
