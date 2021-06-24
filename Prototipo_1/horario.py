from inspect import ArgInfo
from pickle import load, dump
from os.path import exists
from os import rename, remove
from recomendar import recomendar_un_video
from vistos import ListaVistos
import time
import random


DAYS = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

class Horario:
    # Constructor
    def __init__(self, day, time, mat_order) -> None:
        self._materias = set()
        self._sorted_mats = list() # Por aqui sacar las materias asignadas a la hora
        self._mat_order = mat_order
        self.day = day
        self.time = time

    # Añadir materias
    def add(self, materia):
        if materia not in self._materias:
            self._sorted_mats.append(materia)
            self._sorted_mats.sort(key=self._mat_order)
            self._materias.add(materia)
            return 1
        return 0
    def __getitem__(self, index):
        return self._sorted_mats[index]
    def __len__(self):
        return len(self._materias)
    def __str__(self) -> str:
        return f"{self.time: >2} hrs {' '.join(self._sorted_mats) if self._sorted_mats else ''}"
    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.day)}, {repr(self.time)})"


class Day:
    # Constructor
    def __init__(self, week, name, mat_order):
        self.hrs = [Horario(self, i, mat_order) for i in range(8, 22)]
        self.week = week
        self.name = name
        # Para ui
        self._choices_horario = [(horario, None) for horario in self.hrs]
    @property
    def choices_horario(self):  # Si quiero leer los días, entro por acá "choices_horario"
        return self._choices_horario.copy()
    def __str__(self):
        return self.name + "\n" + "\n".join(map(str, self.hrs))
    def __bool__(self):
        return any(self.hrs)
    def generate_recomendations(self):
        raise NotImplementedError

class Week:

    def __init__(self):
        # Llenar un arreglo de dias en la semana
        self.days = [Day(self, name, self.get_mats_order) for name in DAYS]
        self.materias = dict()
        self.lista_vistos = ListaVistos()
        self._mats_order = list()
        self._choices_materia = []
        self._choices_day = [(day, day.name) for day in self.days]

    def __str__(self):
        w_col = max(len(word) for i in [self.materias, DAYS] for word in i)
        row_template = "{: >6} " + " ".join([f"{{: ^{w_col}}}"] * 7)
        lines = [row_template.format('', *DAYS)]
        for i in range(len(self.days[0].hrs)):
            week_hr = [day.hrs[i] for day in self.days]
            day_len = [len(day_hr) for day_hr in week_hr]
            hrow = max(1, *day_len)
            for j in range(hrow):
                row_head = f"{week_hr[0].time: >2} hrs" if j == 0 else ""
                hrs_row = [day_hr[j] if j < hr_len else "" for day_hr, hr_len in zip(week_hr, day_len)]
                lines.append(row_template.format(row_head, *hrs_row))
        return '\n'.join(lines)

    def __bool__(self):
        return any(self.days) or any(self.materias)

    def get_video_recomendation_for_time(self, dia, hora, minutos, vistos):
        if isinstance(dia, Day):
            day = dia
        else:
            day = self.days[dia]
        t = int(60 - minutos)
        if isinstance(hora, Horario):
            i = hora.time - 8
            horario = hora
        else:
            i = hora - 8
            horario = day.hrs[i]
        if horario:
            materia = list(horario)
            # materia = random.choices(materias, weights=[self.materias[m] for m in materias])[0]
            for h in day.hrs[i + 1:]:
                if materia in h:
                    t += 60
                else:
                    break
            return recomendar_un_video(materia[0], vistos, tiempo=t)

    def week_iterator(self, day=None, horario=None):
        if isinstance(day, Day):
            i = self.days.index(day)
        elif day is None:
            i = 0
        else:
            i = day
        if isinstance(horario, Horario):
            assert day is None
            j = horario.time - 8
        elif horario is None:
            j = 0
        else:
            j = horario - 8
        start = (i, j)
        j += 1
        i += j // 14
        j = j % 14
        i = i % 7
        while (i, j) != start:
            yield self.days[i].hrs[j]
            j += 1
            i += j // 14
            j = j % 14
            i = i % 7

    @property
    def choices_materia(self):
        return [(0, "Nueva materia.")] + self._choices_materia

    @property
    def choices_day(self):
        return self._choices_day.copy()

    def get_mats_order(self, materia):
        return self._mats_order.index(materia)

    def add_materia(self, materia, horario=None):
        if materia not in self.materias:
            self.materias[materia] = 0
            self._mats_order.append(materia)
            self._choices_materia.append((materia, materia))
        if horario is not None:
            self.materias[materia] += horario.add(materia)

    def get_vistos(self):
        return self.lista_vistos


class SaveManager:
    def __init__(self, save_path="week.pickle"):
        self.save_path = save_path
        self.week = None

    def __enter__(self):
        if self.week is None:
            if exists(self.save_path):
                try:
                    with open(self.save_path, 'rb') as file:
                        self.week = load(file)
                        if not hasattr(self.week, 'lista_vistos'):
                            self.week.lista_vistos = ListaVistos()
                except Exception:
                    print('Error de carga.')
                    rename(self.save_path, '~' + self.save_path)
                    self.week = Week()
        return self.week

    def __exit__(self, *args):
        bck_path = self.save_path + '.bck'
        if exists(self.save_path):
            if exists(bck_path):
                remove(bck_path)
            rename(self.save_path, bck_path)
        try:
            with open(self.save_path, 'wb') as file:
                dump(self.week, file)
        except Exception:
            print("Error de guardado.")
            if exists(self.save_path):
                remove(self.save_path)
            if exists(bck_path):
                rename(bck_path, self.save_path)
        finally:
            if exists(bck_path):
                remove(bck_path)
