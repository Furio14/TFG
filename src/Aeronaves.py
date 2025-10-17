
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
