from bson import ObjectId
from cogs.conexion import conectar_db

# --- OPERACIONES CLIENTES ---
def registrar_cliente(nombre, email, telefono):
    db = conectar_db()
    if db is None: return False
    try:
        # Evitar emails duplicados manualmente
        if db.clientes.find_one({"email": email}):
            print("El email ya está registrado")
            return False
            
        db.clientes.insert_one({
            "nombre": nombre,
            "email": email,
            "telefono": telefono
        })
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def obtener_clientes():
    db = conectar_db()
    if db is None: return []
    lista = []
    for cli in db.clientes.find():
        lista.append((str(cli["_id"]), cli["nombre"], cli["email"], cli.get("telefono", "")))
    return lista

# --- OPERACIONES PRODUCTOS ---
def registrar_producto(nombre, precio, stock):
    db = conectar_db()
    if db is None: return False
    try:
        db.productos.insert_one({
            "nombre": nombre,
            "precio": precio,
            "stock": stock
        })
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def obtener_productos():
    db = conectar_db()
    if db is None: return []
    lista = []
    for prod in db.productos.find():
        lista.append((str(prod["_id"]), prod["nombre"], f"${prod['precio']}", prod["stock"]))
    return lista

# --- OPERACIONES PEDIDOS ---
def registrar_pedido(cliente_id, producto_id, cantidad):
    db = conectar_db()
    if db is None: return False
    try:
        # Verificar que el cliente y el producto existan realmente en la BD
        cliente = db.clientes.find_one({"_id": ObjectId(cliente_id)})
        producto = db.productos.find_one({"_id": ObjectId(producto_id)})
        
        if not cliente or not producto:
            print("Cliente o Producto no encontrado.")
            return False
            
        # Insertar pedido guardando una referencia limpia (y los nombres para facilitar lecturas)
        db.pedidos.insert_one({
            "cliente_id": ObjectId(cliente_id),
            "cliente_nombre": cliente["nombre"],
            "producto_id": ObjectId(producto_id),
            "producto_nombre": producto["nombre"],
            "cantidad": cantidad
        })
        return True
    except Exception as e:
        print(f"Error al procesar pedido: {e}")
        return False

def obtener_pedidos():
    db = conectar_db()
    if db is None: return []
    lista = []
    for ped in db.pedidos.find():
        lista.append((
            str(ped["_id"]), 
            ped.get("cliente_nombre", "Desconocido"), 
            ped.get("producto_nombre", "Desconocido"), 
            ped["cantidad"]
        ))
    return lista