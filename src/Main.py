import os
from TorreDeControl import *
from GeneradorAeronaves import *
from Aeronaves import * 

def main():
    log = "../log.txt"
    if os.path.exists(log):
        os.remove(log)
    avion = generador()
    controlAterrizajes()
    if avion.info() is not None:
        print(avion.info())

if __name__ == "__main__":
    main()
