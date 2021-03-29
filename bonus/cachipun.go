package main

import (
        "fmt"
        "math/rand"
        "net"        
        //"strconv"
        "strings"
        "time"
)


func main() {
        PUERTO_SERVICIO:="localhost:50001" //DEFINIDO POR DEFECTO          
        jugador1:="0"        
        jugador2:="0"        
        var direccion1 *net.UDPAddr
        var direccion2 *net.UDPAddr
        rondas:=0
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
                if rondas==3{
                        return
                }    
                n, addr, err := connection.ReadFromUDP(buffer)                                  
                mensaje := strings.Split(string(buffer[0:n]), "|")
                if mensaje[0]=="1"{    
                        fmt.Print("[°] El Jugador 1 envio -> ", string(buffer[0:n]),"\n")                                                                            
                        direccion1=addr
                        jugador1=mensaje[1]
                }else{
                      fmt.Print("[°] El Jugador 2 envio -> ", string(buffer[0:n]),"\n")                                                    
                      direccion2=addr  
                      jugador2=mensaje[1]
                }
                if jugador1!="0" && jugador2!="0"{
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
                                rondas=rondas+1
                        }
                }                                                                                     
        }        
        fmt.Println("[°] Termino la partida, muchas gracias por jugar Super-Cachipun 2021")   
}