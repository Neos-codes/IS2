import random
import ytAPI
from copy import copy

def generar_video(tipo):
    """
    Retorna duracion aleatoria en una de las categorias ('corto', 'medio', 'largo').

    Parameters
    ----------
    tipo : str
        Uno de ('corto', 'medio', 'largo').

    Raises
    ------
    ValueError
        Si tipo no es uno de ('corto', 'medio', 'largo').

    Returns
    -------
    int
        Duracion del video.

    """
    span_tipo = {"corto": (1, 4), "medio": (5, 20), "largo": (20, 100)}
    try:
        return random.randint(*span_tipo[tipo])
    except KeyError:
        raise ValueError(f"Tipo debe ser uno de {set(span_tipo.keys())}.")


def random_tags(tags):
    """
    Genera una sequencia aleatoria de tags, con todos los tags apareciendo
    a lo menos una vez antes de que cualquier tag se repita.

    Parameters
    ----------
    tags : sequencia de tags

    Yields
    ------
    tag

    """

    tags = copy(tags)
    random.shuffle(tags)
    yield from tags
    while True:
        yield random.choice(tags)

def recomendar_prueba(tiempo, maxLargos, maxMedios, tags):
    """
    Genera hasta (maxLargos) videos de duracion larga,
    seguido de hasta (maxMedios) videos de duracion media y
    cuantos videos de duracion corta sean necesarios
    para acumular (tiempo - max_d_corta, tiempo].

    Parameters
    ----------
    tiempo : int
        Duracion objetivo de la suma de los videos.
    maxLargos : int
        Maximo numero de videos largos.
    maxMedios : int
        Maximo numero de videos medios.
    tags : int
        Tags para los videos.

    Yields
    ------
    str
        Video con tag aleatorio y duracion aleatoria.

    """
    tags_gen = random_tags(tags)
    tdc_seq = [('largo', maxLargos, 100),
               ('medio', maxMedios, 20),
               ('corto', float('inf'), 4)]

    for tipo, cantidad, max_d in tdc_seq:
        while cantidad > 0 and tiempo > max_d:
            tag = next(tags_gen)
            d = generar_video(tipo)
            cantidad -= 1
            tiempo -= d
            yield f"{tag} {d}"


def recomendar(tiempo, materias):
    tdc_seq = [('long', float('inf'), 100),
               ('medium', float('inf'), 20),
               ('short', float('inf'), 4)]
    materias_gen = random_tags(materias)
    video_gen = dict()
    for tipo, cantidad, max_d in tdc_seq:
        while tiempo > max_d:
            materia = next(materias_gen)
            if materia not in video_gen:
                video_gen[materia] = ytAPI.video_search_gen(busqueda = materia, duracion = tipo)
            video = next(video_gen[materia])
            d = ytAPI.get_video_duration(video)
            if (yield video):
                cantidad -= 1
                tiempo -= d

def tiempo_a_duracion(tiempo):
    if tiempo is None:
        return None
    if tiempo > 40:
        return "long"
    elif tiempo > 20:
        return "medium"
    elif tiempo > 4:
        return "short"
    else:
        return None

def recomendar_un_video(materia, vistos, tiempo=None):
    lista=vistos.getVistos()
    d = tiempo_a_duracion(tiempo)
    while True:
        video = next(ytAPI.video_search(materia, duracion=d))
        if (tiempo is None or video['duration'] <= tiempo) and video not in lista:
            video['materia'] = materia
            #vistos.add(video)
            return video



def main():
    tiempo = int(input("Introduzca una cantidad de tiempo (en minutos)\n"))
    maxLargos = int(input("Elija la cantidad de videos largos maximos que quiere\n"))
    maxMedios = int(input("Elija la cantidad de videos medios maximos que quiere\n"))
    tags = input("Ponga sus tags separados por espacio\n").split()
    #print(list(recomendar(tiempo, maxLargos, maxMedios, tags)))

if __name__ == "__main__":
    main()

