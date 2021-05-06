days_ = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

# clase week tiene lista de clase day y lista de clase materias

class day():
    # Constructor
    # self.hrs = lista con horas desde las 8 am (hora 0) hsta las 9 pm (hora 12)
    def __init__(self):
        self.hrs = []
        for i in range(0, 14):
            self.hrs.append([])
            #print(self.hrs[i])

# END CLASS DAY

class week:

    # Dias de la semana
    days = []

    # Dia 0 (Lunes) al Dia 6 (Domingo)
    def __init__(self):
        for i in range(0, 7):
            self.days.append(day())
        # la semana tiene un set de ramos (comienza vacio)    
        self.ramos = materias()
    
    def addMateria(self):
        self.ramos.addMateria(self.days)
    
    def print_materias(self):
        print("Materias agregadas: ")
        self.ramos.print_materias()

# END CLASS WEEK

class materias():

    
    def __init__(self):
        # Guardaremos las materias en un set
        self.materias_ = set()


    def addMateria(self, dias: list):
        # Recibir nombre del ramo
        print("Nombre de la materia: ")
        name = input()

        # Copia de seguridad en caso de no completar el metodo o salida abrupta
        c_dias = dias.copy()

        # Ver si está dentro del diccionario de ramos
        if not(name.lower() in self.materias_):    # Si lo esta, agregar y preguntar por dias
            print("¿Cuantos dias a la semana tiene esta materia? (del 1 al 7): ")
            n_dias = int(input())
            # dias: lista de dias de la semana    dias_: dias de la semana en que agregarás la materia
            dias_ = []

            # Pedimos que ingrese los dias para anotar la materia
            for i in range(0, n_dias):
                print("Ingrese el numero del dia para agregar la materia: ")
                # Imprimir dias en que no ha agregado la materia
                self.print_dias(dias_)
                # Escoger dia para agregar materia (INPUT)
                dias_.append(int(input()) - 1)        
                # Escoger horas para agregar
                self.add_hora(name, c_dias[dias_[i]], dias_[i])

            # Ahora que llegamos al final, pasamos las copias de seguridad 
            dias = c_dias.copy()
            self.materias_.add(name)

    # END ADDMATERIA (EN CLASS MATERIA)

    def print_materias(self):
        i = 1
        for x in self.materias_:
            mat = x
            print(str(i) + ". " + mat)
            i += 1
    
    # END PRINT_MATERIAS




    def add_hora(self, name_mat: str, dia: day, n_dia: int):
        # Permite agregar horas a self.hrs
        # Imprimir horario del dia en que se quiere agregar la materia

        # While 1 te pregunta por agregar hora en el dia especifico hasta que no quieras agregar mas
        while 1:
            print("Horario de dia " + days_[n_dia])
            # Te imprime todo el horario del dia
            for i in range(0, 14):
                if len(dia.hrs[i]) == 0:
                    #print("Lista vacia!")
                    print(str(i + 8) + " hrs")
                else:
                    str_ = str(i + 8) + " hrs: "
                    #print(str(i + 8) + "hrs ")
                    for j in range(0, len(dia.hrs[i])):
                        str_ += str(dia.hrs[i][j])
                        str_ += " "
                    print(str_)
                    

            print("¿En que hora quiere agregar la materia?")
            hr = int(input())
            dia.hrs[hr - 8].append(name_mat)
            print("¿Desea agregar otra hora de " + name_mat + " el dia " + days_[n_dia] + " YES (Y) / NO (N)")
            hr = input()
            if hr == "N" or hr == "NO" or hr == "N".lower() or hr == "NO".lower():
                break




    def print_dias(self, dias_: list):
        
         # Mostrar dias en los que no ha ingresado aun la materia
        for i in range(0, 7):
            flag = False
            for j in range(0, len(dias_)):
                # Si ya ingresó ese día, no mostrarlo entre las opciones
                # Marcando flag como True
                if i == dias_[j]:
                    flag = True
                    break
                
                # Si no está ingresado ya el día, mostrarlo como opcion
            if not flag:
                print(str(i + 1) + ". " + days_[i])
            # Si ya está ingresado, revisar el dia siguiente
            else:
                continue

# END CLASS MATERIAS

def main():

    week_ = week()

    # Añadir 2 materia a la semana
    week_.addMateria()
    week_.addMateria()

    # Printear materias añadidas
    week_.print_materias()



main()