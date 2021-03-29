package main

import (
        "fmt"
        "math/rand"
        "net"        
        "strconv"         
        "strings"
        "time"
)

func random(min, max int) int {
        return rand.Intn(max-min) + min
}

func ganador_ronda(jugador int,bot int) int{    
    if jugador%2 == bot%2{
        if jugador<bot{
            return 1
        }else{
            return 2
        }
    }else{
        if jugador<bot{
            return 2        
        }else{
            return 1
        }
    }
}

func partida_multiplayer(PORT string){
    jugador1:="0"        
    jugador2:="0"
    j1:=0  
    j2:=0      
    var direccion1 *net.UDPAddr
    var direccion2 *net.UDPAddr   
    fmt.Println("[°] Se iniciará el ejecutor de partidas en el puerto ", PORT)
    s, err := net.ResolveUDPAddr("udp4", "localhost:"+PORT)
    if err != nil {
            fmt.Println(err)
            return
    }
    connection, err := net.ListenUDP("udp4", s)
    if err != nil {
            fmt.Println(err)
            return
    }
    defer connection.Close()
    buffer := make([]byte, 1024)
    rand.Seed(time.Now().Unix())
    for {   
            if j1==3 || j2==3{
                fmt.Println("[°] Termino la partida, muchas gracias por jugar Super-Cachipun 2021")    
                return
            }    
            n, addr, err := connection.ReadFromUDP(buffer)                                  
            mensaje := strings.Split(string(buffer[0:n]), "|")            
            if mensaje[0]=="1"{    
                    fmt.Print("[°] El Jugador 1 envio -> ", string(buffer[0:n]),"\n")                                                                                                
                    jugador1=mensaje[1]
                    direccion1=addr
            }else{
                  fmt.Print("[°] El Jugador 2 envio -> ", string(buffer[0:n]),"\n")                                                                      
                  jugador2=mensaje[1]                  
                  direccion2=addr
            }
            if jugador1!="0" && jugador2!="0"{
                    fmt.Println("\n") 
                    _, err = connection.WriteToUDP([]byte(string(jugador2)), direccion1)
                    if err != nil {
                            fmt.Println(err)
                            return
                    }                                
                    _, err = connection.WriteToUDP([]byte(string(jugador1)), direccion2)
                    if err != nil {
                            fmt.Println(err)
                            return
                    }                                
                    if jugador1!=jugador2{
                        sv, err := strconv.Atoi(jugador1); 
                        if err != nil {
                            fmt.Printf("%T, %v\n", sv, sv)
                        }
                        aux1:=sv
                        sv, err = strconv.Atoi(jugador2); 
                        if err != nil {
                            fmt.Printf("%T, %v\n", sv, sv)
                        }
                        ganador:=ganador_ronda(aux1,sv)
                        if ganador==1{
                            j1=j1+1
                        }else{
                            j2=j2+1
                        }                    
                    }
                jugador2="0"
                jugador1="0"
            }                                                                                     
    }    
}


func main() {
    PUERTO_SERVICIO:="localhost:50001" //DEFINIDO POR DEFECTO          
    IP:="localhost"      
    jugadores:=0
    var direccion1 *net.UDPAddr
    var direccion2 *net.UDPAddr        
    fmt.Println("[°] Bienvenidos al servidor de Super-Cachipun 2021")        
    fmt.Println("[°] El servicio de partidas multiplayer se esta ejecutando en el puerto 5001")  
    s, err := net.ResolveUDPAddr("udp4", PUERTO_SERVICIO)
    if err != nil {
            fmt.Println(err)
            return
    }
    connection, err := net.ListenUDP("udp4", s)
    if err != nil {
            fmt.Println(err)
            return
    }
    defer connection.Close()
    buffer := make([]byte, 1024)
    rand.Seed(time.Now().Unix())                          
    for {
        n, addr, err := connection.ReadFromUDP(buffer)
        fmt.Print("# El cliente envio -> ", string(buffer[0:n]),"\n")                                
        if strings.TrimSpace(string(buffer[0:n])) == "PARTIDA" {                            
                if jugadores == 1 && direccion1!=addr {       
                    direccion2=addr                        
                    PUERTO_PARTIDAS:=random(50010, 50021)                                     
                    mensaje:= "OK|"+IP+"|"+strconv.Itoa(PUERTO_PARTIDAS)
                    go partida_multiplayer(strconv.Itoa(PUERTO_PARTIDAS))
                    _, err = connection.WriteToUDP([]byte(mensaje), direccion1)
                    if err != nil {
                            fmt.Println(err)
                            return
                    }                                
                    _, err = connection.WriteToUDP([]byte(mensaje), direccion2)
                    if err != nil {
                            fmt.Println(err)
                            return
                    }                                                    
                    jugadores=0
                }else{
                    direccion1=addr
                    jugadores=1
                }                        
        }else{
            direccion1=addr
            fmt.Println("[°]El cliente quiere cerrar el servidor la conexion")
            fmt.Printf("Enviarémos : %s\n", string("Terminada"))
            _, err = connection.WriteToUDP([]byte(string("Terminada")), addr)
            if err != nil {
                    fmt.Println(err)
                    return
            }
            return
        }         
    }                       
}