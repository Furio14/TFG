
class Aeronave:
    comienzo = False
    def __init__(self,id,vueloId,origen,destino,horaSalida,horaLlegada):
        self.id = id
        self.vueloId = vueloId
        self.origen = origen
        self.destino = destino
        self.horaSalida = horaSalida
        self.horaLlegada = horaLlegada

    # Te da la info de los aeronaves que se añaden a la cola
    def infoColaAterrizaje(self):
        with open("../log.txt","a") as log:
            if not Aeronave.comienzo:
                print("-----------COMIENZO SIMULACION-----------",file=log)
                Aeronave.comienzo = True
            print("",file=log)
            print("***AVION ANIADIDO A COLA ATERRIZAJE***",file=log)
            print(f"Aeronave: {self.id}",file=log)
            print(f"Vuelo: {self.vueloId}",file=log)
            print(f"Origen: {self.origen}",file=log)
            print(f"Destino: {self.destino}",file=log)
            print(f"Hora de salida: {self.horaSalida}",file=log)
            print(f"Hora de llegada: {self.horaLlegada}",file=log)

    # Te da la info de las aeronaves que ya han aterrizado
    def infoAterrizaje(self):
        with open("../log.txt","a") as log:
            print("",file=log)
            print("***AVION ATERRIZADO***",file=log)
            print(f"Aeronave: {self.id}",file=log)
            print(f"Vuelo: {self.vueloId}",file=log)
            print(f"Origen: {self.origen}",file=log)
            print(f"Destino: {self.destino}",file=log)
            print(f"Hora de salida: {self.horaSalida}",file=log)
            print(f"Hora de llegada: {self.horaLlegada}",file=log)
            
    # Te da la info de las aeronaves que ya estan estacionadas
    def infoEstacionado(self):
        with open("../log.txt","a") as log:
            print("",file=log)
            print("***AVION ESTACIONADO***",file=log)
            print(f"Aeronave: {self.id}",file=log)
            print(f"Vuelo: {self.vueloId}",file=log)
            print(f"Origen: {self.origen}",file=log)
            print(f"Destino: {self.destino}",file=log)
            print(f"Hora de salida: {self.horaSalida}",file=log)
            print(f"Hora de llegada: {self.horaLlegada}",file=log)
    