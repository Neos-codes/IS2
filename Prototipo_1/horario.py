from pickle import load, dump
from os.path import exists


DAYS = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

class Horario:
    def __init__(self, day, time, mat_order) -> None:
        self._materias = set()
        self._sorted_mats = list()
        self._mat_order = mat_order
        self.day = day
        self.time = time
    def add(self, materia):
        if materia not in self._materias:
            self._sorted_mats.append(materia)
            self._sorted_mats.sort(key=self._mat_order)
            self._materias.add(materia)
    def __getitem__(self, index):
        return self._sorted_mats[index]
    def __len__(self):
        return len(self._materias)
    def __str__(self) -> str:
        return f"{self.time: >2} hrs {' '.join(self._sorted_mats) if self._sorted_mats else ''}"
    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.day)}, {repr(self.time)})"


class Day:
    def __init__(self, week, name, mat_order):
        self.hrs = [Horario(self, i, mat_order) for i in range(8, 22)]
        self.week = week
        self.name = name
        self.choices_horario = [(horario, None) for horario in self.hrs]
    def __str__(self):
        return self.name + "\n" + "\n".join(map(str, self.hrs))
    def generate_recomendations(self):
        raise NotImplementedError

class Week:
    def __init__(self):
        self.days = [Day(self, name, self.get_mats_order) for name in DAYS]
        self.materias = set()
        self._mats_order = list()
        self.choices_materia = []
        self.choices_day = [(day, day.name) for day in self.days]
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

    def get_mats_order(self, materia):
        return self._mats_order.index(materia)

    def add_materia(self, materia):
        if materia not in self.materias:
            self.materias.add(materia)
            self._mats_order.append(materia)
            self.choices_materia.append((materia, materia))
    @property
    def ramos(self):
        return 


def check_save(save_path="week.pickle"):
    return exists(save_path)


def load_save(save_path="week.pickle"):
    return load(open(save_path, "rb"))


def save(week, save_path="week.pickle"):
    try:
        dump(week, open(save_path, "wb"))
        return True
    except:
        return False
