import time
from collections import deque
from GeneradorAeronaves import *
from Aeronaves import *

colaAterrizajes = deque()
colaEstacionados = deque()

# Controla todo lo que tiene que ver con el aterrizaje despegue y estacionameinto de aeronaves
def torreDeControl():
    contador = 0
    for minuto in range(0,120):
        if random.random() < 0.2:
            avion = generador()
            controlColaAterrizajes(avion)
            contador += 1
            if avion.infoColaAterrizaje() is not None:
                print(avion.infoColaAterrizaje())
        if random.random() < 0.15 and contador > 0:     
            controlAterrizajes()
            contador -= 1
            time.sleep(0.3)
            controlEstacionados()
        time.sleep(0.5)

# Añade las aeronaves a la torre de aterrizajes
def controlColaAterrizajes(avion):
    colaAterrizajes.append(avion)
    time.sleep(0.5)
    
# Una vez llegan las aeronaves las retira de la otra cola y las añade a la de aterrizados
def controlAterrizajes():
    if colaAterrizajes:
        aterriza = colaAterrizajes.popleft()
        aterriza.infoAterrizaje()
        colaEstacionados.append(aterriza)

# Una vez aterrizan las aeronaves te informa de si esta estacionado
def controlEstacionados():
    estacionado = colaEstacionados.popleft()
    estacionado.infoEstacionado()
