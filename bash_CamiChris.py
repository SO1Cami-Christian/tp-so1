import platform
import subprocess
import os
import time
import signal

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

def cmdCrearDir(path):
	if os.path.exists(path): # se verifica que el path introducido existe
		os.mkdir(os.path.abspath(path)) # se crea el directorio
	else:
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
		print(i++, ": ", comandos[i])

def cmdEjecutar(cadena):
	try:
		subprocess.run(cadena.split())
	except:
		print("Comando no encontrado")



def main():
	historial=[]
	print("Binvenido a BashCamiChris 1.0")
	while True:
		comando = input(">> ")
		if (comando[:6] == "listar"): # -> listar o listar [path]
			cmdListar(comando)
			historial.append("listar")
		elif (comando[:8] == "creardir"): # -> creardir [path]
			cmdCrearDir(comando[10:])
			historial.append("creardir")
		elif (comando == "pwd"): # -> pwd
			cmdPwd()
			historial.append("pwd")
			
		elif (comando[:2] == "ir"): # -> ir [path]
			cmdIr(comando[3:])
			historial.append("ir")
			
		elif (comando == "salir"):
			break
		elif (comando[:8] == "permisos"): # -> permisos [permisos en Octal] [path]
			cmdPermisos(comando[:9])
			historial.append("permisos")
			
		elif (comando[:7] == "history"):
			cmdHistory(historial)
			historial.append("permisos")
			
		elif (comando[:8] == "ejecutar"):
			cmdEjecutar(comando[8:])
			historial.append("ejecutar")
			

if __name__ == "__main__":
    main()
