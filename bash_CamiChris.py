import platform
import subprocess
import os
import time
import signal
import shutil
import distutils.dir_util

def cmdListar(cadena):
	if(len(cadena) == 6): # se listan los archivos del path actual
		path = os.getcwd() # se obtiene el path actual
		lista = os.listdir(path) # se obtienen los archivos
		print("Archivos en ", path, ":")
		print(lista)
	else:
		cadena = cadena.split(sep=' ')
		path = cadena[1] # se guarda el path introducido
		if os.path.exists(path):
			lista = os.listdir(path) # se obtienen los archivos
			print("Archivos en ", path, ":")
			print(lista)
		else:
			print("El path ingresado es incorrecto")

def cmdCrearDir(cadena):
		try:
			os.mkdir(os.path.abspath(cadena)) # se crea el directorio
		except:
			print("El path introducido es incorrecto")

def cmdIr(path):
	if os.path.exists(path): # se verifica el path introducido
		os.chdir(os.path.abspath(path))  # se cambia de directorio al path solicitado
		path_n = os.getcwd() # se obtiene la nueva ubicacion 
		print("El path actual es: ", path_n)
	else:
		print("El path introducido es incorrecto")

def cmdPwd():
	path = os.getcwd() # se obtiene el path actual
	print("El path actual es: ", path) # se imprime

def cmdPermisos(cadena):
	cadena = cadena.split(sep = ' ')
	permisos = cadena[0]
	path = cadena[1]
	if os.path.exists(path):
		os.chmod(os.path.abspath(path), permisos)
	else:
		print("El path introducido es incorrecto")

def cmdHistory(comandos): 
	print("El historial de comandos es:")
	for i in range(0, len(comandos)):
		print(i+1, ": ", comandos[i])

def cmdEjecutar(cadena):
	try:
		subprocess.run(cadena.split())
	except:
		print("Comando no encontrado")

def cmdCopiar(cadena):
	cadena = cadena.split(sep = ' ')
	origen = cadena[0]
	destino = cadena[1]

	#copiar archivo
	if os.path.isfile(origen):
		#creamos directorio si no existe
		if (os.path.exists(destino) == False):
			os.makedirs(destino)    
		try:
			shutil.copy(origen,destino)
			print("Archivo copiado exitosamente.")

		# Se comprueba si el origen y el destino son iguales
		except shutil.SameFileError:
			print("El archivo a copiar es el mismo que el de destino.")

		except PermissionError:
			print("Permission denied.")

		except:
			print("Error al copiar archivo.")
 
	#copiar directorio
	elif os.path.isdir(origen):
		try:
			distutils.dir_util.copy_tree(origen,destino)
		except:
			print("Error al copiar directorio.")

	if(os.path.isfile(origen) == False and os.path.isdir(origen) == False):
		print("No existe el archivo o directorio.")

	
def cmdRenombrar(cadena):
	cadena = cadena.split(sep = ' ')
	original = cadena[0]
	nuevo = cadena[1] 

	if os.path.isfile(original):
		try :
			os.rename(original,nuevo)
			print("Renombrado exitosamente.")

		except:
			print("Error al renombrar.")

	if os.path.isdir(original):
		try :
			os.rename(original,nuevo)
			print("Renombrado exitosamente.")

		except:
			print("Error al renombrar.")

	if(os.path.isfile(original) == False and os.path.isdir(original) == False):
		print("No existe el archivo o directorio.")

def main():
	historial=[]
	print("Bienvenido/a a BashCamiChris 1.0")
	while True:
		comando = input(">> ")
		if (comando[:6] == "listar"): # -> listar o listar [path]
			cmdListar(comando)
			historial.append(comando)

		elif (comando[:8] == "creardir"): # -> creardir [path]
			cmdCrearDir(comando[9:])
			historial.append(comando)

		elif (comando == "pwd"): # -> pwd
			cmdPwd()
			historial.append(comando)
			
		elif (comando[:2] == "ir"): # -> ir [path]
			cmdIr(comando[3:])
			historial.append(comando)
			
		elif (comando == "salir"):
			break

		elif (comando[:8] == "permisos"): # -> permisos [permisos en Octal] [path]
			cmdPermisos(comando[:9])
			historial.append(comando)
			
		elif (comando[:7] == "history"):
			cmdHistory(historial)
			historial.append(comando)
			
		elif (comando[:8] == "ejecutar"):
			cmdEjecutar(comando[8:])
			historial.append(comando)

		elif (comando[:6] == "copiar"):
			cmdCopiar(comando[7:])
			historial.append(comando)

		elif (comando[:9] == "renombrar"):
			cmdRenombrar(comando[10:])
			historial.append(comando)

			

if __name__ == "__main__":
    main()
