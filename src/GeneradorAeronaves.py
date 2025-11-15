import random
from Aeronaves import *
from TorreDeControl import *


#Ciudades (Habria que ver algun dataset o crearlo con estos datos)
ciudades = ["Nueva York", "Milan", "Tokyo", "Beijing", "Shanghai", "Londres"]
vuelos = ["IB","BA","AA","V","AV","LX","DL"]

def generador(evento):
    letra = random.choice("ABCDEFGHIJLKMNOPQRSTUVWXYZ") # genera letra random
    id = f"{letra}{random.randint(0,999)}" # genera un id para un avion aleatorio
    idVuelo = f"{random.choice(vuelos)}{random.randint(0,999)}" # genera un id para un avion aleatorio
    estado = "Llegando" # estado de la aeronave
    pasajeros = random.randint(150,300) # genera un numero random de pasajeros
    origen = random.choice(ciudades) # genera 2 ciudades random
    destino = "Madrid"
    duracion = random.randint(1,5) * 60
    horasAeronave = int(evento.now) # Con el tiempo del reloj de simulacion calculamos los demas tiempos
    horasHastaSalida = ((horasAeronave - duracion)//60)%24
    minsHastaSalida = (horasAeronave - duracion) % 60
    horasHastaLlegada = (horasAeronave // 60) % 24
    minsHastaLlegada = horasAeronave % 60
    horaSalida = f"{horasHastaSalida:02d}:{minsHastaSalida:02d}"
    horaLlegada = f"{(horasHastaLlegada)%24:02d}:{minsHastaLlegada:02d}"            
    return Aeronave(id,idVuelo,estado,pasajeros,origen,destino,horaSalida,horaLlegada,horaLlegadaReal="---",horaEstacionado="---",horaProgramadaSalida="---",horaDespegue="---",tiempoCicloAvion="---")

