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
            #HORAS
            horas = inputDatos("Cuantas horas quieres simular?",24,0,420)
                
            #VUELOS
            vuelos = inputDatos("Introduce la media de vuelos diarios : ",200,100,500)
            
            #MES
            mes = inputMeses("En que mes quieres que empiece la simulacion?","ENERO")
            
            #TURNOS
            retraso = inputTurnos("En que turno quieres comenzar la simulacion?",0)

            #HORAS
            hora = int(horas) * 60 + retraso

        except ValueError as e:
                print("Error",e)
                return
        return hora,mes,retraso,vuelos

def procesos(evento,anuncio,parking,pistaAterrizaje,pistaDespegue,colaAterrizajes,colaEstacionados,colaSalidas,colaDespegues,estadoClima,mes,retraso,turnos,aeronaves):
    yield evento.timeout(retraso)
    evento.process(controlAereo(evento,anuncio,parking,pistaAterrizaje,pistaDespegue,colaAterrizajes,colaEstacionados,colaSalidas,
                                colaDespegues,estadoClima,mes,turnos,aeronaves,retraso))
    
    evento.process(logicaClima(evento,estadoClima,mes))

def resultados(turnos,aeronaves):
     with open("../resultados.txt","w",encoding="utf8") as f:
        f.write("------Resultados Finales de la Simulación------" + "\n")
        f.write("\n" + "*****MADRUGADA*****" + "\n")
        f.write("Total Operaciones Aéreas Madrugada: " + str(turnos["Madrugada"]) + "\n")
        f.write("Media Operaciones Aéreas Madrugada: " + str(round((turnos["Madrugada"]/turnos["dias"]),2)) + "\n")
        f.write("Tasa de Operaciones Llegada λ_h Madrugada: " + str(round((turnos["Madrugada"]/6),2)) + "\n")
        f.write("Tasa de Operaciones Salida λ_h Madrugada: " + str(round((turnos["SalidaMadrugada"]/6),2)) + "\n")
        f.write("\n" + "*****MAÑANA*****" + "\n")
        f.write("Total Operaciones Aéreas Mañana: " + str(turnos["Mañana"]) + "\n")
        f.write("Media Operaciones Aéreas Mañana: " + str(round((turnos["Mañana"]/turnos["dias"]),2)) + "\n")
        f.write("Tasa de Operaciones Llegada λ_h Mañana: " + str(round((turnos["Mañana"]/6),2)) + "\n")
        f.write("Tasa de Operaciones Salida λ_h Mañana: " + str(round((turnos["SalidaMañana"]/6),2)) + "\n")
        f.write("\n" + "*****TARDE*****" + "\n")
        f.write("Total Operaciones Aéreas Tarde: " + str(turnos["Tarde"]) + "\n")
        f.write("Media Operaciones Aéreas Tarde: " + str(round((turnos["Tarde"]/turnos["dias"]),2)) + "\n")
        f.write("Tasa de Operaciones Llegada λ_h Tarde: " + str(round((turnos["Tarde"]/6),2)) + "\n")
        f.write("Tasa de Operaciones Salida λ_h Tarde: " + str(round((turnos["SalidaTarde"]/6),2)) + "\n")
        f.write("\n" + "*****NOCHE*****" + "\n")
        f.write("Total Operaciones Aéreas Noche: " + str(turnos["Noche"]) + "\n")
        f.write("Media Operaciones Aéreas Noche: " + str(round((turnos["Noche"]/turnos["dias"]),2)) + "\n")
        f.write("Tasa de Operaciones Llegada λ_h Noche: " + str(round((turnos["Noche"]/6),2)) + "\n")
        f.write("Tasa de Operaciones Salida λ_h Noche: " + str(round((turnos["SalidaNoche"]/6),2)) + "\n")
        f.write("\n" + "*****DATOS GLOBALES*****" + "\n")
        f.write("Total Operaciones Aéreas: " + str(turnos["Madrugada"] + turnos["Mañana"] + turnos["Tarde"] + turnos["Noche"]) + "\n")
        f.write("Media Operaciones Aéreas: " + str(round(((turnos["Madrugada"] + turnos["Mañana"] + turnos["Tarde"] + turnos["Noche"])/turnos["dias"]),2)) + "\n")
        f.write("Total Aeronaves Simuladas: " + str(Aeronave.totalAeronaves) + "\n")
        f.write("Total Pasajeros: " + str(Aeronave.totalPasajeros) + "\n")
        f.write("Media de Pasajeros por Aeronave: " + str(round((Aeronave.totalPasajeros/Aeronave.totalAeronaves),2)) + "\n")
        f.write("Media Tiempo Ciclo Completo Aeronaves: " + str(int(aeronaves["AeronavesCicloCompletoContadorTiempo"]/aeronaves["AeronavesCicloCompletoContador"])) + " minutos \n")

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
                    print("El numero no esta entre {min} - {max}")

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