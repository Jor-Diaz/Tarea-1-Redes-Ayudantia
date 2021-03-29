import socket
BUFFER_SIZE = 2048
UDP_SOCKET_CLIENTE=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creamos el socket UDP		
mensaje = "2|3"                       
UDP_SOCKET_CLIENTE.sendto(mensaje.encode(),("localhost",50001)) #Enviamos el mensaje OK		
response, _ = UDP_SOCKET_CLIENTE.recvfrom(BUFFER_SIZE) #Obtenemos la respuesta del servidor	
print(response)
UDP_SOCKET_CLIENTE.close()#Cerramos conexion UDP