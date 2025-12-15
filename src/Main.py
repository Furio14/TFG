import os
import time
import random
import simpy
from GeneradorAeronaves import *
from Aeronaves import * 
from FactoresExternos import *
from Input import *
import Graficas

def main():
    log = "../csv/log.csv"
    semilla = 1000
    hora,mes,retraso,vuelos,iteraciones = parametrosIniciales() #se sacan los parametros iniciales que elige el user
    listaResultados = []
    for i in range(int(iteraciones)):
        #si log.txt tiene algo de información, cuando lo ejecutas se reinicia la info
        if os.path.exists(log):
            os.remove(log)
        semillaActual = semilla + i
        print(f"Iteracion: {i}")
        random.seed(semillaActual)
        evento = simpy.Environment()
        pistaAterrizaje = simpy.PriorityResource(evento,capacity=1) #servidor para la pista de aterrizaje
        pistaDespegue = simpy.PriorityResource(evento,capacity=1) #servidor para la pista de despegue
        anuncio = simpy.Resource(evento,capacity = 1) #servidor para la los anuncios de viajes de despegue
        parking = simpy.Store(evento,capacity=50) #servidor para el estacionamiento
        colaAterrizajes = simpy.Store(evento,capacity = 10)
        colaEstacionados = simpy.Store(evento,capacity = 50)
        colaSalidas = simpy.Store(evento,capacity = 1)
        colaDespegues = simpy.Store(evento,capacity = 10)
        parkingBus = simpy.Store(evento,capacity = 10)
        for i in range(1,51):
            parking.put(i)
        for i in range(51,61):
            parkingBus.put(i)
        #DATOS EN LISTAS
        estadoClima = {
            'clima':'Soleado',
            'retraso': 0.0,
            'estadoPistaAterrizaje':'Activa',
            'estadoPistaDespegue':'Activa'
        }
        turnos = {
            "Madrugada": 0,
            "Mañana" : 0,
            "Tarde" : 0,
            "Noche" : 0,
            "SalidaMadrugada": 0,
            "SalidaMañana" : 0,
            "SalidaTarde" : 0,
            "SalidaNoche" : 0,
            "dias" : 1
        }
        aeronaves = {
            "AeronavesEstacionados" : 0,
            "AeronavesEnColaLlegada" : 0,
            "AeronavesEnColaSalida" : 0,
            "AeronavesCicloCompletoContador": 0,
            "AeronavesCicloCompletoContadorTiempo": 0,
            "AeronavesDiarias" : 0
        }
        Aeronave.totalAeronaves = 0
        Aeronave.totalPasajeros = 0
        aeronaves["AeronavesDiarias"] = vuelos
        evento.process(procesos(evento,anuncio,parking,parkingBus,pistaAterrizaje,pistaDespegue,colaAterrizajes,colaEstacionados,colaSalidas,
                                colaDespegues,estadoClima,mes,retraso,turnos,aeronaves))
        evento.run(until=hora) #tiempo que dura la simulacion
        resultados(turnos,aeronaves,listaResultados,semillaActual,i) #te guarda los resultados generales en un txt
    resDataset(listaResultados)


if __name__ == "__main__":
    main()
    Graficas.generadorGraficas()
