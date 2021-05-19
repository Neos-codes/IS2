


def choose_from(choices, prompt_choices="Opciones: ", prompt_input="Ingrece opcion: ", prompt_fail="Opcion no es valida."):
    print(prompt_choices)
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


def new_materia(week):
    while True:
        name = input("Ingrese nombre de nueva materia: ").lower()
        if name not in week.materias:
            week.add_materia(name)
            return name
        print("Materia {name} ya existe.")


def print_horario(week):
    print(week)


def print_materias(week):
    print("Materias:")
    print(' '.join(week.materias))
    print()


def add_horario_to_materia(week, horario=None):
    if horario is None:
        prompr_materia = "Agregar materia:"
    else:
        prompr_materia = f"Agregar a dia {horario.day.name} a las {horario.time} hrs la materia:"
    while True:
        materia = choose_from([(0, "Nueva materia.")] +
                              week.choices_materia + [(1, "Volver atras.")], prompt_choices=prompr_materia)
        if materia == 0:
            materia = new_materia(week)
        elif materia == 1:
            return
        if horario is None:
            add_materia_to_horario(week, materia=materia)
        else:
            horario.add(materia)


def add_materia_to_horario(week, materia=None):
    if materia is None:
        prompt_dia = "Agregar a dia:"
        prompt_horario = "Agregar a horario de dia {day.name}:"
    else:
        prompt_dia = f"Agregar materia '{materia}' a dia:"
        prompt_horario = f"Agregar materia '{materia}' a horario de dia {{day.name}}:"
    while True:
        day = choose_from(week.choices_day +
                          [(0, "Volver atras.")], prompt_choices=prompt_dia)
        if day == 0:
            break
        while True:
            horario = choose_from(
                day.choices_horario + [(0, "Volver atras.")], prompt_choices=prompt_horario.format(day=day))
            if horario == 0:
                break
            if materia is None:
                add_horario_to_materia(week, horario=horario)
            else:
                horario.add(materia)

MAIN_MENU = {"choices": [(print_horario, "Ver mi horario"),
                         (print_materias, "Ver mis materias"),
                         (add_horario_to_materia, "Añadir horas a materias"),
                         (add_materia_to_horario, "Añadir materias a horas"),
                         (0, "Salir")],
             "prompt_choices": "¿Que desea hacer?",
             "prompt_input": "(Ingrese numero):"}
