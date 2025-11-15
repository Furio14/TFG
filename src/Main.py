import os
import time
import random
import simpy
from TorreDeControl import *
from GeneradorAeronaves import *
from Aeronaves import * 
from FactoresExternos import *

def parametrosIniciales():
        try:
            #DATOS DE LOS PARAMETROS
            #HORAS
            horas = input("Cuantas horas quieres simular? : ")
            if int(horas) <= 0:
                raise ValueError("El numero de horas tiene que ser mayor que 0")
            
            #MES
            mes = input("En que mes quieres que empiece la simulacion? : ").upper()
            meses = ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE"
                    ,"OCTUBRE","NOVIEMBRE","DICIEMBRE"]
            
            if mes not in meses:
                raise ValueError("Introdzca un mes valido")
            
            #TURNOS
            turnos = input("En que turno quieres comenzar la simulacion? [Madrugada,Mañana,Tarde,Noche] : ")
            turnosPosibles = turnos.lower()
            if turnosPosibles == "madrugada":
                retraso = 0
            elif turnosPosibles == "mañana":
                retraso = 360
            elif turnosPosibles == "tarde":
                retraso = 720
            elif turnosPosibles == "noche":
                retraso = 1080
            else: 
                raise ValueError("Pon un turno correcto")

            #HORAS
            hora = int(horas) * 60 + retraso
        except ValueError as e:
                print("Error",e)
                return
        return hora,mes,retraso

def procesos(evento,anuncio,parking,pistaAterrizaje,pistaDespegue,colaAterrizajes,colaEstacionados,colaSalidas,colaDespegues,estadoClima,mes,retraso,turnos):
    yield evento.timeout(retraso)
    evento.process(torreDeControl(evento,anuncio,parking,pistaAterrizaje,pistaDespegue,colaAterrizajes,colaEstacionados,colaSalidas,colaDespegues,estadoClima,mes,turnos))
    evento.process(logicaClima(evento,estadoClima,mes))

def main():
    log = "../log.csv"
    #si log.txt tiene algo de información, cuando lo ejecutas se reinicia la info
    if os.path.exists(log):
        os.remove(log)

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
    turnos = {
         "Madrugada": 0,
         "Mañana" : 0,
         "Tarde" : 0,
         "Noche" : 0
    }
    hora,mes,retraso = parametrosIniciales()
    evento.process(procesos(evento,anuncio,parking,pistaAterrizaje,pistaDespegue,colaAterrizajes,colaEstacionados,colaSalidas,colaDespegues,estadoClima,mes,retraso,turnos))
    evento.run(until=hora)
    print("------Resultados Finales de la Simulación------")
    print("Total Aeronaves Simuladas: ",Aeronave.totalAeronaves)
    print("Total Pasajeros: ",Aeronave.totalPasajeros)
    print("Total Operaciones Aéreas Madrugada: ",turnos["Madrugada"])
    print("Total Operaciones Aéreas Mañana: ",turnos["Mañana"])
    print("Total Operaciones Aéreas Tarde: ",turnos["Tarde"])
    print("Total Operaciones Aéreas Noche: ",turnos["Noche"])


if __name__ == "__main__":
    main()
