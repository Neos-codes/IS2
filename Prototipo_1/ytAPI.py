# -*- coding: utf-8 -*-
"""
Created on Thu May 13 15:29:37 2021

@author: caleu
"""
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


def video_search_gen(busqueda, duracion=None):
    params = {"part": "id, snippet",
              "q": busqueda}
    if duracion is not None:
        assert duracion in {'short', 'medium', 'long'}
        params["videoDuration"] = duracion
    search = yt.search()
    req = search.list(**params)
    res = req.execute()
    while True:
        videos = res['items']
        durations = get_durations(videos)
        yield from (v | {"duration": d} for v, d in zip(videos, durations))
        req = search.list_next(req, res)
        res = req.execute()

duration_pattern = re.compile(r"PT(\d+)M(\d+)S")
def get_durations(video_iterable):
    video_ids = [v['id']['videoId'] for v in video_iterable]
    res = yt.videos().list(id=video_ids, part="contentDetails").execute()
    video_durations_str = [v['contentDetails']['duration'] for v in res['items']]
    for v in res['items']:
        duration_str = v['contentDetails']['duration']
        match = duration_pattern.search(duration_str)
        m, s = map(int, match.groups())
        yield m + s / 60.0



def youtube_search(arg):
    search_response = yt.search().list(
        q=arg,
        part="id, snippet",
        maxResults=5
      ).execute()
    videos = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                  search_result["id"]["videoId"]))

    print(videos)

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
