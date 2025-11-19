import os
import time
import random
import simpy
from GeneradorAeronaves import *
from Aeronaves import * 
from FactoresExternos import *
from Input import *

def main():
    log = "../log.csv"
    #si log.txt tiene algo de información, cuando lo ejecutas se reinicia la info
    if os.path.exists(log):
        os.remove(log)
    #random.seed(2)
    evento = simpy.Environment()
    pistaAterrizaje = simpy.Resource(evento,capacity=1)
    pistaDespegue = simpy.Resource(evento,capacity=1)
    anuncio = simpy.Resource(evento,capacity=1)
    parking = simpy.Resource(evento,capacity=50)
    colaAterrizajes = simpy.Store(evento,capacity = 10)
    colaEstacionados = simpy.Store(evento,capacity = 50)
    colaSalidas = simpy.Store(evento,capacity = 1)
    colaDespegues = simpy.Store(evento,capacity = 10)
    #DATOS EN LISTAS
    estadoClima = {
        'clima':'Soleado',
        'retraso': 0.0
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
         "AeronavesCicloCompletoContadorTiempo": 0
    }
    hora,mes,retraso = parametrosIniciales()
    evento.process(procesos(evento,anuncio,parking,pistaAterrizaje,pistaDespegue,colaAterrizajes,colaEstacionados,colaSalidas,
                            colaDespegues,estadoClima,mes,retraso,turnos,aeronaves))
    evento.run(until=hora)
    resultados(turnos,aeronaves)
    


if __name__ == "__main__":
    main()
