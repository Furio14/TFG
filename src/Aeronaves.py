
class Aeronave:
    def __init__(self,id,vueloId,origen,destino,horaSalida,horaLlegada):
        self.id = id
        self.vueloId = vueloId
        self.origen = origen
        self.destino = destino
        self.horaSalida = horaSalida
        self.horaLlegada = horaLlegada

    def info(self):
        print(f"Aeronave: {self.id}")
        print(f"Vuelo: {self.vueloId}")
        print(f"Origen: {self.origen}")
        print(f"Destino: {self.destino}")
        print(f"Hora de salida: {self.horaSalida}")
        print(f"Hora de llegada: {self.horaLlegada}")

        with open("../log.txt","a") as log:
            print("-----------COMIENZO SIMULACION-----------",file=log)
            print(f"Aeronave: {self.id}",file=log)
            print(f"Vuelo: {self.vueloId}",file=log)
            print(f"Origen: {self.origen}",file=log)
            print(f"Destino: {self.destino}",file=log)
            print(f"Hora de salida: {self.horaSalida}",file=log)
            print(f"Hora de llegada: {self.horaLlegada}",file=log)