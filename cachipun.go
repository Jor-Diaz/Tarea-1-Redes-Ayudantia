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

func ejecucion_partidas( PORT string){
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
                n, addr, err := connection.ReadFromUDP(buffer)
                fmt.Print("# El cliente envio -> ", string(buffer[0:n]),"\n")                
                data := []byte(strconv.Itoa(random(1, 4)))                
                if strings.TrimSpace(string(buffer[0:n])) == "STOP" {
                        fmt.Println("[°]El cliente quiere cerrar la conexion")
                        fmt.Printf("Enviarémos : %s\n", string("Terminada"))
                        _, err = connection.WriteToUDP([]byte(string("Terminada")), addr)
                        if err != nil {
                                fmt.Println(err)
                                return
                        }
                        return
                }else{
                        fmt.Printf("Enviarémos : %s\n", string(data))
                        _, err = connection.WriteToUDP(data, addr)
                        if err != nil {
                                fmt.Println(err)
                                return
                        }
                }                        
        }
}

func main() {
        PUERTO_SERVICIO:="localhost:50001" //DEFINIDO POR DEFECTO  
        IP:="localhost"      
        fmt.Println("[°] Bienvenidos al servidor de Super-Cachipun 2021")        
        fmt.Println("[°] El servicio para pedir partidas se ejecutara en el puerto ", PUERTO_SERVICIO)                
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
                        partida:=random(1, 11)                        
                        if partida > 1 {       
                                PUERTO_PARTIDAS:=random(50010, 50021)                                     
                                mensaje:= "OK|"+IP+"|"+strconv.Itoa(PUERTO_PARTIDAS)
                                _, err = connection.WriteToUDP([]byte(mensaje), addr)
                                if err != nil {
                                        fmt.Println(err)
                                        return
                                }                                
                                ejecucion_partidas(strconv.Itoa(PUERTO_PARTIDAS))
                        }else{
                                mensaje:=[]byte("FAIL|X|X")
                                _, err = connection.WriteToUDP(mensaje, addr)
                                if err != nil {
                                        fmt.Println(err)
                                        return
                                }
                        }                
                }else{
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