class ListaVistos:
    def __init__(self):
        self.vistos = list()

    def add(self, video):
         if video not in self.vistos:
            self.vistos.append(video)

    def isVisto(self, video):
        return video in self.vistos

    def getVistos(self):
        return self.vistos

