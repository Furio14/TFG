import os
import time
import random
import simpy
from TorreDeControl import *
from GeneradorAeronaves import *
from Aeronaves import * 
from FactoresExternos import *

def main():
    log = "../log.csv"
    #si log.txt tiene algo de información, cuando lo ejecutas se reinicia la info
    if os.path.exists(log):
        os.remove(log)
    try:
        evento = simpy.Environment()
        
        pistaAterrizaje = simpy.Resource(evento,capacity=1)
        pistaDespegue = simpy.Resource(evento,capacity=1)
        anuncio = simpy.Resource(evento,capacity=1)
        parking = simpy.Resource(evento,capacity=2)
        colaAterrizajes = simpy.Store(evento,capacity = 10)
        colaEstacionados = simpy.Store(evento)
        colaSalidas = simpy.Store(evento)
        colaDespegues = simpy.Store(evento,capacity = 10)
        estadoClima = {
        'clima':'Soleado',
        'retraso': 0.0
    }
        horas = input("Cuantas horas quieres simular? ")
        hora = int(horas) * 60
        if hora <= 0:
            print("El numero de horas tiene que ser mayor que 0")
        evento.process(torreDeControl(evento,anuncio,parking,pistaAterrizaje,pistaDespegue,colaAterrizajes,colaEstacionados,colaSalidas,colaDespegues,estadoClima))
        evento.process(logicaClima(evento,estadoClima))
        evento.run(until=hora)
        print("------Resultados Finales de la Simulación------")
        print("Total Aeronaves Simuladas: ",Aeronave.totalAeronaves)
        print("Total Pasajeros : ",Aeronave.totalPasajeros)

    except ValueError:
        print("No es un número valido")

if __name__ == "__main__":
    main()
