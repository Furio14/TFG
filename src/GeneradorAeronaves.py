import random
from Aeronaves import *

#Ciudades
ciudades = ["Madrid", "Nueva York", "Milán", "Tokyo", "Beijing", "Shanghai", "Londres"]
vuelos = ["IB","BA","AA","V","AV","LX","DL"]

def generador():
    letra = random.choice("ABCDEFGHIJLKMNOPQRSTUVWXYZ") #genera letra random
    hora = random.randint(0,24)
    minuto = random.randint(0,59)
    id = f"{letra}{random.randint(0,999)}" #genera un id para un avión aleatorio
    idVuelo = f"{letra}{random.randint(0,999)}" #genera un id para un avión aleatorio
    origen,destino = random.sample(ciudades,2) #genera 2 ciudades random
    horaSalida = f"{hora:02d}:{minuto:02d}" #genera hora random
    duracion = random.randint(1,10)
    horaLlegada = f"{(hora + duracion)%24:02d}:{minuto:02d}"
    return Aeronave(id,idVuelo,origen,destino,horaSalida,horaLlegada)


