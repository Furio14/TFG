import time
import heapq
import simpy
import random
from collections import deque
from GeneradorAeronaves import *
from Aeronaves import *

colaAterrizajes = deque()
colaEstacionados = deque()
colaSalidas = deque()
colaDespegues = deque()

# Controla todo lo que tiene que ver con el aterrizaje despegue y estacionameinto de aeronaves
def torreDeControl(evento,anuncio,parking,pistaAterrizajes,pistaDespegues):
    while True:
            probAviones = random.expovariate(0.2) # 1/lambda
            yield evento.timeout(probAviones)
            avion = generador() # se generan aviones
            # Ciclo completo de cada avion
            evento.process(cicloAvion(evento,avion,parking,anuncio,pistaAterrizajes,pistaDespegues))
            yield evento.timeout(0.5)

# Nos indica el ciclo completo de cada avion
def cicloAvion(evento,avion,parking,anuncio,pistaAterrizajes,pistaDespegues):
    # Nos indica primero si esta llegando el avion
    yield evento.process(controlLlegadas(evento,avion))
    # Despues de seguido indica si efectivamente ha aterrizado el avion
    yield evento.process(controlAterrizajes(evento,pistaAterrizajes,parking))
    # Después nos indica cuando ha estacionado la aeronave
    yield evento.process(controlEstacionados(evento,parking))
    # Después de estacionar nos dice a que hora está programado el vuelo
    yield evento.process(controlSalidas(evento,anuncio))
    # Nos indica si el avion esta despegando
    yield evento.process(controlDespegues(evento,pistaDespegues))
    
# Una vez solicitan aterrizar los aviones se les añade a la cola de llegadas
def controlLlegadas(evento,avion):
    colaAterrizajes.append(avion)
    avion.infoColaAterrizaje()
    yield evento.timeout(0.5)

# Una vez llegan las aeronaves las retira de la otra cola y las añade a la de aterrizados
def controlAterrizajes(evento,pista,parking):
    if colaAterrizajes:
        aterriza = colaAterrizajes.popleft()
        with pista.request( ) as request: # si hay request de aterrizar en pista
            yield request
            colaEstacionados .append(aterriza)
            aterriza.infoAterrizaje()
            yield evento.timeout(0.5)
        yield evento.timeout(0.5)
    else:
        yield evento.timeout(0.1)

# Una vez aterrizan las aeronaves te informa de si esta estacionado
def controlEstacionados(evento,parking):
    if colaEstacionados:
        estacionado = colaEstacionados.popleft()
        with parking.request() as request: # si hay request de estacionar
            yield request
            colaSalidas.append(estacionado)
            estacionado.infoEstacionado()
            yield evento.timeout(0.5)
    else:
        yield evento.timeout(0.1)

# Una vez estan estacionadas las aeronaves se les asigna una hora de salida para ser anunciado
def controlSalidas(evento,anuncio):
    if colaSalidas:
        salida = colaSalidas.popleft()
        avion = aeronaveSalida(salida)
        with anuncio.request() as request:
            yield request
            colaDespegues.append(salida)
            avion.infoSalidas()
            yield evento.timeout(0.5)
    else:
        yield evento.timeout(0.1)

# Una vez estan estacionadas las aeronaves se les asigna una tarea de salir a pista (no esta implementado el control de flujo de pasajeros)
def controlDespegues(evento,pista):
    if colaDespegues:
        salida = colaDespegues.popleft()
        avion = salida
        with pista.request() as request: #hace request por si no hay ningún avión en la pista
            yield request
            avion.infoDespegues()
            yield evento.timeout(0.5)
    else:
        yield evento.timeout(0.1)

# Una vez una aeronave aterriza (mirar flujo de pasajeros para ver si hay retraso), se le asigna otro destino con diferente id de vuelo y destino
def aeronaveSalida(avion):
    avion.origen = avion.destino
    avion.destino = random.choice(ciudades) # El origen no puede ser también el destino
    vuelo = ''.join(filter(str.isalpha,avion.vueloId))
    numeroVuelo = int(''.join(filter(str.isdigit,avion.vueloId)))
    avion.vueloId = f"{vuelo}{numeroVuelo + random.randint(1,5)}"
    hora,min = map(int, avion.horaLlegada.split(':'))
    horaSalida = hora + random.randint(1,23)
    horaLlegada = horaSalida + random.randint(1,5)
    minSalida = min + random.randint(0,59)
    minLlegada = minSalida + random.randint(0,59)
    funcTiempo(horaSalida,minSalida)
    funcTiempo(horaLlegada,minLlegada)
    avion.horaSalida = f"{horaSalida%24:02d}:{minSalida%24:02d}" # hora de salida respecto a la llegada
    avion.horaLlegada = f"{horaLlegada%24:02d}:{minLlegada%24:02d}"
    return avion

#################################################FUNCIONES AUXILIARES#################################################

def funcTiempo(horas,minutos):
    if minutos > 59:
        minutos -= 60
        horas += 1
    if horas > 23:
        horas -= 24

