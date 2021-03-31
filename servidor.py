import socket

#49152-6535 puertos disponibles
port = 50002 #Puerto ocupado en TCP
BUFFER_SIZE = 2048 
MAQUINA="localhost"
PUERTO_MAQUINA=50001

def PedirPartida(IP, PUERTO):#Funcion para conexion UDP            
    UDP_SOCKET_CLIENTE=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creamos el socket UDP       
    mensaje = "PARTIDA"  #Solicitar partida al servidor cachipun                 
    UDP_SOCKET_CLIENTE.sendto(mensaje.encode(),(IP,PUERTO))   
    response, _ = UDP_SOCKET_CLIENTE.recvfrom(BUFFER_SIZE) 
    UDP_SOCKET_CLIENTE.close()#Cerramos conexion UDP
    respuesta=response.decode()
    print("[°] El servidor de Cachipun respondio ", respuesta)
    return respuesta

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

def terminar_udp(IP, PUERTO):
    UDP_SOCKET_CLIENTE=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creamos el socket UDP       
    mensaje = "STOP"                       
    UDP_SOCKET_CLIENTE.sendto(mensaje.encode(),(IP,PUERTO)) #Enviamos el mensaje OK     
    response, _ = UDP_SOCKET_CLIENTE.recvfrom(BUFFER_SIZE) #Obtenemos la respuesta del servidor 
    UDP_SOCKET_CLIENTE.close()#Cerramos conexion UDP
    return

def intermediario_partida(TCP_SOCKET_CLIENTE,IP,PUERTO):
    while True:   
        data = TCP_SOCKET_CLIENTE.recv(BUFFER_SIZE) #estamos recibiendo lo que dice el cliente
        if data.decode() =="JUGADA": #quiere jugar
            jugada=solicitar_jugada(IP, PUERTO) # le pedimos al bot
            TCP_SOCKET_CLIENTE.send(jugada.encode())  #le pasamos la jugada al cliente
        if data.decode()=="TERMINAR": #no quiere jugar
            TCP_SOCKET_CLIENTE.send("OK".encode())
            terminar_udp(IP, PUERTO) #terminar conexión con cachipun
            print("[°] Partida terminada\n")   
            break
    return

## MAIN
TCP_SOCKET_SERVIDOR=socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Creamos un objeto socket tipo TCP
TCP_SOCKET_SERVIDOR.bind(('', port)) 
TCP_SOCKET_SERVIDOR.listen(1) # Esperamos la conexión del cliente 
print('[°] Conexión abierta. Escuchando solicitudes en el puerto ' +str(port)) 
TCP_SOCKET_CLIENTE, addr = TCP_SOCKET_SERVIDOR .accept() # Establecemos la conexión con el cliente 
print('[°] Conexión establecida con el cliente')
while True:    
    # Recibimos bytes, convertimos en str
    data = TCP_SOCKET_CLIENTE.recv(BUFFER_SIZE)       
    mensaje = data.decode()                
    print("\n")
    print('# Mensaje recibido de cliente: {}'.format(data.decode('utf-8')))         
    if mensaje == "2":                
        terminar_udp(MAQUINA, PUERTO_MAQUINA)    
        print("[°] Conexión terminada")                    
        break                             
    else:            
        print("[°] Consultando estado servidores de Cachipun")           
        respuesta=PedirPartida(MAQUINA, PUERTO_MAQUINA)
        ESTADO,IP,PUERTO=respuesta.split("|")        
        if ESTADO== "FAIL" : # Si el servidor no esta disponible                     
            TCP_SOCKET_CLIENTE.send("FAIL".encode()) # Avisamos al cliente que no se puede jugar       
            print("[°] Los servidores de juego no estan disponibles")                                                             
        else:                         
            TCP_SOCKET_CLIENTE.send("OK".encode()) # Le avisamos al cliente que si esta disponible
            print("[°] Los servidores de juego operativos")         
            intermediario_partida(TCP_SOCKET_CLIENTE,IP,int(PUERTO))                                                                                                                                        
    print("-------------------------------------------")                                                             
print("[°] Apagando servidor")       
TCP_SOCKET_CLIENTE.close()#terminamos la conexion TCP
