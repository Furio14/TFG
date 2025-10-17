import os
import time
import random
from TorreDeControl import *
from GeneradorAeronaves import *
from Aeronaves import * 

def main():
    log = "../log.txt"
    #si log.txt tiene algo de información, cuando lo ejecutas se reinicia la info
    if os.path.exists(log):
        os.remove(log)
    for minuto in range(0,120):
        if random.random() < 0.2:
            avion = generador()
            controlAterrizajes()
            if avion.info() is not None:
                print(avion.info())
        time.sleep(0.5)

if __name__ == "__main__":
    main()
