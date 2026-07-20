from pymongo import MongoClient
import pymongo.errors

IP_VIRTUALBOX = "192.168.18.114"
PUERTO = 27017

# --- NUEVO: Agrega las credenciales de tu MongoDB ---
USUARIO = "admin"
PASSWORD = "Admin123"
BASE_DE_DATOS = "comercioTech"

def conectar_db():
    try:
        # La URI ahora incluye el usuario y la contraseña
        # Nota: authSource=admin le dice a Mongo que verifique las credenciales en la base de datos principal
        uri = f"mongodb://{USUARIO}:{PASSWORD}@{IP_VIRTUALBOX}:{PUERTO}/?authSource=admin"
        
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        client.admin.command('ping') # Verificamos conexión
        
        db = client[BASE_DE_DATOS]
        return db
        
    except pymongo.errors.OperationFailure:
        print("❌ Error de Autenticación: El usuario o la contraseña son incorrectos.")
        return None
    except pymongo.errors.ServerSelectionTimeoutError:
        print("❌ Error de Red: No se pudo alcanzar el servidor.")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None