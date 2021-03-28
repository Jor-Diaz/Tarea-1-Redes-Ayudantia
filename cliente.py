import socket

#49152-6535 puertos disponibles
host='localhost'
port = 50002 #Puerto ocupado en TCP
BUFFER_SIZE = 2048

def menu():
	print("# Ingrese 1 para jugar")
	print("# Ingrese 2 para salir")

def ganador_ronda(jugador,bot):
	if jugador==bot:
		return 0
	elif jugador%2 == bot%2:
		if jugador<bot:
			return 1
		else:
			return 2
	else:
		if jugador<bot:
			return 2
		else:
			return 1

def jugar(IP,PUERTO):
	print("[°] El primer jugador que gane 3 rondas gana la partida\n")	
	bot=0
	jugador=0
	while bot<3 and jugador<3:
		print ("[°] Ingrese 1 para Jugar Piedra ")
		print ("[°] Ingrese 2 para Jugar Papel ")
		print ("[°] Ingrese 3 para Jugar Tijera ")
		jugada=input("Jugada: ")
		jugada_bot=solicitar_jugada(IP, PUERTO)
		ganador=ganador_ronda(int(jugada),int(jugada_bot))
		if ganador==1:
			jugador+=1
			print("[°] Usted gano esta ronda :)")
		elif ganador==2:
			bot+=1
			print("[°] El Bot gano esta ronda :C")
		else:
			print("[°] Esta ronda fue un empate :S")
		print("\n")
		print("[°] El marcador actual es jugador ", jugador, " , Bot ", bot)
	if bot > jugador:
			print("[°] El ganador de la partida fue el Bot :( , más suerte para la proxima!")
	else:
		print("[°] El ganador de la partida fue el Usted :D ,Felicitaciones!")
	terminar_udp(IP, PUERTO)
	return	

def terminar_udp(IP, PUERTO):
	UDP_SOCKET_CLIENTE=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creamos el socket UDP		
	mensaje = "STOP"                       
	UDP_SOCKET_CLIENTE.sendto(mensaje.encode(),(IP,PUERTO)) #Enviamos el mensaje OK		
	response, _ = UDP_SOCKET_CLIENTE.recvfrom(BUFFER_SIZE) #Obtenemos la respuesta del servidor	
	UDP_SOCKET_CLIENTE.close()#Cerramos conexion UDP
	return

def solicitar_jugada(IP, PUERTO):
	jugadas={"1":"Piedra","2":"Papel","3":"Tijera"}
	UDP_SOCKET_CLIENTE=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creamos el socket UDP		
	mensaje = "JUGADA"                       
	UDP_SOCKET_CLIENTE.sendto(mensaje.encode(),(IP,PUERTO)) #Enviamos el mensaje OK		
	response, _ = UDP_SOCKET_CLIENTE.recvfrom(BUFFER_SIZE) #Obtenemos la respuesta del servidor	
	UDP_SOCKET_CLIENTE.close()#Cerramos conexion UDP
	jugada=response.decode()
	print("[°] El bot jugo ", jugadas[jugada])
	return jugada

TCP_SOCKET_CLIENTE=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creamos Conexion TCP
TCP_SOCKET_CLIENTE.connect((host, port)) #Nos conectamos
opcion=""
print("[°]Conexión establecida con el servidor en el puerto "+str(port))
print("\n")
print("##################################################################################")
print("    Bienvenido al juego Super-Cachipun 2021 ")
print("##################################################################################")
while opcion!="2": 
	menu()
	opcion=str(input())
	TCP_SOCKET_CLIENTE.send(opcion.encode())		
	if opcion=="1":					
		data = TCP_SOCKET_CLIENTE.recv(BUFFER_SIZE)#recibimos resultado
		data=data.decode()				
		status,ip,puerto=data.strip().split("|")
		puerto=int(puerto)
		if status=="OK":#si existe la pagina			
			print("[°] Servidores Operativos ")	
			print("[°] Conectando con Super-Cachipun 2021 ")	
			print("\n")		
			print("[°] Comienza el Juego ")
			jugar(ip,puerto)			
			print("[°] Partida Terminada ")
		else:#si es que no esta disponible
			print("[°] El servidor no esta disponible, lamentamos la situación")		
	print("-------------------------------------------\n") 	
TCP_SOCKET_CLIENTE.close()#terminamos la conexion 	
print("\n")
print("##################################################################################")
print(" Gracias por haber jugado Super-Cachipun 2021 ")
print("##################################################################################")
print("[°] Conexion TCP terminada")
