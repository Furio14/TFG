import time
import heapq
import simpy
import random
from collections import deque
from GeneradorAeronaves import *
from Aeronaves import *
from FactoresExternos import *

# Controla todo lo que tiene que ver con el aterrizaje despegue y estacionameinto de aeronaves
def controlAereo(evento,anuncio,parking,pistaAterrizajes,pistaDespegues,colaAterrizajes,colaEstacionados,colaSalidas,colaDespegues,estadoClima,mes,turnos,aeronaves,retraso):
    while True:
            vuelosMedia = 200 #media de vuelos cada dia
            hora = horaActual(evento.now)
            controlHorario(evento,turnos,retraso)
            operaciones = operacionesMes(mes)
            vuelosDiarios = vuelosMedia * operaciones
            vuelosHora = vuelosDiarios * tasaHora[hora]
            lambdaVuelos = (vuelosHora/60)/4 #el aeropueto madrid barajas usa 4 pistas como solol tenemos 1 dividimos todo entre 4
            tiempoGeneracion = random.expovariate(lambdaVuelos)
            yield evento.timeout(tiempoGeneracion)
            avion = generador(evento) # se generan aviones
            controlTurnosLlegadas(hora,turnos)
            Aeronave.totalAeronaves += 1
            Aeronave.totalPasajeros += avion.pasajeros
            # Ciclo completo de cada avion
            evento.process(cicloAvion(evento,avion,parking,anuncio,pistaAterrizajes,pistaDespegues,colaAterrizajes,colaEstacionados,colaSalidas,colaDespegues,estadoClima,mes,turnos,aeronaves))

# Nos indica el ciclo completo de cada avion
def cicloAvion(evento,avion,parking,anuncio,pistaAterrizajes,pistaDespegues,colaAterrizajes,colaEstacionados,colaSalidas,colaDespegues,estadoClima,mes,turnos,aeronaves):
    # Nos indica primero si esta llegando el avion
    yield evento.process(controlLlegadas(evento,avion,colaAterrizajes,estadoClima,mes,aeronaves))
    # Despues de seguido indica si efectivamente ha aterrizado el avion
    yield evento.process(controlAterrizajes(evento,pistaAterrizajes,colaAterrizajes,colaEstacionados,estadoClima,mes,aeronaves))
    # Después nos indica cuando ha estacionado la aeronave
    yield evento.process(controlEstacionados(evento,parking,colaEstacionados,colaSalidas,estadoClima,mes,aeronaves))
    # Después de estacionar nos dice a que hora está programado el vuelo
    yield evento.process(controlSalidas(evento,anuncio,colaSalidas,colaDespegues,estadoClima,mes,aeronaves))
    # Nos indica si el avion esta despegando
    yield evento.process(controlDespegues(evento,parking,pistaDespegues,colaDespegues,estadoClima,mes,turnos,aeronaves))
    
# Una vez solicitan aterrizar los aviones se les añade a la cola de llegadas
def controlLlegadas(evento,avion,colaAterrizajes,estadoClima,mes,aeronaves):
    yield colaAterrizajes.put(avion)
    aeronaves["AeronavesEnColaLlegada"] += 1
    avion.infoColaAterrizaje(evento,estadoClima,mes,aeronaves)

# Una vez llegan las aeronaves las retira de la otra cola y las añade a la de aterrizados
def controlAterrizajes(evento,pista,colaAterrizajes,colaEstacionados,estadoClima,mes,aeronaves):
    if colaAterrizajes:
        aterriza = yield colaAterrizajes.get()
        with pista.request( ) as request: # si hay request de aterrizar en pista
            yield request
            tiempoHastaAterrizar = estadoClima['retraso']
            yield evento.timeout(tiempoHastaAterrizar)
            aterriza.horaLlegadaReal = tiempoEvento(evento.now)
            aterriza.tiempoLlegadaMinutos = int(evento.now)
            aeronaves["AeronavesEnColaLlegada"] -= 1
            aterriza.infoAterrizaje(evento,estadoClima,mes,aeronaves)
            yield colaEstacionados.put(aterriza)   
    else:
        yield evento.timeout(0.1)

# Una vez aterrizan las aeronaves te informa de si esta estacionado
def controlEstacionados(evento,parking,colaEstacionados,colaSalidas,estadoClima,mes,aeronaves):
    if colaEstacionados:
        estacionado = yield colaEstacionados.get()
        req = parking.request()
        # si hay request de estacionar
        yield req
        tiempoHastaEstacionamiento = int(random.triangular(5.0,15.0,mode=10.0))
        yield evento.timeout(tiempoHastaEstacionamiento)
        estacionado.horaEstacionado = tiempoEvento(evento.now)
        aeronaves["AeronavesEstacionados"] += 1
        estacionado.infoEstacionado(evento,estadoClima,mes,aeronaves)
        estacionado.ticketParking = req
        yield colaSalidas.put(estacionado)
    else:
        yield evento.timeout(0.1)

# Una vez estan estacionadas las aeronaves se les asigna una hora de salida para ser anunciado
def controlSalidas(evento,anuncio,colaSalidas,colaDespegues,estadoClima,mes,aeronaves):
    if colaSalidas:
        salida = yield colaSalidas.get()
        avion = aeronaveSalida(evento,salida)
        with anuncio.request() as request:
            yield request
            avion.infoSalidas(evento,estadoClima,mes,aeronaves)
            horaProgramada,minProgramado = funcSplit(avion.horaProgramadaSalida)
            tiempoProgramado = horaProgramada*60 + minProgramado
            tiempoActual = int(evento.now) % 1440
            tiempo = tiempoProgramado - tiempoActual
            if tiempo < -720:
                tiempo += 1440
            tiempoEspera = max(0,tiempo) 
            yield evento.timeout(tiempoEspera)
            yield colaDespegues.put(salida)
    else:
        yield evento.timeout(0.1)

# Una vez estan estacionadas las aeronaves se les asigna una tarea de salir a pista (no esta implementado el control de flujo de pasajeros)
def controlDespegues(evento,parking,pista,colaDespegues,estadoClima,mes,turnos,aeronaves):
    if colaDespegues:
        salida = yield colaDespegues.get()
        avion = salida
        with pista.request() as request: #hace request por si no hay ningún avión en la pista
            yield request
            if(hasattr(avion,'ticketParking')):
                parking.release(avion.ticketParking)
                del avion.ticketParking
            tiempoDespegando = random.uniform(1.0,3.0)
            aeronaves["AeronavesEstacionados"] -= 1
            aeronaves["AeronavesEnColaSalida"] += 1
            avion.infoColaDespegues(evento,estadoClima,mes,aeronaves)
            yield evento.timeout(tiempoDespegando + estadoClima['retraso'])
            avion.horaDespegue = tiempoEvento(evento.now)
            tiempoCiclo = int(evento.now) - avion.tiempoLlegadaMinutos
            avion.tiempoCicloAvion = tiempoEvento(tiempoCiclo)
            avion.horaLlegadaReal = "---"
            aeronaves["AeronavesEnColaSalida"] -= 1
            aeronaves["AeronavesCicloCompletoContadorTiempo"] += int(tiempoCiclo)
            aeronaves["AeronavesCicloCompletoContador"] += 1
            horaDespegue = horaActual(evento.now)
            controlTurnosSalidas(horaDespegue,turnos)
            avion.infoDespegues(evento,estadoClima,mes,aeronaves)
    else:
        yield evento.timeout(0.1)


#################################################FUNCIONES AUXILIARES#################################################
# Una vez una aeronave aterriza (mirar flujo de pasajeros para ver si hay retraso), se le asigna otro destino con diferente id de vuelo y destino
def aeronaveSalida(evento,avion):
    vueloRandom = random.choice(listaVuelos)
    avion.origen = avion.destino
    avion.destino = vueloRandom["Ciudades"] # El origen no puede ser también el destino
    vuelo = ''.join(filter(str.isalpha,avion.vueloId))
    numeroVuelo = int(''.join(filter(str.isdigit,avion.vueloId)))
    avion.vueloId = f"{vuelo}{numeroVuelo + random.randint(1,5)}"
    tiempoActual =int(evento.now) 
    horaSalida = tiempoActual + int(random.triangular(40,70,55)) # asignamos tiempo random de salida
    horaLlegada = horaSalida + vueloRandom["Duracion_Vuelo"]
    horaSalida,minSalida = funcMin(horaSalida)
    horaLlegada,minLlegada = funcMin(horaLlegada)
    avion.horaSalida = f"{horaSalida:02d}:{minSalida:02d}" # hora de salida respecto a la llegada
    avion.horaLlegada = f"{horaLlegada:02d}:{minLlegada:02d}"
    avion.horaProgramadaSalida = avion.horaSalida # lahora programa es igual que la d salida nueva
    return avion

# El tiempo actual del evento en formato horas (xx:xx)
def tiempoEvento(evento):
    hora,min = funcMin(int(evento))
    horaFunc = f"{hora%24:02d}:{min%60:02d}"
    return horaFunc

# Te devuelve el tiempo (130) en horas y minutos 
def funcMin(tiempo):
    hora = (tiempo // 60) % 24
    min = tiempo % 60
    return hora,min

# Te devuelve la hora actual del evento
def horaActual(evento):
    minTotal = int(evento)
    mins = minTotal%1440
    horaActual = mins // 60
    return horaActual

# Separa las horas (xx:xx) en horas y minutos
def funcSplit(param):
    hora,min = map(int, param.split(':'))
    return hora,min

# Cada vez que llega un avion en su turno horario queda registrado
def controlTurnosLlegadas(hora,turnos):
    if hora >=0 and hora <= 5:
        turnos["Madrugada"] +=1
    elif hora >= 6 and hora <= 11:
        turnos["Mañana"] += 1
    elif hora >= 12 and hora <= 17:
        turnos["Tarde"] += 1
    else:
        turnos["Noche"] += 1

# Cada vez que sale un avion en su turno horario queda registrado
def controlTurnosSalidas(hora,turnos):
    if hora >=0 and hora <= 5:
        turnos["SalidaMadrugada"] +=1
    elif hora >= 6 and hora <= 11:
        turnos["SalidaMañana"] += 1
    elif hora >= 12 and hora <= 17:
        turnos["SalidaTarde"] += 1
    else:
        turnos["SalidaNoche"] += 1

# Si la simulacion dura +24 horas se calculan los dias de la simulacion
def controlHorario(evento,turnos,retraso):
    if evento.now - retraso > 1440 * turnos["dias"]:
        print(evento.now)
        turnos["dias"] += 1
            
        
        