
import csv
import random
import time

logs = "../csv/log.csv"
class Aeronave:
    totalPasajeros = 0
    totalAeronaves = 0
    def __init__(self,id,vueloId,estado,pasajeros,origen,destino,horaSalida,horaLlegada,horaLlegadaReal,horaEstacionado,horaProgramadaSalida,horaDespegue,tiempoCicloAvion):
        self.id = id
        self.vueloId = vueloId
        self.estado = estado
        self.pasajeros = pasajeros
        self.origen = origen
        self.destino = destino
        self.horaSalida = horaSalida
        self.horaLlegada = horaLlegada
        self.horaLlegadaReal = horaLlegadaReal
        self.horaEstacionado = horaEstacionado
        self.horaProgramadaSalida = horaProgramadaSalida
        self.horaDespegue = horaDespegue
        self.tiempoCicloAvion = tiempoCicloAvion
        self.tiempoLlegadaMinutos = 0
        self.ticket = ""
        self.gate = ""

    def infoColaAterrizaje(self,evento,estadoClima,mes,aeronaves):
        try:
            with open(logs,"r") as log:
                existeEncabezado = True
        except FileNotFoundError:
            existeEncabezado = False
        with open(logs,"a", newline="") as log:
            writer = csv.writer(log)
            if not existeEncabezado:
                writer.writerow(["Reloj","ID","ID_Vuelo","Estado","Pasajeros","Origen","Destino","Hora_Salida_Origen","Hora_Programada_Llegada_Destino","Hora_Llegada_Destino","Hora_Estacionamiento","Hora_Programada_Salida","Hora_Despegue","Tiempo_Ciclo_Aeronave","Mes","Clima","Aeronaves_En_Cola_Llegada","Aeronaves_En_Estacionamiento","Aeronaves_En_Cola_Salida","Gate"])
            reloj = Aeronave.infoReloj(evento.now)
            self.estado = "Llegando"
            writer.writerow([reloj,self.id,self.vueloId,self.estado,self.pasajeros,self.origen,self.destino,self.horaSalida,self.horaLlegada,self.horaLlegadaReal,self.horaEstacionado,self.horaProgramadaSalida,self.horaDespegue,self.tiempoCicloAvion,mes,estadoClima['clima'],aeronaves["AeronavesEnColaLlegada"],aeronaves["AeronavesEstacionados"],aeronaves["AeronavesEnColaSalida"],""])

    # Te da la info de las aeronaves que ya han aterrizado
    def infoAterrizaje(self,evento,estadoClima,mes,aeronaves):
        reloj = Aeronave.infoReloj(evento.now)
        self.estado = "Aterrizaje"
        with open(logs,"a") as log:
            writer = csv.writer(log)
            writer.writerow([reloj,self.id,self.vueloId,self.estado,self.pasajeros,self.origen,self.destino,self.horaSalida,self.horaLlegada,self.horaLlegadaReal,self.horaEstacionado,self.horaProgramadaSalida,self.horaDespegue,self.tiempoCicloAvion,mes,estadoClima['clima'],aeronaves["AeronavesEnColaLlegada"],aeronaves["AeronavesEstacionados"],aeronaves["AeronavesEnColaSalida"],""])

    # Te da la info de las aeronaves que ya estan estacionadas
    def infoEstacionado(self,evento,estadoClima,mes,aeronaves):
        reloj = Aeronave.infoReloj(evento.now)
        self.estado = "Estacionado"
        with open(logs,"a") as log:
            writer = csv.writer(log)
            writer.writerow([reloj,self.id,self.vueloId,self.estado,self.pasajeros,self.origen,self.destino,self.horaSalida,self.horaLlegada,self.horaLlegadaReal,self.horaEstacionado,self.horaProgramadaSalida,self.horaDespegue,self.tiempoCicloAvion,mes,estadoClima['clima'],aeronaves["AeronavesEnColaLlegada"],aeronaves["AeronavesEstacionados"],aeronaves["AeronavesEnColaSalida"],self.gate])
    
    # Te da la info aproximada de cuando va a salir un vuelo
    def infoSalidas(self,evento,estadoClima,mes,aeronaves):
        reloj = Aeronave.infoReloj(evento.now)
        self.estado = "Programado"
        with open(logs,"a") as log:
            writer = csv.writer(log)
            writer.writerow([reloj,self.id,self.vueloId,self.estado,self.pasajeros,self.origen,self.destino,self.horaSalida,self.horaLlegada,self.horaLlegadaReal,self.horaEstacionado,self.horaProgramadaSalida,self.horaDespegue,self.tiempoCicloAvion,mes,estadoClima['clima'],aeronaves["AeronavesEnColaLlegada"],aeronaves["AeronavesEstacionados"],aeronaves["AeronavesEnColaSalida"],self.gate])

    # Te da la info de cuando un avion se mete en la cola de despegues
    def infoColaDespegues(self,evento,estadoClima,mes,aeronaves):
        reloj = Aeronave.infoReloj(evento.now)
        self.estado = "ColaDespegues"
        with open(logs,"a") as log:
            writer = csv.writer(log)
            writer.writerow([reloj,self.id,self.vueloId,self.estado,self.pasajeros,self.origen,self.destino,self.horaSalida,self.horaLlegada,self.horaLlegadaReal,self.horaEstacionado,self.horaProgramadaSalida,self.horaDespegue,self.tiempoCicloAvion,mes,estadoClima['clima'],aeronaves["AeronavesEnColaLlegada"],aeronaves["AeronavesEstacionados"],aeronaves["AeronavesEnColaSalida"],self.gate])


    # Te da la info de cuando ha despegado un avion, si han habido retrasos etc etc
    def infoDespegues(self,evento,estadoClima,mes,aeronaves):
        reloj = Aeronave.infoReloj(evento.now)
        self.estado = "Despegando"
        with open(logs,"a") as log:
            writer = csv.writer(log)
            writer.writerow([reloj,self.id,self.vueloId,self.estado,self.pasajeros,self.origen,self.destino,self.horaSalida,self.horaLlegada,self.horaLlegadaReal,self.horaEstacionado,self.horaProgramadaSalida,self.horaDespegue,self.tiempoCicloAvion,mes,estadoClima['clima'],aeronaves["AeronavesEnColaLlegada"],aeronaves["AeronavesEstacionados"],aeronaves["AeronavesEnColaSalida"],""])

    def infoReloj(evento):
            minsActuales = int(evento)
            minDia = minsActuales % 1440
            hora = minDia//60
            min = minDia%60
            reloj = f"{hora:02d}:{min:02d}"
            return reloj
    
