import random
import csv
from Aeronaves import *

# Revisa todo el dataset y te da los datos por filas
def datosCSV(archivo):
    vuelos = []
    with open(archivo,mode = 'r', encoding='utf8') as a:
        lector = csv.DictReader(a)
        for fila in lector:
            fila['Duracion_Vuelo'] = int(fila['Duracion_Vuelo'])
            vuelos.append(fila)
    return vuelos

listaVuelos = datosCSV("../ciudades.csv")

#Genera aeronaves
def generador(evento):
    vueloRandom = random.choice(listaVuelos)
    letra = random.choice("ABCDEFGHIJLKMNOPQRSTUVWXYZ") # genera letra random
    id = f"{letra}{random.randint(0,999)}" # genera un id para un avion aleatorio
    idVuelo = vueloRandom["Vuelo_ID"] # genera un id para un avion aleatorio
    estado = "Llegando" # estado de la aeronave
    pasajeros = random.randint(150,300) # genera un numero random de pasajeros
    origen = vueloRandom["Ciudades"] # genera ciudades 
    destino = "Madrid"
    duracion = vueloRandom["Duracion_Vuelo"]
    horasAeronave = int(evento.now) # Con el tiempo del reloj de simulacion calculamos los demas tiempos
    horasHastaSalida = ((horasAeronave - duracion)//60)%24
    minsHastaSalida = (horasAeronave - duracion) % 60
    horasHastaLlegada = (horasAeronave // 60) % 24
    minsHastaLlegada = horasAeronave % 60
    horaSalida = f"{horasHastaSalida:02d}:{minsHastaSalida:02d}"
    horaLlegada = f"{(horasHastaLlegada)%24:02d}:{minsHastaLlegada:02d}"            
    return Aeronave(id,idVuelo,estado,pasajeros,origen,destino,horaSalida,horaLlegada,horaLlegadaReal="---",horaEstacionado="---",horaProgramadaSalida="---",horaDespegue="---",tiempoCicloAvion="---")

