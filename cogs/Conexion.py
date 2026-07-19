from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# CONFIGURACIÓN: Cambia esto por la IP de tu máquina virtual en VirtualBox
IP_VIRTUALBOX = "localhost"  # Si usas reenvío de puertos o "192.168.X.X" si es puente
PUERTO = 27017

def conectar_db():
    try:
        # Definimos un timeout corto (3 segundos) por si la VM está apagada
        client = MongoClient(f"mongodb://{IP_VIRTUALBOX}:{PUERTO}/", serverSelectionTimeoutMS=3000)
        # Forzar una consulta para verificar la conexión real
        client.admin.command('ping')
        
        # Base de datos llamada "comerciotech"
        db = client["comerciotech"]
        return db
    except ConnectionFailure:
        print("Error: No se pudo conectar a MongoDB. ¿Está encendida la máquina virtual?")
        return None