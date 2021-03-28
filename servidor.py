import socket

#49152-6535 puertos disponibles
port = 50002 #Puerto ocupado en TCP
BUFFER_SIZE = 2048 
MAQUINA="localhost"
PUERTO_MAQUINA=50001

def PedirPartida(IP, PUERTO):#Funcion para conexion UDP            
    UDP_SOCKET_CLIENTE=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creamos el socket UDP       
    mensaje = "PARTIDA"                       
    UDP_SOCKET_CLIENTE.sendto(mensaje.encode(),(IP,PUERTO))   
    response, _ = UDP_SOCKET_CLIENTE.recvfrom(BUFFER_SIZE) 
    UDP_SOCKET_CLIENTE.close()#Cerramos conexion UDP
    respuesta=response.decode()
    print("[°] El servidor de Cachipun respondio ", respuesta)
    return respuesta

def terminar_udp(IP, PUERTO):
    UDP_SOCKET_CLIENTE=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creamos el socket UDP       
    mensaje = "STOP"                       
    UDP_SOCKET_CLIENTE.sendto(mensaje.encode(),(IP,PUERTO)) #Enviamos el mensaje OK     
    response, _ = UDP_SOCKET_CLIENTE.recvfrom(BUFFER_SIZE) #Obtenemos la respuesta del servidor 
    UDP_SOCKET_CLIENTE.close()#Cerramos conexion UDP
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
        if ESTADO== "FAIL" : # si el url no se encuentra en la web ni en la LRU                        
            TCP_SOCKET_CLIENTE.send(respuesta.encode()) # Hacemos echo convirtiendo de nuevo a bytes       
            print("[°] Los servidores de juego no estan disponibles")                                                             
        else:                         
            TCP_SOCKET_CLIENTE.send(respuesta.encode()) # Enviamos el ok al cliente para la conexion UDP
            print("[°] Los servidores de juego operativos")                                                                     
            print("[°] Enviando Datos al cliente")                                   
            print("[°] Regresando a Conexion TCP")                                   
    print("-------------------------------------------")                                                             
print("[°] Apagando servidor")       
TCP_SOCKET_CLIENTE.close()#terminamos la conexion TCP
