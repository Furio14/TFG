#Torre de Control
from collections import deque
from GeneradorAeronaves import *
from Aeronaves import *

colaAterrizajes = deque()

def controlAterrizajes():
    for i in range(9):
        avion = generador()
        colaAterrizajes.append(avion)
    
def controlEstacionados():
    colaEstacionados = deque()
    for i in range(9):
        colaEstacionados.append(colaAterrizajes.popleft())
