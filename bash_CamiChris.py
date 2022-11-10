import platform
import subprocess
import os 
import time

print("Binvenido a BashCamiChris 1.0")
while True:
	comando = input(">> ")
	if "listar" in comando:
		if comando == "listar":
			path = os.getcwd() # se obtiene el path actual
			lista = os.listdir(path) # se obtienen los archivos
			print("Archivos en ", path, ":")
			print(lista)
		else:
			path = comando[7:len(comando)] # se guarda el path introducido
			if os.path.exists(path):
				lista = os.listdir(path) # se obtienen los archivos
				print("Archivos en ", path, ":")
				print(lista)
			else:
				print("El path ingresado es incorrecto")
	if "creardir" in comando: # recibe como parametro el path
		path = comando[9:len(comando)]
		if os.path.exists(path):
			nombre_dir=input("Ingresa el nombre del directorio nuevo: ")
			path_n = os.path.join(path, nombre_dir) # el path con el nombre del directorio
			os.mkdir(path_n) 
		else:
			print("El path introducido es incorrecto")

	if "salir" in comando:
		break

