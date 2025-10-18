
import csv


class Aeronave:
    comienzo = False
    def __init__(self,id,vueloId,origen,destino,horaSalida,horaLlegada,aterrizado,estacionado):
        self.id = id
        self.vueloId = vueloId
        self.origen = origen
        self.destino = destino
        self.horaSalida = horaSalida
        self.horaLlegada = horaLlegada
        self.aterrizado = aterrizado
        self.estacionado = estacionado

    def infoColaAterrizaje(self):
        logs = "../log.csv"
        #CSV
        try:
            with open(logs,"r") as log:
                existeEncabezado = True
        except FileNotFoundError:
            existeEncabezado = False

        with open(logs,"a", newline="") as log:
            writer = csv.writer(log)

            if not existeEncabezado:
                writer.writerow(["ID","ID_Vuelo","Origen","Destino","Hora_Salida","Hora_Llegada","Aterrizado","Estacionado"])
            
            writer.writerow([self.id,self.vueloId,self.origen,self.destino,self.horaSalida,self.horaLlegada,self.aterrizado,self.estacionado])
            
###################################################################################################################
            #if not Aeronave.comienzo:
            #    print("-----------COMIENZO SIMULACION-----------",file=log)
            #    Aeronave.comienzo = True
            #print("",file=log)
            #print("***AVION ANIADIDO A COLA ATERRIZAJE***",file=log)
            #print(f"Aeronave: {self.id}",file=log)
            #print(f"Vuelo: {self.vueloId}",file=log)
            #print(f"Origen: {self.origen}",file=log)
            #print(f"Destino: {self.destino}",file=log)
            #print(f"Hora de salida: {self.horaSalida}",file=log)
            #print(f"Hora de llegada: {self.horaLlegada}",file=log)
###################################################################################################################

    # Te da la info de las aeronaves que ya han aterrizado
    def infoAterrizaje(self):
        logs = "../log.csv"
        self.aterrizado = True
        with open(logs,"a") as log:
            writer = csv.writer(log)
            writer.writerow([self.id,self.vueloId,self.origen,self.destino,self.horaSalida,self.horaLlegada,self.aterrizado,self.estacionado])

###################################################################################################################
            #print("",file=log)
            #print("***AVION ATERRIZADO***",file=log)
            #print(f"Aeronave: {self.id}",file=log)
            #print(f"Vuelo: {self.vueloId}",file=log)
            #print(f"Origen: {self.origen}",file=log)
            #print(f"Destino: {self.destino}",file=log)
            #print(f"Hora de salida: {self.horaSalida}",file=log)
            #print(f"Hora de llegada: {self.horaLlegada}",file=log)
###################################################################################################################  
# 
#         
    # Te da la info de las aeronaves que ya estan estacionadas
    def infoEstacionado(self):
        logs = "../log.csv"
        self.estacionado = True
        with open(logs,"a") as log:
            writer = csv.writer(log)
            writer.writerow([self.id,self.vueloId,self.origen,self.destino,self.horaSalida,self.horaLlegada,self.aterrizado,self.estacionado])

###################################################################################################################
            #print("",file=log)
            #print("***AVION ESTACIONADO***",file=log)
            #print(f"Aeronave: {self.id}",file=log)
            #print(f"Vuelo: {self.vueloId}",file=log)
            #print(f"Origen: {self.origen}",file=log)
            #print(f"Destino: {self.destino}",file=log)
            #print(f"Hora de salida: {self.horaSalida}",file=log)
            #print(f"Hora de llegada: {self.horaLlegada}",file=log)
###################################################################################################################
    