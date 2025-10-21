
import csv
import random
import time

logs = "../log.csv"
class Aeronave:
    comienzo = False
    def __init__(self,id,vueloId,estado,pasajeros,origen,destino,horaSalida,horaLlegada):
        self.id = id
        self.vueloId = vueloId
        self.estado = estado
        self.pasajeros = pasajeros
        self.origen = origen
        self.destino = destino
        self.horaSalida = horaSalida
        self.horaLlegada = horaLlegada


    def infoColaAterrizaje(self):
        try:
            with open(logs,"r") as log:
                existeEncabezado = True
        except FileNotFoundError:
            existeEncabezado = False

        with open(logs,"a", newline="") as log:
            writer = csv.writer(log)
            if not existeEncabezado:
                writer.writerow(["ID","ID_Vuelo","Estado","Pasajeros","Origen","Destino","Hora_Salida","Hora_Llegada"])
            self.estado = "Llegando"
            writer.writerow([self.id,self.vueloId,self.estado,self.pasajeros,self.origen,self.destino,self.horaSalida,self.horaLlegada])
            time.sleep(random.randint(1,2))
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
        self.estado = "Aterrizaje"
        with open(logs,"a") as log:
            writer = csv.writer(log)
            writer.writerow([self.id,self.vueloId,self.estado,self.pasajeros,self.origen,self.destino,self.horaSalida,self.horaLlegada])
            time.sleep(random.randint(1,2))
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
        self.estado = "Estacionado"
        with open(logs,"a") as log:
            writer = csv.writer(log)
            writer.writerow([self.id,self.vueloId,self.estado,self.pasajeros,self.origen,self.destino,self.horaSalida,self.horaLlegada])
            time.sleep(random.randint(1,2))

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
    
    # Te da la info aproximada de cuando va a salir un vuelo
    def infoSalidas(self):
        self.estado = "Programado"
        with open(logs,"a") as log:
            writer = csv.writer(log)
            writer.writerow([self.id,self.vueloId,self.estado,self.pasajeros,self.origen,self.destino,self.horaSalida,self.horaLlegada])
            time.sleep(random.randint(1,2))

    # Te da la info de cuando ha despegado un avion, si han habido retrasos etc etc
    def infoDespegues(self):
        self.estado = "Despegando"
        with open(logs,"a") as log:
            writer = csv.writer(log)
            writer.writerow([self.id,self.vueloId,self.estado,self.pasajeros,self.origen,self.destino,self.horaSalida,self.horaLlegada])
            time.sleep(random.randint(1,2))
