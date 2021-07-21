from argparse import ArgumentParser
from horario import DAYS, SaveManager
import ui

# Esto es un test para mostrar info en el horario, borrar eventualmente
# TO DO: Borrar esto al finalizar tests
def test():
    hrs_days = []

    for i in range(7):
        hrs_days.append([])
        for j in range(13):
            if j % 2 == 0:
                hrs_days[i].append(None)
            else:
                hrs_days[i].append("nombre_materia")

    return hrs_days

def graphical_ui(week):
    # ----- Ventana ----- #

    vistos = week.get_vistos()
    favoritos = week.get_favoritos()
    # Aqui iran los frames
    frames = {}

    # Aqui van los gadgets de la matriz horarios
    h_gadgets = []

    # Aqui los labels de los días y las horas del horario
    labels_days = []
    labels_hrs = []

    # TO DO: ESTO ES UN TEST, BORRAR EVENTUALMENTE
    hrs_days = test()

    # Crear Ventana
    w = ui.create_window()

    # Crear frames
    ui.create_frames(w, frames)

    # Llenar grid de Horario
    ui.horario_fill(frames["horario"], h_gadgets, week, labels_days, labels_hrs)

    # Crear botones de opciones
    ui.create_option_buttons(frames, week, h_gadgets, vistos,favoritos)

    # Loop de ejecución de la ventana
    w.mainloop()

    # ----- END VENTANA ----- #


def cmd_ui(week):
    vistos = week.get_vistos()
    ##print("hola")
    while True:
        # Escoger opcion
        operation = ui.choose_from(**ui.MAIN_MENU)
        if callable(operation):
            if operation == ui.print_vistos:
                operation(week.get_vistos())
            else:
                operation(week)
        else:
            return 0

# Una clase "week" contiene 7 objetos "day" y 1 objeto "Materia"
def main(gui=None):
    ##print(gui)
    with SaveManager() as week:
        if gui is True:
            print(1)
            return graphical_ui(week, week.lista_vistos)
        if gui is False:
            print(2)
            return cmd_ui(week, week.lista_vistos)
        if gui is None:
            print(3)
            return graphical_ui(week)
            '''try:
                return graphical_ui(week)
            except Exception:
                print("hola2")
                return cmd_ui'''


if __name__ == "__main__":
    parser = ArgumentParser('Prototipo 2')
    parser.add_argument('--gui', action="store_true", default=None)
    parser.add_argument('--no-gui', action="store_false", default=None, dest='gui')
    #print(parser)
    main(**vars(parser.parse_args()))
