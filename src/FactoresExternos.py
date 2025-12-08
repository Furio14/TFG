import random
from Aeronaves import Aeronave

#############################################Factor Horario/Meteorologico#############################################

tasaHora = {0:0.1,1:0.1,2:0.08,3:0.07,4:0.07,5:0.08,
            6:0.1,7:0.2,8:0.3,9:0.3,10:0.4,11:0.4,
            12:0.4,13:0.45,14:0.4,15:0.5,16:0.45,17:0.4,
            18:0.35,19:0.3,20:0.25,21:0.2,22:0.15,23:0.1}

Invierno = {"Soleado":0.3,"Nublado":0.4,"Lluvioso":0.2,"Niebla":0.05,"Tormenta":0.05}
Primavera = {"Soleado":0.6,"Nublado":0.25,"Lluvioso":0.1,"Niebla":0.02,"Tormenta":0.05}
Verano = {"Soleado":0.8,"Nublado":0.15,"Lluvioso":0.03,"Niebla":0.01,"Tormenta":0.03}
Otonio = {"Soleado":0.5,"Nublado":0.3,"Lluvioso":0.15,"Niebla":0.02,"Tormenta":0.05}


def climaRandom(estados):
    estado = list(estados.keys())
    prob = list(estados.values())
    return random.choices(estado,prob,k=1)[0]

def logicaClima(evento,estado,mes):
    while True:
        if mes in ["DICIEMBRE","ENERO","FEBRERO"]: estacionActual = Invierno
        elif mes in ["MARZO","ABRIL","MAYO"]: estacionActual = Primavera
        elif mes in ["JUNIO","JULIO","AGOSTO"]: estacionActual = Verano
        else: estacionActual = Otonio
        clima = climaRandom(estacionActual)
        if clima != estado['clima']:
            estado['clima'] = clima
            if clima == 'Nublado':
                estado['retraso'] = 1.5
            elif clima == 'Lluvioso':
                estado['retraso'] = 2
            elif clima == 'Niebla':
                estado['retraso'] = 2.5
            elif clima == 'Tormenta':
                estado['retraso'] = 3.5
            else: estado['retraso'] = 0

        yield evento.timeout(60) 


#############################################Flujo de Pasajeros#############################################

def operacionesMes(mes):
    # Calculado teniendo en cuenta la media de operaciones del año 2024 y las operaciones del mes 
    # del aeropuerto de Madrid (proporcionado por AENA)
    # (operaciones del mes / media de operaciones de todo el año)
    match mes:
        case "ENERO":
            demandaMensual = 0.9    
        case "FEBRERO":
            demandaMensual = 0.88
        case "MARZO":
            demandaMensual = 0.98
        case "ABRIL":
            demandaMensual = 0.99
        case "MAYO":
            demandaMensual = 1.04
        case "JUNIO":
            demandaMensual = 1.04
        case "JULIO":
            demandaMensual = 1.08
        case "AGOSTO":
            demandaMensual = 1.05
        case "SEPTIEMBRE":
            demandaMensual = 1.04
        case "OCTUBRE":
            demandaMensual = 1.01
        case "NOVIEMBRE":
            demandaMensual = 0.98
        case "DICIEMBRE":
            demandaMensual = 1.02
    return demandaMensual

def generadorAverias(evento,pista,estado,modo,min,max):
    while True:
        tiempo = random.uniform(min,max)
        yield evento.timeout(tiempo)
        estado[modo] = 'Cerrada'
        with pista.request(priority=0) as req:
            yield req
            yield evento.timeout(random.uniform(20,30))
        estado[modo] = 'Activa'