import random

# esta funcion genera una duracion aleatoria en relacion al tipo de video pedido, es mas que nada para probar el algoritmo
# tipo: tipo de duracion del video
def GenerarVideo(tipo):
	if tipo == "corto":#video corto
		return random.randint(1,4)
	elif tipo == "medio":#video medio
		return random.randint(5,20)
	elif tipo == "largo":#video largo
		return random.randint(20,100)
	else:#ninguno
		print("por favor ingrese un tipo valido")
		return -1

#elige un tag aleatorio del conjunto tags
#tags: conjunto de tags
#eliminar: variable booleana que dicide si el elemento elegido es borrado del conjunto
def RandomTag(tags, eliminar):

	n = len(tags)#tamaño del conjunto

	index = random.randint(0,n - 1)#eleccion aleatoria

	result = tags[index]#se obtiene el tag

	if eliminar:
		tags.remove(result)#se elimina del conjunto

	return result

#esta funcion corresponde al algortimo de recomendacion
#tiempo: tiempo libre asignado
#maxLargos: maximo numero de videos largos permitidos por el usuario
#maxMedios: maximo numero de videos medios permitidos por el usuario
#maxCortos: maximo numero de videos cortos permitidos por el usuario
def Recomendar(tiempo, maxLargos, maxMedios, tags):
	videos = []#donde se guardan los resultados

	auxTag = []#auxiliar donde se guardan los tags que seran eliminados

	for t in tags:
		auxTag.append(t)#se guardan los tags en el auxiliar

	#se inicializan contadores
	numLargos = 0
	numMedios = 0
	numCortos = 0

	#mientras haya tiempo para un video corto
	while tiempo >= 4:

		#se ve si se han puesto todos los tags al menos una vez
		if len(auxTag) > 0:
			tag = RandomTag(auxTag, True)
		else:
			tag = RandomTag(tags, False)


		videoAux = 0#auxiliar de duracion

		#si se puede agregar videos largos
		if tiempo >= 100 and numLargos < maxLargos:
			videoAux = GenerarVideo("largo")
			numLargos += 1

		#si se puede agregar videos medios
		elif tiempo >= 20 and numMedios < maxMedios:
			videoAux = GenerarVideo("medio")
			numMedios += 1

		#si se puede agregar videos cortos
		else:
			videoAux = GenerarVideo("corto")

		tiempo -= videoAux#se reduce el tiempo restante

		video = tag + " " + str(videoAux)

		videos.append(video)#se agrega el video al resultado

	return videos

def Main():
	#se piden datos al usuario
	tiempo = int(input("introduzca una cantidad de tiempo (en minutos)\n"))

	maxLargos = int(input("elija la cantidad de videos largos maximos que quiere\n"))

	maxMedios = int(input("elija la cantidad de videos medios maximos que quiere\n"))

	tags = input("ponga sus tags separados por espacio\n")

	tags = tags.split()

	listaVideos = Recomendar(tiempo, maxLargos, maxMedios, tags)

	print(listaVideos)

Main()


