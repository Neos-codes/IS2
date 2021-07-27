from googleapiclient.discovery import build
from threading import Condition, Event, Lock, Thread, Semaphore, get_ident
from PIL import Image
from urllib.request import urlopen
from io import BytesIO
import re

_cmp = {k: f"(?:(?P<{k}>\d+){k.upper()})?" for k in 'YMWDhms'}
_DURATION_PATTERN = re.compile("P{Y}{M}{W}{D}(?:T{h}{m}{s})?".format_map(_cmp))

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


class YoutubeSearch:
    _materias = dict()
    _search = yt.search()
    _videos = yt.videos()
    _req_limiter = Semaphore(value=1)
    materia: str
    _background_thread: Thread
    _target_update: Event
    _size_update: Event
    _target_lock: Lock
    _size_lock: Lock
    _target_size: int
    _size: int
    resultados: dict
    indice: list
    _EXCEPTIONS = {}

    @classmethod
    def prefetch(cls, *materias):
        for materia in materias:
            cls(materia)

    def __new__(cls, materia: str):
        if materia not in cls._materias:
            self: cls = super().__new__(cls)
            self.materia = materia
            self._target_update = Event()
            self._size_update = Event()
            self._target_lock = Lock()
            self._size_lock = Lock()
            self._target_size = 0
            self._size = 0
            self.resultados = dict()
            self.indice = list()
            cls._materias[materia] = self
        return cls._materias[materia]

    def __init__(self, materia):
        if not hasattr(self, '_background_thread') or not self._background_thread.is_alive():
            if self.materia in self._EXCEPTIONS:
                e = self._EXCEPTIONS.pop(self.materia)
                raise e
            else:
                self._background_thread = Thread(
                    target=self._bgupdate, daemon=True)
                self._background_thread.start()

    def __len__(self):
        with self._size_lock:
            return self._size

    def __iter__(self):
        i = 0
        while self._background_thread.is_alive():
            size = len(self)
            if i == size:
                self._size_update.wait()
            else:
                for id in self.indice[i:size]:
                    yield self.resultados[id]
                i = size

    @property
    def _target(self):
        with self._target_lock:
            self._target_update.clear()
            return self._target_size

    @_target.setter
    def _target(self, value):
        with self._target_lock:
            if value + 10 > self._target_size:
                self._target_size = value + 10
                self._target_update.set()

    def _bgupdate(self):
        try:
            self._target_size = 10
            token = self._next(count=10)
            while token is not None:
                if self._size < self._target:
                    self._size_update.clear()
                    token = self._next(token=token)
                else:
                    get_thumbnails(self.resultados.values())
                    self._target_update.wait()
            self._size_update.set()
        except Exception as e:
            self._EXCEPTIONS[self.materia] = e
            return

    def _next(self, count=10, token=None):
        with self._req_limiter:
            print(f'Fetch materia:{self.materia} token:{token}')
            res = self._search.list(q=self.materia, part="id, snippet",
                                    type="video", maxResults=count,
                                    pageToken=token).execute()
        items = ((item['id']['videoId'], item) for item in res['items'])
        new_items = {id: item for id, item in items if id not in self.resultados}
        new_ids = list(new_items.keys())
        if new_ids:
            self._get_durations(new_items)
            self.resultados.update(new_items)
            self.indice += new_ids
            with self._size_lock:
                self._size = len(self.resultados)
                self._size_update.set()
        if 'nextPageToken' in res:
            return res['nextPageToken']
        else:
            return None

    @classmethod
    def _get_durations(cls, items):
        assert items
        with cls._req_limiter:
            print(f'Fetch duraciones')
            res = cls._videos.list(id=list(items.keys()), part="contentDetails").execute()
        for item in res['items']:
            id = item['id']
            match = _DURATION_PATTERN.search(item['contentDetails']['duration'])
            Y = match.group('Y')
            total = 0 if Y is None else int(Y)
            for f, t in zip([12, 365 / 12 / 7, 7, 24, 60, 60], match.groups()[1:]):
                total *= f
                total += 0 if t is None else int(t)
            items[id]['duration'] = total

    def __getitem__(self, index):
        if isinstance(index, int) and index >= 0:
            self._target = index
            while index >= len(self):
                if self._background_thread.is_alive():
                    if self._size_update.wait(0.5):
                        if self.materia in self._EXCEPTIONS:
                            e = self._EXCEPTIONS.pop(self.materia)
                            raise e
                else:
                    raise IndexError
            return self.resultados[self.indice[index]]


def prefetch_materias(*materias):
    YoutubeSearch.prefetch(*materias)


def get_thumbnail(videos: list, done_condition: Condition, take_lock: Lock, res='default') -> None:
    while True:
        with take_lock:
            if videos:
                video = videos.pop()
            else:
                break
        res_dict = video['snippet']['thumbnails'][res]
        print(f'Fetch thumbnail:{res} video:{video["snippet"]["title"]}')
        with urlopen(res_dict['url']) as thumbnail:
            res_dict['image'] = Image.open(BytesIO(thumbnail.read()))
    with done_condition:
        done_condition.notify()


def get_thumbnails(videos: list, threads=5, res='default') -> list:
    done_condition = Condition()
    take_lock = Lock()
    tasks = []
    missing_videos = [
        video for video in videos if 'image' not in video['snippet']['thumbnails'][res]]
    if missing_videos:
        with done_condition:
            for i in range(min(threads, len(missing_videos))):
                tasks.append(Thread(target=get_thumbnail,
                                    args=(missing_videos, done_condition, take_lock),
                                    kwargs={'res': res}, daemon=True))
                tasks[-1].start()
            done_condition.wait_for(lambda: all('image'
                                    in v['snippet']['thumbnails'][res]
                                    for v in videos))

    return [v['snippet']['thumbnails'][res]['image'] for v in videos]



def video_search_gen(busqueda, duracion=None):
    yield from YoutubeSearch(busqueda)

def video_search(busqueda, duracion=None, cache=None):
    yield video_search_gen(busqueda)

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
