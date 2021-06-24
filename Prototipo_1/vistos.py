class ListaVistos:
    def __init__(self):
        self.vistos = list()

    def add(self, video):
         if video not in self.vistos:
            self.vistos.insert(0, video)  # THIS
            #self.vistos.append(video)

    def __contains__(self, value):
        return any(value['id']['videoId'] == visto['id']['videoId'] for visto in self.vistos)

    def isVisto(self, video):
        return video in self.vistos

    def getVistos(self):
        return self.vistos
