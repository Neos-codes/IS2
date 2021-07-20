# -*- coding: utf-8 -*-
"""
Created on Thu May 13 15:29:37 2021

@author: caleu
"""
from googleapiclient.discovery import build

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

def youtube_search(arg):
    yt = build ('youtube', 'v3', developerKey = API_KEY)

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

youtube_search("destripando la historia")

def get_vid():
     yt = build ('youtube', 'v3', developerKey = API_KEY)

     search_response = yt.videos().list(
        part='snippet, contentDetails',
        id='dQw4w9WgXcQ'
      ).execute()


     #print(search_response)
# eliminar videos ya vistos contenidos en serch_response,
# luego usar list_next()
