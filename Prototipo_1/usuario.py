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
        save_path = f"{nombre}.pickle"
        if exists(save_path):
            try:
                with open(save_path, 'rb') as file:
                    saved_user: Usuario = load(file)
                    self.week = saved_user.week
                    self.nombre = saved_user.nombre
                    self.hash = saved_user.hash
            except Exception:
                print('Error de carga.')
                bck_save_path = save_path + '.bck'
                if exists(bck_save_path):
                    remove(bck_save_path)
                rename(save_path, bck_save_path)
        if not hasattr(self, 'week'):
            self.week = Week()
        if not hasattr(self, 'nombre'):
            self.nombre = nombre

    # Retorna falso si la contraseña es incorrecta o el usuario no existe
    def check_password(self, password: str) -> bool:
        hashed_message = digest(password.encode(), _MESSAGE, 'sha512')
        if hasattr(self, 'hash') and compare_digest(self.hash, hashed_message):
            return True
        return False

    # Retorna falso si la cuenta ya existe
    def set_password(self, password: str) -> bool:
        if hasattr(self, 'hash'):
            return False
        else:
            self.hash = digest(password.encode(), _MESSAGE, 'sha512')
            return True

    def save(self):
        if hasattr(self, 'hash'):
            save_path = f"{self.nombre}.pickle"
            bck_path = save_path + '.bck'
            if exists(save_path):
                if exists(bck_path):
                    remove(bck_path)
                rename(save_path, bck_path)
            try:
                with open(save_path, 'wb') as file:
                    dump(self, file)
            except Exception:
                print("Error de guardado.")
                if exists(save_path):
                    remove(save_path)
                if exists(bck_path):
                    rename(bck_path, save_path)
            finally:
                if exists(bck_path):
                    remove(bck_path)
