import platform
import subprocess
import os
import time
import signal
import shutil
# import distutils.dir_util
import ftplib
import logging
import psutil # instalar desde la terminal -> pip install psutil

# ---LOGS--- #
	#IMPORTANTE:: SE DEBE CREAR LA CARPETA /var/log/shell ANTES
def logTransferencias(status, mensaje):
	# Configuramos el logger
	logging.basicConfig(filename='/home/camidorego/Desktop/LOGS/shell_transferencias.log',
						filemode='w',
						level=logging.INFO,
						format='%(asctime)s %(message)s')

	# Creamos el objeto logger
	logger = logging.getLogger()

	if status==1:
		# Transferencia exitosa
		logger.info(mensaje) 
	elif status == 0:
		# Transferencia con error
		logger.info(mensaje)

def logErrores(mensaje):
	# Configuramos el logger
	logging.basicConfig(filename='/home/camidorego/Desktop/LOGS/sistema_error.log',
						filemode='w',
						level=logging.INFO,
						format='%(asctime)s %(message)s')
	# Creamos el objeto logger
	logger = logging.getLogger()

	# Se escribe el mensaje de error
	logger.info(mensaje)

def logMovimientos(mensaje):
	# Configuramos el logger
	logging.basicConfig(filename='/home/camidorego/Desktop/LOGS/registro_movimientos.log',
						filemode='w',
						level=logging.INFO,
						format='%(asctime)s %(message)s')
	# Creamos el objeto logger
	logger = logging.getLogger()

	# Se escribe el mensaje 
	logger.info(mensaje)



# ---COMANDOS--- #

#Funcion para listar un directorio -> listar o listar [path]
def cmdListar(cadena):
	if(len(cadena) == 6): # se listan los archivos del path actual
		path = os.getcwd() # se obtiene el path actual
		lista = os.listdir(path) # se obtienen los archivos
		print("Archivos en ", path, ":")
		print(lista)

		# Se guarda en el log de movimientos
		mensaje = "listar: se listaron los archivos de " + path 
		logMovimientos(mensaje)
	else:
		cadena = cadena.split(sep=' ')
		path = cadena[1] # se guarda el path introducido
		if os.path.exists(path):
			lista = os.listdir(path) # se obtienen los archivos
			print("Archivos en ", path, ":")
			print(lista)

			# Se guarda en el log de movimientos
			mensaje = "listar: se listaron los archivos de " + path 
			logMovimientos(mensaje)
		else:
			print("El path ingresado es incorrecto")

			# Se guarda en el log de errores
			mensaje = "listar: El path ingresado es incorrecto"
			logErrores(mensaje)

#Fucnion para crear un directorio -> creardir [path]
def cmdCrearDir(cadena):
	cadena=cadena.split(sep=' ')
	for i in range(0, len(cadena)-1):
		try:
			os.mkdir(os.path.abspath(cadena[i])) # se crea el directorio
			print("se creo el directorio correctamente")
		# Se guarda en el log de movimientos
			mensaje = "creardir: se creo un directorio en " + cadena[i] 
			logMovimientos(mensaje)
		except FileExistsError:
			print("La carpeta ya existe")

		# Se guarda en el log de errores
		mensaje = "creardir: La carpeta ya existe"
		logErrores(mensaje)

#Funcion para ir a un directorio -> ir [path]
def cmdIr(path):
	
	if os.path.exists(path): # se verifica el path introducido
		try:
			os.chdir(os.path.abspath(path))  # se cambia de directorio al path solicitado
			path_n = os.getcwd() # se obtiene la nueva ubicacion 
			print("El path actual es: ", path_n)

			# Se guarda en el log de movimientos
			mensaje = "ir: el usuario se movio desde " + path + " a " + path_n
			logMovimientos(mensaje)
		except:
			print("Error al cambiar de directorio")

			# Se guarda en el log de errores
			mensaje = "ir: Error al cambiar de directorio"
			logErrores(mensaje)

	else:
		print("El path introducido es incorrecto")

		# Se guarda en el log de errores
		mensaje = "ir: El path ingresado es incorrecto"
		logErrores(mensaje)

#Funcion para obtener el path del directorio actual -> pwd
def cmdPwd():
	path = os.getcwd() # se obtiene el path actual
	print("El path actual es: ", path) # se imprime

	# Se guarda en el log de movimientos
	mensaje = "pwd: se mostro " + path 
	logMovimientos(mensaje)

#Funcion para cambiar los permisos de un directorio -> permisos [permisos en Octal] [path]
def cmdPermisos(cadena):
	cadena = cadena.split(sep = ' ')
	permisos = cadena[0]
	path = cadena[1]
	
	if os.path.exists(path):
		try:
			os.chmod(os.path.abspath(path), permisos)

			# Se guarda en el log de movimientos
			mensaje = "permisos: se cambiaron los permisos de " + path 
			logMovimientos(mensaje)
		except:
			print("Error al cambiar los permisos")

			# Se guarda en el log de errores
			mensaje = "permisos: Error al cambiar los permisos"
			logErrores(mensaje)
	else:
		print("El path introducido es incorrecto")

		# Se guarda en el log de errores
		mensaje = "permisos: El path ingresado es incorrecto"
		logErrores(mensaje)

#Funcion que imprime el historial de comandos
def cmdHistory(comandos): 
	print("El historial de comandos es:")
	for i in range(0, len(comandos)):
		print(i+1, ": ", comandos[i])

	# Se guarda en el log de movimientos
	mensaje = "historial: se mostraron los comandos del historial " 
	logMovimientos(mensaje)

#Funcion para ejecutar otros comandos de linux
def cmdEjecutar(cadena):
	try:
		subprocess.run(cadena.split())

		# Se guarda en el log de movimientos
		mensaje = "ejecutar: se ejecuto " + cadena 
		logMovimientos(mensaje)
	except:
		print("Comando no encontrado")

		# Se guarda en el log de errores
		mensaje = "ejecutar: comando no encontrado" + cadena
		logErrores(mensaje)

#Funcion para buscar una cadena dentro de un archivo  -> buscar "cadena a buscar"
def cmdBuscar(cadena):
	cadena = cadena.split(sep=' ')
	path = cadena[0]
	palabra = cadena[1]

	if(os.path.isfile(path)):
		a = open(path,"r") # se abre el archivo
		texto = a.read()  # se guarda el contenido en texto 

		if palabra in texto: # se busca la cadena
			print("La cadena existe en el archivo.")

			# Se guarda en el log de movimientos
			mensaje = "buscar: se encontro la cadena en el archivo"  
			logMovimientos(mensaje)
		else:
			print("La cadena no existe en el archivo.")
			# Se guarda en el log de errores
			mensaje = "buscar: La cadena no existe en el archivo."
			logErrores(mensaje)

			# Se guarda en el log de movimientos
			mensaje = "buscar: no se encontro la cadena en el archivo"  
			logMovimientos(mensaje)
	else:
		print("No existe el archivo.")
		# Se guarda en el log de errores
		mensaje = "buscar: No existe el archivo."
		logErrores(mensaje)

#Funcion para transferir archivos via ftp
def cmdTransferencia():
	# se solicita la informacion necesaria -- VISITAR https://dlptest.com/ftp-test/ PARA INFO DE PRUEBA
	hostname=input("Ingrese el host: ")
	username=input("Ingrese le nombre de usuario: ")
	password=input("Ingrese la contrasena: ")

	# nos conectamos a un servidor FTP
	ftp_server=ftplib.FTP(hostname, username, password)

	# forzamos que la codificacion sea en el formato Unicode
	ftp_server.encoding="utf-8"

	# se solicita el nomnbre del archivo con su respectiva extension
	archivo=input("Ingrese el nombre del archivo: ") # se debe ingresar con su extension
	

	try:
		while True:
			# se le pregunta al usuario que desea hacer con el archivo
			opcion=int(input("OPCIONES:\n 1)Subir archivo \n 2)Descargar archivo \n 3)Ver lista de archivos del servidor \n SELECCIONE UNA OPCION: "))
			
			if opcion==1: 
				with open(archivo, "rb") as file: # el archivo se lee en binario
					ftp_server.storbinary(f"STOR {archivo}", file) # se sube el archivo
				print("Se subio el archivo exitosamente")

				# se listan los archivos del servidor
				print("LISTA DE ARCHIVOS DEL SERVIDOR: ")
				ftp_server.dir()

				# Se informa en el log
				mensaje = "FTP UPLOAD: " + archivo
				status = 1
				logTransferencias(status, mensaje)

				# se cierra la conexion
				ftp_server.quit()

				# Se guarda en el log de movimientos
				mensaje2 = "transferencia: se subio el archivo " + archivo
				logMovimientos(mensaje2)

				break

			if opcion==2:
				with open(archivo, "wb") as file: # el archivo se escribe en binario
					ftp_server.retrbinary(f"RETR {archivo}", file.write) # se descarga el archivo
				print("Se descargo el archivo exitosamente")

				# se listan los archivos del servidor
				print("LISTA DE ARCHIVOS DEL SERVIDOR: ")
				ftp_server.dir()

				# se muestra el contenido del archivo descargado
				print("El archivo descargado fue: %s", archivo)
				file=open(archivo, "r")
				print("CONTENIDO DEL ARCHIVO:  ", file.read())

				# Se informa en el log
				mensaje = "FTP DOWNLOAD: " + archivo
				status = 1
				logTransferencias(status, mensaje)

				# se cierra la conexion
				ftp_server.quit()

				# Se guarda en el log de movimientos
				mensaje2 = "transferencia: se descargo el archivo " + archivo
				logMovimientos(mensaje2)

				break

			elif opcion==3:
				print("LISTA DE ARCHIVOS DEL SERVIDOR: ")
				ftp_server.dir()

			else:
				print("Opcion fuera de rango, vuelva a ingresar")
	except:
		print("Ocurrio un error")

		# Se informa en el log
		mensaje = "FTP ERROR: " + archivo
		status = 0
		logTransferencias(status, mensaje)

		# se cierra la conexion
		ftp_server.quit() # se cierra la conexion

		# Se guarda en el log de errores
		mensaje2 = "transferencia: error en la transferencia del archivo " + archivo
		logErrores(mensaje2)
def cmdKill():
	# el usuario elije el pid del proceso que quiere terminar
	while True:
		opcion1 = int(input("OPCIONES: \n 1)Ver lista de procesos corriendo \n 2)Ya tengo el PID del proceso que quiero terminar \n Elije una opcion: "))
		if opcion1 == 1:
			for proc in psutil.process_iter():
				try:
					processName = proc.name()
					processID = proc.pid
					print(processName , ' ::: ', processID)
				except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
					pass
		elif opcion1 == 2:
			break
		else:
			print("Opcion fuera de rango, vuelva a ingresar")
	
	pid=int(input("Ingresa el pid del proceso: "))
	os.kill(pid, signal.SIGKILL)
	print("Se termino el proceso")

	# Se guarda en el log de movimientos
	mensaje = "kill: se termino el proceso " + str(pid) 
	logMovimientos(mensaje)

# Funcion para copiar archivo/s y/o directorio/s a un path especifico -> copiar [archivos/directorios] [path_destino]
def cmdCopiar(cadena):
    # Se separa el argumento por los espacios
	cadena = cadena.split(sep = ' ')
	print("Cantidad=", len(cadena))
    # El path de destino esta es el ultimo objeto del argumento
	destino = cadena[len(cadena)-1] 
    
	for i in range(0, len(cadena)-1):
        # Si lo que se quiere copiar es un directorio
		try:
			shutil.copytree(cadena[i], destino)
			print("Se copio exitosamente el directorio ", cadena[i])

            # Se escribe el mensaje en el log
			msg="copiar: Se copio exitosamente el directorio" + cadena[i]
			logMovimientos(msg)

        # Si lo que se quiere copiar es un archivo
		except OSError as err: 
			if err.errno==errno.ENOTDIR:
				shutil.copy2(cadena[i], destino)
				print("Se copio exitosamente el archivo ", cadena[i])

				# Se escribe el mensaje en el log
				msg = "copiar: Se copio exitosamente el archivo" + cadena[i]
				logMovimientos(msg)

			else:
				print("Error: %s" %err)

				# Se escribe el mensaje en el log
				msg="copiar:  " + err
				logErrores(msg)

# Funcion para renombrar un archivo o directorio -> renombrar [archivo_original] [archivo_con_nombre_nuevo]
def cmdRenombrar(cadena): 
	# Se separan los paths en arrays
	cadena = cadena.split(sep = ' ')
	original = cadena[0]
	nuevo = cadena[1] 

	if os.path.exists(original):
		try :
			os.rename(original,nuevo)
			print("Renombrado exitosamente a ") + nuevo

			# Se guarda en el log de movimientos
			mensaje = "renombrar: se renombro exitosamente" + nuevo
			logMovimientos(mensaje)

		except:
			print("Error al renombrar ") + nuevo
			# Se guarda en el log de errores
			mensaje = "renombrar: Error al renombrar " + nuevo
			logErrores(mensaje)


	else:
		print("No existe el archivo o directorio.")
		# Se guarda en el log de errores
		mensaje = "renombrar: No existe el archivo o directorio."
		logErrores(mensaje)

# Funcion para mover archivo/s y/o directorio/s a un path especifico -> mover [archivos/directorios] [path_destino]
def cmdMover(cadena): 
	#se separan los paths en arrays
	cadena = cadena.split(sep=' ') 

	# el path de destino es el ultimo elemento del array
	destino=cadena[len(cadena)-1]

	for i in range(0, len(cadena)-1):
		if os.path.exists(cadena[i]):
			try :
				shutil.move(cadena[i], destino) # Se mueve al path de destino
				print("Se movio exitosamente ", cadena[i])

				# Se guarda en el log de movimientos
				mensaje = "mover: se movio exitosamente" + cadena[i]
				logMovimientos(mensaje)

			except:
				print("Error al mover.")
				# Se guarda en el log de errores
				mensaje = "mover: Error al mover " + cadena[i]
				logErrores(mensaje)


		else:
			print("No existe el archivo o directorio ") + cadena[i]	
			# Se guarda en el log de errores
			mensaje = "mover: No existe el archivo o directorio " + cadena[i]
			logErrores(mensaje)



#Funcion main
def main():
	historial=[]
	print("Binvenido a BashCamiChris 1.0")
	while True:
		comando = input(">> ")

		if (comando[:6] == "listar"): 
			cmdListar(comando)
			historial.append("listar")

		elif (comando[:8] == "creardir"): 
			cmdCrearDir(comando[9:])
			historial.append("creardir")

		elif (comando == "pwd"): 
			cmdPwd()
			historial.append("pwd")
			
		elif (comando[:2] == "ir"): 
			cmdIr(comando[3:])
			historial.append("ir")
			
		elif (comando == "salir"):
			break

		elif (comando[:8] == "permisos"):
			cmdPermisos(comando[:9])
			historial.append("permisos")
			
		elif (comando[:7] == "history"):
			cmdHistory(historial)
			historial.append("permisos")
			
		elif (comando[:8] == "ejecutar"):
			cmdEjecutar(comando[8:])
			historial.append("ejecutar")

		elif (comando[:6] == "copiar"):
			cmdCopiar(comando[7:])
			historial.append(comando)

		elif (comando[:9] == "renombrar"):
			cmdRenombrar(comando[10:])
			historial.append(comando)

		elif (comando[:5] == "mover"):
			cmdMover(comando[6:])
			historial.append(comando)

		elif (comando[:6] == "buscar"):
			cmdBuscar(comando[7:])
			historial.append(comando)

		elif (comando[:8]=="transfer"):
			cmdTransferencia()
			historial.append("transfer")

		elif (comando[:4]=="kill") :
			cmdKill()
			historial.append("kill")
		
		elif(comando[:6]=="copiar"):
			cmdCopiar(comando[7:])
			historial.append("copiar")

		elif (comando[:9]=="renombrar"):
			cmdRenombrar(comando[10:])
			historial.append("renombrar")
		
		elif(comando[:5]=="mover"):
			cmdMover(comando[6:])
			historial.append("mover")
			

if __name__ == "__main__":
    main()
