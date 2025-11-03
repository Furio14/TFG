import random
from Aeronaves import *
from TorreDeControl import *

horasAeronave = 0
minutosAeronave = 0
comienzoSimulacion = False

#Ciudades
ciudades = ["Nueva York", "Milan", "Tokyo", "Beijing", "Shanghai", "Londres"]
vuelos = ["IB","BA","AA","V","AV","LX","DL"]

def generador():
    global minutosAeronave
    global horasAeronave
    global comienzoSimulacion
    letra = random.choice("ABCDEFGHIJLKMNOPQRSTUVWXYZ") # genera letra random
    minutoSalida = random.randint(0,59)
    minutoLlegada = random.randint(0,59)
    id = f"{letra}{random.randint(0,999)}" # genera un id para un avion aleatorio
    idVuelo = f"{random.choice(vuelos)}{random.randint(0,999)}" # genera un id para un avion aleatorio
    estado = "Llegando" # estado de la aeronave
    pasajeros = random.randint(150,300) # genera un numero random de pasajeros
    origen = random.choice(ciudades) # genera 2 ciudades random
    destino = "Madrid"
    duracion = random.randint(1,5)
    if not comienzoSimulacion: # al inicio de la simulacion ponemos unos parametros iniciales
        horaSalida = f"{horasAeronave:02d}:{minutosAeronave:02d}"
        horaLlegada = f"{(horasAeronave + duracion)%24:02d}:{minutoLlegada:02d}"
        horasAeronave = horasAeronave + duracion
        minutosAeronave = minutoLlegada + duracion
        comienzoSimulacion = True
    else:
            if (minutosAeronave + duracion) > 59: # si se soberpasa el rango de 59 mins se pasa a la siguiente hora y minuto
                horasAeronave += 1
                minutosAeronave = random.randint(0,4)
            horaSalida = f"{(horasAeronave-duracion)%24:02d}:{minutoSalida:02d}"
            horaLlegada = f"{(horasAeronave)%24:02d}:{minutosAeronave + duracion:02d}"
            minutosAeronave = minutosAeronave + duracion
            
    return Aeronave(id,idVuelo,estado,pasajeros,origen,destino,horaSalida,horaLlegada,horaEstacionado="---",horaProgramadaSalida="---",horaDespegue="---")

