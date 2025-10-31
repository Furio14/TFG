def demandaPasajeros(mes,dia):
    demandaMes(mes)
    demandaSemana(dia)

def demandaMes(mes):
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

def demandaSemana(semana):
    global demandaSemanal
    match semana:
        case "Lunes":
            demandaSemanal = 1.1
        case "Martes":
            demandaSemanal = 0.8
        case "Miercoles":
            demandaSemanal = 0.9
        case "Jueves":
            demandaSemanal = 1.1
        case "Viernes":
            demandaSemanal = 1.3
        case "Sabado":
            demandaSemanal = 0.8
        case "Domingo":
            demandaSemanal = 1.2
