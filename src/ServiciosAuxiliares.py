import random

def servicioLimpieza():
    tiempo = int(random.triangular(10,20,15))
    return tiempo

def servicioCombustible():
    tiempo = int(random.triangular(15,30,25))
    return tiempo

def servicioCatering():
    tiempo = random.randint(10,20)
    return tiempo

def servicioEmbarque():
    tiempo = random.randint(15,30)
    return tiempo