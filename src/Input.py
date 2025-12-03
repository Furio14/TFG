import os
import time
import random
import simpy
import pandas as pd
from TorreDeControl import *
from GeneradorAeronaves import *
from Aeronaves import * 
from FactoresExternos import *

def parametrosIniciales():
        try:
            #HORAS
            horas = inputDatos("Cuantas horas quieres simular?",24,0,168)
                
            #VUELOS
            vuelos = inputDatos("Introduce la media de vuelos diarios ",200,100,400)
            
            #MES
            mes = inputMeses("En que mes quieres que empiece la simulacion?","ENERO")
            
            #TURNOS
            retraso = inputTurnos("En que turno quieres comenzar la simulacion?",0)

            #HORAS
            hora = int(horas) * 60 + retraso

            iteraciones = inputDatos("Cuantas iteraciones quieres realizar con estos params?",50,1,70)

        except ValueError as e:
                print("Error",e)
                return
        return hora,mes,retraso,vuelos,iteraciones

# Funcion que se encarga de que empieze el proceso a cierta hora
def procesos(evento,anuncio,parking,pistaAterrizaje,pistaDespegue,colaAterrizajes,colaEstacionados,colaSalidas,colaDespegues,estadoClima,mes,retraso,turnos,aeronaves):
    yield evento.timeout(retraso)
    evento.process(controlAereo(evento,anuncio,parking,pistaAterrizaje,pistaDespegue,colaAterrizajes,colaEstacionados,colaSalidas,
                                colaDespegues,estadoClima,mes,turnos,aeronaves,retraso))
    
    evento.process(logicaClima(evento,estadoClima,mes))

def resultados(turnos,aeronaves,resultados,semilla,i):
     resultados.append({
          "Prueba": i + 1,
          "Semilla": semilla,
          "TotalOperacionesAereas": turnos["Madrugada"] + turnos["Mañana"] + turnos["Tarde"] + turnos["Noche"],
          "MediaOperacionesAereas": round(((turnos["Madrugada"] + turnos["Mañana"] + turnos["Tarde"] + turnos["Noche"])/turnos["dias"]),2),
          "AeronavesTotales": Aeronave.totalAeronaves,
          "PasajerosTotales": Aeronave.totalPasajeros,
          "MediaPasajerosAeronave": round((Aeronave.totalPasajeros/Aeronave.totalAeronaves),2),
          "MediaTiempoCicloAeronaves": int(aeronaves["AeronavesCicloCompletoContadorTiempo"]/aeronaves["AeronavesCicloCompletoContador"]),
          "TotalMadrugada": turnos["Madrugada"],
          "MediaMadrugada":round((turnos["Madrugada"]/turnos["dias"]),2),
          "TasaLlegadaMadrugada": round((turnos["Madrugada"]/6),2),
          "TasaSalidaMadrugada": round((turnos["SalidaMadrugada"]/6),2),
          "TotalMañana": turnos["Mañana"],
          "MediaMañana":round((turnos["Mañana"]/turnos["dias"]),2),
          "TasaLlegadaMañana": round((turnos["Mañana"]/6),2),
          "TasaSalidaMañana": round((turnos["SalidaMañana"]/6),2),
          "TotalTarde": turnos["Tarde"],
          "MediaTarde":round((turnos["Tarde"]/turnos["dias"]),2),
          "TasaLlegadaTarde": round((turnos["Tarde"]/6),2),
          "TasaSalidaTarde": round((turnos["SalidaTarde"]/6),2),
          "TotalNoche": turnos["Noche"],
          "MediaNoche":round((turnos["Noche"]/turnos["dias"]),2),
          "TasaLlegadaNoche": round((turnos["Noche"]/6),2),
          "TasaSalidaNoche": round((turnos["SalidaNoche"]/6),2),

     })

def resDataset(listaResultados):
     dataset = pd.DataFrame(listaResultados)
     dataset.to_csv("../csv/resultados.csv",index=False,sep=',',decimal=',')
     analisis = [
        "TotalOperacionesAereas",
        "PasajerosTotales",
        "MediaTiempoCicloAeronaves",
        "TotalMadrugada",
        "TotalMañana",
        "TotalTarde",
        "TotalNoche"
     ]
     datasetEstadisticas = dataset[analisis].agg(['mean','min','max','std','var'])
     datasetEstadisticas.index = ["Media","Minimo","Maximo","DesviacionTipica","Varianza"]
     datasetEstadisticas.loc["Varianza","PasajerosTotales"] = None
     datasetEstadisticas.index.name = "Metricas"
     datasetEstadisticas = datasetEstadisticas.round(2)
     datasetEstadisticas.to_csv("../csv/estadisticas.csv",sep=",",decimal=",")
     print("FIN EXPERIMENTO")


##########################################Funciones Auxiliares##########################################

def inputDatos(pregunta,default,min,max):
     mensaje = f"{pregunta} [Default:{default}|Min:{min}|Max:{max}] : "
     while True:
          inputUser = input(mensaje)
          if inputUser == "":
            return default
          else:
               res = int(inputUser)
               if min <= res <= max:
                    return res
               else:
                    print(f"El numero no esta entre {min} - {max}")

def inputTurnos(pregunta,default):
    turnos = f"{pregunta} [MADRUGADA|Mañana|Tarde|Noche] : "
    while True:
        inputUser = input(turnos)
        if inputUser == "":
            return default
        turnosPosibles = inputUser.lower()
        if turnosPosibles == "madrugada":
            return default
        elif turnosPosibles == "mañana":
            retraso = 360
            return retraso
        elif turnosPosibles == "tarde":
            retraso = 720
            return retraso
        elif turnosPosibles == "noche":
            retraso = 1080
            return retraso
        else: 
            print("Pon un turno correcto")

def inputMeses(pregunta,default):
    mensaje = f"{pregunta} : "
    meses = ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE"
            ,"OCTUBRE","NOVIEMBRE","DICIEMBRE"]
    while True:
        inputUser = input(mensaje).upper()
        if inputUser == "":
                return default
        else:
            if inputUser not in meses:
                print("Introduzca un mes valido")
            else :
                 return inputUser
