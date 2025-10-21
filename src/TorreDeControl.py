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
listaAviones = []

# Controla todo lo que tiene que ver con el aterrizaje despegue y estacionameinto de aeronaves
def torreDeControl(evento,pistaAterrizajes,parking):
    global avion
    while True:
        if random.random() < 0.2: # se generan aviones
            avion = generador()
            avion.contador += 1
            listaAviones.append(avion)
            evento.process(controlColas(evento,avion,colaAterrizajes))
            avion.infoColaAterrizaje()
        for avion in listaAviones:
            if random.random() < 0.15 and  avion.contador > 0:
                evento.process(controlAterrizajes(evento,pistaAterrizajes,parking))
                avion.contador += 1
            if random.random() < 0.2 and  avion.contador > 1 and avion.estado != "Programado":
                avion = aeronaveSalida(avion)
                evento.process(controlColas(evento,avion,colaSalidas))
                avion.infoSalidas()
                print(evento.now)

        yield evento.timeout(0.5)

# Añade las aeronaves a la torre de aterrizajes
def controlColas(evento,avion,colas):
    colas.append(avion)
    yield evento.timeout(0.5)
    
# Una vez llegan las aeronaves las retira de la otra cola y las añade a la de aterrizados
def controlAterrizajes(evento,pista,parking):
    if colaAterrizajes:
        aterriza = colaAterrizajes.popleft()
        with pista.request( ) as request: # si hay request de aterrizar en pista
            yield request
            aterriza.infoAterrizaje()
            yield evento.timeout(0.5)
        colaEstacionados.append(aterriza)
        evento.process(controlEstacionados(evento,parking))
        yield evento.timeout(0.5)
    else:
        yield evento.timeout(0.1)

# Una vez aterrizan las aeronaves te informa de si esta estacionado
def controlEstacionados(evento,parking):
    if colaEstacionados:
        estacionado = colaEstacionados.popleft()
        with parking.request() as request: # si hay request de estacionar
            yield request
            estacionado.infoEstacionado()
            yield evento.timeout(0.5)
    else:
        yield evento.timeout(0.1)

# Una vez estan estacionadas las aeronaves se les asigna una tarea de salir a pista (no esta implementado el control de flujo de pasajeros)
def controlSalidas(evento,pista):
    if colaSalidas:
        salida = colaSalidas.popleft()
        with pista.request() as request:
            yield request
            salida.infoSalidas()
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

