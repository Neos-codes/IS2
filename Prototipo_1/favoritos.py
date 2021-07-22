#CARLOS
class ListaFav:
    def __init__(self):
        self.favoritos = list()

    def add(self, video):
         if video not in self.favoritos:
            self.favoritos.insert(0, video)  # THIS
            #self.vistos.append(video)

    def __contains__(self, value):
        return any(value['id']['videoId'] == visto['id']['videoId'] for visto in self.favoritos)

    def isFavorito(self, video):
        return video in self.favoritos

    def getFavoritos(self):
        return self.favoritos
    
    def deleteFavoritos(self,element):
        self.favoritos.remove(element)
        
    def getTam(self):
        return len(self.favoritos)
