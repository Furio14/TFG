import os
import time
import random
from TorreDeControl import *
from GeneradorAeronaves import *
from Aeronaves import * 

def main():
    log = "../log.csv"
    #si log.txt tiene algo de información, cuando lo ejecutas se reinicia la info
    if os.path.exists(log):
        os.remove(log)
    torreDeControl()

if __name__ == "__main__":
    main()
