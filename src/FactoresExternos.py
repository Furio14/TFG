import random
from Aeronaves import Aeronave

#############################################Factor Horario/Meteorologico#############################################

tasaHora = {0:0.05,1:0.04,2:0.03,3:0.03,4:0.02,5:0.03,
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

def logicaClima(evento,estado):
    while True:
        mes = Aeronave.mes
        if mes in ["Diciembre","Enero","Febrero"]: estacionActual = Invierno
        elif mes in ["Marzo","Abril","Mayo"]: estacionActual = Primavera
        elif mes in ["Junio","Julio","Agosto"]: estacionActual = Verano
        else: estacionActual = Otonio
        clima = climaRandom(estacionActual)
        if clima in ['Lluvioso','Niebla','Tormenta']:
            estado['retraso'] = 1.5
        elif clima == 'Nublado':
            estado['retraso'] = 0.5
        else: estado['retraso'] = 0
        yield evento.timeout(60) 


#############################################Flujo de Pasajeros#############################################

def demandaPasajeros(mes):
    global demandaMensual
    # Calculado teniendo en cuenta la media de operaciones del año 2024 y las operaciones del mes 
    # del aeropuerto de Madrid (proporcionado por AENA)
    # (operaciones del mes / media de operaciones de todo el año)
    match mes:
        case "Enero":
            demandaMensual = 0.9    
        case "Febrero":
            demandaMensual = 0.88
        case "Marzo":
            demandaMensual = 0.98
        case "Abril":
            demandaMensual = 0.99
        case "Mayo":
            demandaMensual = 1.04
        case "Junio":
            demandaMensual = 1.04
        case "Julio":
            demandaMensual = 1.08
        case "Agosto":
            demandaMensual = 1.05
        case "Septiembre":
            demandaMensual = 1.04
        case "Octubre":
            demandaMensual = 1.01
        case "Noviembre":
            demandaMensual = 0.98
        case "Diciembre":
            demandaMensual = 1.02