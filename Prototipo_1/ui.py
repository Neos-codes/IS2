from recomendar import recomendar_un_video
import horario
import time
import vistos
import tkinter as tk
from tkinter import messagebox
import webbrowser
from ytAPI import youtube_search, video_search_gen
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO

#from ytAPI import video_search

days_names = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
hours_day = list(range(8, 21))
vistos_index = 0

# Crear ventana (desde main)
def create_window():
    window = tk.Tk()
    window.title("Prototipo")   # Aqui debería ir el nombre del SW

    return window

# Crear Frames (desde main)
def create_frames(window, frames: dict):
    # Para el horario
    horario = tk.LabelFrame(window, text = "Horario", padx = 5, pady = 5)
    horario.grid(row = 0, column = 1)
    frames["horario"] = horario

    # Para los botones de opciones
    options = tk.LabelFrame(window, text = "Opciones", padx = 5, pady = 5)
    options.grid(row = 0, column = 0)
    frames["opciones"] = options

# Se usa en create_optionMenu_gadgets
def asignar_hora(dia: int, hora: int, materia: str, week):
    hr = week.days[dia].hrs[hora]
    hr._sorted_mats.clear()
    hr._materias.clear()
    # Si la materia no es "vacio" ("---""), agregar
    if materia != "---":
        hr.add(materia)

# Se usa en create_option_buttons
def addMateria(frame: tk.Tk, week: horario.Week, gadgets: list):
    # Obtener lista de materias ya agregadas
    materias = []
    for x in week.choices_materia[1:]:
        materias.append(x[0])

    # Esta funcion se llama desde el boton de "aceptar"
    def isInMaterias(materias: list, new_mat: tk.Entry, week: horario.Week, window: tk.Toplevel):
        temp_str = new_mat.get()
        if not temp_str in materias:
            week.add_materia(temp_str)
            materias.append(temp_str)
            # Aqui hacer update de los optionMenu
            create_optionMenu_gadgets(frame, gadgets, materias, week, update = True)
            window.destroy()

        else:
            tk.messagebox.showerror("Error!", "La materia ya existe")

    # Crear nueva ventana
    top = tk.Toplevel()
    top.title("Añadir materia")

    # Label
    label = tk.Label(top, text = "Ingrese el nombre de la nueva materia:")
    label.grid(row = 0, column = 0)

    # Añadir input field
    e = tk.Entry(top, width = 30)
    e.grid(row = 1, column = 0)

    # Añadir boton de aceptar
    btn = tk.Button(top, text = "Aceptar", command = lambda: isInMaterias(materias, e, week, top))
    btn.grid(row = 2, column = 0)

# Crear/actualizar "optionMenu's" del horario (desde main y addMateria)
def create_optionMenu_gadgets(frame: tk.Tk, gadgets: list, materias: list, week: horario.Week, update = False):
    # Borrar referencias a botones antiguos
    if update:
        for x in gadgets:
            for g in x:
                g.destroy()
            x.clear()
        gadgets.clear()

    if not "---" in materias:
        materias.append("---")
    # Crear optionMenus nuevos
    for i in range(7):
        gadgets.append([])   # Añadimos una lista para los gadgets del día "i"
        for j in range(13):  # Por cada hora del día "i"
            clicked = tk.StringVar()
            # Si no hay una materia asignada a la hora del dia, se coloca "---"
            if not week.days[i].hrs[j]:
                clicked.set("---")
            # Caso contrario, se le asigna la materia que hay en la hora del día como parametro en la interfaz
            else:
                clicked.set(week.days[i].hrs[j][0])
            # Se define la función a llamar cuando se escoja otra materia
            foo = lambda materia = clicked.get(), dia = i, hr = j: asignar_hora(dia, hr, materia, week)
            # Se crea el boton
            new_options = tk.OptionMenu(frame, clicked, *materias, command = foo)
            # Se agrega a la lista de gadgets
            gadgets[i].append(new_options)
            # Se posiciona en la grid del frame
            new_options.grid(row = j + 1, column = i + 1)

# Rellenar horas del horario (desde main)
def horario_fill(frame, gadgets: list, week, labels_days: list, labels_hrs: list):
    # Agregar materias a la lista "materias"
    materias = []
    for x in week.choices_materia[1:]:
        materias.append(x[0])
    materias += ["---"]


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

    # Crear uptionMenu fields
    create_optionMenu_gadgets(frame, gadgets, materias, week, update = False)

# Crear ventana que muestra el historial (desde create_option_buttons)
def ver_historial(vistos: vistos.ListaVistos):
    # Crear nueva ventana
    top = tk.Toplevel()
    top.title("Historial")

    # Label de titulo:
    label = tk.Label(top, text = "Video:")
    label.grid(row = 0, column = 0)

    # Mostrar info de video en pantalla
    video = vistos.getVistos()[0]   # Por test es solo el primero

    # Obtener thumbnail video
    u = urlopen(video['snippet']['thumbnails']['default']['url'])
    raw_data = u.read()
    u.close()

    # Mostrar thumbnail video
    img = Image.open(BytesIO(raw_data))
    img = ImageTk.PhotoImage(img)
    thumbnail_label = tk.Label(top, image=img)
    thumbnail_label.image = img
    thumbnail_label.grid(row = 1, column = 1)

    # Mostrar titulo del video
    title = tk.Label(top, text=video['snippet']['title'])
    title.grid(row = 2, column = 1)

    # Botones de accion
    next_b = tk.Button(top, text = "Siguiente")
    next_b.grid(row = 3, column = 2)

    back_b = tk.Button(top, text = "Anterior")
    back_b.grid(row = 3, column = 0)

    play_b = tk.Button(top, text = "Play",
    command = lambda: webbrowser.open(f"https://www.youtube.com/watch?v={video['id']['videoId']}"))
    play_b.grid(row = 3, column = 1)

# Crear botones de accion que se usan en la interfaz (desde main y create_option_buttons)
def create_option_buttons(horario_f, options_f, week, gadgets, vistos):
    # Añadir materia
    new_materia = tk.Button(options_f, text = "Añadir Materia", command = lambda: addMateria(horario_f, week, gadgets))
    new_materia.grid(row = 0, column = 0)
    # Recomendar
    recomendar = tk.Button(options_f, text = "Ver videos recomendados", command = lambda: ver_videos_recomendados(week, vistos))
    recomendar.grid(row = 1, column = 0)
    # Historial
    historial = tk.Button(options_f, text = "Ver historial", command = lambda: ver_historial(vistos))
    historial.grid(row = 2, column = 0)
    # Favoritos
    favoritos = tk.Button(options_f, text = "Videos Favoritos", command = lambda: print("EN CONSTRUCCION"))
    favoritos.grid(row = 3, column = 0)

# ----- END INTERFAZ ----- #

def choose_from(choices, prompt_choices="Opciones: ", prompt_input="Ingrese opcion: ", prompt_fail="Opcion no es valida.", prompt_go_back="Volver atras.", go_back_option=True):
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
    #print_video(video)
    return video

def get_video_b(week: horario.Week, vistos: vistos.ListaVistos):
    '''
    Esta funcion es una copia de get_video() para poder hacerle cambios
    libremente sin alterar el funcionamiento del resto del programa.
    Es una version simplificada que no da opciones para agregar materias
    en caso de que no haya ninguna asignada para el momento.
    Por ahora esta funcion solo es utilizada en ver_videos_recomendados().

    Parameters
    ----------
    week : horario.Week
        DESCRIPTION.
    vistos : vistos.ListaVistos
        DESCRIPTION.

    Returns
    -------
    video : TYPE
        DESCRIPTION.

    '''
    if not week:
        return None
    datetime = time.struct_time(time.localtime())
    video = week.get_video_recomendation_for_time(datetime.tm_wday, datetime.tm_hour, datetime.tm_min, vistos)
    #print_video(video)
    return video

def print_vistos(vistos: vistos.ListaVistos):
    lista = vistos.getVistos()
    print()
    if not lista:
        print("No hay videos vistos.")
    else:
        for video in lista:
            print_video(video)
    print()

def play_video(video, vistos: vistos.ListaVistos):
    '''
    Reproduce un video en el navegador predeterminado

    Parameters
    ----------
    video : TYPE
        DESCRIPTION.
    vistos : vistos.ListaVistos
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    webbrowser.open(f"https://www.youtube.com/watch?v={video['id']['videoId']}")
    vistos.add(video)

def n_videos(week, vistos, n=5):
    datetime = time.struct_time(time.localtime())
    # horario = next(h for h in week.week_iterator(datetime.tm_wday, datetime.tm_hour-1) if h)
    hr = datetime.tm_hour-8
    if hr < 0 or hr > 12:
        return None

    horario = week.days[datetime.tm_wday].hrs[datetime.tm_hour-8]
    if horario:
        materia = horario[0]
        search = video_search_gen(materia)
        videos = []
        while n:
            video = next(search)
            if video not in vistos:
                # video['materia'] = materia
                videos.append(video)
                n -= 1

        return videos
    else:
        return None


def ver_videos_recomendados(week, vistos):
    '''
    Abre una ventana que muestra una lista de videos recomendados, de acuerdo
    a la materia asignada al bloque de hora correspondiente al del momento.

    Parameters
    ----------
    week : TYPE
        DESCRIPTION.
    vistos : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    play_button_list = []
    title_label_list = []
    thumbnail_list = []
    if not week:
        #error message
        return

    lista_videos = n_videos(week, vistos)

    if lista_videos is None:
        tk.messagebox.showwarning("Error", "No tiene ninguna materia asignada para esta hora")
        return

    # video = get_video_b(week, vistos)
    # if video is None:
    #     tk.messagebox.showwarning("Error", "No tiene ninguna materia asignada para esta hora")
    #     return

    newWindow = tk.Toplevel()
    newWindow.title("Videos recomendados")
    newWindow.geometry("500x700")

    title = tk.Label(newWindow, text="Recomendaciones para este bloque:", font=("Verdana", 12))
    title.pack(pady = 8)

    i = 0
    vid_grid = tk.Frame(newWindow)

    for vid in lista_videos:
        u = urlopen(vid['snippet']['thumbnails']['default']['url'])
        raw_data = u.read()
        u.close()
        img = Image.open(BytesIO(raw_data))
        #img = img.resize((250, 250))
        img = ImageTk.PhotoImage(img)
        thumbnail_label = tk.Label(vid_grid, image=img)
        thumbnail_label.image = img
        thumbnail_list.append(thumbnail_label)
        thumbnail_label.grid(column = 0, row = i, sticky='e')


        title_label = tk.Label(vid_grid, text=vid['snippet']['title'])
        title_label_list.append(title_label)
        title_label.grid(column = 0, row = i+1, columnspan=2, pady = (0, 15))

        button = tk.Button(vid_grid, text="Play",
                       command = lambda v = vid: play_video(v, vistos))
        play_button_list.append(button)
        button.grid(column = 1, row = i)

        i += 2


    vid_grid.pack()

    # #print(video['snippet']['thumbnails']['default']['url'])
    # u = urlopen(video['snippet']['thumbnails']['default']['url'])
    # raw_data = u.read()
    # u.close()
    # #print(raw_data)

    # img = Image.open(BytesIO(raw_data))
    # #img = img.resize((250, 250))
    # img = ImageTk.PhotoImage(img)
    # thumbnail_label = tk.Label(newWindow, image=img)
    # thumbnail_label.image = img
    # thumbnail_label.pack()

    # label1 = tk.Label(newWindow, text=video['snippet']['title'])
    # label1.pack()

    # button = tk.Button(newWindow, text="Play",
    #                    command = lambda: webbrowser.open(f"https://www.youtube.com/watch?v={video['id']['videoId']}"))
    # button.pack()


def boof() :

    top = tk.Toplevel()

MAIN_MENU = {"choices": [(print_horario, "Ver mi horario."),
                         (print_materias, "Ver mis materias."),
                         (add_horario_to_materia, "Añadir horas a materias."),
                         (add_materia_to_horario, "Añadir materias a horas."),
                         (get_video, "Recibir recomendacion de video."),
                         (print_vistos, "Ver videos vistos.")],
             "prompt_choices": "¿Que desea hacer?",
             "prompt_input": "(Ingrese numero):",
             "prompt_go_back": "Salir"}
