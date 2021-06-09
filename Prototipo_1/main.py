from horario import Week, DAYS, check_save, load_save, save
from vistos import ListaVistos
import ui

# Una clase "week" contiene 7 objetos "day" y 1 objeto "Materia"
def main():
    if check_save():
        week = load_save()
    else:
        week = Week()
    vistos = ListaVistos()
    while True:
        # Escoger opcion
        operation = ui.choose_from(**ui.MAIN_MENU)
        if callable(operation):
            if(operation==ui.get_video):
                operation(week, vistos)
            elif(operation==ui.print_vistos): 
                operation(vistos)
            else:
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
