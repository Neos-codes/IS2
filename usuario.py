from horario import Week

class Usuario:
    def __init__(self, nombre, password):
        self.week = Week()
        self.nombre = nombre
        self.password = password
        
    def compare(self, nombre, password):
        return (self.nombre==nombre and self.password==password)