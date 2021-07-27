from hmac import digest, compare_digest
from horario import Week
from os.path import exists
from os import remove, rename
from vistos import ListaVistos
from pickle import load, dump

with open('message.txt', 'rb') as file:
    _MESSAGE = file.read()

class Usuario:
    week: Week
    nombre: str
    hash: bytes

    def __init__(self, nombre):
        self.week = Week()
        self.usuario = nombre

    # Retorna falso si la contraseña es incorrecta o el usuario no existe
    def check_password(self, password: str) -> bool:
        hashed_message = digest(password.encode(), _MESSAGE, 'sha512')
        if hasattr(self, 'hash') and compare_digest(self.hash, hashed_message):
            self._save = True
            return True
        return False

    # Retorna falso si la cuenta ya existe
    def set_password(self, password: str) -> bool:
        if hasattr(self, 'hash'):
            return False
        else:
            self.hash = digest(password.encode(), _MESSAGE, 'sha512')
            self._save = True
            return True


class SaveManager:
    usuario: Usuario
    def __init__(self, nombre):
        self.nombre = nombre
        self.save_path = f'{nombre}.pickle'

    def __enter__(self) -> Usuario:
        if exists(self.save_path):
            try:
                with open(self.save_path, 'rb') as file:
                    self.usuario = load(file)
                    if not hasattr(self.usuario, 'week'):
                        self.usuario.week = Week()
                    if not hasattr(self.usuario, 'lista_vistos'):
                        self.usuario.week.lista_vistos = ListaVistos()
                    if not hasattr(self.usuario, 'lista_favoritos'):
                        self.usuario.week.lista_vistos = ListaVistos()

            except Exception:
                print('Error de carga.')
                bck_save_path = '~' + self.save_path
                if exists(bck_save_path):
                    remove(bck_save_path)
                rename(self.save_path, bck_save_path)
                self.usuario = Usuario(self.nombre)
        else:
            self.usuario = Usuario(self.nombre)
        return self.usuario

    def __exit__(self, *args):
        if hasattr(self.usuario, '_save'):
            delattr(self.usuario, '_save')
            bck_path = self.save_path + '.bck'
            if exists(self.save_path):
                if exists(bck_path):
                    remove(bck_path)
                rename(self.save_path, bck_path)
            try:
                with open(self.save_path, 'wb') as file:
                    dump(self.usuario, file)
            except Exception:
                print("Error de guardado.")
                if exists(self.save_path):
                    remove(self.save_path)
                if exists(bck_path):
                    rename(bck_path, self.save_path)
            finally:
                if exists(bck_path):
                    remove(bck_path)
