from googleapiclient.discovery import build
import re

try:
    API_KEY = open('key', 'r').read().strip()
except FileNotFoundError:
    API_KEY = input("Api key no encontrado, por favor ingresar: ").strip()
    res = input("¿Desea guardar esta api key?[Y/n]").lower()
    while res not in  ['yes', 'y', 'si', 'no, n']:
        print('Respuesta no valida.')
        res = input("¿Desea guardar esta api key?[Y/n]").lower()
    if res in ['yes', 'y', 'si']:
        open('key', 'w').write(API_KEY)
finally:
    yt = build('youtube', 'v3', developerKey=API_KEY)

class VideoCache:
    def __init__(self):
        self.busquedas = dict()
    def __contains__(self, args):
        busqueda, duracion = args
        return busqueda in self.busquedas and duracion in self.busquedas[busqueda]
    def get(self, busqueda, duracion):
        return self.busquedas[busqueda][duracion]
    def set(self, busqueda, duracion, generator):
        if busqueda not in self.busquedas:
            self.busquedas[busqueda] = {duracion: generator}
        else:
            self.busquedas[busqueda][duracion] = generator


def video_search_gen(busqueda, duracion=None):
        # Diccionario
        params = {"part": "id, snippet",
                "q": busqueda, "type": "video"}
        if duracion is not None:
            assert duracion in {'short', 'medium', 'long'}
            params["videoDuration"] = duracion
        search = yt.search()
        req = search.list(**params)
        res = req.execute()
        while True:
            videos = res['items']
            durations = get_durations(videos)
            for v, d in zip(videos, durations):
                v['duration'] = d
                yield v
            req = search.list_next(req, res)
            res = req.execute()


def video_search(busqueda, duracion=None, cache=VideoCache()):
    if (busqueda, duracion) in cache:
        video_gen = cache.get(busqueda, duracion)
    else:
        video_gen = video_search_gen(busqueda, duracion=duracion)
        cache.set(busqueda, duracion, video_gen)
    yield next(video_gen)


duration_pattern = re.compile(r"PT(?:(?P<h>\d+)H)?(?:(?P<m>\d+)M)?(?:(?P<s>\d+)S)?")
def get_durations(video_iterable):
    video_ids = [v['id']['videoId'] for v in video_iterable]
    res = yt.videos().list(id=video_ids, part="contentDetails").execute()
    video_durations_str = [v['contentDetails']['duration'] for v in res['items']]
    for v in res['items']:
        duration_str = v['contentDetails']['duration']
        match = duration_pattern.search(duration_str)
        h, m, s = [0 if i is None else int(i) for i in match.groups()]
        yield h * 60 + m + s / 60.0



def youtube_search(arg):
    search_response = yt.search().list(
        q=arg,
        part="id, snippet",
        maxResults=5
      ).execute()
    videos = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            # videos.append("%s (%s)" % (search_result["snippet"]["title"],
            #                       search_result["id"]["videoId"]))
            videos.append(search_result)

    #print(videos)
    return videos

def get_vid():
     yt = build ('youtube', 'v3', developerKey = API_KEY)

     search_response = yt.videos().list(
        part='snippet, contentDetails',
        id='dQw4w9WgXcQ'
      ).execute()


     #print(search_response)
# eliminar videos ya vistos contenidos en serch_response,
# luego usar list_next()

def main():
    youtube_search("destripando la historia")

if __name__ == "__main__":
    main()