import random

#Ciudades
ciudades = ["Madrid, Nueva York, Milán, Tokyo, Beijing, Shanghai, Londres"]
vuelos = ["IB","BA","AA","V","AV","LX","DL"]

def generador():
    letra = random.choice("ABCDEFGHIJLKMNOPQRSTUVWXYZ") #genera letra random
    id = f"{letra}{random.randint(0,999)}" #genera un id para un avión aleatorio
    idVuelo = f"{letra}{random.randint(0,999)}" #genera un id para un avión aleatorio
    origen,destino = random.sample(ciudades,2)
    