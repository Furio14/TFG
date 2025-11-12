import time
import heapq
import simpy
import random
from collections import deque
from GeneradorAeronaves import *
from Aeronaves import *

# Controla todo lo que tiene que ver con el aterrizaje despegue y estacionameinto de aeronaves
def torreDeControl(evento,anuncio,parking,pistaAterrizajes,pistaDespegues,colaAterrizajes,colaEstacionados,colaSalidas,colaDespegues):
    while True:
            probAviones = random.expovariate(0.2) # 1/lambda
            yield evento.timeout(probAviones)
            avion = generador(evento) # se generan aviones
            # Ciclo completo de cada avion
            evento.process(cicloAvion(evento,avion,parking,anuncio,pistaAterrizajes,pistaDespegues,colaAterrizajes,colaEstacionados,colaSalidas,colaDespegues))

# Nos indica el ciclo completo de cada avion
def cicloAvion(evento,avion,parking,anuncio,pistaAterrizajes,pistaDespegues,colaAterrizajes,colaEstacionados,colaSalidas,colaDespegues):
    # Nos indica primero si esta llegando el avion
    yield evento.process(controlLlegadas(evento,avion,colaAterrizajes))
    # Despues de seguido indica si efectivamente ha aterrizado el avion
    yield evento.process(controlAterrizajes(evento,pistaAterrizajes,colaAterrizajes,colaEstacionados))
    # Después nos indica cuando ha estacionado la aeronave
    yield evento.process(controlEstacionados(evento,parking,colaEstacionados,colaSalidas))
    # Después de estacionar nos dice a que hora está programado el vuelo
    yield evento.process(controlSalidas(evento,anuncio,colaSalidas,colaDespegues))
    # Nos indica si el avion esta despegando
    yield evento.process(controlDespegues(evento,pistaDespegues,colaDespegues))
    
# Una vez solicitan aterrizar los aviones se les añade a la cola de llegadas
def controlLlegadas(evento,avion,colaAterrizajes):
    yield colaAterrizajes.put(avion)
    avion.infoColaAterrizaje(evento)
    yield evento.timeout(0.5)

# Una vez llegan las aeronaves las retira de la otra cola y las añade a la de aterrizados
def controlAterrizajes(evento,pista,colaAterrizajes,colaEstacionados):
    if colaAterrizajes:
        aterriza = yield colaAterrizajes.get()
        with pista.request( ) as request: # si hay request de aterrizar en pista
            yield request
            tiempoHastaAterrizar = 0
            yield evento.timeout(tiempoHastaAterrizar)
            aterriza.horaLlegadaReal = tiempoEvento(evento.now)
            aterriza.infoAterrizaje(evento)
            yield colaEstacionados.put(aterriza)   
    else:
        yield evento.timeout(0.1)

# Una vez aterrizan las aeronaves te informa de si esta estacionado
def controlEstacionados(evento,parking,colaEstacionados,colaSalidas):
    if colaEstacionados:
        estacionado = yield colaEstacionados.get()
        with parking.request() as request: # si hay request de estacionar
            yield request
            tiempoHastaEstacionamiento = int(random.triangular(5.0,15.0,mode=10.0))
            yield evento.timeout(tiempoHastaEstacionamiento)
            estacionado.horaEstacionado = tiempoEvento(evento.now)
            estacionado.infoEstacionado(evento)
            yield colaSalidas.put(estacionado)
    else:
        yield evento.timeout(0.1)

# Una vez estan estacionadas las aeronaves se les asigna una hora de salida para ser anunciado
def controlSalidas(evento,anuncio,colaSalidas,colaDespegues):
    if colaSalidas:
        salida = yield colaSalidas.get()
        avion = aeronaveSalida(evento,salida)
        with anuncio.request() as request:
            yield request
            avion.infoSalidas(evento)
            horaProgramada,minProgramado = funcSplit(avion.horaProgramadaSalida)
            tiempoProgramado = horaProgramada*60 + minProgramado
            tiempoEspera = max(0,tiempoProgramado - int(evento.now)) 
            yield evento.timeout(tiempoEspera)
            yield colaDespegues.put(salida)
    else:
        yield evento.timeout(0.1)

# Una vez estan estacionadas las aeronaves se les asigna una tarea de salir a pista (no esta implementado el control de flujo de pasajeros)
def controlDespegues(evento,pista,colaDespegues):
    if colaDespegues:
        salida = yield colaDespegues.get()
        avion = salida
        with pista.request() as request: #hace request por si no hay ningún avión en la pista
            yield request
            tiempoDespegando = random.uniform(1.0,3.0)
            yield evento.timeout(tiempoDespegando)
            avion.horaDespegue = tiempoEvento(evento.now)
            hora,min = funcSplit(avion.horaLlegadaReal)
            tiempoCiclo = abs(hora*60+min - int(evento.now))
            avion.tiempoCicloAvion = tiempoEvento(tiempoCiclo)
            avion.horaLlegadaReal = "---"
            avion.infoDespegues(evento)
    else:
        yield evento.timeout(0.1)

# Una vez una aeronave aterriza (mirar flujo de pasajeros para ver si hay retraso), se le asigna otro destino con diferente id de vuelo y destino
def aeronaveSalida(evento,avion):
    avion.origen = avion.destino
    avion.destino = random.choice(ciudades) # El origen no puede ser también el destino
    vuelo = ''.join(filter(str.isalpha,avion.vueloId))
    numeroVuelo = int(''.join(filter(str.isdigit,avion.vueloId)))
    avion.vueloId = f"{vuelo}{numeroVuelo + random.randint(1,5)}"
    tiempoActual =int(evento.now) 
    horaSalida = tiempoActual + int(random.triangular(100,200,140)) # asignamos tiempo random de salida
    horaLlegada = horaSalida + random.randint(120,300)
    horaSalida,minSalida = funcMin(horaSalida)
    horaLlegada,minLlegada = funcMin(horaLlegada)
    avion.horaSalida = f"{horaSalida:02d}:{minSalida:02d}" # hora de salida respecto a la llegada
    avion.horaLlegada = f"{horaLlegada:02d}:{minLlegada:02d}"
    avion.horaProgramadaSalida = avion.horaSalida # lahora programa es igual que la d salida nueva
    return avion

#################################################FUNCIONES AUXILIARES#################################################
def tiempoEvento(evento):
    hora,min = funcMin(int(evento))
    horasTiempo,minsTiempo = funcTiempo(hora,min)
    horaFunc = f"{horasTiempo%24:02d}:{minsTiempo%60:02d}"
    return horaFunc

def funcTiempo(horas,minutos):
    if minutos > 59:
        hora = minutos // 60
        minutos %= 60
        horas += hora
    if horas > 23:
        horas %= 24
    return horas,minutos

def funcMin(tiempo):
    hora = (tiempo // 60) % 24
    min = tiempo % 60
    return hora,min

def funcSplit(param):
    hora,min = map(int, param.split(':'))
    return hora,min
