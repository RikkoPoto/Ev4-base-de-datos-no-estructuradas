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
    if db is None: return False, "Error de conexión."
    codigo = codigo.strip()
    
    # REQUISITO N°13: Integridad Referencial
    # Si el cliente ya compró algo, no se puede borrar.
    if db.pedidos.find_one({"codigo_cliente": codigo}):
        return False, "DENEGADO: No se puede eliminar a este cliente porque ya tiene pedidos históricos asociados en el sistema."
        
    res = db.clientes.delete_one({"codigo": codigo})
    if res.deleted_count > 0:
        return True, "Cliente eliminado exitosamente."
    return False, "No se encontró el cliente a eliminar."


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
    if db is None: return False, "Error de conexión."
    codigo = codigo.strip()
    
    # REQUISITO N°13: Integridad Referencial
    # Si el producto está mencionado dentro del arreglo "detalle" de cualquier pedido, no se borra.
    if db.pedidos.find_one({"detalle.codigo_producto": codigo}):
        return False, "DENEGADO: No se puede eliminar este producto porque forma parte de recibos ya emitidos en el sistema."
        
    res = db.productos.delete_one({"codigo": codigo})
    if res.deleted_count > 0:
        return True, "Producto eliminado exitosamente."
    return False, "No se encontró el producto a eliminar."


from datetime import datetime

# ==================== PEDIDOS ====================
def registrar_pedido(codigo_cliente, carrito):
    """
    carrito debe ser una lista de diccionarios: [{"codigo": "PROD-101", "cantidad": 2}, ...]
    """
    db = conectar_db()
    if db is None: return False, "Error de conexión a la base de datos."
    
    cliente = db.clientes.find_one({"codigo": codigo_cliente.strip()})
    if not cliente: return False, "El cliente ingresado no existe."
    if not carrito: return False, "El carrito está vacío. Seleccione al menos un producto."
    
    total_pedido = 0
    detalles = []
    
    # 1. Validar el stock de TODOS los productos antes de hacer descuentos
    for i, item in enumerate(carrito):
        prod = db.productos.find_one({"codigo": item["codigo"]})
        if not prod: return False, f"El producto {item['codigo']} no existe."
        
        stock_actual = int(prod.get("stock", 0))
        if item["cantidad"] > stock_actual:
            return False, f"Stock insuficiente. Solo quedan {stock_actual} de {prod.get('nombre')}."
        if item["cantidad"] <= 0:
            return False, "Las cantidades deben ser mayores a cero."
            
        t_linea = float(prod.get("precio", 0)) * item["cantidad"]
        total_pedido += t_linea
        
        detalles.append({
            "numero_linea": i + 1,
            "codigo_producto": prod["codigo"],
            "cantidad": item["cantidad"],
            "total_linea": t_linea
        })
        
    # 2. Si todo el stock es válido, procedemos a descontarlo
    for item in carrito:
        db.productos.update_one(
            {"codigo": item["codigo"]},
            {"$inc": {"stock": -item["cantidad"]}}
        )
        
    # 3. Registrar el pedido con el arreglo completo
    db.pedidos.insert_one({
        "numero": db.pedidos.count_documents({}) + 1001,
        "fecha": datetime.now(), 
        "codigo_cliente": cliente["codigo"], 
        "total": total_pedido,
        "detalle": detalles
    })
    
    return True, "Pedido creado y stock actualizado exitosamente."

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
    if db is None: return False, "Error de conexión."
    try:
        # Buscamos el pedido ANTES de eliminarlo para saber qué productos devolver
        pedido = db.pedidos.find_one({"numero": int(numero_pedido)})
        if not pedido: return False, "Pedido no encontrado."
        
        # --- REQUISITO N°12: DEVOLVER STOCK A BODEGA ---
        for det in pedido.get("detalle", []):
            cod_prod = det.get("codigo_producto")
            cant = det.get("cantidad", 0)
            if cod_prod:
                db.productos.update_one(
                    {"codigo": cod_prod},
                    {"$inc": {"stock": cant}} # Número positivo devuelve el stock
                )
        
        # Ahora sí, eliminamos el pedido
        res = db.pedidos.delete_one({"numero": int(numero_pedido)})
        if res.deleted_count > 0:
            return True, "Pedido anulado y stock actualizado."
        return False, "No se pudo eliminar el pedido."
    except ValueError:
        return False, "Número de pedido inválido."