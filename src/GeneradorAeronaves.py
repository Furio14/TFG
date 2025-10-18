import random
from Aeronaves import *

horasAeronave = f"{0:02d}"
minutosAeronave = f"{0:02d}"
comienzoSimulacion = False

#Ciudades
ciudades = ["Madrid", "Nueva York", "Milan", "Tokyo", "Beijing", "Shanghai", "Londres"]
vuelos = ["IB","BA","AA","V","AV","LX","DL"]

def generador():
    global minutosAeronave
    global horasAeronave
    global comienzoSimulacion
    letra = random.choice("ABCDEFGHIJLKMNOPQRSTUVWXYZ") # genera letra random
    hora = random.randint(0,24)
    minutoSalida = random.randint(0,59)
    minutoLlegada = random.randint(0,59)
    id = f"{letra}{random.randint(0,999)}" # genera un id para un avión aleatorio
    idVuelo = f"{random.choice(vuelos)}{random.randint(0,999)}" # genera un id para un avión aleatorio
    origen,destino = random.sample(ciudades,2) # genera 2 ciudades random
    duracion = random.randint(1,5)
    if not comienzoSimulacion:
        horaSalida = f"{horasAeronave}:{minutosAeronave}"
        horaLlegada = f"{(hora + duracion)%24:02d}:{minutoLlegada:02d}"
        horasAeronave = hora + duracion
        minutosAeronave = minutoLlegada + duracion
        comienzoSimulacion = True
    else:
            if (minutosAeronave + duracion) > 59:
                horasAeronave += 1
                minutosAeronave = random.randint(0,4)
            horaSalida = f"{horasAeronave - duracion:02d}:{minutoSalida:02d}"
            horaLlegada = f"{(horasAeronave)%24:02d}:{minutosAeronave + duracion:02d}"
            minutosAeronave = minutosAeronave + duracion
            
    return Aeronave(id,idVuelo,origen,destino,horaSalida,horaLlegada)
