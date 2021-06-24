from horario import Week, DAYS, check_save, load_save, save
from vistos import ListaVistos
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


# Una clase "week" contiene 7 objetos "day" y 1 objeto "Materia"
def main():

    if check_save():
        week = load_save()
    else:
        week = Week()
    vistos = ListaVistos()

    
    # ----- Ventana ----- #

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
    ui.create_option_buttons(frames["horario"], frames["opciones"], week, h_gadgets, vistos)

    # Loop de ejecución de la ventana
    w.mainloop()

    # ----- END VENTANA ----- #


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
