from bson.objectid import ObjectId
from cogs.conexion import conectar_db

# ==================== CLIENTES ====================
def registrar_cliente(nombre, apellido, calle, numero, comuna, fono):
    db = conectar_db()
    if db is None: return False
    
    # LÓGICA DE AUTO-INCREMENTO
    ultimo = db.clientes.find_one(sort=[("codigo", -1)]) # Busca el último registro
    if ultimo and "codigo" in ultimo and ultimo["codigo"].startswith("CLI-"):
        try:
            # Extrae el número (ej: CLI-003 -> 3) y le suma 1
            num = int(ultimo["codigo"].split("-")[1])
            codigo_nuevo = f"CLI-{num + 1:03d}" # Formatea con 3 ceros (CLI-004)
        except:
            codigo_nuevo = "CLI-001"
    else:
        codigo_nuevo = "CLI-001"
        
    db.clientes.insert_one({
        "codigo": codigo_nuevo, 
        "nombre": nombre, 
        "apellido_paterno": apellido,
        "domicilio": {"calle": calle, "numero": numero, "comuna": comuna},
        "fono": fono
    })
    return True

def obtener_clientes():
    db = conectar_db()
    if db is None: return []
    return [(c.get("codigo"), c.get("nombre"), c.get("apellido_paterno"), 
             f"{c.get('domicilio', {}).get('calle', '')} {c.get('domicilio', {}).get('numero', '')}, {c.get('domicilio', {}).get('comuna', '')}", 
             c.get("fono")) for c in db.clientes.find().sort("codigo", 1)]

def obtener_cliente_por_codigo(codigo):
    db = conectar_db()
    return db.clientes.find_one({"codigo": codigo})

def actualizar_cliente(codigo, nombre, apellido, calle, numero, comuna, fono):
    db = conectar_db()
    if db is None: return False
    res = db.clientes.update_one(
        {"codigo": codigo},
        {"$set": {"nombre": nombre, "apellido_paterno": apellido, "fono": fono,
                  "domicilio.calle": calle, "domicilio.numero": numero, "domicilio.comuna": comuna}}
    )
    return res.modified_count > 0

def eliminar_cliente(codigo):
    db = conectar_db()
    if db is None: return False
    # Agregamos .strip() para limpiar espacios accidentales
    res = db.clientes.delete_one({"codigo": codigo.strip()})
    return res.deleted_count > 0


# ==================== PRODUCTOS ====================
def registrar_producto(nombre, precio, stock):
    db = conectar_db()
    if db is None: return False
    
    # LÓGICA DE AUTO-INCREMENTO
    ultimo = db.productos.find_one(sort=[("codigo", -1)])
    if ultimo and "codigo" in ultimo and ultimo["codigo"].startswith("PROD-"):
        try:
            num = int(ultimo["codigo"].split("-")[1])
            codigo_nuevo = f"PROD-{num + 1:03d}"
        except:
            codigo_nuevo = "PROD-101"
    else:
        codigo_nuevo = "PROD-101"
        
    db.productos.insert_one({
        "codigo": codigo_nuevo, 
        "nombre": nombre, 
        "precio": precio, 
        "stock": stock
    })
    return True

def obtener_productos():
    db = conectar_db()
    if db is None: return []
    return [(p.get("codigo"), p.get("nombre"), p.get("precio"), p.get("stock")) for p in db.productos.find().sort("codigo", 1)]

def obtener_producto_por_codigo(codigo):
    db = conectar_db()
    return db.productos.find_one({"codigo": codigo})

def actualizar_producto(codigo, nombre, precio, stock):
    db = conectar_db()
    res = db.productos.update_one({"codigo": codigo}, {"$set": {"nombre": nombre, "precio": precio, "stock": stock}})
    return res.modified_count > 0

def eliminar_producto(codigo):
    db = conectar_db()
    res = db.productos.delete_one({"codigo": codigo})
    return res.deleted_count > 0


from datetime import datetime

# ==================== PEDIDOS ====================
def registrar_pedido(codigo_cliente, codigo_producto, cantidad):
    db = conectar_db()
    if db is None: return False
    
    # Buscamos que existan
    cliente = db.clientes.find_one({"codigo": codigo_cliente.strip()})
    producto = db.productos.find_one({"codigo": codigo_producto.strip()})
    
    if not cliente or not producto: 
        return False
        
    # Calculamos el total usando el precio del producto
    precio_unitario = float(producto.get("precio", 0))
    total_linea = precio_unitario * cantidad
    
    # Generamos un número de pedido autoincremental simple
    numero_pedido = db.pedidos.count_documents({}) + 1001

    # Insertamos respetando EXACTAMENTE la estructura de tu imagen
    db.pedidos.insert_one({
        "numero": numero_pedido,
        "fecha": datetime.now(),
        "codigo_cliente": cliente["codigo"],
        "total": total_linea,
        "detalle": [
            {
                "numero_linea": 1,
                "codigo_producto": producto["codigo"],
                "cantidad": cantidad,
                "total_linea": total_linea
            }
        ]
    })
    return True

def obtener_pedidos():
    db = conectar_db()
    if db is None: return []
    
    lista = []
    for p in db.pedidos.find().sort("numero", 1): 
        numero_pedido = p.get("numero", "N/A") 
        cod_cli = p.get("codigo_cliente", "")
        
        # 1. CRUCE CLIENTE
        cliente_db = db.clientes.find_one({"codigo": cod_cli})
        if cliente_db:
            nom_cli = f"{cliente_db.get('nombre', '')} {cliente_db.get('apellido_paterno', '')}".strip()
        else:
            nom_cli = "Desconocido"

        # 2. CRUCE PRODUCTO Y AGRUPACIÓN
        detalles = p.get("detalle", [])
        if not detalles:
            lista.append((numero_pedido, cod_cli, nom_cli, "N/A", "Sin productos", 0))
            continue
            
        # Si el arreglo tiene exactamente 1 producto, se muestra normal
        if len(detalles) == 1:
            det = detalles[0]
            cod_prod = det.get("codigo_producto", "")
            cant = det.get("cantidad", 0)
            
            prod_db = db.productos.find_one({"codigo": cod_prod})
            if prod_db:
                nom_prod = prod_db.get("nombre", "")
            else:
                nom_prod = "Desconocido"
                
            lista.append((numero_pedido, cod_cli, nom_cli, cod_prod, nom_prod, cant))
            
        # Si el arreglo tiene más de 1 producto, se agrupa como "Varios"
        else:
            total_cant = sum(d.get("cantidad", 0) for d in detalles)
            lista.append((numero_pedido, cod_cli, nom_cli, "Varios", "Varios Productos", total_cant))
            
    return lista

#Ventana Emergetne - DETALLE PEDIDO
def obtener_pedido_por_numero(numero):
    db = conectar_db()
    if db is None: return None
    try:
        # Buscamos el documento completo del pedido
        return db.pedidos.find_one({"numero": int(numero)})
    except ValueError:
        return None

def eliminar_pedido(numero_pedido):
    db = conectar_db()
    try:
        # Convertimos a número entero porque en MongoDB se guardó como int (ej: 1001)
        res = db.pedidos.delete_one({"numero": int(numero_pedido)})
        return res.deleted_count > 0
    except ValueError:
        # Evita caídas si el registro es muy antiguo y dice "N/A"
        return False
    except Exception as e:
        print(f"Error al eliminar pedido: {e}")
        return False