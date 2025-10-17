from TorreDeControl import *
from GeneradorAeronaves import *
from Aeronaves import * 

def main():
    avion = generador()
    controlAterrizajes()
    print("Aeronave: ", avion.info())

if __name__ == "__main__":
    main()
