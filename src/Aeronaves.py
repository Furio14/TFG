
def _init_(self,id,vueloId,origen,destino,horaSalida,horaLlegada):
    self.id = id
    self.vueloId = vueloId
    self.origen = origen
    self.destino = destino
    self.horaSalida = horaSalida
    self.horaLlegada = horaLlegada

def info(self):
    print("Aeronave: {self.id}")
    print("Vuelo: {self.vueloId}")
    print("Origen: {self.origen}")
    print("Destino: {self.destino}")
    print("Hora de salida: {self.horaSalida}")
    print("Hora de llegada: {self.horaLlegada}")
