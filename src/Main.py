import os
import time
import random
import simpy
from TorreDeControl import *
from GeneradorAeronaves import *
from Aeronaves import * 

def main():
    log = "../log.csv"
    #si log.txt tiene algo de información, cuando lo ejecutas se reinicia la info
    if os.path.exists(log):
        os.remove(log)
    evento = simpy.Environment()
    
    pista = simpy.Resource(evento,capacity=1)
    parking = simpy.Resource(evento,capacity=2)

    evento.process(torreDeControl(evento,pista,parking))
    evento.run(until=140)

if __name__ == "__main__":
    main()
