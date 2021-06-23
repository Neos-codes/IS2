from recomendar import recomendar_un_video
import horario
import time
import vistos
import tkinter as tk

days_names = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
hours_day = list(range(8, 21))

# Crear ventana
def create_window():
    window = tk.Tk()
    window.title("Prototipo")   # Aqui debería ir el nombre del SW

    return window

# Crear Frames
def create_frames(window, frames: dict):
    # Para el horario
    horario = tk.LabelFrame(window, text = "Horario", padx = 5, pady = 5)
    horario.grid(row = 0, column = 1)
    frames["horario"] = horario

    # Para los botones de opciones
    options = tk.LabelFrame(window, text = "Opciones", padx = 5, pady = 5)
    options.grid(row = 0, column = 0)
    frames["opciones"] = options

def asignar_hora(dia: int, hora: int, materia: str):
    #print("EN CONSTRUCCION dia:" + str(days_names[dia - 1]) + "hora:" + str(hora + 7) + "materia:" + materia)
    print(dia)
    print(hora)
    print(materia)

# Rellenar horas del horario
# TO DO: AÑADIR NUEVO PARAMETRO PARA SACAR LOS NOMBRE DE LAS MATERIAS EN LA HORA DEL DIA
def horario_fill(frame, gadgets: list, week, labels_days: list, labels_hrs: list, hrs_days: list):
    # Agregar opcion "Asignar" a las materias para el boton de opciones
    materias = week._mats_order + ["---"]
    
    # Crear labels de los días en el horario
    for i in range(7):
        new_label = tk.Label(frame, text = days_names[i], padx = 30, pady = 10)
        labels_days.append(new_label)
        new_label.grid(row = 0, column = i + 1)
    
    # Crear labels de las horas en el horario
    for i in range(13):
        new_label = tk.Label(frame, text = str(hours_day[i]), padx = 5, pady = 8)
        labels_hrs.append(new_label)
        new_label.grid(row = i + 1, column = 0)

    for i in range(7):
        gadgets.append([])   # Añadimos una lista para los gadgets del día "i"
        for j in range(13):  # Por cada hora del día "i"
            # Si en hrs_days hay un "None", se coloca el boton agregar
            if hrs_days[i][j] == None:
                clicked = tk.StringVar()
                clicked.set(materias[len(materias) - 1].title())
                foo = lambda materia = clicked.get(), dia = i + 1, hr = j + 1: asignar_hora(dia, hr, materia)
                new_options = tk.OptionMenu(frame, clicked, *materias, command = foo)
                gadgets[i].append(new_options)
                new_options.grid(row = j + 1, column = i + 1)
            # Si hay una materia, se coloca el nombre de la materia
            # TO DO: Aqui deberiamos reemplazar materia por el nombre de la materia en la hora del dia
            else:
                new_text = tk.Label(frame, text = "Materia", padx = 5, pady = 8)  # Completar
                gadgets[i].append(new_text)
                new_text.grid(row = j + 1, column = i + 1)


# Botones para añadir materia, ver historia, etc
# TO DO: Terminar las funciones lambda
def create_option_buttons(frame):
    # Añadir materia
    new_materia = tk.Button(frame, text = "Añadir Materia", command = lambda: print("Nueva materia añadida"))
    new_materia.grid(row = 0, column = 0)
    # Recomendar
    recomendar = tk.Button(frame, text = "Ver videos recomendados", command = lambda: print("Ver videos recomendados"))
    recomendar.grid(row = 1, column = 0)
    # Historial
    historial = tk.Button(frame, text = "Ver historial", command = lambda: print("Ver historial"))
    historial.grid(row = 2, column = 0)
    # Favoritos
    favoritos = tk.Button(frame, text = "Videos Favoritos", command = lambda: print("Mostrar videos favoritos"))
    favoritos.grid(row = 3, column = 0)

def choose_from(choices, prompt_choices="Opciones: ", prompt_input="Ingrece opcion: ", prompt_fail="Opcion no es valida.", prompt_go_back="Volver atras.", go_back_option=True):
    print(prompt_choices)
    if not isinstance(choices, list):
        choices = list(choices)
    if go_back_option:
        choices = choices + [(-1, prompt_go_back)]
    valid_choices = set(range(len(choices)))
    for i, (value, label) in enumerate(choices):
        if label is None:
            label = value
        print(f"{i}.", label)
    while True:
        index = input(prompt_input).lower()
        if index.isdigit():
            index = int(index)
        if index in valid_choices:
            value, label = choices[index]
            return value
        print(prompt_fail)


def new_materia(week: horario.Week):
    while True:
        name = input("Ingrese nombre de nueva materia: ").lower()
        if name not in week.materias:
            week.add_materia(name)
            return name
        print("Materia {name} ya existe.")


def print_horario(week: horario.Week):
    print(week)


def print_materias(week: horario.Week):
    print("Materias:")
    print(' '.join(week.materias))
    print()


def add_horario_to_materia(week: horario.Week, horario=None):
    if horario is None:
        prompr_materia = "Agregar materia:"
    else:
        prompr_materia = f"Agregar a dia {horario.day.name} a las {horario.time} hrs la materia:"
    while True:
        materia = choose_from(week.choices_materia, prompt_choices=prompr_materia)
        if materia == 0:
            materia = new_materia(week)
        elif materia == -1:
            return
        if horario is None:
            add_materia_to_horario(week, materia=materia)
        else:
            week.add_materia(materia, horario)


def add_materia_to_horario(week: horario.Week, materia=None):
    if materia is None:
        prompt_dia = "Agregar a dia:"
        prompt_horario = "Agregar a horario de dia {day.name}:"
    else:
        prompt_dia = f"Agregar materia '{materia}' a dia:"
        prompt_horario = f"Agregar materia '{materia}' a horario de dia {{day.name}}:"
    while True:
        day = choose_from(week.choices_day, prompt_choices=prompt_dia)
        if day == -1:
            break
        while True:
            horario = choose_from(day.choices_horario, prompt_choices=prompt_horario.format(day=day))
            if horario == -1:
                break
            if materia is None:
                add_horario_to_materia(week, horario=horario)
            else:
                week.add_materia(materia, horario)

def print_video(video):
    print()
    print("Materia:", video["materia"])
    print(video['snippet']['title'])
    print("Canal:", video['snippet']['channelTitle'])
    print(f"Duracion[mm:ss]: {video['duration']: >2.0f}:{60 * (video['duration'] % 1):0>2.0f}")
    print(video['snippet']['description'])
    print(f"Url: https://www.youtube.com/watch?v={video['id']['videoId']}")
    print()

def get_video(week: horario.Week, vistos: vistos.ListaVistos):
    if not week:
        video = recomendar_un_video(new_materia(week), vistos)
    datetime = time.struct_time(time.localtime())
    video = week.get_video_recomendation_for_time(datetime.tm_wday, datetime.tm_hour, datetime.tm_min, vistos)
    while video is None:
        choice = choose_from([(0, "Hora mas proxima."), (1, "Hora especifica."), (2, "Materia especifica.")],
                            prompt_choices="No tiene ninguna materia registrada a esta hora. Desea una recomendacion para: ")
        if choice == -1:
            return
        elif choice == 0:
            horario = next(filter(None, week.week_iterator(day=datetime.tm_wday, horario=datetime.tm_hour)))
            video = week.get_video_recomendation_for_time(horario.day, horario, 0, vistos)
        elif choice == 1:
            while video is None:
                day = choose_from(filter(lambda x: x[0], week.choices_day), prompt_choices="Dia:")
                if day == -1:
                    break
                while video is None:
                    horario = choose_from(filter(lambda x: x[0], day.choices_horario), prompt_choices="Hora:")
                    if horario == -1:
                        break
                    video = week.get_video_recomendation_for_time(day, horario, 0, vistos)
        elif choice == 2:
            materia = choose_from(week.choices_materia)
            if materia == -1:
                continue
            elif materia == 0:
                materia = new_materia(week)
            video = recomendar_un_video(materia, vistos)
    print_video(video)

def print_vistos(vistos: vistos.ListaVistos):
    lista = vistos.getVistos()
    print()
    if not lista:
        print("No hay videos vistos.")
    else:
        for video in lista:
            print_video(video)
    print()

MAIN_MENU = {"choices": [(print_horario, "Ver mi horario."),
                         (print_materias, "Ver mis materias."),
                         (add_horario_to_materia, "Añadir horas a materias."),
                         (add_materia_to_horario, "Añadir materias a horas."),
                         (get_video, "Recibir recomendacion de video."),
                         (print_vistos, "Ver videos vistos.")],
             "prompt_choices": "¿Que desea hacer?",
             "prompt_input": "(Ingrese numero):",
             "prompt_go_back": "Salir"}

